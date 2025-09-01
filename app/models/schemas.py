"""
Pydantic schemas for API requests and responses.
"""

from typing import List, Optional, Literal
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class PrivacyLevel(str, Enum):
    """Privacy levels for data analysis."""
    PUBLIC = "public"
    AGGREGATED = "aggregated"
    K_ANONYMOUS = "k_anonymous"

class OutputType(str, Enum):
    """Types of outputs that can be generated."""
    PLOT = "plot"
    TABLE = "table"
    CODE = "code"
    EXPLANATION = "explanation"

class AskRequest(BaseModel):
    """Request model for /ask endpoint."""
    question: str = Field(..., description="User's analysis question")
    dataset_id: str = Field(default="alzheimers_cohort_v1", description="Dataset identifier")
    outputs: List[OutputType] = Field(default=[OutputType.PLOT, OutputType.TABLE], description="Desired output types")
    privacy_level: PrivacyLevel = Field(default=PrivacyLevel.K_ANONYMOUS, description="Privacy protection level")

class JobResponse(BaseModel):
    """Response model for job creation."""
    job_id: str = Field(..., description="Unique job identifier")
    status: str = Field(default="queued", description="Job status")
    message: str = Field(..., description="Response message")

class JobStatus(str, Enum):
    """Job status enumeration."""
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class JobResult(BaseModel):
    """Response model for job results."""
    job_id: str = Field(..., description="Job identifier")
    status: JobStatus = Field(..., description="Current job status")
    artifacts: List[str] = Field(default=[], description="Generated artifact names")
    error: Optional[str] = Field(None, description="Error message if failed")
    created_at: datetime = Field(..., description="Job creation timestamp")
    completed_at: Optional[datetime] = Field(None, description="Job completion timestamp")
    code_hash: Optional[str] = Field(None, description="Hash of generated code")
    data_version: Optional[str] = Field(None, description="Dataset version used")
    output_hash: Optional[str] = Field(None, description="Hash of generated outputs")

class AuditLog(BaseModel):
    """Audit log entry."""
    job_id: str = Field(..., description="Job identifier")
    question: str = Field(..., description="User question")
    code_hash: str = Field(..., description="Hash of generated code")
    data_version: str = Field(..., description="Dataset version")
    output_hash: str = Field(..., description="Hash of outputs")
    privacy_level: PrivacyLevel = Field(..., description="Privacy level used")
    timestamp: datetime = Field(..., description="Timestamp of operation")
    user_ip: Optional[str] = Field(None, description="User IP address")
