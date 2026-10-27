# Small official Python base image for the Streamlit UI
FROM python:3.11-slim
WORKDIR /app

# Copy requirements first: this layer is cached until requirements.txt changes
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the code last: editing app.py only rebuilds this cheap layer
COPY app.py .

# Streamlit listens on 8501; bind 0.0.0.0 so the host can reach it
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501", "--server.headless=true", "--browser.gatherUsageStats=false"]
