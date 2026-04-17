"""
agents/config_agent.py
======================
Config Agent – uses RAG over fMRIPrep / BIDS documentation to generate
a valid Docker command for the given run parameters.

All paths, model names, and pipeline flags come from the central Config
object; nothing is hardcoded in this file.
"""

from __future__ import annotations

import logging
from pathlib import Path

from config_loader import Config

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
        try:
            chain = self._get_qa_chain()
            if chain is not None:
                return self._llm_command(chain)
        except Exception as exc:
            logger.warning("LLM command generation failed (%s) – falling back to rule-based.", exc)

        return self._rule_based_command()

    # ---------------------------------------------------------------------- #
    #  Internal helpers
    # ---------------------------------------------------------------------- #

    def _rule_based_command(self) -> str:
        """Build the Docker command purely from Config values (no LLM)."""
        cfg = self.cfg
        has_fmap = cfg.has_fieldmap()

        parts = [
            "docker run --rm",
            f"-v {cfg.bids_dir}:/data:ro",
            f"-v {cfg.output_dir}:/out",
            f"-v {cfg.license_file}:/opt/freesurfer/license.txt:ro",
            cfg.docker_image,
            "/data /out participant",
            f"--participant-label {cfg.participant_id.replace('sub-', '')}",
        ]

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

        if cfg.session_id:
            parts.append(f"--session-id {cfg.session_id}")

        if not has_fmap:
            parts.append("--use-syn-sdc")

        parts.append("--fs-no-reconall")
        parts.append("-w /out/work")

        cmd = " \\\n  ".join(parts)
        logger.info("Rule-based command generated:\n%s", cmd)
        return cmd

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
"""
        response = chain.invoke(query)
        result = response.get("result", "") if isinstance(response, dict) else str(response)
        # Strip any accidental markdown fences
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
        db_dir   = self.cfg.vector_db_dir

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
        )
        return self._qa_chain

    def _build_llm(self):
        """Return the configured LLM instance, or None on failure."""
        provider = self.cfg.llm_provider
        model    = self.cfg.llm_model
        temp     = self.cfg.llm_temperature

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