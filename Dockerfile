FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
  && rm -rf /var/lib/apt/lists/*

# copy and install python dependencies
# --no-cache-dir -> prevents pip from caching packages
# this reduces the image size
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# expose port 8000 for the app
EXPOSE 8000

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8000", "wsgi:app"]
