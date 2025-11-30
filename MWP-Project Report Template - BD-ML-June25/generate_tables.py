#!/usr/bin/env python3
"""
Generate LaTeX tables from automation_results.json files
"""

import json
import os
import sys
from pathlib import Path
from typing import List, Dict, Any

def read_json_file(filepath: str) -> Dict[str, Any]:
    """Read JSON results file"""
    with open(filepath, 'r') as f:
        return json.load(f)

def generate_training_table(json_data: Dict[str, Any]) -> str:
    """Generate LaTeX training metrics table"""
    rounds = json_data.get('rounds', [])
    
    lines = []
    
    # Handle both dict and list formats
    if isinstance(rounds, dict):
        # Convert dict format to list format
        rounds_list = []
        for round_idx, devices in sorted(rounds.items(), key=lambda x: int(x[0])):
            rounds_list.append({'round': int(round_idx), 'devices': devices})
        rounds = rounds_list
    
    for round_data in rounds:
        round_idx = round_data.get('round')
        devices = round_data.get('devices', [])
        
        for device in devices:
            device_id = device.get('device_id', 'unknown')
            # Format device name for display
            if device_id == 'device3':
                device_display = 'Device 3 (faulty)'
            else:
                device_display = device_id.capitalize().replace('device', 'Device ')
            
            lines.append(f"        {round_idx} & {device_display} & "
                        f"{device.get('num_samples')} & "
                        f"{device.get('train_accuracy', 0):.4f} & "
                        f"{device.get('train_loss', 0):.4f} & "
                        f"{device.get('val_accuracy', 0):.4f} & "
                        f"{device.get('val_loss', 0):.4f} & "
                        f"{device.get('reward_tokens', 0):.2f} \\\\")
    
    return '\n'.join(lines)

def generate_inference_table(json_data: Dict[str, Any]) -> str:
    """Generate LaTeX inference metrics table"""
    inference = json_data.get('inference_summary', {})
    
    lines = []
    lines.append(f"        {inference.get('num_samples', 0)} & "
                f"{inference.get('accuracy', 0):.2f} \\\\")
    
    return '\n'.join(lines)

def update_chapter7_table(table_label: str, training_data: str, inference_data: str, 
                         template_file: str = "chapter7.tex") -> None:
    """Update a specific table in chapter7.tex"""
    
    # Map table labels to section names for identification
    table_map = {
        'tab:baseline_fedavg': ('Baseline: FedAvg without Enhancements', training_data, inference_data),
        'tab:dynamic_sampling': ('Dynamic Sampling Evaluation', training_data, inference_data),
        'tab:fedavg_plus': ('With FedAvg\\,+ ', training_data, inference_data),
        'tab:streaming_chunks': ('Incremental Streaming Performance', training_data, inference_data),
    }
    
    if table_label not in table_map:
        print(f"Unknown table label: {table_label}")
        return
    
    section_name, train_rows, infer_rows = table_map[table_label]
    
    # Read the template
    with open(template_file, 'r') as f:
        content = f.read()
    
    # This is a basic implementation - you might want to use more sophisticated
    # text replacement or LaTeX parsing for production use
    print(f"\nFor {section_name}:")
    print(f"\nTraining table rows:")
    print(train_rows)
    print(f"\nInference table rows:")
    print(infer_rows)
    
    # TODO: Actually replace content in file (this requires careful parsing
    # of LaTeX to avoid breaking other content)

def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python generate_tables.py <json_file1> [json_file2] ...")
        print("       python generate_tables.py baseline.json dynamic_sampling.json fedavg_plus.json streaming.json")
        sys.exit(1)
    
    json_files = sys.argv[1:]
    
    print("%" + "=" * 80)
    print("% Generated LaTeX table rows from automation results")
    print("%" + "=" * 80)
    
    for json_file in json_files:
        if not os.path.exists(json_file):
            print(f"\nWarning: File not found: {json_file}")
            continue
        
        print(f"\n% Processing: {json_file}")
        json_data = read_json_file(json_file)
        
        scenario = json_data.get('scenario', 'unknown')
        print(f"% Scenario: {scenario}")
        
        training_rows = generate_training_table(json_data)
        inference_rows = generate_inference_table(json_data)
        
        print("\n% Training metrics table:")
        print(training_rows)
        
        print("\n% Inference metrics table:")
        print(inference_rows)
        
        print("\n% Copy the rows above into the corresponding tables in chapter7.tex")

if __name__ == '__main__':
    main()

