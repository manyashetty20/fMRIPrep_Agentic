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
│   ├── config_agent.py       # Pillar 1: Setup & RAG Logic
│   ├── vision_agent.py       # Pillar 2: Visual QC (ViT/ResNet)
│   ├── diagnostic_agent.py   # Pillar 3: Log Analysis
│   └── recovery_agent.py     # Pillar 4: Orchestration (LangGraph)
├── data/
│   ├── bids_input/           # Raw BIDS-compliant fMRI data
│   └── docs/                 # Manuals for RAG (fMRIPrep & BIDS)
├── database/                 # Persistent Vector DB (Chroma)
├── scripts/                  # Generated fMRIPrep shell scripts
└── main.py                   # System Orchestrator
```

---

# ⚙️ Setup Instructions

## 1️⃣ Environment Configuration

Create a virtual environment and install dependencies.

This setup uses:

- **Groq** → reasoning (Llama 3)  
- **HuggingFace** → local embeddings  
- **ChromaDB** → vector database  

(OpenAI-free setup)

```bash
python3 -m venv venv
source venv/bin/activate

pip install \
langchain-groq \
langchain-classic \
langchain-community \
sentence-transformers \
chromadb \
pypdf \
unstructured
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
