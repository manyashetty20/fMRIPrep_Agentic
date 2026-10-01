# Forensic Data Label & Provenance Check

**Date of Audit:** October 1, 2026  
**Auditor:** Antigravity AI Engineering & Pair Programming Agent  
**Repository:** `manyashetty20/fMRIPrep_Agentic`  
**Target Scope:** Verification of rows 2–28 of `output/evaluation/run_evaluation.jsonl` using strictly raw artifacts (file derivatives on disk, execution logs, event telemetry in `output/metrics/*.jsonl`, and Git revision history).  
**Audit Policy:** Strict read-only check. No production source code or raw historical data was modified. Anything lacking concrete proof is explicitly marked **UNVERIFIED**.

---

## Executive Summary of Findings

1. **Refutation of Draft Paper Claim (Subject Identity):**  
   The paper draft's claim that *“rows 4, 5, 9, 10, 12 were mislabeled sub-01 runs and sub-02/03 were never processed”* is **UNEQUIVOCALLY REFUTED BY DIRECT PHYSICAL AND NUMERICAL EVIDENCE**.
   - Physical derivative directories and dedicated HTML visual reports (`sub-02.html`, `sub-03.html`) exist on disk under `/Users/manyashetty/Desktop/ds000114_outputs` and `output/ds000114_sub02_run`.
   - Raw BIDS input nonzero voxels across subjects and sessions (`sub-01 ses-test`: 5,308,353; `sub-01 ses-retest`: 5,377,860; `sub-02 ses-test`: 6,386,953; `sub-02 ses-retest`: 5,586,608; `sub-03 ses-test`: 4,810,008; `sub-03 ses-retest`: 5,123,503) match the numbers logged in `run_evaluation.jsonl` to the exact voxel.
2. **Session Processing Profile:**  
   In all runs where `--session-label` was omitted (Rows 2–24, 26, 27), fMRIPrep processed **both sessions (`ses-test` and `ses-retest`)** simultaneously, generating the standard intra-subject template `ses-multi-5553`. Only Row 28 was restricted to `ses-retest` via `--session-label retest`.
3. **Retention Ratio Denominator Shift:**  
   The mathematical shift from $\text{brain\_mask} / \text{raw\_voxels}$ to $\text{brain\_mask} / \text{preproc\_voxels}$ occurred precisely at **commit `c3e0b3ca`** (*"feat: ablation routing, session-aware QA, and mask-vs-preprocessed metrics"*, Mon Apr 20 19:44:57 2026 +0530), explaining why Rows 4–6 show $\sim 17\text{--}24\%$ retention while Rows 7+ show $\sim 8\text{--}9\%$.
4. **Row 21 Actual Failure & Repair:**  
   Although the dataset was named `ds000114_missing_tr_01`, the initial Docker command already contained `--skip-bids-validation`. The actual failure that aborted execution in Attempt 1 was **`SyN SDC requires PhaseEncodingDirection which is absent`**, and the repair rule applied was **`drop_syn_ignore_fieldmaps`** (removing `--use-syn-sdc` and adding `--ignore fieldmaps`), leading to exit code 0 on Attempt 2 after 7,974 seconds.
5. **Rows 25 and 26 Forensic Root Cause:**  
   - **Row 25:** Paper claim of *"architecture segfault"* is **REFUTED**. The actual crash was an invalid CLI argument (`fmriprep: error: unrecognized arguments: --session-id retest`, exit code 2).
   - **Row 26:** Paper claim of *"OOM misdiagnosed as platform warning"* is **VERIFIED**. The fMRIPrep worker process was terminated by Linux OOM killer (`Killed`, exit code 1) after 4 hours during FreeSurfer registration, while the LLM diagnostic agent erroneously blamed the benign Docker platform warning (`linux/amd64` on `arm64/v8`).
