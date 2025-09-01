"""
Sandbox service for executing Python code in isolated Docker containers.
"""

import json
import subprocess
import tempfile
import os
from typing import Dict, Any, Optional
from pathlib import Path
import docker
from app.core.config import settings

class SandboxService:
    """Service for executing code in isolated sandbox containers."""
    
    def __init__(self):
        self.client = docker.from_env()
        self.image = settings.sandbox_image
        self.timeout = settings.sandbox_timeout
    
    def execute_code(self, code: str, job_id: str) -> Dict[str, Any]:
        """
        Execute Python code in isolated sandbox container.
        
        Args:
            code: Python code to execute
            job_id: Job identifier for artifact organization
            
        Returns:
            Execution result with status and artifacts
        """
        try:
            # Create temporary input file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                input_data = {'code': code}
                json.dump(input_data, f)
                input_file = f.name
            
            # Prepare container paths
            artifacts_dir = Path(settings.artifact_dir) / job_id
            artifacts_dir.mkdir(parents=True, exist_ok=True)
            
            # Run sandbox container
            result = self._run_container(input_file, artifacts_dir)
            
            # Clean up
            os.unlink(input_file)
            
            return result
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'artifacts': []
            }
    
    def _run_container(self, input_file: str, artifacts_dir: Path) -> Dict[str, Any]:
        """Run sandbox container with code execution."""
        
        # Container configuration
        container_config = {
            'image': self.image,
            'command': ['python', 'sandbox_runner.py'],
            'volumes': {
                str(artifacts_dir): {'bind': '/artifacts', 'mode': 'rw'},
                str(Path(settings.dataset_path).parent): {'bind': '/data', 'mode': 'ro'},
                input_file: {'bind': '/tmp/input.json', 'mode': 'ro'}
            },
            'stdin_open': True,
            'detach': False,
            'remove': True,
            'network_disabled': True,
            'mem_limit': '512m',
            'cpu_period': 100000,
            'cpu_quota': 50000,  # 50% CPU limit
        }
        
        try:
            # Read input data
            with open(input_file, 'r') as f:
                input_data = f.read()
            
            # Run container
            container = self.client.containers.run(
                **container_config,
                input=input_data.encode(),
                timeout=self.timeout
            )
            
            # Parse output
            output = container.decode('utf-8').strip()
            result = json.loads(output)
            
            # Check for generated artifacts
            artifacts = []
            if result['status'] == 'success':
                artifacts = self._collect_artifacts(artifacts_dir)
                result['artifacts'] = artifacts
            
            return result
            
        except subprocess.TimeoutExpired:
            return {
                'status': 'error',
                'error': 'Execution timeout',
                'artifacts': []
            }
        except json.JSONDecodeError:
            return {
                'status': 'error',
                'error': 'Invalid output format',
                'artifacts': []
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': f'Container execution failed: {str(e)}',
                'artifacts': []
            }
    
    def _collect_artifacts(self, artifacts_dir: Path) -> list:
        """Collect generated artifacts from artifacts directory."""
        artifacts = []
        
        if artifacts_dir.exists():
            for file_path in artifacts_dir.iterdir():
                if file_path.is_file():
                    artifacts.append(file_path.name)
        
        return artifacts
    
    def cleanup_artifacts(self, job_id: str):
        """Clean up artifacts for a specific job."""
        artifacts_dir = Path(settings.artifact_dir) / job_id
        if artifacts_dir.exists():
            import shutil
            shutil.rmtree(artifacts_dir)
