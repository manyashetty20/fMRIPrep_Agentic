# Publication Testing Suite

This folder contains **evaluation runners** (not unit tests) for journal-style experiments:
baseline comparison, full agentic runs, ablations, failure injection, and result aggregation.

Detailed docs for each suite live in [`testing/docs/`](docs/).

---

## Quick start

### 1. Prerequisites

```bash
cd /Users/manyashetty/Desktop/Agentic_fMRIPrep
source venv/bin/activate
pip install pyyaml nibabel   # yaml for test configs; nibabel for failure injection
```

- `license.txt` in project root (FreeSurfer)
- Docker running (`docker info`)
- A BIDS dataset on disk (e.g. OpenNeuro `ds000114`)

### 2. Configure paths

```bash
cp testing/config/publication_battery.example.yaml testing/config/publication_battery.yaml
```

Edit `testing/config/publication_battery.yaml` and set `bids_dir` to your real dataset root, e.g.:

```yaml
bids_dir: /Users/manyashetty/Desktop/ds000114
```

**Do not paste comments on the same line as commands** — run only:

```bash
python testing/run_baseline.py
```

not `python testing/run_baseline.py # vanilla fMRIPrep` (the shell treats `# ...` as extra arguments).

### 2b. Start Docker (required for real fMRIPrep)

Open **Docker Desktop** and wait until it is fully started, then verify:

```bash
docker info
```

### 3. Fast smoke test (no Docker, ~2 min)

Verifies orchestration + recovery loop with mock fMRIPrep:

```bash
python testing/run_smoke.py
```

### 4. Real evaluation runs

Run suites individually (recommended first):

```bash
# Baseline fMRIPrep (no agents)
python testing/run_baseline.py

# Full agentic pipeline
python testing/run_agentic.py

# Ablation study (4 conditions × all participants)
python testing/run_ablation.py

# One failure-injection case
python testing/run_failure_injection.py --mode missing_tr --participant sub-01 --force
```

Or run the full battery (long; many hours depending on dataset):

```bash
python testing/run_publication_battery.py
```

### 5. Generate paper tables

```bash
python testing/analyze_results.py
```

Outputs land in `testing/results/reports/`:
- `evaluation_summary.md`
- `baseline_vs_agentic.csv`
- `ablation_summary.csv`
- `failure_injection_matrix.csv`

Raw metrics append to `testing/results/evaluation/run_evaluation.csv` and `baseline_evaluation.csv`.

---

## Suite index

| Script | Doc | Purpose |
|--------|-----|---------|
| `run_smoke.py` | [docs/01_smoke_test.md](docs/01_smoke_test.md) | Mock-Docker orchestration smoke test |
| `run_baseline.py` | [docs/02_baseline_comparison.md](docs/02_baseline_comparison.md) | Vanilla fMRIPrep baseline |
| `run_agentic.py` | [docs/03_agentic_full_run.md](docs/03_agentic_full_run.md) | Full agentic system |
| `run_ablation.py` | [docs/04_ablation_study.md](docs/04_ablation_study.md) | Disable recovery / diagnosis / vision |
| `run_failure_injection.py` | [docs/05_failure_injection.md](docs/05_failure_injection.md) | Controlled BIDS defects + recovery |
| `analyze_results.py` | [docs/06_analyze_results.md](docs/06_analyze_results.md) | Aggregate CSV → tables |
| `run_publication_battery.py` | (this README) | Run all suites sequentially |

---

## Dry-run mode

Print commands without executing fMRIPrep:

```bash
python testing/run_agentic.py --dry-run
python testing/run_publication_battery.py --dry-run
```

---

## Output layout

```text
testing/results/
├── evaluation/          # run_evaluation.csv, baseline_evaluation.csv
├── outputs/             # fMRIPrep derivatives per suite
├── bids_mutated/        # failure-injection copies
├── logs/                # per-run stdout/stderr
├── manifests/           # JSON metadata per run
└── reports/             # analyze_results.py summaries
```

`testing/results/` is gitignored.

---

## Recommended publication order

1. `run_smoke.py` — confirm loop works
2. `run_baseline.py` + `run_agentic.py` on ds000114 (sub-01..03)
3. `run_ablation.py` on sub-01 (faster) or full cohort
4. `run_failure_injection.py` for each mode
5. `analyze_results.py` — build tables for the manuscript
