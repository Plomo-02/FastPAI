FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update
RUN apt-get install -y build-essential
RUN rm -rf /var/lib/apt/lists/*

# Copy only requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies with pip cache
RUN pip install --no-cache-dir -r requirements.txt
# No need to COPY source files since we're using volumes

ENTRYPOINT ["python", "-m","uvicorn", "main:app"]
CMD ["--host", "0.0.0.0", "--port", "8000"] 