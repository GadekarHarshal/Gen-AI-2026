
FROM python:3.13-slim

# Set the working directory
WORKDIR /app

# Prevent Python from creating bytecode files
ENV PYTHONDONTWRITEBYTECODE=1

# Show Python output immediately
ENV PYTHONUNBUFFERED=1

# Allow Python to import packages from /app
ENV PYTHONPATH=/app

# Install Python dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY app/ ./app/
COPY ui/ ./ui/
COPY prompts/ ./prompts/
COPY data/records.json ./data/records.json

# Create directory for ChromaDB
RUN mkdir -p /app/data/chroma_db

# Expose FastAPI and Streamlit ports
EXPOSE 8000 8501

# Start FastAPI by default
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
