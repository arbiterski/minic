"""
API endpoints for the Alzheimer's Disease Analysis Database.
"""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse
from pathlib import Path
from app.models.schemas import AskRequest, JobResponse, JobResult
from app.services.job_service import JobService
from app.core.config import settings

router = APIRouter()

# Dependency
def get_job_service() -> JobService:
    return JobService()

@router.post("/ask", response_model=JobResponse)
async def ask_question(
    request: AskRequest,
    job_service: JobService = Depends(get_job_service)
):
    """
    提交新的分析問題。
    
    Args:
        request: 包含問題和參數的分析請求
        
    Returns:
        包含工作 ID 的回應
    """
    try:
        job_id = job_service.create_job(
            question=request.question,
            dataset_id=request.dataset_id,
            outputs=request.outputs,
            privacy_level=request.privacy_level
        )
        
        return JobResponse(
            job_id=job_id,
            status="queued",
            message=f"分析工作已建立成功！問題：{request.question}"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/result/{job_id}", response_model=JobResult)
async def get_job_result(
    job_id: str,
    job_service: JobService = Depends(get_job_service)
):
    """
    Get job status and results.
    
    Args:
        job_id: Job identifier
        
    Returns:
        Job result with status and artifacts
    """
    job_result = job_service.get_job_status(job_id)
    
    if not job_result:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return job_result

@router.get("/files/{job_id}/{filename}")
async def get_job_file(
    job_id: str,
    filename: str,
    job_service: JobService = Depends(get_job_service)
):
    """
    Get generated files for a job.
    
    Args:
        job_id: Job identifier
        filename: Name of the file to retrieve
        
    Returns:
        File content
    """
    # Verify job exists
    job_result = job_service.get_job_status(job_id)
    if not job_result:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Check if file exists
    file_path = Path(settings.artifact_dir) / job_id / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    # Return file
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type='application/octet-stream'
    )

@router.delete("/jobs/{job_id}")
async def delete_job(
    job_id: str,
    job_service: JobService = Depends(get_job_service)
):
    """
    Delete a job and clean up artifacts.
    
    Args:
        job_id: Job identifier
        
    Returns:
        Success message
    """
    try:
        job_service.cleanup_job(job_id)
        return {"message": "Job deleted successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
