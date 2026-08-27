# Test 01 — Smoke Test (Mock Docker)

## Purpose

Verify the **agentic control loop** without running real fMRIPrep:

`planner → executor → diagnostic → recovery → QA`

Uses a mock `docker` shim that simulates an OOM failure (exit 137) on the first attempt, then succeeds.

## When to run

- After any change to `agents/orchestrator.py`, diagnostic, or recovery logic
- Before starting long real-fMRIPrep evaluation runs
- Does **not** require OpenNeuro data or Docker daemon

## Command

```bash
cd /Users/manyashetty/Desktop/Agentic_fMRIPrep
source venv/bin/activate
python testing/run_smoke.py
```

Dry-run (print underlying command only):

```bash
python testing/run_smoke.py --dry-run
```

## Expected outcome

- Exit code `0`
- Log: `tmp/full_agent_smoke/smoke_run.log`
- Evaluation row appended (OOM recovery demo)
- Second attempt reports `final_status: completed`

## Artifacts

| Path | Description |
|------|-------------|
| `tmp/full_agent_smoke/smoke_run.log` | Full stdout/stderr |
| `tmp/full_agent_smoke/outputs/agentic_results/sub-01/` | QA + run summary |
| `testing/results/manifests/smoke_test.json` | Suite manifest |

## Paper use

Cite as a **controlled orchestration demo**, not as scientific validation of preprocessing quality.
