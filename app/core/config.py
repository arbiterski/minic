"""
Configuration management for the application.
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings."""
    
    # API Configuration
    api_title: str = "Alzheimer's Disease Analysis Database API"
    api_version: str = "1.0.0"
    api_description: str = "Secure platform for analyzing medical data with AI-generated code"
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    
    # Redis Configuration
    redis_url: str = "redis://localhost:6379"
    redis_db: int = 0
    
    # Dataset Configuration
    dataset_path: str = "/data/alzheimers_cohort_v1"
    artifact_dir: str = "/app/artifacts"
    
    # Privacy Configuration
    k_anonymity: int = 10
    
    # LLM Configuration
    anthropic_api_key: Optional[str] = None
    claude_model: str = "claude-3-sonnet-20240229"
    
    # Claude Code Server Configuration
    claude_code_server_url: str = "http://localhost:3000"
    claude_code_server_timeout: int = 30000
    
    # Sandbox Configuration
    sandbox_image: str = "dementia-sandbox:latest"
    sandbox_timeout: int = 300  # 5 minutes
    
    # Security Configuration
    max_code_length: int = 10000
    allowed_modules: list = ["pandas", "matplotlib.pyplot", "duckdb", "numpy"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Global settings instance
settings = Settings()
