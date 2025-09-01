FROM python:3.11-slim

WORKDIR /sandbox

# Install only essential packages for data analysis
RUN pip install --no-cache-dir \
    pandas==2.1.4 \
    openpyxl==3.1.2 \
    pyarrow==14.0.2 \
    duckdb==0.9.2 \
    matplotlib==3.8.2

# Create directories
RUN mkdir -p /data /artifacts

# Set environment variables
ENV DATASET_PATH=/data
ENV ARTIFACT_DIR=/artifacts
ENV PYTHONPATH=/sandbox

# Copy sandbox runner script
COPY sandbox_runner.py /sandbox/

# Security: Disable network access (comment out problematic line)
# RUN rm -f /etc/resolv.conf

# Default command
CMD ["python", "sandbox_runner.py"]
