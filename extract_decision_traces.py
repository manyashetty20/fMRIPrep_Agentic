#!/usr/bin/env python3
"""
Extract decision trace examples for Table 4 from log files.
"""

import json
from pathlib import Path
import re

# Look at log files for decision traces
logs_dir = Path("./testing/results/logs")
if not logs_dir.exists():
    print(f"Logs directory not found: {logs_dir}")
    exit(1)

print("Extracting decision trace examples for Table 4...")
print("="*120)

# Find recent log files
log_files = sorted(logs_dir.glob("**/*.log"), key=lambda x: x.stat().st_mtime, reverse=True)[:5]

decision_traces = []

for log_file in log_files:
    print(f"\nAnalyzing: {log_file}")
    
    with open(log_file, 'r') as f:
        content = f.read()
        
        # Extract decision sequence
        trace = {
            'log_file': log_file.name,
            'initial_command': None,
            'error': None,
            'diagnosis': None,
            'recovery_action': None,
            'recovered_command': None,
            'result': None
        }
        
        # Find initial command
        cmd_match = re.search(r'Running: (docker run[^\n]+)', content)
        if cmd_match:
            trace['initial_command'] = cmd_match.group(1)[:100] + "..."
        
        # Find error
        error_match = re.search(r'Execution failed \(exit \d+\): ([^\n]+)', content)
        if error_match:
            trace['error'] = error_match.group(1)[:100] + "..."
        
        # Find diagnosis
        diag_match = re.search(r'Diagnosis:\*\*ROOT CAUSE:\*\* ([^\n]+)', content, re.DOTALL)
        if diag_match:
            trace['diagnosis'] = diag_match.group(1)[:150] + "..."
        
        # Find recovery action
        recovery_match = re.search(r'RecoveryAgent applied (\d+) fix rule\(s\): (\[[^\]]+\])', content)
        if recovery_match:
            trace['recovery_action'] = recovery_match.group(2)
        
        # Find recovered command
        recovered_match = re.search(r'Recovered command:\s+(docker run[^\n]+)', content)
        if recovered_match:
            trace['recovered_command'] = recovered_match.group(1)[:100] + "..."
        
        # Find result
        if 'completed' in content or 'PASS' in content:
            trace['result'] = 'SUCCESS'
        elif 'Max recovery attempts' in content:
            trace['result'] = 'FAILED_MAX_ATTEMPTS'
        else:
            trace['result'] = 'UNKNOWN'
        
        if trace['initial_command'] and trace['error']:
            decision_traces.append(trace)
            print(f"  Found trace: {trace['error'][:50]}... -> {trace['result']}")

print(f"\nFound {len(decision_traces)} decision traces")

# Print detailed examples
print("\n" + "="*120)
print("DECISION TRACE EXAMPLES")
print("="*120)

for i, trace in enumerate(decision_traces[:3], 1):
    print(f"\nExample {i}:")
    print(f"  Initial Command: {trace['initial_command']}")
    print(f"  Error: {trace['error']}")
    print(f"  Diagnosis: {trace['diagnosis']}")
    print(f"  Recovery Action: {trace['recovery_action']}")
    print(f"  Result: {trace['result']}")

# Export
with open('./table_4_data.json', 'w') as f:
    json.dump(decision_traces, f, indent=2)

print("\nData exported to table_4_data.json")
