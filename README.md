# Agentic fMRIPrep Pipeline

Autonomous fMRIPrep wrapper: agents generate Docker commands, diagnose crashes, apply repairs, and re-run within a bounded LangGraph loop. Rule-based anatomical QA scores derivatives after a successful run.

This README describes **what the code actually does**. Claims that are planned but not implemented are marked explicitly.

---

## Project structure

```text
Agentic_fMRIPrep/
├── agents/
│   ├── config_agent.py       # RAG / rule-based Docker command generation
│   ├── diagnostic_agent.py   # Log diagnosis (LLM or regex heuristics)
│   ├── recovery_agent.py     # Diagnosis → command / BIDS sidecar repairs
│   └── orchestrator.py       # LangGraph loop + rule-based QA node
├── data/
│   ├── bids_input/           # Toy BIDS dataset
│   ├── docs/                 # PDFs for RAG (fmriprep_manual.pdf, bids_spec.pdf)
│   └── fmriprep_cli_flags.txt
├── database/vector_store/    # Chroma embeddings (created at runtime)
├── logs/                     # agentic_run.log
├── output/
│   ├── evaluation/           # run_evaluation.csv / .jsonl
│   ├── metrics/              # metrics_<run_id>.jsonl (per-run event logs)
│   └── pdf/                  # Generated PDF reports (optional scripts)
├── outputs/                  # Default fMRIPrep output root
├── scripts/
│   ├── inject_failures.py    # Controlled BIDS defect injection
│   ├── run_baseline.py       # Plain fMRIPrep baseline (no agent loop)
│   ├── mock_docker.py        # Smoke-test Docker shim
│   └── …
├── testing/
│   ├── run_*.py              # Publication experiment runners
│   ├── analyze_results.py    # Paper tables from CSV + metrics
│   ├── fixtures/gold_standard_commands.yaml
│   └── config/               # publication_battery.yaml
├── bids_discovery.py
├── config_loader.py
├── config.yaml
├── evaluation_export.py      # Flatten run → CSV/JSONL row
├── metrics_logger.py         # Central structured event logger
├── main.py
├── requirements.txt
└── license.txt               # FreeSurfer license (gitignored; you must add it)
```

There is **no** `vision_agent.py`. Anatomical QA lives inside `agents/orchestrator.py` as the LangGraph node `vision_agent` (`vision_agent_node`).

---

## Setup

### 1. FreeSurfer license

