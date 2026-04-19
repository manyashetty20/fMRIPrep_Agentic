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


OUTPUT_PATH = ROOT / "output" / "pdf" / "agentic_fmriprep_error_report.pdf"

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
        leading=10.3,
        textColor=colors.HexColor("#1e2933"),
        spaceAfter=2,
    )
)
styles.add(
    ParagraphStyle(
        name="TightBullet",
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
    return Paragraph(f"&bull; {text}", styles["TightBullet"])


def build_pdf() -> Path:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUTPUT_PATH),
        pagesize=LETTER,
        leftMargin=0.58 * inch,
        rightMargin=0.58 * inch,
        topMargin=0.52 * inch,
        bottomMargin=0.48 * inch,
        title="Agentic fMRIPrep Error Report",
        author="Codex",
    )

    story = [
        Paragraph("Agentic fMRIPrep Error Report", styles["DocTitle"]),
        Paragraph(
            "Summary of errors encountered during smoke-test and real toy-data runs, plus how the pipeline or operator resolved them.",
            styles["Body"],
        ),
        Paragraph("Current Assessment", styles["Section"]),
        bullet("The agent flow is working well for the tested toy-data pipeline: planning, execution, diagnosis, recovery, rerun, and QA all completed on the final real run."),
        bullet("It is not accurate to call the system perfect yet. It still uses deterministic recovery rules and a few configured defaults such as fallback readout time and optional convenience flags."),
        bullet("The hardcoded incorrect output-path assumption was removed; QA now discovers the real derivative layout and writes structured results to agentic_results/sub-01/."),
        Paragraph("Encountered Errors", styles["Section"]),
        bullet("Synthetic smoke-test OOM failure: the mock docker shim forced an out-of-memory style exit 137. Diagnosis labeled it as memory pressure, recovery added --low-mem and reduced nprocs to 1, and the second attempt succeeded. This proved the orchestration loop."),
        bullet("Real environment failure: Docker daemon unavailable or inaccessible. Diagnosis correctly identified a Docker daemon/permission problem. This was not fixed by code; it required starting Docker and making the socket reachable from the shell."),
        bullet("Real fMRIPrep failure: missing readout timing metadata for the BOLD files. Initially the pipeline failed during SDC/fmap setup. Recovery was upgraded to add --fallback-total-readout-time 0.05, and config generation was further improved to add that flag proactively when metadata inspection shows it is needed."),
        bullet("Real QA-path failure: the vision step originally assumed outputs would live under output_dir/fmriprep/sub-01/. The successful run actually wrote derivatives under output_dir/sub-01/. The QA code was changed to resolve the real subject derivative directory from the output tree instead of assuming one fixed layout."),
        bullet("Real reporting issue: QA originally exposed an arbitrary Quality Score formula. That was replaced with concrete metrics: raw nonzero voxels, preprocessed nonzero voxels, brain-mask nonzero voxels, retention ratio, skull-strip reduction, MNI output presence, and a simple QA Summary."),
        Paragraph("How The Model Fixed Them", styles["Section"]),
        bullet("Diagnosis logic now chooses one primary cause with evidence instead of emitting a noisy stack of loosely matching regex labels."),
        bullet("Recovery logic now retries only when it produced a real command change; otherwise it stops instead of looping on the same command."),
        bullet("Config generation now inspects BOLD sidecar metadata before launch and can proactively include --fallback-total-readout-time 0.05 for non-anat runs when TotalReadoutTime or EffectiveEchoSpacing-based timing cannot be inferred."),
        bullet("QA results are now printed in the final report and saved to qa_report.txt and qa_metrics.json under the run output."),
        Paragraph("Latest Successful Real Run", styles["Section"]),
        bullet("Run: tmp/real_toy_outputs_retry4"),
        bullet("Attempts: 1"),
        bullet("QA Summary: PASS"),
        bullet("Raw voxels: 262,144; preprocessed voxels: 261,502; brain-mask voxels: 258,048"),
        bullet("Brain-mask retention ratio: 98.4%; skull-strip reduction: 1.6%"),
        bullet("Normalization: MNI-space preprocessed output file detected"),
        Paragraph("Result Files", styles["Section"]),
        bullet("QA report: tmp/real_toy_outputs_retry4/agentic_results/sub-01/qa_report.txt"),
        bullet("QA metrics: tmp/real_toy_outputs_retry4/agentic_results/sub-01/qa_metrics.json"),
        bullet("Run report: tmp/real_toy_outputs_retry4/sub-01.html"),
    ]

    doc.build(story)
    return OUTPUT_PATH


if __name__ == "__main__":
    print(build_pdf())
