from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, "/tmp/codex_pdf_deps")

from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


OUTPUT_PATH = ROOT / "output" / "pdf" / "agentic_fmriprep_app_summary.pdf"


def bullet(text: str) -> Paragraph:
    return Paragraph(f"&bull; {text}", styles["bullet"])


styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        name="TitleCard",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#12344d"),
        spaceAfter=8,
    )
)
styles.add(
    ParagraphStyle(
        name="Section",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=10.2,
        leading=12,
        textColor=colors.HexColor("#0b5f7a"),
        spaceBefore=6,
        spaceAfter=3,
    )
)
styles.add(
    ParagraphStyle(
        name="BodyTight",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=8.7,
        leading=10.7,
        textColor=colors.HexColor("#1e2933"),
        spaceAfter=3,
    )
)
styles.add(
    ParagraphStyle(
        name="bullet",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=10.2,
        leftIndent=10,
        firstLineIndent=-7,
        bulletIndent=0,
        textColor=colors.HexColor("#1e2933"),
        spaceAfter=1.5,
    )
)
styles.add(
    ParagraphStyle(
        name="Mini",
        parent=styles["BodyText"],
        fontName="Helvetica-Oblique",
        fontSize=7.6,
        leading=9.1,
        textColor=colors.HexColor("#5b6570"),
        spaceBefore=5,
    )
)


def build_pdf() -> Path:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    doc = SimpleDocTemplate(
        str(OUTPUT_PATH),
        pagesize=LETTER,
        leftMargin=0.58 * inch,
        rightMargin=0.58 * inch,
        topMargin=0.5 * inch,
        bottomMargin=0.48 * inch,
        title="Agentic fMRIPrep App Summary",
        author="Codex",
    )

    story = [
        Paragraph("Agentic fMRIPrep", styles["TitleCard"]),
        Paragraph(
            "One-page repo-based summary of the application in "
            "/Users/manyashetty/Desktop/Agentic_fMRIPrep.",
            styles["BodyTight"],
        ),
        Spacer(1, 2),
        Paragraph("What It Is", styles["Section"]),
        Paragraph(
            "A Python application that wraps fMRIPrep in a LangGraph-driven agent loop so command generation, execution, "
            "failure diagnosis, recovery, and post-run QA can happen with less manual intervention. "
            "The repo positions it as an autonomous preprocessing pipeline for BIDS-formatted neuroimaging data.",
            styles["BodyTight"],
        ),
        Paragraph("Who It’s For", styles["Section"]),
        Paragraph(
            "Primary user: a neuroimaging researcher or data engineer who runs fMRIPrep on BIDS datasets and wants help "
            "with configuration, retries, and quality checks.",
            styles["BodyTight"],
        ),
        Paragraph("What It Does", styles["Section"]),
        bullet("Loads runtime settings from YAML, environment variables, and CLI overrides via a central Config object."),
        bullet("Builds an fMRIPrep Docker command from repo config and dataset facts such as participant ID and fieldmap presence."),
        bullet("Optionally uses local PDF manuals plus embeddings/Chroma for RAG-backed command generation when dependencies are available."),
        bullet("Executes the generated command and captures stdout/stderr for downstream handling."),
        bullet("Diagnoses failures with either an LLM or regex heuristics for common fMRIPrep, Docker, metadata, and memory issues."),
        bullet("Applies command-level recovery fixes and loops through retries up to the configured maximum."),
        bullet("Runs a post-execution QA step that compares expected anatomical input/output files and reports simple voxel-based checks when possible."),
        Paragraph("How It Works", styles["Section"]),
        Paragraph(
            "<b>Entry point:</b> main.py parses CLI args, builds Config, validates paths, and invokes a compiled LangGraph app. "
            "<b>Core services:</b> agents/config_agent.py generates the Docker command; agents/orchestrator.py runs the planner-executor-detective-engineer loop; "
            "agents/diagnostic_agent.py interprets failures; agents/recovery_agent.py rewrites the command; config_loader.py resolves config; "
            "local docs live in data/docs/; vectors persist in database/vector_store/; data enters from data/bids_input/; outputs land in outputs/. "
            "<b>Data flow:</b> config + BIDS paths -> command generation -> subprocess execution -> logs -> diagnosis -> command repair/retry -> output QA -> final console report.",
            styles["BodyTight"],
        ),
        Paragraph("How to Run", styles["Section"]),
        bullet("Create and activate a Python virtual environment."),
        bullet("Install the packages named in README.md: langchain-groq, langgraph, sentence-transformers, nibabel, docker, and chromadb. Exact dependency manifest: Not found in repo."),
        bullet("Place a valid license.txt in the repo root and ensure Docker is running."),
        bullet("Keep the local manuals in data/docs/ and BIDS input in data/bids_input/ (both are present in this repo snapshot)."),
        bullet("Set GROQ_API_KEY if using the default Groq-backed configuration, then run python main.py."),
        Paragraph(
            "Repo gaps explicitly marked: tests/CI setup not found in repo; a packaged dependency file such as requirements.txt or pyproject.toml not found in repo.",
            styles["Mini"],
        ),
    ]

    doc.build(story)
    return OUTPUT_PATH


if __name__ == "__main__":
    path = build_pdf()
    print(path)
