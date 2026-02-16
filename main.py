from agents.config_agent import ConfigAgent

# This will index the PDFs in your data/docs/ folder
agent = ConfigAgent()

# Test if it can generate a command based on the manuals
test_command = agent.generate_command(bids_dir="./data/bids_input", participant_id="sub-01")
print(f"Generated fMRIPrep Command: {test_command}")