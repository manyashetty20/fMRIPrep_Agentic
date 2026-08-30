"""
agents/config_agent.py
======================
Config Agent – uses RAG over fMRIPrep / BIDS documentation to generate
a valid Docker command for the given run parameters.

All paths, model names, and pipeline flags come from the central Config
object; nothing is hardcoded in this file.

Metrics (inspectable)
---------------------
``generate_command`` emits a ``config_command_generated`` event via
``metrics_logger.emit`` including final flags, fallback reasons, RAG chunk
ids, gold-standard correctness, and hallucination (unknown-flag) findings.
"""

from __future__ import annotations

import logging
import re
import shlex
import time
from pathlib import Path
from typing import Any

import yaml

from config_loader import Config
from metrics_logger import emit, estimate_llm_cost_usd, extract_llm_usage

logger = logging.getLogger(__name__)


class ConfigAgent:
    """
    Builds an fMRIPrep Docker command using:
      1. RAG over local documentation (fMRIPrep manual, BIDS spec)
      2. Scan-time facts (participant ID, fieldmap presence, pipeline flags)
    """

    def __init__(self, cfg: Config) -> None:
        self.cfg = cfg
        self._qa_chain = None  # lazy-loaded
        self._official_flags: set[str] | None = None
        self._last_rag_chunks: list[dict[str, Any]] = []
        self._last_llm_usage: dict[str, Any] = {}
        self._generation_method: str = "rule_based"

    # ---------------------------------------------------------------------- #
    #  Public API
    # ---------------------------------------------------------------------- #

    def generate_command(self) -> str:
        """
        Return a complete, ready-to-run Docker command string.

        The command is built deterministically from cfg values.
        An LLM is consulted only when the documentation RAG chain is
        available and the user has chosen to use it.
        """
        t0 = time.perf_counter()
        self._last_rag_chunks = []
        self._last_llm_usage = {}
        self._generation_method = "rule_based"
        fallback_flags: list[dict[str, str]] = []

        try:
            chain = self._get_qa_chain()
            if chain is not None:
                cmd = self._llm_command(chain)
                self._generation_method = "rag_llm"
            else:
                cmd, fallback_flags = self._rule_based_command_with_reasons()
        except Exception as exc:
            logger.warning("LLM command generation failed (%s) – falling back to rule-based.", exc)
            cmd, fallback_flags = self._rule_based_command_with_reasons()
            self._generation_method = "rule_based_after_llm_error"

        elapsed = time.perf_counter() - t0
        flag_list = self._extract_flag_stems(cmd)
        hallucinated = self._hallucination_check(cmd)
        
        # Flag validation: reject commands with unknown flags to prevent execution failures
        if hallucinated:
            logger.warning(
                "Generated command contains unrecognized fMRIPrep flags: %s. "
                "Falling back to rule-based generation to ensure valid command.",
                hallucinated
            )
            cmd, fallback_flags = self._rule_based_command_with_reasons()
            self._generation_method = "rule_based_after_flag_validation"
            flag_list = self._extract_flag_stems(cmd)
            hallucinated = self._hallucination_check(cmd)
            # If rule-based also has issues (shouldn't happen), log but proceed
            if hallucinated:
                logger.error("Rule-based command also contains unrecognized flags: %s", hallucinated)
        elif self._generation_method == "rag_llm":
            # LLM generation passed validation, but still record rule-based fallbacks for comparison
            _, fallback_flags = self._rule_based_command_with_reasons()
        
        gold = self._gold_standard_check(cmd)
        cost = estimate_llm_cost_usd(
            self._last_llm_usage.get("prompt_tokens"),
            self._last_llm_usage.get("completion_tokens"),
            input_rate_per_m=self.cfg.llm_cost_per_million_input_tokens,
            output_rate_per_m=self.cfg.llm_cost_per_million_output_tokens,
        )

        emit(
            "config_agent",
            "config_command_generated",
            generation_method=self._generation_method,
            command=cmd,
            flags=flag_list,
            fallback_flags=fallback_flags,
            rag_chunks=self._last_rag_chunks,
            hallucination_unknown_flags=hallucinated,
            hallucination_pass=len(hallucinated) == 0,
            gold_standard=gold,
            duration_seconds=round(elapsed, 4),
            llm_usage=self._last_llm_usage,
            llm_cost_usd_estimate=cost,
            validation_flagged=len(hallucinated) > 0,
        )
        return cmd

    # ---------------------------------------------------------------------- #
    #  Internal helpers
    # ---------------------------------------------------------------------- #

    def _rule_based_command(self) -> str:
        cmd, _ = self._rule_based_command_with_reasons()
        return cmd

    def _rule_based_command_with_reasons(self) -> tuple[str, list[dict[str, str]]]:
        """Build the Docker command purely from Config values (no LLM)."""
        cfg = self.cfg
        has_fmap = cfg.has_fieldmap()
        fallbacks: list[dict[str, str]] = []

        parts = [
            "docker run --rm",
            f"-v {cfg.bids_dir}:/data:ro",
            f"-v {cfg.output_dir}:/out",
            f"-v {cfg.license_file}:/opt/freesurfer/license.txt:ro",
            cfg.docker_image,
            "/data /out participant",
            f"--participant-label {cfg.participant_id.replace('sub-', '')}",
        ]

        if cfg.session_id:
            parts.append(f"--session-label {cfg.session_id}")

        if cfg.skip_bids_validation:
            parts.append("--skip-bids-validation")
        if cfg.anat_only:
            parts.append("--anat-only")
        if cfg.sloppy:
            parts.append("--sloppy")
        if cfg.low_mem:
            parts.append("--low-mem")

        parts.append(f"--mem_mb {cfg.mem_mb}")
        parts.append(f"--nprocs {cfg.nprocs}")
        if cfg.output_space:
            parts.append(f"--output-spaces {cfg.output_space}")

        if not has_fmap:
            parts.append("--use-syn-sdc")
            fallbacks.append(
                {
                    "flag": "--use-syn-sdc",
                    "reason": "No fieldmap directory found for participant; enabling fieldmap-less SyN SDC.",
                }
            )

        if not cfg.anat_only and cfg.missing_readout_timing_metadata():
            parts.append(f"--fallback-total-readout-time {cfg.fallback_total_readout_time}")
            fallbacks.append(
                {
                    "flag": "--fallback-total-readout-time",
                    "reason": "BOLD sidecars lack TotalReadoutTime / EffectiveEchoSpacing+PhaseEncodingDirection.",
                }
            )

        parts.append("--fs-no-reconall")
        parts.append("-w /out/work")

        cmd = " \\\n  ".join(parts)
        logger.info("Rule-based command generated:\n%s", cmd)
        return cmd, fallbacks

    def _llm_command(self, chain) -> str:
        """Ask the LLM (with RAG context) to produce the Docker command."""
        cfg = self.cfg
        has_fmap = cfg.has_fieldmap()

        query = f"""
Context:
  BIDS_DIR          = {cfg.bids_dir}
  OUTPUT_DIR        = {cfg.output_dir}
  LICENSE_FILE      = {cfg.license_file}
  PARTICIPANT       = {cfg.participant_id}
  SESSION           = {cfg.session_id or "none"}
  FIELDMAPS_FOUND   = {has_fmap}
  ANAT_ONLY         = {cfg.anat_only}
  SLOPPY_MODE       = {cfg.sloppy}
  LOW_MEM           = {cfg.low_mem}
  MEM_MB            = {cfg.mem_mb}
  NPROCS            = {cfg.nprocs}
  DOCKER_IMAGE      = {cfg.docker_image}

TASK: Generate a single fMRIPrep Docker run command using the paths above.
RULES:
  1. Use EXACTLY the paths given for the volume mounts.
  2. Output ONLY the bare shell command – no markdown fences, no explanation.
  3. If FIELDMAPS_FOUND is False, add --use-syn-sdc.
  4. If ANAT_ONLY is True, add --anat-only.
  5. If SLOPPY_MODE is True, add --sloppy.
  6. If LOW_MEM is True, add --low-mem and --mem_mb {cfg.mem_mb}.
  7. If SESSION is not "none", add --session-label {cfg.session_id} (NOT --session-id).
"""
        # Prefer retriever+LLM so we can log source chunks for retrieval-precision analysis.
        retriever = getattr(chain, "retriever", None)
        if retriever is not None:
            try:
                docs = retriever.invoke(query) if hasattr(retriever, "invoke") else retriever.get_relevant_documents(query)
                self._last_rag_chunks = [
                    {
                        "source": str(getattr(d, "metadata", {}).get("source", "")),
                        "page": getattr(d, "metadata", {}).get("page"),
                        "excerpt": (getattr(d, "page_content", "") or "")[:400],
                    }
                    for d in (docs or [])[:8]
                ]
            except Exception as exc:
                logger.warning("Could not retrieve RAG chunks for metrics (%s).", exc)

        response = chain.invoke(query)
        if isinstance(response, dict):
            result = response.get("result", "")
            source_docs = response.get("source_documents") or []
            if source_docs and not self._last_rag_chunks:
                self._last_rag_chunks = [
                    {
                        "source": str(getattr(d, "metadata", {}).get("source", "")),
                        "page": getattr(d, "metadata", {}).get("page"),
                        "excerpt": (getattr(d, "page_content", "") or "")[:400],
                    }
                    for d in source_docs[:8]
                ]
            # RetrievalQA may wrap the LLM message; try nested usage.
            self._last_llm_usage = extract_llm_usage(response.get("raw") or response)
        else:
            result = str(response)
            self._last_llm_usage = extract_llm_usage(response)

        result = result.replace("```bash", "").replace("```sh", "").replace("```", "").strip()
        logger.info("LLM-generated command:\n%s", result)
        return result

    def _get_qa_chain(self):
        """Lazily build the RAG chain. Returns None if dependencies are missing."""
        if self._qa_chain is not None:
            return self._qa_chain

        try:
            from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
            from langchain_huggingface import HuggingFaceEmbeddings
            from langchain_community.vectorstores import Chroma
            from langchain_classic.chains import RetrievalQA
        except ImportError as exc:
            logger.warning("RAG dependencies not installed (%s). Using rule-based generation.", exc)
            return None

        docs_dir = self.cfg.docs_dir
        db_dir = self.cfg.vector_db_dir

        if not docs_dir.exists() or not any(docs_dir.glob("*.pdf")):
            logger.warning("No PDFs found in %s. Using rule-based generation.", docs_dir)
            return None

        logger.info("Loading documentation from %s …", docs_dir)
        loader = DirectoryLoader(str(docs_dir), glob="*.pdf", loader_cls=PyPDFLoader)
        docs = loader.load()

        embeddings = HuggingFaceEmbeddings(model_name=self.cfg.embedding_model)
        vector_db = Chroma.from_documents(
            documents=docs,
            embedding=embeddings,
            persist_directory=str(db_dir),
        )

        llm = self._build_llm()
        if llm is None:
            return None

        self._qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vector_db.as_retriever(),
            return_source_documents=True,
        )
        return self._qa_chain

    def _build_llm(self):
        """Return the configured LLM instance, or None on failure."""
        provider = self.cfg.llm_provider
        model = self.cfg.llm_model
        temp = self.cfg.llm_temperature

        try:
            if provider == "groq":
                from langchain_groq import ChatGroq
                return ChatGroq(model_name=model, temperature=temp)
            elif provider == "openai":
                from langchain_openai import ChatOpenAI
                return ChatOpenAI(model_name=model, temperature=temp)
            elif provider == "anthropic":
                from langchain_anthropic import ChatAnthropic
                return ChatAnthropic(model_name=model, temperature=temp)
            else:
                logger.warning("Unknown LLM provider '%s'. Using rule-based generation.", provider)
                return None
        except Exception as exc:
            logger.warning("Failed to initialise LLM (%s). Using rule-based generation.", exc)
            return None

    # ------------------------------------------------------------------ #
    #  Flag validation / gold-standard scoring
    # ------------------------------------------------------------------ #

    def _load_official_flags(self) -> set[str]:
        if self._official_flags is not None:
            return self._official_flags
        path = self.cfg.official_flags_file
        flags: set[str] = set()
        if path.is_file():
            for line in path.read_text().splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                flags.add(line.split()[0])
        else:
            logger.warning("Official flags file missing: %s", path)
        self._official_flags = flags
        return flags

    @staticmethod
    def _extract_flag_stems(command: str) -> list[str]:
        normalised = re.sub(r"\\\s*\n\s*", " ", command).strip()
        try:
            tokens = shlex.split(normalised)
        except ValueError:
            tokens = normalised.split()
        stems: list[str] = []
        for tok in tokens:
            if tok.startswith("-"):
                stem = tok.split("=", 1)[0]
                if stem not in stems:
                    stems.append(stem)
        return stems

    def _hallucination_check(self, command: str) -> list[str]:
        """
        Return generated flag stems that are NOT in the official fMRIPrep flag list.

        Docker / path tokens (``docker``, ``-v``, image name, positional args) are ignored.
        """
        official = self._load_official_flags()
        if not official:
            return []
        # Allow common docker CLI flags that appear before the image entrypoint.
        docker_ok = {"-v", "-e", "--rm", "--user", "-u", "--gpus", "-w", "-ti"}
        # Temporarily allow --session-label until it's added to the official flags file
        # Also allow --fs-license-file as an alternative license mounting approach
        temporarily_allowed = {"--session-label", "--fs-license-file"}
        unknown: list[str] = []
        for stem in self._extract_flag_stems(command):
            if stem in docker_ok or stem in temporarily_allowed:
                continue
            if stem not in official:
                unknown.append(stem)
        return unknown

    def _gold_standard_check(self, command: str) -> dict[str, Any]:
        """
        Compare generated flags against ``evaluation.gold_standard_file``.

        Returns a dict with ``matched``, ``missing_required``, ``forbidden_present``,
        and ``correct`` (bool). If no fixture exists for this dataset, ``correct`` is None.
        """
        path = self.cfg.gold_standard_file
        result: dict[str, Any] = {
            "dataset_key": self.cfg.bids_dir.name,
            "fixture_path": str(path),
            "correct": None,
            "missing_required": [],
            "forbidden_present": [],
            "missing_flag_values": {},
        }
        if not path.is_file():
            result["error"] = "gold_standard_file_missing"
            return result

        try:
            raw = yaml.safe_load(path.read_text()) or {}
        except Exception as exc:
            result["error"] = str(exc)
            return result

        datasets = raw.get("datasets") or {}
        spec = datasets.get(self.cfg.bids_dir.name)
        if not spec:
            result["error"] = "no_fixture_for_dataset"
            return result

        normalised = re.sub(r"\\\s*\n\s*", " ", command)
        stems = set(self._extract_flag_stems(command))
        missing = [f for f in (spec.get("required_flags") or []) if f not in stems]
        forbidden = [f for f in (spec.get("forbidden_flags") or []) if f in stems]
        missing_vals: dict[str, dict[str, str]] = {}
        for flag, expected in (spec.get("required_flag_values") or {}).items():
            # Match "--flag VALUE" or "--flag=VALUE"
            pattern = re.compile(
                rf"(?:^|\s){re.escape(flag)}(?:=|\s+)(\S+)",
                re.MULTILINE,
            )
            m = pattern.search(normalised)
            actual = m.group(1) if m else None
            if actual != str(expected):
                missing_vals[flag] = {"expected": str(expected), "actual": actual or ""}

        result["missing_required"] = missing
        result["forbidden_present"] = forbidden
        result["missing_flag_values"] = missing_vals
        result["correct"] = not missing and not forbidden and not missing_vals
        result["notes"] = spec.get("notes", "")
        return result
