# version 3.11-slim, lightweight Python Docker image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
  && rm -rf /var/lib/apt/lists/*

# copy and install python dependencies
# --no-cache-dir -> prevents pip from caching packages
# this reduces the image size
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy project, all files and folders
# it copies app, wsgi.py, requirements.txt, etc.
COPY . .

# expose port 8000 for the app
EXPOSE 8000

# start the app with gunicorn
# gunicorn ? it's a production-ready web server for Python web applications
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8000", "wsgi:app"]
