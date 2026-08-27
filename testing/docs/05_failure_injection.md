# Test 05 — Failure Injection

## Purpose

Create **controlled BIDS defects** in an isolated copy, then run the agentic pipeline and record whether diagnosis + recovery succeed.

Original data is never modified.

## Modes

| Mode | Defect | Applicability |
|------|--------|---------------|
| `missing_tr` | Removes `RepetitionTime` from BOLD JSON sidecars | Needs func BOLD |
| `bad_readout` | Removes `TotalReadoutTime` / `EffectiveEchoSpacing` | Needs func BOLD |
| `missing_fmap` | Hides `fmap/` directory | Subject must have fieldmaps |
| `oom` | No file change — use smoke test | See Test 01 |

## Commands

```bash
# Missing RepetitionTime → recovery should repair sidecar from NIfTI header
python testing/run_failure_injection.py --mode missing_tr --participant sub-01 --force

# Missing readout timing → recovery should add --fallback-total-readout-time
python testing/run_failure_injection.py --mode bad_readout --participant sub-01 --force

# Hidden fieldmaps → recovery should adjust SDC flags
python testing/run_failure_injection.py --mode missing_fmap --participant sub-01 --force
```

`--force` replaces an existing mutated BIDS copy.

## Tagged in evaluation CSV

Runs pass `--injected-failure-mode <mode>` so `run_evaluation.csv` includes the `injected_failure_mode` column.

## Artifacts

| Path | Description |
|------|-------------|
| `testing/results/bids_mutated/<dataset>/<mode>_<participant>/` | Mutated BIDS copy |
| `.agentic_failure_injection.json` | Injection manifest inside mutated tree |
| `testing/results/manifests/failure/<mode>/...` | Run manifest |

## Failure matrix (paper)

| Mode | Participant | Applicable? | Diagnosed? | Recovered? | Final status |
|------|-------------|-------------|------------|------------|--------------|

Fill from `testing/results/reports/failure_injection_matrix.csv` after `analyze_results.py`.

## Notes

- `missing_fmap` **skips** subjects without a fieldmap directory (script will error).
- Some combinations (e.g. missing TR + SyN SDC edge cases) may still fail after max retries — report honestly in limitations.
