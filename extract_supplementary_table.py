#!/usr/bin/env python3
"""
Extract detailed run-level metrics for Supplementary Table S1.
"""

import json
from pathlib import Path
from collections import defaultdict

# Check evaluation exports
eval_dir = Path("./output/evaluation")
if not eval_dir.exists():
    print(f"Evaluation directory not found: {eval_dir}")
    exit(1)

# Find evaluation JSONL files
eval_files = sorted(eval_dir.glob("run_evaluation.jsonl"))

if not eval_files:
    print("No evaluation files found")
    exit(1)

print("Extracting detailed run-level metrics for Supplementary Table S1...")
print("="*120)

all_runs = []

for eval_file in eval_files:
    with open(eval_file, 'r') as f:
        for line in f:
            record = json.loads(line)
            
            # Extract comprehensive run data
            run_data = {
                'run_id': eval_file.name,
                'participant': record.get('participant', 'unknown'),
                'dataset_id': record.get('dataset_id', 'unknown'),
                'config_type': 'inferred from dataset_id',
                'brain_mask_retention_ratio': record.get('brain_mask_retention_ratio'),
                'skull_strip_reduction': record.get('skull_strip_reduction'),
                'raw_nonzero_voxels': record.get('raw_nonzero_voxels'),
                'preprocessed_nonzero_voxels': record.get('preprocessed_nonzero_voxels'),
                'brain_mask_nonzero_voxels': record.get('brain_mask_nonzero_voxels'),
                'qa_summary': record.get('qa_summary'),
                'final_status': record.get('final_status'),
                'total_attempts': record.get('attempt_count', 0),
                'timestamp': eval_file.name.split('_')[1] if '_' in eval_file.name else 'unknown',
            }
            
            # Infer config type from dataset_id
            dataset_id = record.get('dataset_id', '')
            if 'missing_tr' in dataset_id:
                run_data['config_type'] = 'failure_injection_missing_tr'
            elif 'bad_readout' in dataset_id:
                run_data['config_type'] = 'failure_injection_bad_readout'
            elif dataset_id == 'bids':
                run_data['config_type'] = 'anat_only'
            else:
                run_data['config_type'] = 'full_pipeline'
            
            all_runs.append(run_data)

# Also extract recovery timing from metrics
metrics_dir = Path("./output/metrics")
if metrics_dir.exists():
    metrics_files = sorted(metrics_dir.glob("metrics_*.jsonl"))
    
    recovery_by_run = defaultdict(list)
    
    for metrics_file in metrics_files:
        # Match metrics file to run
        run_id_part = metrics_file.name.split('_')[1] if '_' in metrics_file.name else metrics_file.name
        
        with open(metrics_file, 'r') as f:
            for line in f:
                event = json.loads(line)
                
                if event.get('event_type') == 'recovery_applied':
                    recovery_by_run[run_id_part].append({
                        'attempt': event.get('retry_attempt'),
                        'duration': event.get('duration_seconds'),
                        'root_cause': event.get('root_cause_received'),
                        'actions': event.get('repair_actions', []),
                    })
                
                if event.get('event_type') == 'subject_run_completed':
                    total_attempts = event.get('attempt_count', 0)
                    # Update matching runs
                    for run in all_runs:
                        if run_id_part in run['run_id']:
                            run['total_attempts'] = total_attempts
    
    # Add recovery data to runs
    for run in all_runs:
        run_id_part = run['run_id'].split('_')[1] if '_' in run['run_id'] else run['run_id']
        if run_id_part in recovery_by_run:
            run['recovery_events'] = recovery_by_run[run_id_part]
            run['recovery_count'] = len(recovery_by_run[run_id_part])
        else:
            run['recovery_events'] = []
            run['recovery_count'] = 0

# Print detailed table
print(f"{'Run ID':<30} {'Participant':<12} {'Config Type':<30} {'Brain Mask %':<12} {'Skull Strip %':<12} {'Attempts':<8} {'Recovery':<8} {'QA':<8}")
print("-" * 120)

for run in sorted(all_runs, key=lambda x: x['run_id']):
    brain_mask = f"{run['brain_mask_retention_ratio']*100:.1f}%" if run['brain_mask_retention_ratio'] else "N/A"
    skull_strip = f"{run['skull_strip_reduction']*100:.1f}%" if run['skull_strip_reduction'] else "N/A"
    
    print(f"{run['run_id'][:30]:<30} {run['participant']:<12} {run['config_type']:<30} {brain_mask:<12} {skull_strip:<12} {run['total_attempts']:<8} {run['recovery_count']:<8} {run['qa_summary']:<8}")

print("="*120)
print(f"Total runs: {len(all_runs)}")

# Group by config type
by_config = defaultdict(list)
for run in all_runs:
    by_config[run['config_type']].append(run)

print("\nRuns by configuration type:")
for config_type, runs in sorted(by_config.items()):
    print(f"  {config_type}: {len(runs)} runs")

# Export to JSON for LaTeX table generation
with open('./supplementary_table_data.json', 'w') as f:
    json.dump(all_runs, f, indent=2)

print("\nData exported to supplementary_table_data.json")
