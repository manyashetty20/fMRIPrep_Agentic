from agents.config_agent import ConfigAgent
from agents.diagnostic_agent import DiagnosticAgent
from agents.recovery_agent import RecoveryAgent
from orchestrator import app

# 1. INITIAL PLAN (The Architect)
print("\n--- [STAGE 1: INITIAL CONFIGURATION] ---")
config_agent = ConfigAgent()
original_cmd = config_agent.generate_command(bids_dir="./data/bids_input", participant_id="sub-01")
print(f"PLAN: {original_cmd}")

# 2. THE CRASH (Simulated)
print("\n--- [STAGE 2: EXECUTION FAILED] ---")
simulated_crash_log = "Node: fmriprep.workflow.anatomical.skull_strip. ERROR: RuntimeException: Command '3dSkullStrip' failed. Out of Memory."
print(f"CRASH DETECTED: {simulated_crash_log}")

# 3. THE DIAGNOSIS (The Detective)
print("\n--- [STAGE 3: DIAGNOSTIC ANALYSIS] ---")
diag_agent = DiagnosticAgent()
diagnosis = diag_agent.diagnose_crash(simulated_crash_log)
print(f"DETECTIVE REPORT: {diagnosis[:300]}...") # Printing first 300 chars for brevity

# 4. THE RECOVERY (Self-Healing)
print("\n--- [STAGE 4: AUTONOMOUS RECOVERY] ---")
recovery_agent = RecoveryAgent()
fixed_cmd = recovery_agent.apply_fix(original_cmd, diagnosis)

print("✅ RECOVERY SUCCESSFUL")
print(f"OLD COMMAND: {original_cmd}")
print(f"NEW FIXED COMMAND: {fixed_cmd}")


print("🚀 Starting Agentic fMRIPrep Loop...")
final_state = app.invoke({
    "command": "",
    "log": "",
    "history": [],
    "status": "planning"
})

print("\n✨ FINAL OUTPUT ✨")
print(f"Status: {final_state['status']}")
print(f"Final Executed Command: {final_state['command']}")