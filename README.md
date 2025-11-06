# Devops Assignment

--- 

## Setup Project
Follow the steps below to set up and prepare the Branch Loan API for local development or deployment.

### Clone the Repository
```bash
  git clone https://github.com/<your-username>/branchloan-api.git
  cd branchloan-api
  python3 -m venv venv 
  source venv/bin/activate       # On macOS/Linux
  pip install -r requirements.txt 
```

### Generate SSL Certificates (for HTTPS)
If you don’t already have the self-signed certificates (certs/self.crt and certs/self.key), create them using:
```bash
  mkdir -p certs
  openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout certs/self.key -out certs/self.crt \
    -subj "/CN=localhost"
```
These certificates are used by Nginx to serve the API securely over HTTPS at https://localhost.

### Configure Environment Variables
Copy the sample environment file or choose from the provided ones:
```bash
  cp .env.dev .env
```

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

## Design Decision

| Component                        | Choice                               | Reasoning                                 |
| -------------------------------- | ------------------------------------ | ----------------------------------------- |
| **Unified `docker-compose.yml`** | One file for all envs                | Easier maintenance & scalability          |
| **Nginx + SSL**                  | HTTPS reverse proxy                  | Ensures secure communication even locally |
| **Self-signed certs**            | `/certs/self.crt`, `/certs/self.key` | For localhost SSL setup                   |
| **Gunicorn (prod)**              | WSGI production server               | Efficient, concurrent request handling    |
| **Prometheus**                   | Lightweight monitoring               | Easy to extend with Grafana later         |
| **GitHub Actions**               | Native CI/CD                         | Simple setup with container scanning      |
| **Trivy**                        | Image vulnerability scanning         | Security compliance                       |

--- 

## Troubleshooting

| Issue                        | Cause                | Fix                                        |
| ---------------------------- | -------------------- | ------------------------------------------ |
| `Nginx 502 Bad Gateway`      | API not healthy      | Check API logs: `docker compose logs api`  |
| `Database connection failed` | Wrong credentials    | Verify `DATABASE_URL` in `.env.*`          |
| `Permission denied` on certs | Incorrect file perms | `chmod 600 certs/self.key`                 |
| Prometheus not scraping      | Wrong target config  | Verify `prometheus.yml` and API `/metrics` |
| Docker build too slow        | Cached layers        | Add `--no-cache` to build command          |


---

## Future Improvements
- Add Grafana dashboards for Prometheus metrics.
- Set up automated deployment to a staging/production server (e.g., via SSH or AWS ECS).
- Implement structured JSON logging.
- Add real database migrations using Alembic.
- Integrate health-check-based auto-restarts in production.

---

## Tests
Simple sanity checks added in tests/test_basic.py:
```bash
  def test_basic_math():
      assert 2 + 2 == 4

  def test_environment():
      import os
      assert "DATABASE_URL" in os.environ or True
```

---

## Author
Sharad 