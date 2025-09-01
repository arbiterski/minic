#!/usr/bin/env python3
"""
Sandbox runner for executing user-generated Python code safely.
This script runs in an isolated Docker container with no network access.
"""

import os
import sys
import json
import traceback
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import duckdb

def load_dataset():
    """Load dataset from DATASET_PATH, preferring Parquet over Excel."""
    dataset_path = os.environ.get('DATASET_PATH', '/data')
    
    # Try to load Parquet first
    parquet_path = Path(dataset_path) / 'patients.parquet'
    if parquet_path.exists():
        return pd.read_parquet(parquet_path)
    
    # Fallback to Excel
    excel_path = Path(dataset_path) / 'patients.xlsx'
    if excel_path.exists():
        return pd.read_excel(excel_path)
    
    raise FileNotFoundError(f"No dataset found in {dataset_path}")

def save_artifacts(artifacts_dir: str, outputs: dict):
    """Save generated artifacts to ARTIFACT_DIR."""
    artifacts_path = Path(artifacts_dir)
    artifacts_path.mkdir(exist_ok=True)
    
    for name, content in outputs.items():
        if name == 'plot':
            plt.savefig(artifacts_path / 'plot.png', dpi=300, bbox_inches='tight')
        elif name == 'table':
            content.to_csv(artifacts_path / 'summary.csv', index=False)
        elif name == 'code':
            with open(artifacts_path / 'generated_code.py', 'w') as f:
                f.write(content)
        elif name == 'explanation':
            with open(artifacts_path / 'explanation.txt', 'w') as f:
                f.write(content)

def main():
    """Main execution function."""
    try:
        # Load dataset
        df = load_dataset()
        
        # Read input from stdin (JSON)
        input_data = json.loads(sys.stdin.read())
        code = input_data.get('code', '')
        
        # Execute the code in a controlled environment
        local_vars = {
            'df': df,
            'pd': pd,
            'plt': plt,
            'duckdb': duckdb,
            'os': os,
            'Path': Path
        }
        
        # Execute code
        exec(code, {'__builtins__': {}}, local_vars)
        
        # Collect outputs
        outputs = {}
        
        # Check for plot
        if 'plot' in local_vars:
            outputs['plot'] = local_vars['plot']
        
        # Check for table
        if 'table' in local_vars:
            outputs['table'] = local_vars['table']
        
        # Check for explanation
        if 'explanation' in local_vars:
            outputs['explanation'] = str(local_vars['explanation'])
        
        # Save artifacts
        artifacts_dir = os.environ.get('ARTIFACT_DIR', '/artifacts')
        save_artifacts(artifacts_dir, outputs)
        
        # Return success
        result = {
            'status': 'success',
            'outputs': list(outputs.keys()),
            'error': None
        }
        
        print(json.dumps(result))
        
    except Exception as e:
        # Return error
        result = {
            'status': 'error',
            'outputs': [],
            'error': str(e),
            'traceback': traceback.format_exc()
        }
        
        print(json.dumps(result))
        sys.exit(1)

if __name__ == '__main__':
    main()
