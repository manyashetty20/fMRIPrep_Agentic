#!/usr/bin/env python3
"""Batch: ds000102, run-1 only, two arms (pe, mj). Resumable. Usage: python run_batch.py [sub-XX ...]"""
import csv, json, shutil, subprocess, sys, time
from pathlib import Path

DESK = Path.home() / "Desktop"
REPO = DESK / "Agentic_fMRIPrep"
SRC = DESK / "ds000102"
B = DESK / "batch"
ARMS = {  # arm: (config, injector mode or None, tag)
    "pe": ("config_pe.yaml", None, "syn_pe"),
    "mj": ("config_tr.yaml", "malformed_json", "malformed_json"),
}
FIELDS = ["dataset", "subject", "arm", "git_commit", "main_exit", "wall_seconds", "final_status",
          "attempt_count", "last_exit_code", "qa_status", "qa_summary", "retention", "reduction",
          "applied_rule_ids", "config_generation_method", "llm_total_tokens", "note"]

def sh(cmd, **kw):
    return subprocess.run(cmd, **kw)

def build_mini(sub):
    d = B / "src" / sub
    shutil.rmtree(d, ignore_errors=True)
    (d / sub / "anat").mkdir(parents=True)
    (d / sub / "func").mkdir()
    shutil.copy(SRC / "dataset_description.json", d)
    t = json.loads((SRC / "task-flanker_bold.json").read_text())
    t.pop("CogAtlasID", None)  # public file has an invalid CogAtlasID; removed for all subjects
    (d / "task-flanker_bold.json").write_text(json.dumps(t, indent=2) + "\n")
    shutil.copy(SRC / sub / "anat" / f"{sub}_T1w.nii.gz", d / sub / "anat")
    for f in (SRC / sub / "func").glob(f"{sub}_task-flanker_run-1_*"):
        shutil.copy(f, d / sub / "func")
    return d

def wait_docker_idle():
    waited = 0
    while sh(["docker", "ps", "-q"], capture_output=True, text=True).stdout.strip():
        time.sleep(60); waited += 60
        if waited > 3600:
            sys.exit("Docker container still running after 1 h - stopping batch.")

def already_done(done, sub, arm):
    return (sub, arm) in done

def main():
    B.mkdir(exist_ok=True)
    (B / "logs").mkdir(exist_ok=True); (B / "reports").mkdir(exist_ok=True)
    res = B / "results.csv"
    done = set()
    if res.exists():
        done = {(r["subject"], r["arm"]) for r in csv.DictReader(open(res))}
    else:
        csv.DictWriter(open(res, "w", newline=""), FIELDS).writeheader()
    commit = sh(["git", "rev-parse", "--short", "HEAD"], cwd=REPO, capture_output=True, text=True).stdout.strip()
    subs = sys.argv[1:] or sorted(p.name for p in SRC.glob("sub-*"))
    for sub in subs:
        for arm, (cfg, mode, tag) in ARMS.items():
            if (sub, arm) in done:
                continue
            wait_docker_idle()
            mini = build_mini(sub)
            bids = mini
            note = ""
            if mode:
                mut = B / "mut" / f"{arm}_{sub}"
                shutil.rmtree(mut, ignore_errors=True); mut.parent.mkdir(exist_ok=True)
                r = sh([sys.executable, "scripts/inject_failures.py", "--bids-dir", str(mini), "--work-dir", str(mut),
                        "--mode", mode, "--participant", sub], cwd=REPO, capture_output=True, text=True)
                if r.returncode != 0:
                    note = "injection failed: " + r.stderr[-200:]
                bids = mut
            out, ev = B / "out" / f"{arm}_{sub}", B / "eval" / f"{arm}_{sub}"
            shutil.rmtree(out, ignore_errors=True); shutil.rmtree(ev, ignore_errors=True)
            t0 = time.time()
            with open(B / "logs" / f"{arm}_{sub}.log", "w") as lf:
                p = sh([sys.executable, "main.py", "--config", cfg, "--bids-dir", str(bids), "--output-dir", str(out),
                        "--evaluation-export-root", str(ev), "--license", "./license.txt", "--participant", sub,
                        "--max-retries", "3", "--injected-failure-mode", tag], cwd=REPO, stdout=lf, stderr=subprocess.STDOUT)
            row = {"dataset": "ds000102", "subject": sub, "arm": arm, "git_commit": commit,
                   "main_exit": p.returncode, "wall_seconds": round(time.time() - t0), "note": note}
            try:
                rows = list(csv.DictReader(open(ev / "evaluation" / "run_evaluation.csv")))
                last = rows[-1]
                row.update({"final_status": last.get("final_status"), "attempt_count": last.get("attempt_count"),
                            "last_exit_code": last.get("last_exit_code"), "qa_status": last.get("qa_status"),
                            "qa_summary": last.get("qa_summary"), "retention": last.get("brain_mask_retention_ratio"),
                            "reduction": last.get("skull_strip_reduction"), "applied_rule_ids": last.get("applied_rule_ids"),
                            "config_generation_method": last.get("config_generation_method"),
                            "llm_total_tokens": last.get("llm_total_tokens")})
            except Exception as e:
                row["note"] = (note + " no evaluation row: " + str(e))[:200]
            if row.get("last_exit_code") in ("125", "126", "127") and row["wall_seconds"] < 60:
                sys.exit(f"Docker/infrastructure failure on {sub} {arm} (exit {row.get('last_exit_code')}); "
                         "row NOT recorded. Fix Docker and rerun.")
            rep = out / f"{sub}.html"
            if rep.exists():
                rdir = B / "reports" / f"{arm}_{sub}"
                rdir.mkdir(parents=True, exist_ok=True)
                shutil.copy(rep, rdir / f"{sub}.html")
                figs = out / sub / "figures"
                if figs.exists():
                    shutil.copytree(figs, rdir / sub / "figures", dirs_exist_ok=True)
            with open(res, "a", newline="") as f:
                csv.DictWriter(f, FIELDS).writerow(row)
            shutil.rmtree(out, ignore_errors=True)       # frees ~GBs; metrics are in results.csv and logs
            shutil.rmtree(B / "mut" / f"{arm}_{sub}", ignore_errors=True)
            print(f"{sub} {arm}: exit={p.returncode} attempts={row.get('attempt_count')} qa={row.get('qa_summary')} "
                  f"{row['wall_seconds']}s", flush=True)

if __name__ == "__main__":
    main()
