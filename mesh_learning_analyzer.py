#!/usr/bin/env python3
# Mesh Learning Analyzer - Statistical processing of historical mesh data
# This runs on the printer to generate optimized meshes from aggregated data

import json
import numpy as np
from pathlib import Path

VARIABLES_FILE = Path.home() / "printer_data" / "config" / "variables.cfg"

def load_variables():
    """Load variables.cfg data"""
    if not VARIABLES_FILE.exists():
        return {}
    
    content = VARIABLES_FILE.read_text()
    # Parse the simple key = value format
    variables = {}
    for line in content.split('\n'):
        if '=' in line and not line.strip().startswith('#'):
            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip()
            try:
                # Try to eval as Python literal
                variables[key] = eval(value)
            except:
                variables[key] = value
    return variables

def analyze_mesh_history():
    """Generate statistics from mesh learning database"""
    variables = load_variables()
    
    if 'mesh_history' not in variables:
        print("No mesh learning data found in variables.cfg")
        return
    
    mesh_history = variables['mesh_history']
    
    print("\n=== Mesh Learning Analysis ===\n")
    
    for bucket_key in sorted(mesh_history.keys()):
        bucket = mesh_history[bucket_key]
        temp = bucket_key.replace('temp_', '')
        samples = bucket['samples']
        
        if not samples:
            continue
        
        print(f"Temperature: {temp}°C")
        print(f"  Total calibrations: {bucket['count']}")
        print(f"  Samples stored: {len(samples)}")
        
        # Analyze point variance
        if len(samples) > 1:
            # Extract all point arrays
            point_arrays = []
            for sample in samples:
                # Convert nested list structure to numpy array
                points = np.array(sample['points'])
                point_arrays.append(points)
            
            # Stack arrays for statistical analysis
            stacked = np.stack(point_arrays)
            
            # Calculate statistics
            mean_mesh = np.mean(stacked, axis=0)
            std_mesh = np.std(stacked, axis=0)
            
            avg_std = np.mean(std_mesh)
            max_std = np.max(std_mesh)
            
            print(f"  Average variance: ±{avg_std:.4f}mm")
            print(f"  Maximum variance: ±{max_std:.4f}mm")
            print(f"  Confidence: {((1 - avg_std/0.1) * 100):.1f}%")
            
            # Find most stable points
            flat_std = std_mesh.flatten()
            stable_pct = (flat_std < 0.01).sum() / len(flat_std) * 100
            print(f"  Stable points (<0.01mm): {stable_pct:.1f}%")
        
        print()

def generate_averaged_mesh(temp_bucket):
    """Generate statistically averaged mesh for temperature bucket"""
    variables = load_variables()
    
    if 'mesh_history' not in variables:
        print("No mesh learning data available")
        return None
    
    mesh_history = variables['mesh_history']
    bucket_key = f"temp_{temp_bucket}"
    
    if bucket_key not in mesh_history:
        print(f"No data for {temp_bucket}°C")
        return None
    
    samples = mesh_history[bucket_key]['samples']
    
    if len(samples) < 2:
        print("Need at least 2 samples for averaging")
        return samples[0]['points'] if samples else None
    
    # Extract point arrays
    point_arrays = [np.array(s['points']) for s in samples]
    stacked = np.stack(point_arrays)
    
    # Calculate mean with outlier rejection
    mean_mesh = np.mean(stacked, axis=0)
    std_mesh = np.std(stacked, axis=0)
    
    # Weighted average - recent samples weighted more heavily
    weights = np.linspace(0.5, 1.0, len(samples))
    weighted_mean = np.average(stacked, axis=0, weights=weights)
    
    print(f"\nGenerated averaged mesh for {temp_bucket}°C:")
    print(f"  Samples used: {len(samples)}")
    print(f"  Average deviation: ±{np.mean(std_mesh):.4f}mm")
    print(f"  Mesh improvement: {(1 - np.mean(std_mesh)/0.05)*100:.1f}%")
    
    return weighted_mean.tolist()

def export_for_klipper(temp_bucket, mesh_points, mesh_params):
    """Export averaged mesh in Klipper format"""
    output = f"\n[bed_mesh learned_{temp_bucket}]\n"
    output += "version = 1\n"
    output += "points =\n"
    
    for row in mesh_points:
        output += "  " + ", ".join([f"{x:.6f}" for x in row]) + "\n"
    
    for key, value in mesh_params.items():
        output += f"{key} = {value}\n"
    
    return output

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "analyze":
            analyze_mesh_history()
        elif sys.argv[1] == "generate":
            temp = int(sys.argv[2]) if len(sys.argv) > 2 else 60
            mesh = generate_averaged_mesh(temp)
            if mesh:
                print("\nAveraged mesh data:")
                print(json.dumps(mesh, indent=2))
    else:
        print("Usage:")
        print("  mesh_learning_analyzer.py analyze       - Show statistics")
        print("  mesh_learning_analyzer.py generate [temp] - Generate averaged mesh")
