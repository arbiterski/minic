"""
Background worker for processing analysis jobs.
"""

import time
import logging
from app.services.job_service import JobService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main worker function."""
    logger.info("Starting Alzheimer's Disease Analysis Worker")
    
    job_service = JobService()
    
    try:
        while True:
            # Process pending jobs
            # In a real implementation, this would poll Redis or use RQ
            logger.info("Worker running...")
            time.sleep(10)
            
    except KeyboardInterrupt:
        logger.info("Worker stopped by user")
    except Exception as e:
        logger.error(f"Worker error: {e}")
        raise

if __name__ == "__main__":
    main()
