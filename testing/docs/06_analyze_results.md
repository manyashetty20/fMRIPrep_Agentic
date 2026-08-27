# Test 06 — Analyze Results

## Purpose

Turn raw evaluation CSVs into **publication-ready summary tables** without manual spreadsheet work.

## Input files

| File | Source |
|------|--------|
| `testing/results/evaluation/run_evaluation.csv` | Agentic + ablation + failure runs |
| `testing/results/evaluation/baseline_evaluation.csv` | `run_baseline.py` |

If you used the default project `output/evaluation/` instead, pass `--eval-root ./output`.

## Command

```bash
python testing/analyze_results.py
```

Custom paths:

```bash
python testing/analyze_results.py \
  --eval-root ./testing/results/evaluation \
  --out-dir ./testing/results/reports
```

## Output files

| File | Contents |
|------|----------|
| `evaluation_summary.md` | All tables in one Markdown doc |
| `ablation_summary.csv` | Grouped success / attempts / wall-clock by agent flags |
| `baseline_vs_agentic.csv` | Paired comparison per dataset + participant |
| `failure_injection_matrix.csv` | Injected failure outcomes |
| `meta.json` | Row counts and source paths |

## When to run

- After each evaluation batch completes
- Before generating manuscript figures/tables
- Safe to re-run anytime (read-only on source CSVs)

## Tips

- Clear or archive old CSVs if you want a clean study cohort (or filter by `timestamp` in analysis).
- Copy `reports/*.csv` directly into LaTeX / Word table generators.
- For statistical tests (e.g. paired Wilcoxon on wall-clock), export CSVs to R/Python separately.