1. Register at the [FreeSurfer registration page](https://surfer.nmr.mgh.harvard.edu/registration.html).
2. Save the license as `license.txt` in the project root (gitignored).

### 2. Python environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Additional packages used by agents / testing (not all pinned in requirements.txt today):
pip install langchain-groq langgraph langchain-community langchain-huggingface \
  langchain-classic chromadb sentence-transformers pyyaml docker
```

`requirements.txt` currently lists only `nibabel`. Install the LangChain / Groq / Chroma stack as above for full agent behaviour. Without those packages the config and diagnostic agents fall back to rule-based / regex paths.

### 3. Groq API key (optional but used when LLM path is available)

```bash
export GROQ_API_KEY='your_groq_api_key'
```

Default provider in `config.yaml` is Groq (`llama-3.3-70b-versatile`). OpenAI / Anthropic providers exist in code behind `llm.provider` but are not required. Embeddings use local `sentence-transformers` (`all-MiniLM-L6-v2`).

### 4. RAG documentation

Place PDFs under `data/docs/`. The repo expects files such as:

- `data/docs/fmriprep_manual.pdf`
- `data/docs/bids_spec.pdf`

If PDFs or LangChain deps are missing, `ConfigAgent` uses rule-based command generation only.

---

## Agents (what the code does)

| Component | File | Behaviour |
|-----------|------|-----------|
| **ConfigAgent** | `agents/config_agent.py` | Builds an fMRIPrep `docker run …` command from `Config` (fieldmaps → `--use-syn-sdc`, readout gaps → `--fallback-total-readout-time`, etc.). Optionally uses RetrievalQA over `data/docs/`. Returns an in-memory command string (does **not** write a script under `scripts/`). |
| **DiagnosticAgent** | `agents/diagnostic_agent.py` | Parses failure logs. Tries configured LLM first; on failure/unavailable uses regex heuristics (`_HEURISTICS`). Does **not** query NeuroStars. |
| **RecoveryAgent** | `agents/recovery_agent.py` | Matches diagnosis text to `_FIX_RULES` and mutates the command and/or BIDS sidecars (e.g. inject `RepetitionTime`). |
| **Orchestrator** | `agents/orchestrator.py` | LangGraph: `planner → executor ⇄ detective → engineer → executor → vision_agent \| success_finalize`. Retries bounded by `agents.max_recovery_attempts`. |
| **QA node** (not a separate agent file) | `orchestrator.vision_agent_node` | After success (when `vision_enabled`): checks derivative presence + nibabel voxel ratios vs `qa.*` thresholds in `config.yaml`. Verdicts: **PASS / WARN / FAIL / SKIPPED**. No ViT/ResNet; HTML images are not scored by a vision model. |

### LangGraph loop

```text
planner → executor
            ├─ success + vision_enabled  → vision_agent → END
            ├─ success + !vision_enabled → success_finalize → END
            └─ fail → detective → engineer → executor (until max attempts / unrecoverable)
                         └─ then vision_agent for partial QA when possible
```

---

## Running

```bash
python main.py
# overrides:
python main.py --participant sub-01 --bids-dir ./data/bids_input --mem-mb 4000
```

Baseline (no agent loop) for overhead comparison:

```bash
python scripts/run_baseline.py --bids-dir ./data/bids_input --participant sub-01
```

Publication suites live under `testing/` (see `testing/README.md`).

---

## Metrics and evaluation

### What is logged

1. **Per-run JSONL events** — `metrics_logger.MetricsLogger` writes `output/metrics/metrics_<run_id>.jsonl` (path configurable via `evaluation.metrics_dir` in `config.yaml`). Every event includes `timestamp`, `agent_name`, `event_type`, `subject_id`, `run_id`.

   Notable `event_type` values:
   - `config_command_generated` — flags, fallback reasons, RAG chunks, gold-standard / hallucination checks, LLM usage
   - `diagnosis_completed` — log excerpt, root cause, `regex_heuristic` vs `llm_fallback`, duration
   - `recovery_applied` — repair actions, command before/after, retry attempt, duration
   - `state_transition` / `execution_completed` / `subject_run_completed` — orchestrator timeline, wall clock, fMRIPrep CLI time, orchestration overhead
   - `qa_completed` — voxel counts, mask ratio, skull-strip %, MNI success, verdict, **explicit thresholds**

2. **Aggregate CSV/JSONL** — `evaluation_export.build_evaluation_row` + `append_evaluation_exports` → `output/evaluation/run_evaluation.csv` (and `.jsonl`). Also mirrored under each run’s `…/agentic_results/<participant>/`.

### Configurable evaluation inputs (`config.yaml`)

- `evaluation.gold_standard_file` → `testing/fixtures/gold_standard_commands.yaml`
- `evaluation.official_flags_file` → `data/fmriprep_cli_flags.txt`
- `evaluation.failure_injection_modes` / `default_injection_trials`
- `qa.*` thresholds (also presets in `config_loader.py`)
- LLM cost rates for USD estimates from Groq token metadata when present

**Gold-standard flags for `data/bids_input`** were derived from the current `config.yaml` defaults (anat-only, no fmap → `--use-syn-sdc`, etc.). Confirm or edit `testing/fixtures/gold_standard_commands.yaml` before citing numbers in a paper. Additional datasets need their own fixture entries.

### Failure-injection trials

```bash
# N independent trials: inject → run pipeline → delete mutated copy
python testing/run_failure_injection.py \
  --mode missing_tr --participant sub-01 --trials 3 --force

# Modes: missing_tr, bad_readout, missing_fmap, strip_phase_encoding,
#         malformed_json, truncate_json, oom (oom uses mock docker; see script)
```

### Analysis / paper tables

```bash
python testing/analyze_results.py \
  --eval-root ./output \
  --metrics-dir ./output/metrics \
  --out-dir ./testing/results/reports
```

Produces CSV + `evaluation_summary.md` including diagnostic accuracy, recovery success rate, mean retries, mean±std diagnosis/recovery time, regex vs LLM split, efficiency (wall / fMRIPrep CLI / orchestration overhead), and config gold-standard / hallucination rates.

Inspectable analysis functions are documented at the top of `testing/analyze_results.py`.

---

## Key features (accurate)

- Modular agent files + LangGraph orchestration
- Groq-first LLM path with local embeddings; OpenAI not required for the default config
- Crash-aware retry with configurable ablation flags (`recovery_enabled`, `diagnosis_enabled`, `vision_enabled`)
- Structured metrics suitable for paper tables
- Rule-based anatomical QA with thresholds cited from `config.yaml`

**Not implemented (do not claim):** Vision Transformer / ResNet scoring of HTML QC images; NeuroStars retrieval for diagnosis; writing a ready script into `/scripts/` from the Config Agent.

---

## Research note

This project is a step toward agent-managed neuroimaging pipelines. Treat automated QA as a heuristic gate, not a replacement for expert visual QC when publishing results.
