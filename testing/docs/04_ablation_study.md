# Test 04 — Ablation Study

## Purpose

Measure contribution of each agent by disabling one component at a time.

## Conditions

| Condition | CLI flag | What is disabled |
|-----------|----------|------------------|
| `full` | (none) | Nothing — same as `run_agentic.py` |
| `no_recovery` | `--no-recovery` | Recovery / engineer loop |
| `no_diagnosis` | `--no-diagnosis` | Diagnostic agent on failures |
| `no_vision` | `--no-vision` | Post-run QA stage |

## Command

All four conditions × all participants:

```bash
python testing/run_ablation.py
```

One condition only:

```bash
python testing/run_ablation.py --condition no_recovery --participant sub-01
```

## Output layout

```text
testing/results/outputs/ablation_<condition>/<dataset>/<participant>/
```

## Metrics for paper Table

Group rows in `run_evaluation.csv` by:

- `recovery_enabled`
- `diagnosis_enabled`
- `vision_enabled`

Report per group:

- Success rate (`final_status == completed`)
- Mean `attempt_count`
- Mean `wall_clock_seconds`
- Recovery success rate (`successful_recovery`)

## Analysis

```bash
python testing/analyze_results.py
```

See `testing/results/reports/ablation_summary.csv`.

## Interpretation guide

- **no_recovery** fails more on injected/real errors → recovery agent adds value
- **no_diagnosis** may loop blindly or fail faster → diagnosis adds value
- **no_vision** should not affect `final_status` much; compare `qa_summary` instead
