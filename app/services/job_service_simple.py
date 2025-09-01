"""
Simplified Job Service for testing basic functionality.
"""

import uuid
import hashlib
from datetime import datetime
from typing import Dict, Any, Optional
from app.models.schemas import JobStatus, JobResult, AuditLog

class JobServiceSimple:
    """Simplified service for managing analysis jobs."""
    
    def __init__(self):
        self.jobs: Dict[str, JobResult] = {}
    
    def create_job(self, question: str, dataset_id: str, outputs: list, privacy_level: str) -> str:
        """
        Create a new analysis job.
        
        Args:
            question: User's analysis question
            dataset_id: Dataset identifier
            outputs: Desired output types
            privacy_level: Privacy protection level
            
        Returns:
            Job ID
        """
        job_id = str(uuid.uuid4())
        
        # Create job record
        job = JobResult(
            job_id=job_id,
            status=JobStatus.QUEUED,
            artifacts=[],
            created_at=datetime.utcnow(),
            code_hash=None,
            data_version="v1.0",
            output_hash=None
        )
        
        self.jobs[job_id] = job
        
        # Simulate job processing
        self._simulate_job_processing(job_id, question, outputs, privacy_level)
        
        return job_id
    
    def get_job_status(self, job_id: str) -> Optional[JobResult]:
        """
        Get job status and results.
        
        Args:
            job_id: Job identifier
            
        Returns:
            Job result or None if not found
        """
        return self.jobs.get(job_id)
    
    def _simulate_job_processing(self, job_id: str, question: str, outputs: list, privacy_level: str):
        """Simulate job processing for testing."""
        try:
            # Update status
            self.jobs[job_id].status = JobStatus.PROCESSING
            
            # Simulate processing time
            import time
            time.sleep(2)
            
            # Generate mock results
            mock_artifacts = []
            if "plot" in outputs:
                mock_artifacts.append("plot.png")
            if "table" in outputs:
                mock_artifacts.append("summary.csv")
            if "code" in outputs:
                mock_artifacts.append("generated_code.py")
            if "explanation" in outputs:
                mock_artifacts.append("explanation.txt")
            
            # Update job with results
            self.jobs[job_id].status = JobStatus.COMPLETED
            self.jobs[job_id].artifacts = mock_artifacts
            self.jobs[job_id].completed_at = datetime.utcnow()
            
            # Generate mock hashes
            code_hash = hashlib.sha256(question.encode()).hexdigest()
            self.jobs[job_id].code_hash = code_hash
            
            output_hash = hashlib.sha256(str(mock_artifacts).encode()).hexdigest()
            self.jobs[job_id].output_hash = output_hash
            
        except Exception as e:
            # Update job with error
            self.jobs[job_id].status = JobStatus.FAILED
            self.jobs[job_id].error = str(e)
            self.jobs[job_id].completed_at = datetime.utcnow()
    
    def cleanup_job(self, job_id: str):
        """Clean up job artifacts."""
        if job_id in self.jobs:
            del self.jobs[job_id]
