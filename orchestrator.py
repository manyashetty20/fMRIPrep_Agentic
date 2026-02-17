from typing import TypedDict, Annotated, List
from langgraph.graph import StateGraph, END
import operator
import os
import subprocess

# 1. Define the State
class AgentState(TypedDict):
    command: str
    log: str
    history: Annotated[List[str], operator.add]
    status: str  

# 2. Initialize Agents
from agents.config_agent import ConfigAgent
from agents.diagnostic_agent import DiagnosticAgent
from agents.recovery_agent import RecoveryAgent

config = ConfigAgent()
detective = DiagnosticAgent()
engineer = RecoveryAgent()

# 3. Define the Nodes
def planning_node(state: AgentState):
    print("--- [GRAPH] Planning Phase ---")
    # Use absolute paths to avoid the messy "$HOME/./" output
    bids_dir = os.path.abspath("./data/bids_input")
    participant_id = "sub-01"
    
    fmap_path = os.path.join(bids_dir, participant_id, 'fmap')
    has_fmap = os.path.exists(fmap_path) and os.path.isdir(fmap_path) and len(os.listdir(fmap_path)) > 0
    
    cmd = config.generate_command(bids_dir, participant_id, has_fmap)
    return {"command": cmd, "status": "executing"}

def execution_node(state: AgentState):
    print(f"--- [GRAPH] Execution Phase ---")
    
    bids_dir = os.path.abspath("./data/bids_input")
    out_dir = os.path.abspath("./outputs")
    license_path = os.path.abspath("./license.txt")
    
    # TOY CONFIG: Added --sloppy and very low resource caps
    cmd = (
        f"docker run --rm "
        f"-v {bids_dir}:/data:ro "
        f"-v {out_dir}:/out "
        f"-v {license_path}:/opt/freesurfer/license.txt:ro "
        f"poldracklab/fmriprep:latest "
        f"/data /out participant "
        f"--skip-bids-validation "
        f"--anat-only "
        f"--sloppy "       # <--- Crucial: Reduces math precision for speed
        f"--low-mem "
        f"--mem_mb 4000 "  # Caps RAM usage
        f"--nprocs 1 "     # No multitasking
        f"-w /out/work"
    )

    print(f"🚀 Running TOY PIPELINE validation...")
    
    try:
        subprocess.run(cmd, shell=True, check=True)
        return {"status": "success", "command": cmd}
    except Exception as e:
        return {"log": str(e), "status": "diagnosing"}
    
def diagnostic_node(state: AgentState):
    print("--- [GRAPH] Diagnostic Phase ---")
    report = detective.diagnose_crash(state['log'])
    return {"history": [report], "status": "recovering"}

def recovery_node(state: AgentState):
    print("--- [GRAPH] Recovery Phase ---")
    # Apply fix
    new_cmd = engineer.apply_fix(state['command'], state['history'][-1])
    # Ensure the command in state is updated so the loop recognizes the fix
    return {"command": new_cmd, "status": "executing"}

def vision_agent_node(state: AgentState):
    print("--- [GRAPH] Vision Quality Phase ---")
    
    # Paths for comparison
    input_img = "./data/bids_input/sub-01/anat/sub-01_T1w.nii.gz"
    output_img = "./outputs/fmriprep/sub-01/anat/sub-01_desc-preproc_T1w.nii.gz"
    
    print(f"🧐 Comparing Input: {input_img}")
    print(f"✨ Against Output: {output_img}")
    
    # This is where your future labeled model will sit.
    # For now, we simulate the 'Comparison Logic'
    comparison_report = (
        "VISUAL AUDIT: Preprocessing successful. \n"
        "- Skull-stripping: REMOVED non-brain tissue (neck/dura).\n"
        "- Normalization: ALIGNED to MNI152 template.\n"
        "- Quality Score: 0.94/1.0"
    )
    
    return {"history": [comparison_report], "status": "completed"}

# 4. Build the Graph
workflow = StateGraph(AgentState)

# Add all Nodes
workflow.add_node("planner", planning_node)
workflow.add_node("executor", execution_node)
workflow.add_node("detective", diagnostic_node)
workflow.add_node("engineer", recovery_node)
workflow.add_node("vision_agent", vision_agent_node) # Vision added here

# --- DEFINE THE FLOW ---

# Start with Planning
workflow.set_entry_point("planner")
workflow.add_edge("planner", "executor")

# The Logic Gate for Execution
# We ONLY define this once to avoid the ValueError
workflow.add_conditional_edges(
    "executor",
    lambda x: x["status"],
    {
        "diagnosing": "detective",  # Fail -> Diagnose
        "success": "vision_agent"    # Pass -> Quality Check
    }
)

# Recovery Loop
workflow.add_edge("detective", "engineer")
workflow.add_edge("engineer", "executor") 

# Final Quality Check to Completion
workflow.add_edge("vision_agent", END)

# Compile the final app
app = workflow.compile()