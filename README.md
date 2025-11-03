# Devops Assignment

---

## Structure
```bash
  ├── app/                     # Flask Application Code
  ├── certs/                   # Self-signed certificates
  │   ├── self.crt
  │   └── self.key
  ├── nginx.conf               # Reverse Proxy + HTTPS Config
  ├── prometheus.yml           # Prometheus Config
  ├── docker-compose.yml       # Multi-environment setup
  ├── .env.dev                 # Development environment variables
  ├── .env.staging             # Staging environment variables
  ├── .env.prod                # Production environment variables
  ├── .github/workflows/ci.yml # GitHub Actions pipeline
  ├── tests/                   # Unit tests
  └── README.md
```
---

## Running the Application
This project uses Docker Compose to manage different environments — development, staging, and production.

### Prerequisites
Make sure you have the following installed:
1. Docker
2. Docker Compose
3. Python 3.11+

### Environment Setup
Each environment has its own .env configuration file:
1. .env.dev → Development
2. .env.staging → Staging
3. .env.prod → Production

### dev env
```bash
  FLASK_ENV=""
  POSTGRES_USER=""
  POSTGRES_PASSWORD=""
  POSTGRES_DB=""
  DATABASE_URL=""
  DB_MEMORY_LIMIT=""
  DB_CPU_LIMIT=""
  LOG_LEVEL=""
  API_PORT=""
  NGINX_PORT=""
  FLASK_APP=""
```

### staging env
```bash
  FLASK_ENV=""
  POSTGRES_USER=""
  POSTGRES_PASSWORD=""
  POSTGRES_DB=""
  DATABASE_URL=""
  DB_MEMORY_LIMIT=""
  DB_CPU_LIMIT=""
  LOG_LEVEL=""
  API_PORT=""
  NGINX_PORT=""
```

### prod env
```bash
  FLASK_ENV=""
  POSTGRES_USER=""
  POSTGRES_PASSWORD=""
  POSTGRES_DB=""
  DATABASE_URL=""
  DB_MEMORY_LIMIT=""
  DB_CPU_LIMIT=""
  LOG_LEVEL=""
  GUNICORN_WORKERS=""
  API_PORT=""
  NGINX_PORT=""
``` 

### Development Environment
Build and start containers using the development configuration:
```bash 
  docker compose --env-file .env.dev up --build 
```
1. Hot reload enabled
2. Debug logging
3. Light resource limits
4. HTTPS enabled (via Nginx)

### Staging Environment
Build and start containers using the staging configuration:
```bash 
  docker compose --env-file .env.staging up --build 
```
1. Mimics production
2. Medium resources
3. Info-level logging

### Production Environment
Build and start containers using the production configuration:
```bash 
  docker compose --env-file .env.prod up --build 
```
1. Gunicorn-based serving
2. HTTPS enabled (via Nginx)
3. Resource constraints & persistence

### Stopping Containers
To stop running containers (any environment) with remove all containers, networks, and volumes:
```bash
  docker compose down -v
```

### Access the Application
- API Endpoint: https://branchloans/health
- Prometheus Dashboard: http://localhost:9090

---

## CI/CD Pipeline Overview
Location: .github/workflows/ci.yml

### Stages
1. Test Stage
  - Runs Pytest to verify functionality
  - Fails early on test errors
2. Build Stage
  - Builds Docker image with commit SHA tag
3. Security Scan Stage
  - Runs Trivy scan for OS/library vulnerabilities
  - Pipeline fails on critical issues
4. Push Stage
  - Pushes image to Docker Hub if all stages succeed
  - Tags images as both ${{ github.sha }} and latest

### Trigger Events
- On push to main
- On pull_request (test only, no image push)

### Secrets Used
- DOCKERHUB_USERNAME
- DOCKERHUB_TOKEN
All sensitive data is managed securely using GitHub Secrets.

---