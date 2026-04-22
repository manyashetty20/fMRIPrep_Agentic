from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, "/tmp/codex_pdf_deps")

from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

OUTPUT_PATH = ROOT / "output" / "pdf" / "capstone_report_corrections.pdf"

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="TitleX", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=17, leading=21, textColor=colors.HexColor("#12344d"), spaceAfter=6))
styles.add(ParagraphStyle(name="SectionX", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=10.5, leading=12, textColor=colors.HexColor("#0b5f7a"), spaceBefore=7, spaceAfter=3))
styles.add(ParagraphStyle(name="BodyX", parent=styles["BodyText"], fontName="Helvetica", fontSize=8.5, leading=10.4, textColor=colors.HexColor("#1e2933"), spaceAfter=2))
styles.add(ParagraphStyle(name="BulletX", parent=styles["BodyText"], fontName="Helvetica", fontSize=8.4, leading=10, leftIndent=10, firstLineIndent=-7, textColor=colors.HexColor("#1e2933"), spaceAfter=1.2))

def b(text: str) -> Paragraph:
    return Paragraph(f"&bull; {text}", styles["BulletX"])


def build() -> Path:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(str(OUTPUT_PATH), pagesize=LETTER, leftMargin=0.58*inch, rightMargin=0.58*inch, topMargin=0.52*inch, bottomMargin=0.48*inch, title="Capstone Report Corrections", author="Codex")

    story = [
        Paragraph("Capstone Report Corrections (Repo-Verified)", styles["TitleX"]),
        Paragraph("Use this as a replacement checklist for capstone_report.pdf so claims match the current implementation.", styles["BodyX"]),

        Paragraph("Critical Replacements", styles["SectionX"]),
        b("Replace references to separate BIDS Agent and Resource Agent as active graph nodes. Current graph nodes are planner, executor, detective (diagnostic), engineer (recovery), vision_agent, and success_finalize."),
        b("Replace 'quality score 0.94/1.0' language. Current QA outputs categorical summary PASS/WARN/FAIL with explicit voxel and file-presence metrics."),
        b("Replace naming-conflict recovery text that claims -nogcareg/-nocanorm injection. Current rule for naming conflict ensures --fs-no-reconall."),
        b("Update diagnostic section: there is now a dedicated priority-85 heuristic for missing PhaseEncodingDirection with SyN/fieldmap-less SDC.") ,
        b("Update recovery section: missing TR handling now performs BIDS sidecar repair by writing RepetitionTime from NIfTI headers, then retries with command-change-safe behavior."),

        Paragraph("Chapter 3 Replacement Text", styles["SectionX"]),
        Paragraph("Replace MAS node list with:", styles["BodyX"]),
        b("Orchestrator graph: planner -> executor -> (success -> vision_agent or success_finalize) ; on failure -> detective -> engineer -> executor (bounded retries)."),
        b("Diagnostic and Recovery are the active failure-handling agents; BIDS metadata repair is performed inside Recovery logic, not a standalone graph node."),

        Paragraph("Chapter 5 Replacement Text", styles["SectionX"]),
        b("Diagnostic heuristics currently include: missing readout timing, OOM, missing TR, PhaseEncodingDirection absent for SyN SDC, fieldmap/SDC errors, FreeSurfer license errors, naming conflicts, and Docker daemon errors."),
        b("Recovery details: OOM adds low-memory flags and nprocs control; missing TR triggers sidecar repair by extracting TR from BOLD NIfTI headers; SyN/PhaseEncoding failures remove --use-syn-sdc and enforce --ignore fieldmaps."),
        b("Generic fieldmap recovery now conditionally adds --use-syn-sdc only when --ignore is not already present, and always ensures --ignore fieldmaps."),

        Paragraph("Chapter 6 Replacement Text", styles["SectionX"]),
        b("Replace numeric Vision score narrative with measured outputs: qa_summary (PASS/WARN/FAIL), qa_warn_count, qa_fail_count, report_found, output_found, mni_found, brain_mask_found, and voxel metrics in qa_metrics.json."),
        b("Use output paths under output_dir/agentic_results/<participant>/ for qa_report.txt, qa_metrics.json, and run_summary.json as primary evidence artifacts."),

        Paragraph("Missing Sections To Add", styles["SectionX"]),
        b("Ablation study table: full system vs no-recovery vs no-diagnosis vs no-vision (success rate, attempts, wall-clock)."),
        b("Baseline comparison table: plain fMRIPrep (scripts/run_baseline.py) vs agentic runs using same participants and settings."),
        b("Failure-injection applicability matrix: for each dataset/subject/mode (missing_tr, bad_readout, missing_fmap, oom), mark applicable/skipped and recovery outcome."),
        b("Reproducibility appendix: git commit hash, exact commands, machine specs, Docker image tag, config used, and dataset IDs/subject lists."),

        Paragraph("Exact Artifacts To Cite", styles["SectionX"]),
        b("run_summary.json (per run): final_status, attempt_count, events timeline."),
        b("qa_metrics.json (per run): objective QA metrics and summary."),
        b("output/evaluation/run_evaluation.csv and baseline_evaluation.csv: aggregate tables for report figures."),

        Spacer(1, 8),
        Paragraph("Generated from current repository state and intended to replace outdated claims in capstone_report.pdf.", styles["BodyX"]),
    ]

    doc.build(story)
    return OUTPUT_PATH


if __name__ == "__main__":
    print(build())
