# Small official Python base image
FROM python:3.11-slim
WORKDIR /app

# Copy requirements first: this layer is cached until requirements.txt changes
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the code last: editing app/ only rebuilds this cheap layer
COPY app ./app

# Model weights go to a mounted cache dir, not into the image
ENV HF_HOME=/hf_cache

# Document the port and start the API on all interfaces
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
