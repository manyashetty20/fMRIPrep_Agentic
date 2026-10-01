#!/usr/bin/env python3
"""
Extract recovery performance metrics for Table 2.
"""

import json
from pathlib import Path
from collections import defaultdict

metrics_dir = Path("./output/metrics")
if not metrics_dir.exists():
    print(f"Metrics directory not found: {metrics_dir}")
    exit(1)

metrics_files = sorted(metrics_dir.glob("metrics_*.jsonl"))

print("Extracting recovery performance metrics for Table 2...")
print("="*100)

# Track failure modes and their outcomes
failure_modes = defaultdict(lambda: {
    'attempts': 0,
    'successful_recoveries': 0,
    'failed_recoveries': 0,
    'repair_types': defaultdict(int),
    'recovery_times': [],
    'total_attempts_before_success': []
})

for metrics_file in metrics_files:
    with open(metrics_file, 'r') as f:
        for line in f:
            event = json.loads(line)
            
            if event.get('event_type') == 'recovery_applied':
                root_cause = event.get('root_cause_received', 'unknown')
                duration = event.get('duration_seconds', 0)
                actions = event.get('repair_actions', [])
                attempt = event.get('retry_attempt', 0)
                
                # Categorize failure mode
                if 'PhaseEncodingDirection' in root_cause or 'SyN' in root_cause:
                    mode = 'missing_phase_encoding_direction'
                elif 'RepetitionTime' in root_cause or 'BIDS_FIX' in root_cause:
                    mode = 'missing_repetition_time'
                elif 'MEMORY' in root_cause.upper() or 'OOM' in root_cause.upper():
                    mode = 'out_of_memory'
                elif 'TTY' in root_cause.upper() or 'pseudo-tty' in root_cause.lower():
                    mode = 'docker_tty_issue'
                elif 'license' in root_cause.lower():
                    mode = 'freesurfer_license'
                else:
                    mode = 'other'
                
                failure_modes[mode]['attempts'] += 1
                failure_modes[mode]['recovery_times'].append(duration)
                
                # Track repair types
                for action in actions:
                    failure_modes[mode]['repair_types'][action] += 1
                
                # Consider recovery successful if it happened
                failure_modes[mode]['successful_recoveries'] += 1
            
            if event.get('event_type') == 'subject_run_completed':
                attempts = event.get('attempt_count', 0)
                final_status = event.get('final_status', 'unknown')
                
                if final_status == 'completed':
                    # Track total attempts for successful runs
                    failure_modes['all_runs']['total_attempts_before_success'].append(attempts)

# Print summary
print(f"{'Failure Mode':<35} {'Attempts':<10} {'Success Rate':<12} {'Mean Time (s)':<12} {'Repair Types':<30}")
print("-" * 100)

for mode, data in sorted(failure_modes.items()):
    if mode == 'all_runs':
        continue
    
    attempts = data['attempts']
    successes = data['successful_recoveries']
    success_rate = f"{successes/attempts*100:.0f}%" if attempts > 0 else "N/A"
    
    mean_time = f"{sum(data['recovery_times'])/len(data['recovery_times']):.3f}" if data['recovery_times'] else "N/A"
    
    repair_types = ", ".join([f"{k}({v})" for k, v in data['repair_types'].items()])
    
    print(f"{mode:<35} {attempts:<10} {success_rate:<12} {mean_time:<12} {repair_types:<30}")

print("="*100)

# Overall statistics
all_attempts = sum(data['attempts'] for mode, data in failure_modes.items() if mode != 'all_runs')
all_successes = sum(data['successful_recoveries'] for mode, data in failure_modes.items() if mode != 'all_runs')
all_times = [t for data in failure_modes.values() for t in data['recovery_times']]

print(f"Overall: {all_attempts} recovery attempts, {all_successes} successful ({all_successes/all_attempts*100:.0f}%)")
print(f"Mean recovery time: {sum(all_times)/len(all_times):.3f}s" if all_times else "No timing data")

# Track command generation performance
print("\n" + "="*100)
print("Command Generation Performance")
print("="*100)

generation_data = defaultdict(lambda: {
    'llm_generated': 0,
    'rule_based': 0,
    'hallucinated_flags': 0,
    'valid_commands': 0,
    'invalid_commands': 0
})

for metrics_file in metrics_files:
    with open(metrics_file, 'r') as f:
        for line in f:
            event = json.loads(line)
            
            if event.get('event_type') == 'command_generated':
                method = event.get('generation_method', 'unknown')
                hallucinated = event.get('hallucinated_flags', [])
                
                if 'llm' in method.lower():
                    generation_data['all']['llm_generated'] += 1
                    if hallucinated:
                        generation_data['all']['hallucinated_flags'] += len(hallucinated)
                        generation_data['all']['invalid_commands'] += 1
                    else:
                        generation_data['all']['valid_commands'] += 1
                elif 'rule' in method.lower():
                    generation_data['all']['rule_based'] += 1
                    generation_data['all']['valid_commands'] += 1

print(f"LLM commands: {generation_data['all']['llm_generated']}")
print(f"Rule-based commands: {generation_data['all']['rule_based']}")
print(f"Valid commands: {generation_data['all']['valid_commands']}")
print(f"Invalid commands (hallucinated): {generation_data['all']['invalid_commands']}")
print(f"Hallucinated flags total: {generation_data['all']['hallucinated_flags']}")

# Export data
export_data = {
    'failure_modes': dict(failure_modes),
    'command_generation': dict(generation_data)
}

with open('./table_2_3_data.json', 'w') as f:
    json.dump(export_data, f, indent=2)

print("\nData exported to table_2_3_data.json")
