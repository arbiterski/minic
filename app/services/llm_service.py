"""
LLM service for generating Python code from natural language questions.
"""

import os
import hashlib
from typing import List, Optional
from app.models.schemas import OutputType, PrivacyLevel
from app.core.config import settings

class LLMService:
    """Service for interacting with LLM (Claude)."""
    
    def __init__(self):
        self.api_key = settings.anthropic_api_key
        self.model = settings.claude_model
    
    def generate_code(self, question: str, outputs: List[OutputType], privacy_level: PrivacyLevel) -> str:
        """
        Generate Python code from natural language question.
        
        Args:
            question: User's analysis question
            outputs: Desired output types
            privacy_level: Privacy protection level
            
        Returns:
            Generated Python code as string
        """
        if not self.api_key:
            # Return stub code when API key is not available
            return self._generate_stub_code(question, outputs, privacy_level)
        
        # TODO: Implement actual Claude API call
        return self._generate_stub_code(question, outputs, privacy_level)
    
    def _generate_stub_code(self, question: str, outputs: List[OutputType], privacy_level: PrivacyLevel) -> str:
        """Generate stub code for demonstration purposes."""
        
        # Base template
        code_template = f'''# Generated code for: {question}
# Privacy level: {privacy_level}
# Outputs: {', '.join(outputs)}

import pandas as pd
import matplotlib.pyplot as plt

# Load data (already available as 'df')
print(f"Dataset shape: {{df.shape}}")
print(f"Columns: {{list(df.columns)}}")

# Basic analysis
summary_stats = df.describe()

# Privacy protection
if {privacy_level.value} == "k_anonymous":
    # Apply k-anonymity (k={settings.k_anonymity})
    if len(df) < {settings.k_anonymity}:
        print("Dataset too small for k-anonymity")
        summary_stats = pd.DataFrame()
    else:
        # Aggregate data to ensure k-anonymity
        summary_stats = df.groupby(df.columns[0]).agg('count').reset_index()
        summary_stats = summary_stats[summary_stats.iloc[:, 1] >= {settings.k_anonymity}]

# Generate outputs
'''
        
        # Add specific output generation
        if OutputType.TABLE in outputs:
            code_template += '''
# Create summary table
table = summary_stats
print("Summary table generated")
'''
        
        if OutputType.PLOT in outputs:
            code_template += '''
# Create visualization
plt.figure(figsize=(10, 6))
if not summary_stats.empty:
    summary_stats.iloc[:, 1].plot(kind='bar')
    plt.title('Data Distribution')
    plt.xlabel('Category')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plot = plt.gcf()
else:
    plot = None
    plt.close()
'''
        
        if OutputType.EXPLANATION in outputs:
            code_template += '''
# Generate explanation
explanation = f"Analysis of {{len(df)}} records with {privacy_level.value} privacy protection. "
if not summary_stats.empty:
    explanation += f"Generated {{len(summary_stats)}} aggregated categories."
else:
    explanation += "No results due to privacy constraints."
'''
        
        return code_template
    
    def get_code_hash(self, code: str) -> str:
        """Generate hash for code content."""
        return hashlib.sha256(code.encode()).hexdigest()
