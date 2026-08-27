# Test 03 — Full Agentic Run

## Purpose

Run the **complete agentic pipeline** with all agents enabled:

- Config / planning
- Execution
- Diagnosis on failure
- Recovery + retry (bounded)
- QA after success

## When to run

- Main evaluation condition for publication tables
- Run on every subject in your study cohort

## Command

```bash
python testing/run_agentic.py
```

Single subject:

```bash
python testing/run_agentic.py --participant sub-02
```

## Metrics recorded

Appended to `testing/results/evaluation/run_evaluation.csv`:

| Field | Meaning |
|-------|---------|
| `final_status` | completed / failed |
| `attempt_count` | Total execution attempts |
| `successful_recovery` | Failed first, succeeded after recovery |
| `initial_failure_type` | First error class |
| `qa_summary` | PASS / WARN / FAIL |
| `wall_clock_seconds` | End-to-end time |
| `recovery_enabled` | true (full system) |

## Per-run artifacts

Under `testing/results/outputs/agentic_full/<dataset>/<participant>/agentic_results/<participant>/`:

- `run_summary.json` — event timeline
- `config_snapshot.json` — resolved config + BIDS facts
- `qa_metrics.json` — voxel / file-presence QA
- `qa_report.txt` — human-readable QA
- `evaluation_row.json` — single-row export

## Expected runtime

Depends on dataset size and `pipeline` settings in YAML. ds000114 full runs are typically **30–60+ minutes per subject**.

## Paper use

Primary **success rate** and **mean attempts** columns for the main results table.