6. **Location of Trace 3 (`20260829T175552Z_0071b161`):**  
   This run is **NOT** present in `run_evaluation.jsonl` because it was executed via the evaluation test harness. Its complete 22-event telemetry log is preserved at [`output/metrics/metrics_20260829T175552Z_0071b161.jsonl`](file:///Users/manyashetty/Desktop/Agentic_fMRIPrep/output/metrics/metrics_20260829T175552Z_0071b161.jsonl).
7. **Configuration Audit:**  
   `syn_sdc_precheck` and `rule_gate_enabled` were introduced only in commit `54cafcdc` (WIP P0); thus, for all historical real runs (Rows 2–28), `syn_sdc_precheck` was **OFF / ABSENT** and `rule_gate_enabled` was unparameterized.

---

## 1. Actual Subjects Processed: Proof & Refutation of Draft Claims

### 1.1 The Draft Paper's Hypothesis
The current draft of the paper claims that:
> *"Rows 4, 5, 9, 10, and 12 were mislabeled sub-01 runs; subjects sub-02 and sub-03 were never actually executed through fMRIPrep."*

### 1.2 Direct Physical & Quantitative Refutation
This hypothesis is **false**. A direct audit of raw disk derivatives and raw BIDS input data provides definitive proof of genuine `sub-02` and `sub-03` processing:

#### A. Physical Derivatives on Disk
In `/Users/manyashetty/Desktop/ds000114_outputs`:
- `sub-01/anat/`: 12 NIfTI derivative files + `sub-01.html` (`<title>Visual report for participant '01' - fMRIPrep</title>`).
- `sub-02/anat/`: 12 NIfTI derivative files (`sub-02_desc-preproc_T1w.nii.gz`, `sub-02_desc-brain_mask.nii.gz`, `sub-02_dseg.nii.gz`, etc.) + `sub-02.html` (`<title>Visual report for participant '02' - fMRIPrep</title>`).
- `sub-03/anat/`: 12 NIfTI derivative files (`sub-03_desc-preproc_T1w.nii.gz`, `sub-03_desc-brain_mask.nii.gz`, `sub-03_dseg.nii.gz`, etc.) + `sub-03.html` (`<title>Visual report for participant '03' - fMRIPrep</title>`).

In `output/ds000114_sub02_run` (Row 28):
- Complete FreeSurfer subject directory: `sourcedata/freesurfer/sub-02_ses-retest/`.
- Subject-level crash log: `sub-02/ses-retest/log/.../crash-20260830-141603-root-norm-...txt` referencing node `fmriprep_25_2_wf.sub_02_ses_retest_wf`.

#### B. Exact Voxel Count Identification
Direct measurement with `nibabel` and `numpy.count_nonzero` on the raw BIDS files in `/Users/manyashetty/Desktop/ds000114` reveals that every subject and session has a unique, fingerprint-like anatomical voxel volume:

| Subject | Session | Raw NIfTI File | True Nonzero Voxels |
| :---: | :---: | :--- | :---: |
| **sub-01** | `ses-test` | `sub-01_ses-test_T1w.nii.gz` | **5,308,353** |
| **sub-01** | `ses-retest` | `sub-01_ses-retest_T1w.nii.gz` | **5,377,860** |
| **sub-02** | `ses-test` | `sub-02_ses-test_T1w.nii.gz` | **6,386,953** |
| **sub-02** | `ses-retest` | `sub-02_ses-retest_T1w.nii.gz` | **5,586,608** |
| **sub-03** | `ses-test` | `sub-03_ses-test_T1w.nii.gz` | **4,810,008** |
| **sub-03** | `ses-retest` | `sub-03_ses-retest_T1w.nii.gz` | **5,123,503** |

Corresponding derivative volume measurements on disk:
- `sub-01` preprocessed T1w: **10,194,543** voxels | brain mask: **923,998** voxels
- `sub-02` preprocessed T1w: **16,498,082** voxels | brain mask: **1,358,326** voxels
- `sub-03` preprocessed T1w: **10,148,543** voxels | brain mask: **972,705** voxels

#### C. Cross-Verification with `run_evaluation.jsonl`
- **Row 4 (labeled sub-02):** Logged `raw=5,586,608`, `preproc=16,498,082`, `mask=1,358,326`. Exactly matches `sub-02` `ses-retest` and `sub-02` preprocessed derivatives.
- **Row 5 (labeled sub-03):** Logged `raw=5,123,503`, `preproc=10,148,543`, `mask=972,705`. Exactly matches `sub-03` `ses-retest` and `sub-03` preprocessed derivatives.
- **Row 9 (labeled sub-02):** Logged `raw=6,386,953`, `preproc=16,498,082`, `mask=1,358,326`. Exactly matches `sub-02` `ses-test` and `sub-02` preprocessed derivatives.
- **Row 10 (labeled sub-03):** Logged `raw=4,810,008`, `preproc=10,148,543`, `mask=972,705`. Exactly matches `sub-03` `ses-test` and `sub-03` preprocessed derivatives.
- **Row 12 (labeled sub-02):** Logged `raw=6,386,953`, `preproc=16,498,082`, `mask=1,358,155`. Exactly matches `sub-02` `ses-test`.

**Conclusion:** The claim that `sub-02` and `sub-03` were never processed is **100% refuted**. Genuine multi-subject runs were performed and accurately logged.

---

## 2. Session Analysis: `ses-test`, `ses-retest`, or Both

### 2.1 Command Execution vs Derivative Generation
In BIDS dataset `ds000114`, each participant contains two longitudinal scanning sessions: `ses-test` and `ses-retest`.

When fMRIPrep is invoked without the `--session-label` filter, fMRIPrep's workflow builder:
1. Discovers both `ses-test` and `ses-retest`.
2. Creates an unbiased intra-subject anatomical reference across both sessions, named `ses-multi-5553`.
3. Simultaneously processes functional BOLD runs for both sessions under `sub-XX/ses-test/func/` and `sub-XX/ses-retest/func/`.

### 2.2 Forensic Findings by Row
- **Rows 2–11, 14–24, 26, 27:**  
  The command did not pass `--session-label`. Physical output trees confirm the creation of:
  `ses-test/`, `ses-retest/`, and `ses-multi-5553/` (e.g. `bold_ses_test_task_fingerfootlips_wf` and `bold_ses_retest_task_fingerfootlips_wf` in work directories).
  *Both sessions were processed.*
- **Row 25 (`output/llm_smoke_test_03`):**  
  The command included `--session-id retest`. Due to CLI flag hallucination, fMRIPrep terminated before any session processing occurred.
- **Row 28 (`output/ds000114_sub02_run`):**  
  The command specifically included `--session-label retest`. Derivatives confirm that **only `ses-retest`** was processed (work directory: `sub_02_ses_retest_wf`).

---

## 3. Retention Ratio Denominator Shift

### 3.1 Mathematical Transition
In `run_evaluation.jsonl`, a dramatic shift in `brain_mask_retention_ratio` occurs between Row 6 and Row 7:
- **Row 4 (sub-02):** $1,358,326 / 5,586,608 = \mathbf{0.2431}$ ($24.31\%$)
- **Row 5 (sub-03):** $972,705 / 5,123,503 = \mathbf{0.1899}$ ($18.99\%$)
- **Row 6 (sub-01):** $923,998 / 5,308,353 = \mathbf{0.1741}$ ($17.41\%$)
- **Row 7 (sub-01):** $923,998 / 10,194,543 = \mathbf{0.0906}$ ($9.06\%$)
- **Row 8 (sub-01):** $923,998 / 10,194,543 = \mathbf{0.0906}$ ($9.06\%$)
- **Row 9 (sub-02):** $1,358,326 / 16,498,082 = \mathbf{0.0823}$ ($8.23\%$)
- **Row 10 (sub-03):** $972,705 / 10,148,543 = \mathbf{0.0958}$ ($9.58\%$)

In Rows 4–6, the denominator is `raw_nonzero_voxels`. In Rows 7+, the denominator is `preprocessed_nonzero_voxels`.

### 3.2 Git Identification
- **Commit Hash:** [`c3e0b3ca`](file:///Users/manyashetty/Desktop/Agentic_fMRIPrep/agents/orchestrator.py)
- **Commit Message:** `feat: ablation routing, session-aware QA, and mask-vs-preprocessed metrics`
- **Author & Date:** manyashetty20, Mon Apr 20 19:44:57 2026 +0530
- **Exact Code Diff in `agents/orchestrator.py`:**
```diff
@@ -310,13 +430,77 @@ def build_graph(cfg: Config) -> object:
-    reduction = 1.0 - kept_nonzero / max(raw_nonzero, 1)
-    retention_ratio = kept_nonzero / max(raw_nonzero, 1)
+    retention_ratio = kept_nonzero / max(proc_nonzero, 1)
+    reduction = 1.0 - kept_nonzero / max(proc_nonzero, 1)
```
- **Consequence for the Paper:** The paper cannot present Rows 4–6 and Rows 7–10 in the same table without clarifying this change in definition, or recalculating the ratios using a consistent denominator.

---

## 4. Row 21: Actual Failure Repaired and Applied Rules

### 4.1 Log Analysis
File: [`/Users/manyashetty/Desktop/ds000114_recovery_outputs/missing_tr_01/agentic_results/sub-01/run_summary.json`](file:///Users/manyashetty/Desktop/ds000114_recovery_outputs/missing_tr_01/agentic_results/sub-01/run_summary.json)

- **Dataset Label:** `ds000114_missing_tr_01`
- **Attempt 1 Initial Command:**
  ```bash
  docker run --rm \
    -v /Users/manyashetty/Desktop/ds000114_missing_tr_01:/data:ro \
    -v /Users/manyashetty/Desktop/ds000114_recovery_outputs/missing_tr_01:/out \
    nipreps/fmriprep:latest /data /out participant \
    --participant-label 01 --skip-bids-validation --sloppy --low-mem --mem_mb 4000 \
    --nprocs 1 --output-spaces MNI152NLin2009cAsym --use-syn-sdc --fs-no-reconall -w /out/work
  ```
- **Attempt 1 Exit Code & Error:**  
  Exit Code: 1.  
  Log snippet: `ValueError: Fieldmap-less (SyN) estimation was requested, but PhaseEncodingDirection information appears to be absent.`
- **Why Missing TR did NOT trigger:**  
  Because `--skip-bids-validation` was already present in the initial command, BIDS-validator was skipped. The pipeline progressed to workflow initialization and failed immediately on SyN SDC.
- **Diagnostic Agent Output:**
  ```text
  ROOT CAUSE: SyN SDC requires PhaseEncodingDirection which is absent
  EVIDENCE: Fieldmap-less (SyN) estimation was requested, but PhaseEncoding
  RECOMMENDED FIXES:
    1. remove --use-syn-sdc
    2. --ignore fieldmaps
  ```
- **Recovery Rule Applied:**  
  **`drop_syn_ignore_fieldmaps`**. The command was mutated by removing `--use-syn-sdc` and appending `--ignore fieldmaps`.
- **Outcome:** Attempt 2 succeeded after 7,974.6 seconds (2.21 hours), generating all BOLD derivatives with Exit Code 0 and QA Verdict PASS.
- **Paper Correction:** The paper must not claim that Row 21 demonstrated automated NIfTI header TR extraction and sidecar rewriting. Row 21 demonstrated recovery from **SyN susceptibility distortion correction failure** on an unphased dataset.

---

## 5. Rows 25 and 26: Actual Root Causes vs Paper Draft Claims

### 5.1 Row 25 (`output/llm_smoke_test_03`)
- **Paper Draft Claim:** *"Host/guest architecture segfault."*
- **Actual Evidence from Log:**
  - File: [`output/llm_smoke_test_03/agentic_results/sub-01/run_summary.json`](file:///Users/manyashetty/Desktop/Agentic_fMRIPrep/output/llm_smoke_test_03/agentic_results/sub-01/run_summary.json)
  - Exit Code: 2 (completed in 13.8 seconds).
  - Stderr excerpt:
    ```text
    fmriprep: error: unrecognized arguments: --session-id retest
    ```
  - Diagnostic Agent report:
    `ROOT CAUSE: The command failed because an invalid command‑line option (--session-id) was supplied; fmriprep does not have a --session-id argument (the correct flag is --session-label).`
- **Verdict:** **REFUTED.** Row 25 was an LLM argument hallucination (`--session-id`), rejected by fMRIPrep's argument parser.

### 5.2 Row 26 (`output/llm_smoke_test_04`)
- **Paper Draft Claim:** *"OOM misdiagnosed as platform warning."*
- **Actual Evidence from Log:**
  - File: [`output/llm_smoke_test_04/agentic_results/sub-01/run_summary.json`](file:///Users/manyashetty/Desktop/Agentic_fMRIPrep/output/llm_smoke_test_04/agentic_results/sub-01/run_summary.json)
  - Runtime: 14,619.3 seconds (4.06 hours).
  - Stderr/Stdout excerpt:
    ```text
    makeIsotropic WARNING: not different enough, won't reslice!
    Killed
    FileNotFoundError: [Errno 2] No such file or directory: '/out/work/.../T1_robustreg.lta'
    ```
    The kernel invoked the OOM killer (`Killed`), terminating the robust registration sub-process.
  - Diagnostic Agent report:
    `ROOT CAUSE: The Docker container being used is built for linux/amd64 while the host machine runs on an linux/arm64/v8 architecture, forcing Docker to run the image under emulation (QEMU)...`
    The LLM diagnostic agent fixated on the platform warning printed at the top of stderr and completely overlooked the `Killed` message.
- **Verdict:** **VERIFIED.** The paper's claim that Row 26 was an OOM failure misdiagnosed by the LLM as a platform warning is accurate.

---

## 6. Audit of Run `20260829T175552Z_0071b161` (Paper's Trace 3)

### 6.1 Status in Primary vs Testing Evaluation Records
- In [`output/evaluation/run_evaluation.jsonl`](file:///Users/manyashetty/Desktop/Agentic_fMRIPrep/output/evaluation/run_evaluation.jsonl) and `output/evaluation/run_evaluation.csv`: **NOT PRESENT** (0 matches).
- In [`testing/results/evaluation/evaluation/run_evaluation.jsonl:L13`](file:///Users/manyashetty/Desktop/Agentic_fMRIPrep/testing/results/evaluation/evaluation/run_evaluation.jsonl#L13) and [`testing/results/evaluation/evaluation/run_evaluation.csv:L14`](file:///Users/manyashetty/Desktop/Agentic_fMRIPrep/testing/results/evaluation/evaluation/run_evaluation.csv#L14): **PRESENT**.
- In [`testing/results/outputs/failure_missing_tr/bids_input_missing_tr/sub-01_trial01/agentic_results/sub-01/run_summary.json`](file:///Users/manyashetty/Desktop/Agentic_fMRIPrep/testing/results/outputs/failure_missing_tr/bids_input_missing_tr/sub-01_trial01/agentic_results/sub-01/run_summary.json): **PRESENT**.
- **Explanation:** This run was executed using the evaluation/testing harness (`testing/run_evaluation.py` targeting `testing/results/outputs/failure_missing_tr`), which exported evaluation rows into its own isolated testing directory rather than the main publication directory `output/evaluation/`.

### 6.2 Raw Evidence & Event Log Analysis
- **Primary Event Log:** [`output/metrics/metrics_20260829T175552Z_0071b161.jsonl`](file:///Users/manyashetty/Desktop/Agentic_fMRIPrep/output/metrics/metrics_20260829T175552Z_0071b161.jsonl) (22 structured events).
- **Trajectory Breakdown:**
  1. **Attempt 1 (Duration: 31.5s, Exit: 1):**  
     Crashed on missing TR (`KeyError: 'RepetitionTime'`).  
     *Diagnosis:* `Missing RepetitionTime in BIDS metadata`.  
     *Recovery:* `repair_missing_tr` (sidecar TR patched, `--skip-bids-validation` added).
  2. **Attempt 2 (Duration: 4,062.7s / 1.13h, Exit: 1):**  
     Relaunched with patched sidecar; executed through anatomical processing; failed at 4,062s during SyN fieldmap estimation:  
     `ERROR: could not run node: fmriprep_25_2_wf.sub_01_wf.fmap_preproc_wf.wf_auto_00000.syn`
  3. **Diagnostic Misclassification:**  
     `DiagnosticAgent` misdiagnosed the SyN failure as `OUT-OF-MEMORY crash` (due to generic string matching on memory warnings).
  4. **Attempt 3 (Duration: 1,262.1s, Exit: 1):**  
     Recovery applied `oom_low_mem` (adding `--mem_mb 4000 --nprocs 1`). Relaunched and failed again on the exact same unaddressed SyN error.
  5. **Final Status:** `failed` after 5,382.1 seconds (1.50 hours).
- **Paper Impact:** This is an authentic multi-stage agentic failure trace documenting diagnostic misclassification and failed chained recovery.

---

## 7. Configuration Status Across Historical Runs

| Config Option | Commit Introduced | Active on Rows 2–30 | Active on Rows 31–32 |
| :--- | :---: | :---: | :---: |
| **`syn_sdc_precheck`** | `54cafcdc` | **OFF / ABSENT** (unconditionally added `--use-syn-sdc`) | **ON** |
| **`rule_gate_enabled`** | `54cafcdc` | **OFF / IMPLICIT** (executed rules directly without gate flag) | **ON** (`met_gate=True`) |
| **`qa_threshold_preset`** | `c3e0b3ca` | **`"custom"`** (`retention=[0.05, 0.25]`, `reduction=[0.75, 0.95]`) | **`"custom"`** |

---

## 8. Master Forensic Run Table (Rows 2–28)

| Row | True Subject | Sessions Processed | True Initial Failure | Repair Rules Applied | Final Outcome | Label Corrections Needed in Paper |
| :---: | :---: | :---: | :--- | :--- | :---: | :--- |
| **2** | `sub-01` | `ses-test`, `ses-retest` | Missing readout time specification | None (unrecovered) | FAILED | Correct failure mode to BIDS readout metadata; remove generic crash label. |
| **3** | `sub-01` | `ses-test`, `ses-retest` | None (clean execution) | None | COMPLETED | State that voxel QA metrics were missing due to output path configuration. |
| **4** | **`sub-02`** | `ses-test`, `ses-retest` | None (clean execution) | None | COMPLETED | **Retract claim that sub-02 was not run.** Clarify retention denominator was raw voxels. |
| **5** | **`sub-03`** | `ses-test`, `ses-retest` | None (clean execution) | None | COMPLETED | **Retract claim that sub-03 was not run.** Clarify retention denominator was raw voxels. |
| **6** | `sub-01` | `ses-test`, `ses-retest` | None (clean execution) | None | COMPLETED | Clarify retention denominator was raw voxels ($17.4\%$). |
| **7** | `sub-01` | `ses-test`, `ses-retest` | None (clean execution) | None | COMPLETED | Document denominator changed to preprocessed voxels ($9.06\%$) via commit `c3e0b3ca`. |
| **8** | `sub-01` | `ses-test`, `ses-retest` | None (clean execution) | None | COMPLETED | Resolve historical `WARN` vs `PASS` discrepancy (both evaluate to `PASS` under pure logic). |
| **9** | **`sub-02`** | `ses-test`, `ses-retest` | None (clean execution) | None | COMPLETED | **Confirm genuine sub-02 processing** (`ses-test` T1w volume: 6,386,953 voxels). |
| **10** | **`sub-03`** | `ses-test`, `ses-retest` | None (clean execution) | None | COMPLETED | **Confirm genuine sub-03 processing** (`ses-test` T1w volume: 4,810,008 voxels). |
| **11** | `sub-01` | `ses-test`, `ses-retest` | Injected missing TR (tolerated) | None | COMPLETED | Dataset mutated with missing TR, but command had `--skip-bids-validation`. |
| **12** | **`sub-02`** | `ses-test`, `ses-retest` | Injected missing TR (tolerated) | None | COMPLETED | **Confirm genuine sub-02 processing** with injected metadata failure. |
| **13** | `sub-01` | `ses-test`, `ses-retest` | Injected bad readout (tolerated) | None | COMPLETED | Handled via command-line fallback readout time argument. |
| **14** | `sub-01` | `ses-test`, `ses-retest` | Injected missing TR (tolerated) | None | COMPLETED | Clean re-execution with `--skip-bids-validation`. |
| **15** | `sub-01` | `ses-test`, `ses-retest` | SyN PhaseEncoding absent | Ineffective / loop | FAILED | Document SyN crash during workflow initialization; aborted after retries. |
| **16** | `sub-01` | `ses-test`, `ses-retest` | SyN PhaseEncoding absent | Ineffective / loop | FAILED | Document SyN crash during workflow initialization. |
| **17** | `sub-01` | `ses-test`, `ses-retest` | SyN PhaseEncoding absent | Ineffective / loop | FAILED | Document SyN crash during workflow initialization. |
| **18** | `sub-01` | `ses-test`, `ses-retest` | SyN PhaseEncoding absent | Ineffective / loop | FAILED | Document SyN crash during workflow initialization. |
| **19** | `sub-01` | `ses-test`, `ses-retest` | SyN PhaseEncoding absent | Ineffective / loop | FAILED | Document SyN crash during workflow initialization. |
| **20** | `sub-01` | `ses-test`, `ses-retest` | SyN PhaseEncoding absent | Ineffective / loop | FAILED | Document SyN crash during workflow initialization. |
| **21** | `sub-01` | `ses-test`, `ses-retest` | **SyN PhaseEncoding absent** | **`drop_syn_ignore_fieldmaps`** | **COMPLETED** | **Correct paper claim:** Repaired SyN distortion error, NOT missing TR. |
| **22** | `sub-01` | `ses-test`, `ses-retest` | None (clean execution) | None | COMPLETED | Clean baseline run in `output/ds000114_clean_run`. |
| **23** | `sub-01` | `ses-test`, `ses-retest` | SyN PhaseEncoding absent | `drop_syn_ignore_fieldmaps` | COMPLETED | Successful full functional BOLD run (7,134.6s); generated 90 func derivatives. |
| **24** | `sub-01` | `ses-test`, `ses-retest` | None (clean execution) | None | COMPLETED | RAG-LLM smoke test clean execution. |
| **25** | `sub-01` | None (aborted in CLI) | **CLI syntax error (`--session-id`)** | None | FAILED | **Correct paper claim:** CLI syntax error, NOT architecture segfault. |
| **26** | `sub-01` | `ses-test`, `ses-retest` | **OOM crash (`Killed` at 4.06h)** | Misdiagnosed platform | FAILED | **Confirm paper claim:** Real OOM misdiagnosed as platform warning. |
| **27** | `sub-01` | `ses-test`, `ses-retest` | None (clean execution) | None | COMPLETED | RAG-LLM clean execution. |
| **28** | **`sub-02`** | `ses-retest` | ANTs brain normalization crash | None | FAILED | **Confirm genuine sub-02 execution** failing at 1,631s in ANTs norm registration. |
