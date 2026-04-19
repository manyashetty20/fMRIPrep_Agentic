from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, "/tmp/codex_pdf_deps")

from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer


OUTPUT_PATH = ROOT / "output" / "pdf" / "agentic_fmriprep_agents_and_recovery.pdf"

styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        name="DocTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#12344d"),
        spaceAfter=6,
    )
)
styles.add(
    ParagraphStyle(
        name="Subtitle",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9.2,
        leading=11.2,
        textColor=colors.HexColor("#334e68"),
        spaceAfter=8,
    )
)
styles.add(
    ParagraphStyle(
        name="Section",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=10.5,
        leading=12,
        textColor=colors.HexColor("#0b5f7a"),
        spaceBefore=7,
        spaceAfter=3,
    )
)
styles.add(
    ParagraphStyle(
        name="Body",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=10.5,
        textColor=colors.HexColor("#1e2933"),
        spaceAfter=2,
    )
)
styles.add(
    ParagraphStyle(
        name="AgentBullet",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=8.4,
        leading=10.0,
        leftIndent=10,
        firstLineIndent=-7,
        textColor=colors.HexColor("#1e2933"),
        spaceAfter=1.5,
    )
)


def bullet(text: str) -> Paragraph:
    return Paragraph(f"&bull; {text}", styles["AgentBullet"])


