"""
Privacy protection utilities for data analysis.
"""

import pandas as pd
from typing import List, Tuple
from app.core.config import settings

def apply_k_anonymity(df: pd.DataFrame, k: int = None) -> pd.DataFrame:
    """
    Apply k-anonymity to ensure privacy protection.
    
    Args:
        df: Input DataFrame
        k: K-anonymity parameter (default from settings)
        
    Returns:
        DataFrame with k-anonymity applied
    """
    if k is None:
        k = settings.k_anonymity
    
    if len(df) < k:
        # Dataset too small for k-anonymity
        return pd.DataFrame()
    
    # Simple k-anonymity implementation
    # In production, use more sophisticated algorithms
    if len(df) >= k:
        # Group by first column and ensure each group has at least k members
        grouped = df.groupby(df.columns[0]).filter(lambda x: len(x) >= k)
        return grouped
    
    return pd.DataFrame()

def aggregate_data(df: pd.DataFrame, columns: List[str] = None) -> pd.DataFrame:
    """
    Aggregate data to reduce privacy risks.
    
    Args:
        df: Input DataFrame
        columns: Columns to aggregate (default: all numeric columns)
        
    Returns:
        Aggregated DataFrame
    """
    if columns is None:
        columns = df.select_dtypes(include=['number']).columns.tolist()
    
    if not columns:
        return df
    
    # Create aggregated summary
    agg_dict = {}
    for col in columns:
        if col in df.columns:
            agg_dict[col] = ['mean', 'std', 'min', 'max', 'count']
    
    if agg_dict:
        aggregated = df.agg(agg_dict)
        return aggregated
    
    return df

def sanitize_outputs(df: pd.DataFrame, privacy_level: str) -> pd.DataFrame:
    """
    Sanitize outputs based on privacy level.
    
    Args:
        df: Input DataFrame
        privacy_level: Privacy protection level
        
    Returns:
        Sanitized DataFrame
    """
    if privacy_level == "public":
        return df
    
    elif privacy_level == "aggregated":
        return aggregate_data(df)
    
    elif privacy_level == "k_anonymous":
        return apply_k_anonymity(df)
    
    else:
        # Default to most restrictive
        return apply_k_anonymity(df)
