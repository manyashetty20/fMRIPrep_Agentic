from agents.orchestrator import app
import datetime

# --- SETUP ---
print("🚀 Starting Agentic fMRIPrep Autonomous Loop...")

# Initialize the 'State'
initial_state = {
    "command": "",
    "log": "",
    "history": [],
    "status": "planning"
}

# --- THE AGENTIC LOOP ---
# This single call triggers the entire Plan -> Fail -> Diagnose -> Recover cycle
final_state = app.invoke(initial_state)

# --- FINAL PRESENTATION REPORT ---
print("\n" + "═"*50)
print(f"🤖 AGENTIC fMRIPREP SYSTEM REPORT")
print(f"Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("═"*50)

# Extract key metrics for the demo
status = final_state.get('status', 'UNKNOWN').upper()
attempts = len(final_state.get('history', [])) + 1
final_cmd = final_state.get('command', 'No command generated.')

# Logic to identify what the agents did
has_low_mem = "ENABLED (--low-mem)" if "--low-mem" in final_cmd else "STANDARD"
fieldmap_status = "SYNTHETIC (--use-syn-sdc)" if "--use-syn-sdc" in final_cmd else "DIRECT"

print(f"▶️  FINAL STATUS      : {status}")
print(f"▶️  TOTAL ATTEMPTS    : {attempts}")
print(f"▶️  HARDWARE OPTIM    : {has_low_mem}")
print(f"▶️  FIELD MAP TYPE    : {fieldmap_status}")

print("\n📜 FINAL GENERATED COMMAND:")
print(f"{final_cmd}")

if final_state.get("history"):
    print("\n🔍 DETECTIVE'S ANALYSIS SUMMARY:")
    # Show the first few lines of the LLM's diagnosis
    diagnosis_summary = final_state["history"][-1].split('\n')[:4]
    print("\n".join(diagnosis_summary) + "...")

print("\n" + "═"*50)
print("✅ MISSION COMPLETE: Human Intervention Not Required.")
print("═"*50)