def build_pdf() -> Path:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUTPUT_PATH),
        pagesize=LETTER,
        leftMargin=0.58 * inch,
        rightMargin=0.58 * inch,
        topMargin=0.5 * inch,
        bottomMargin=0.48 * inch,
        title="Agentic fMRIPrep Agents and Recovery",
        author="Codex",
    )

    story = [
        Paragraph("Agentic fMRIPrep: Agents, Errors, and Recovery", styles["DocTitle"]),
        Paragraph(
            "Repo-grounded overview of the four-agent loop, how each stage works, the main errors encountered during toy-data and smoke runs, and how the pipeline rectified them.",
            styles["Subtitle"],
        ),
        Paragraph("Agent Loop", styles["Section"]),
        bullet("Config Agent: builds the fMRIPrep Docker command from Config values, participant information, dataset facts, and local docs when RAG is available. In the current code it can proactively add flags such as --use-syn-sdc, --fs-no-reconall, and --fallback-total-readout-time when metadata inspection indicates they are needed."),
        bullet("Executor: runs the generated command, captures stdout and stderr, and records a structured execution event for each attempt."),
        bullet("Diagnostic Agent: reads the failure log and identifies one primary root cause with evidence and suggested fixes. If no LLM is available it falls back to heuristics for common issues such as missing readout timing, out-of-memory, fieldmap problems, FreeSurfer licensing, and Docker daemon failures."),
        bullet("Recovery Agent: rewrites the failed command with targeted fixes. Examples include adding --low-mem and reducing --nprocs for memory failures, or adding --fallback-total-readout-time for missing readout timing."),
        bullet("Vision / QA stage: runs only after a successful execution, resolves the real derivatives layout from the output tree, and writes qa_report.txt plus qa_metrics.json with concrete metrics instead of an arbitrary score."),
        Paragraph("How The Pipeline Works", styles["Section"]),
        bullet("LangGraph state machine in agents/orchestrator.py wires the loop as planner -> executor -> detective -> engineer -> executor, with a vision step after success."),
        bullet("main.py now writes publication-style provenance artifacts for each run: run_summary.json, config_snapshot.json, qa_report.txt, and qa_metrics.json under output_dir/agentic_results/sub-01/."),
        bullet("Retries are bounded by max_recovery_attempts, but the graph now stops early if recovery does not produce a real command change. This prevents wasteful reruns of the same command."),
        Paragraph("Observed Errors And Rectification", styles["Section"]),
        bullet("Synthetic smoke-test OOM failure: the smoke harness intentionally triggered exit code 137 with an out-of-memory message. Diagnosis labeled it OUT-OF-MEMORY crash, recovery added --low-mem and reduced --nprocs to 1, and the second attempt succeeded."),
        bullet("Real toy-data metadata failure: fMRIPrep failed because BOLD metadata lacked usable readout timing. Recovery was upgraded to add --fallback-total-readout-time 0.05, and config generation was later improved to include that flag proactively before the first attempt when metadata is missing."),
        bullet("Real environment failure: Docker permission or daemon access problems were correctly diagnosed as a Docker daemon / permissions error. Because recovery had no valid command-level fix, the pipeline now stops instead of looping uselessly."),
        bullet("QA path failure: the original QA logic assumed outputs always lived under output_dir/fmriprep/sub-01. The code now discovers either output_dir/sub-01 or output_dir/fmriprep/sub-01, which fixed false QA misses on real toy-data runs."),
        bullet("Reporting issue: the old Quality Score formula was removed. QA now reports raw nonzero voxels, preprocessed nonzero voxels, brain-mask voxels, brain-mask retention ratio, skull-strip reduction, MNI file detection, and a simple QA Summary."),
        Paragraph("Smoke Recovery Demo", styles["Section"]),
        bullet("Smoke run location: tmp/full_agent_smoke/"),
        bullet("Attempt 1 failed with exit 137 and the message 'out of memory'."),
        bullet("Diagnosis: ROOT CAUSE: OUT-OF-MEMORY crash. Evidence: out of memory."),
        bullet("Recovered command added --low-mem and rewrote the command to use --nprocs 1."),
        bullet("Attempt 2 succeeded and Vision / QA ran automatically afterward."),
        PageBreak(),
        Paragraph("Validated Toy-Data Result", styles["Section"]),
        bullet("Validated run: tmp/real_toy_outputs_pub3"),
        bullet("Attempts: 1. The Config Agent added --fallback-total-readout-time 0.05 proactively, so the run succeeded on the first try."),
        bullet("QA Summary: PASS"),
        bullet("Raw voxels: 262,144"),
        bullet("Preprocessed voxels: 261,502"),
        bullet("Brain-mask voxels: 258,332"),
        bullet("Brain-mask retention ratio: 98.5%"),
        bullet("Skull-strip reduction: 1.5%"),
        bullet("Normalization: MNI-space preprocessed output file detected."),
        Paragraph("Why This Is Stronger Now", styles["Section"]),
        bullet("The system is more autonomous because known metadata issues can be corrected before the first execution instead of only after a crash."),
        bullet("The system is more honest because diagnosis focuses on the primary cause, QA is based on explicit metrics, and no-op recoveries no longer consume extra attempts."),
        bullet("The system is more publishable because every run now saves provenance and QA artifacts that can be inspected, compared, and reported."),
        Paragraph("Current Limits", styles["Section"]),
        bullet("This is still not a claim of perfect autonomy. Recovery is still rule-guided, not open-ended scientific reasoning."),
        bullet("The smoke success path is a controlled demo using mock Docker. It proves the orchestration loop, not full scientific validity."),
        bullet("A strong journal paper would still need multi-dataset evaluation, baselines, quantitative recovery rates, and external QA validation beyond the current heuristic checks."),
        Paragraph("Useful Output Files", styles["Section"]),
        bullet("Smoke log: tmp/full_agent_smoke/smoke_run.log"),
        bullet("Toy-data run summary: tmp/real_toy_outputs_pub3/agentic_results/sub-01/run_summary.json"),
        bullet("Toy-data config snapshot: tmp/real_toy_outputs_pub3/agentic_results/sub-01/config_snapshot.json"),
        bullet("Toy-data QA report: tmp/real_toy_outputs_pub3/agentic_results/sub-01/qa_report.txt"),
        bullet("Toy-data QA metrics: tmp/real_toy_outputs_pub3/agentic_results/sub-01/qa_metrics.json"),
    ]

    doc.build(story)
    return OUTPUT_PATH


if __name__ == "__main__":
    print(build_pdf())
