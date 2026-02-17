# 🧠 Agentic fMRIPrep Pipeline

This project transforms the standard **fMRIPrep** workflow into an autonomous, decision-driven system using **Agentic AI**.

It eliminates the need for:

- Manual parameter selection  
- Manual visual quality control  
- Manual error diagnosis  
- Manual pipeline restarts  

---

## 📂 Project Structure

```text
Agentic_fMRIPrep/
├── agents/
│   ├── orchestrator.py       # LangGraph Orchestration (State & Recovery)
│   ├── bids_agent.py         # Metadata Validation & Self-Healing
│   ├── resource_agent.py     # Hardware Monitoring (CPU/RAM/Docker)
│   ├── pipeline_agent.py     # Command Generation (fMRIPrep/FreeSurfer)
│   └── vision_agent.py       # Quality Assurance (Visual Audit)
├── data/
│   ├── bids_input/           # BIDS data (Toy Data $64^3$ crops)
│   └── docs/                 # Manuals for RAG (fMRIPrep & BIDS)
├── outputs/                  # Final Preprocessed NIfTI and HTML reports
├── license.txt               # Required: FreeSurfer License (See Setup)
└── main.py                   # System Entry Point

```

---

# ⚙️ Setup Instructions

This guide will help you configure your environment for the **Agentic fMRIPrep Pipeline**. Follow these steps in order to ensure all dependencies and credentials are properly established.

---

### 1️⃣ FreeSurfer License (Required)
This pipeline requires a valid FreeSurfer license to run anatomical segmentation and surface reconstruction.

1. **Obtain a license:** Register for a free license at the [Official FreeSurfer Registration Page](https://surfer.nmr.mgh.harvard.edu/registration.html).
2. **Download:** You will receive the license information via email.
3. **Save:** Create a file named `license.txt` in the **root directory** of this project and paste your license details inside.
4. **Security:** This file is automatically excluded via `.gitignore` to prevent accidental public sharing of your credentials.

---

### 2️⃣ Environment Configuration
The system uses **Groq** for high-speed LLM reasoning and **LangGraph** for multi-agent orchestration. It is recommended to use a Python virtual environment.

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the environment
source venv/bin/activate

# Install core dependencies
pip install \
  langchain-groq \
  langgraph \
  sentence-transformers \
  nibabel \
  docker \
  chromadb
```
---

## 2️⃣ API Key Configuration

Add your Groq key to your shell profile (`~/.zshrc` or `~/.bashrc`) or run:

```bash
export GROQ_API_KEY='your_groq_api_key'
```

---

## 3️⃣ Documentation Requirements

Place the following PDF manuals inside:

```
data/docs/
```

### Required files:

- `fMRIPrep_Documentation.pdf`
- `BIDS_Specification.pdf`

These documents power the **Config Agent’s RAG system**.

---

# 🧠 The Four Pillars of Agency

| Pillar | AI Model | Knowledge Source | Output |
|--------|----------|-----------------|--------|
| **Config Agent** | Groq + RAG | fMRIPrep & BIDS Manuals | Ready-to-run Shell Script |
| **Vision Agent** | Vision Transformer (ViT/ResNet) | HTML QC Report Images | Pass/Fail Score |
| **Diagnostic Agent** | LLM | Log Files + NeuroStars Posts | Root Cause Analysis |
| **Recovery Agent** | LangGraph | Human If/Then Logic | Automatic Pipeline Restart |

---

# 🔄 How It Works

## 🧩 Config Agent

- Reads BIDS dataset  
- Checks dataset completeness  
- Uses RAG over official manuals  
- Automatically selects optimal flags  

Example:
- Adds `--use-syn-sdc` if fieldmaps are missing  

Output:
- Ready-to-run shell script in `/scripts/`

---

## 👁 Vision Agent

- Parses fMRIPrep HTML reports  
- Extracts QC images  
- Detects:
  - Poor skull stripping  
  - Warped brains  
  - Bad masks  
  - Registration issues  

Output:
- Pass/Fail score with confidence  

---

## 🔍 Diagnostic Agent

- Reads fMRIPrep logs  
- Identifies:
  - Memory errors  
  - Missing fieldmaps  
  - Nipype crashes  
  - Dependency failures  

Output:
- Root-cause explanation  

---

## 🔁 Recovery Agent

- Uses diagnostic feedback  
- Modifies configuration dynamically  
- Re-runs the pipeline automatically  
- Maintains state via LangGraph  

Result:
- Fully autonomous crash recovery  

---

# ▶️ Running the System

```bash
python main.py
```

The system will:

1. Validate BIDS input  
2. Generate the fMRIPrep script  
3. Execute preprocessing  
4. Perform QC  
5. Diagnose failures (if any)  
6. Automatically recover and restart  

---

# 🚀 Key Features

- Fully autonomous preprocessing  
- OpenAI-free architecture  
- Local embeddings  
- Crash-aware workflow  
- Self-healing pipeline  
- Modular agent-based design  

---

## 🧪 Research Vision

Agentic fMRIPrep represents a step toward **self-driving scientific workflows**, where AI agents manage complex research pipelines with minimal human oversight.
