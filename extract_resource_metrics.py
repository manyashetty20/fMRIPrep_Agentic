#!/usr/bin/env python3
"""
Extract resource metrics for Table 5 from metrics data.
"""

import json
from pathlib import Path
from collections import defaultdict

metrics_dir = Path("./output/metrics")
if not metrics_dir.exists():
    print(f"Metrics directory not found: {metrics_dir}")
    exit(1)

metrics_files = sorted(metrics_dir.glob("metrics_*.jsonl"))

print("Extracting resource metrics for Table 5...")
print("="*100)

resource_data = defaultdict(lambda: {
    'llm_calls': 0,
    'llm_tokens_estimated': 0,
    'total_duration': 0,
    'agent_decision_time': 0,
    'execution_time': 0,
    'memory_usage': []
})

for metrics_file in metrics_files:
    with open(metrics_file, 'r') as f:
        for line in f:
            event = json.loads(line)
            
            # Track LLM calls
            if event.get('event_type') == 'diagnosis_completed':
                llm_usage = event.get('llm_usage', {})
                total_tokens = llm_usage.get('total_tokens', 0)
                if total_tokens:
                    resource_data['all']['llm_calls'] += 1
                    resource_data['all']['llm_tokens_estimated'] += total_tokens
            
            if event.get('event_type') == 'config_command_generated':
                llm_usage = event.get('llm_usage', {})
                total_tokens = llm_usage.get('total_tokens', 0)
                if total_tokens:
                    resource_data['all']['llm_calls'] += 1
                    resource_data['all']['llm_tokens_estimated'] += total_tokens
            
            # Track agent decision time
            if event.get('event_type') in ['recovery_applied', 'diagnosis_completed']:
                duration = event.get('duration_seconds', 0)
                resource_data['all']['agent_decision_time'] += duration
            
            # Track total duration
            if event.get('event_type') == 'subject_run_completed':
                duration = event.get('duration_seconds', 0)
                resource_data['all']['total_duration'] += duration
                
                # Estimate execution time (total - agent time)
                resource_data['all']['execution_time'] += max(0, duration - resource_data['all']['agent_decision_time'])

print(f"{'Metric':<30} {'Value':<20}")
print("-" * 50)

print(f"{'Total LLM calls':<30} {resource_data['all']['llm_calls']:<20}")
print(f"{'Estimated total tokens':<30} {resource_data['all']['llm_tokens_estimated']:<20}")
print(f"{'Agent decision time (total)':<30} {resource_data['all']['agent_decision_time']:.2f}s")
print(f"{'Estimated execution time':<30} {resource_data['all']['execution_time']:.2f}s")
print(f"{'Total duration':<30} {resource_data['all']['total_duration']:.2f}s")

if resource_data['all']['total_duration'] > 0:
    overhead_pct = (resource_data['all']['agent_decision_time'] / resource_data['all']['total_duration']) * 100
    print(f"{'Agent overhead percentage':<30} {overhead_pct:.2f}%")

# Estimate costs (Groq pricing: ~$0.05-0.10 per million tokens)
cost_estimate = (resource_data['all']['llm_tokens_estimated'] / 1_000_000) * 0.10
print(f"{'Estimated LLM cost':<30} ${cost_estimate:.4f}")

print("="*100)

# Export
with open('./table_5_data.json', 'w') as f:
    json.dump(dict(resource_data), f, indent=2)

print("Data exported to table_5_data.json")
