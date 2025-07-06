# Base image
FROM python:3.11-slim

# Set environment vars
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 5000

# Run the app
CMD ["python", "webapp.py"]

RUN pip install --upgrade pip && pip install -r requirements.txt

# Download the spaCy model
RUN python -m spacy download en_core_web_sm
