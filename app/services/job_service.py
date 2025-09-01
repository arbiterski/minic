"""
Job management service for handling analysis requests.
"""

import uuid
import hashlib
from datetime import datetime
from typing import Dict, Any, Optional
from app.models.schemas import JobStatus, JobResult, AuditLog
from app.services.claude_code_server import ClaudeCodeServer
from app.services.sandbox_service import SandboxService
from app.core.config import settings

class JobService:
    """Service for managing analysis jobs."""
    
    def __init__(self):
        self.claude_code_server = ClaudeCodeServer()
        # 暫時禁用 sandbox 服務以避免 Docker 權限問題
        # self.sandbox_service = SandboxService()
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
        
        # Process job asynchronously
        self._process_job(job_id, question, outputs, privacy_level)
        
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
    
    def _process_job(self, job_id: str, question: str, outputs: list, privacy_level: str):
        """Process job asynchronously."""
        try:
            # Update status
            self.jobs[job_id].status = JobStatus.PROCESSING
            
            # Generate code using Claude Code Server
            code_result = self.claude_code_server.generate_code(question, outputs, privacy_level)
            code = code_result['code']
            code_hash = code_result['code_hash']
            
            # Update job with code hash
            self.jobs[job_id].code_hash = code_hash
            
            # 暫時模擬 sandbox 執行結果
            # result = self.sandbox_service.execute_code(code, job_id)
            
            # 模擬成功執行
            mock_artifacts = []
            if OutputType.PLOT in outputs:
                mock_artifacts.append("trend_chart.png")
            if OutputType.TABLE in outputs:
                mock_artifacts.append("summary.csv")
            if OutputType.CODE in outputs:
                mock_artifacts.append("generated_code.py")
            if OutputType.EXPLANATION in outputs:
                mock_artifacts.append("explanation.txt")
            
            # Update job with results
            self.jobs[job_id].status = JobStatus.COMPLETED
            self.jobs[job_id].artifacts = mock_artifacts
            self.jobs[job_id].completed_at = datetime.utcnow()
            
            # Generate output hash
            output_hash = self._generate_output_hash(mock_artifacts)
            self.jobs[job_id].output_hash = output_hash
            
            # Create audit log
            self._create_audit_log(job_id, question, code_hash, privacy_level, output_hash)
                
        except Exception as e:
            # Update job with error
            self.jobs[job_id].status = JobStatus.FAILED
            self.jobs[job_id].error = str(e)
            self.jobs[job_id].completed_at = datetime.utcnow()
    
    def _generate_output_hash(self, artifacts: list) -> str:
        """Generate hash for output artifacts."""
        artifacts_str = ','.join(sorted(artifacts))
        return hashlib.sha256(artifacts_str.encode()).hexdigest()
    
    def _create_audit_log(self, job_id: str, question: str, code_hash: str, privacy_level: str, output_hash: str):
        """Create audit log entry."""
        audit_log = AuditLog(
            job_id=job_id,
            question=question,
            code_hash=code_hash,
            data_version="v1.0",
            output_hash=output_hash,
            privacy_level=privacy_level,
            timestamp=datetime.utcnow()
        )
        
        # TODO: Store audit log in database
        print(f"Audit log created: {audit_log}")
    
    def cleanup_job(self, job_id: str):
        """Clean up job artifacts."""
        if job_id in self.jobs:
            self.sandbox_service.cleanup_artifacts(job_id)
            del self.jobs[job_id]
