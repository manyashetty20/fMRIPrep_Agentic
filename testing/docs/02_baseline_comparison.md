# Test 02 — Baseline Comparison

## Purpose

Run **vanilla fMRIPrep** (single command, no diagnosis, no recovery) on the same subjects and settings as agentic runs.

Results append to `testing/results/evaluation/baseline_evaluation.csv` for side-by-side tables.

## When to run

- Before or after `run_agentic.py` on the same dataset
- Required for the paper claim: *“agentic layer improves success rate / reduces manual intervention”*

## Prerequisites

- `testing/config/publication_battery.yaml` configured
- Docker + FreeSurfer `license.txt`
- BIDS dataset with T1w (and func if not `--anat-only`)

## Command

```bash
python testing/run_baseline.py
```

Single subject:

```bash
python testing/run_baseline.py --participant sub-01
```

Dry-run:

```bash
python testing/run_baseline.py --dry-run
```

## Metrics recorded

- `final_status` — completed / failed
- `attempt_count` — always 1 for baseline
- `wall_clock_seconds`
- `first_exit_code` / `last_exit_code`
- `run_mode=baseline`

## Artifacts

| Path | Description |
|------|-------------|
| `testing/results/outputs/baseline/<dataset>/<participant>/` | fMRIPrep outputs |
| `.../agentic_results/<participant>/baseline_run.json` | Command + stderr tail |
| `testing/results/evaluation/baseline_evaluation.csv` | Aggregate metrics |

## Analysis

```bash
python testing/analyze_results.py
```

See `testing/results/reports/baseline_vs_agentic.csv`.

## Notes

- Baseline uses the same rule-based `ConfigAgent` command builder as the planner (no LLM loop).
- If baseline fails on metadata issues that agentic fixes, that is **evidence for the paper**.
