#!/usr/bin/env python3
"""
Create sample dataset for Alzheimer's Disease Analysis Database.
"""

import pandas as pd
import numpy as np
from pathlib import Path

def create_sample_dataset():
    """Create a sample dataset for testing."""
    
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Generate sample data
    n_patients = 1000
    
    data = {
        'patient_id': range(1, n_patients + 1),
        'age': np.random.normal(75, 10, n_patients).astype(int),
        'gender': np.random.choice(['M', 'F'], n_patients),
        'mmse_score': np.random.normal(20, 8, n_patients).astype(int),
        'cdr_score': np.random.choice([0, 0.5, 1, 2, 3], n_patients, p=[0.3, 0.3, 0.2, 0.15, 0.05]),
        'education_years': np.random.normal(12, 4, n_patients).astype(int),
        'apoe_genotype': np.random.choice(['E2/E2', 'E2/E3', 'E2/E4', 'E3/E3', 'E3/E4', 'E4/E4'], n_patients),
        'diagnosis_date': pd.date_range('2020-01-01', periods=n_patients, freq='D'),
        'follow_up_months': np.random.exponential(24, n_patients).astype(int),
        'medication': np.random.choice(['Donepezil', 'Rivastigmine', 'Galantamine', 'Memantine', 'None'], n_patients),
        'comorbidity_count': np.random.poisson(2, n_patients),
        'family_history': np.random.choice([True, False], n_patients, p=[0.3, 0.7])
    }
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Clean up data
    df['age'] = df['age'].clip(50, 100)
    df['mmse_score'] = df['mmse_score'].clip(0, 30)
    df['education_years'] = df['education_years'].clip(0, 25)
    df['follow_up_months'] = df['follow_up_months'].clip(1, 60)
    df['comorbidity_count'] = df['comorbidity_count'].clip(0, 5)
    
    # Create data directory
    data_dir = Path('data/alzheimers_cohort_v1')
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Save as Parquet (preferred format)
    parquet_path = data_dir / 'patients.parquet'
    df.to_parquet(parquet_path, index=False)
    print(f"✅ Sample dataset saved as Parquet: {parquet_path}")
    print(f"   Records: {len(df)}")
    print(f"   Columns: {len(df.columns)}")
    
    # Save as Excel (fallback format)
    excel_path = data_dir / 'patients.xlsx'
    df.to_excel(excel_path, index=False)
    print(f"✅ Sample dataset saved as Excel: {excel_path}")
    
    # Display sample data
    print("\n📊 Sample Data Preview:")
    print(df.head())
    
    print("\n📈 Dataset Summary:")
    print(df.describe())
    
    print("\n🔍 Column Information:")
    for col in df.columns:
        if df[col].dtype == 'object':
            print(f"  {col}: {df[col].nunique()} unique values")
        else:
            print(f"  {col}: {df[col].dtype}, range: {df[col].min()}-{df[col].max()}")
    
    return df

if __name__ == "__main__":
    create_sample_dataset()
