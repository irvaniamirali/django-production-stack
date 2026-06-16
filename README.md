# Django Production Stack

A **production-ready, containerized Django application** with enterprise-grade CI/CD, Infrastructure as Code (IaC), and automated deployment. Built to demonstrate modern DevOps practices and scalable web application architecture.

---

## Overview

This project is a complete, battle-tested template for deploying Django applications in production environments. It solves common challenges like environment consistency, secret management, zero-downtime deployments, and infrastructure automation.

---

## Key Features

| Feature | Description |
|---------|-------------|
| **Multi-stage Docker Builds** | Optimized image sizes with separate build/runtime stages |
| **Automated CI/CD** | GitHub Actions pipeline with linting, testing, and automatic image publishing |
| **GitHub Container Registry** | Private container registry integration with automatic versioning |
| **Infrastructure as Code** | Ansible playbooks for server setup and application deployment |
| **Secret Management** | Ansible Vault for encrypted sensitive data (API keys, passwords) |
| **Health Checks** | Container health checks and database readiness verification |
| **Nginx Reverse Proxy** | Production-grade static file serving and request routing |
| **PostgreSQL Database** | Managed database container with persistent volumes |
| **Monitoring Ready** | Structured logging, health endpoints, and container status tracking |
| **Security Hardened** | Environment isolation, non-root user, secrets never committed |

---

## Technologies Used

| Category | Technologies |
|----------|--------------|
| **Backend** | Django 6.0, Python 3.11, Gunicorn |
| **Database** | PostgreSQL 15 |
| **Web Server** | Nginx (reverse proxy + static files) |
| **Containerization** | Docker, Docker Compose, Docker multi-stage builds |
| **CI/CD** | GitHub Actions (linting, testing, build, push) |
| **Infrastructure** | Ansible (setup + deployment playbooks), Ansible Vault |
| **Container Registry** | GitHub Container Registry (GHCR) |
| **Code Quality** | Flake8 |
| **Process Management** | Gunicorn with gthread worker class |

---

## CI/CD Pipeline

The GitHub Actions workflow automatically runs on every push to `main`:

```yaml
Stage 1: Lint & Test
├── Checkout code
├── Setup Python 3.11
├── Install dependencies
└── Run flake8 validation

Stage 2: Build & Push (main branch only)
├── Setup Docker Buildx
├── Login to GHCR
├── Generate version tags (git-sha + latest)
└── Build + push multi-arch image
```
Tags applied automatically: `latest`, `git-<commit-sha>`, `main`

---

## Infrastructure as Code

### Ansible Architecture

```
ansible/
├── ansible.cfg              # Central configuration
├── inventories/production/
│   ├── hosts.yml           # Target server definition
│   └── group_vars/
│       ├── all.yml         # Non-sensitive vars
│       └── vault.yml       # Encrypted secrets (Ansible Vault)
├── playbooks/
│   ├── setup.yml           # Initial server provisioning
│   └── deploy.yml          # Application deployment
```

#### What Ansible automates:
- Docker & Docker Compose installation

- System dependencies (PostgreSQL client, Python, curl)

- User permissions (docker group addition)

- Project directory structure creation

- Secure .env file generation from vault secrets

- Docker network creation

- Container orchestration (dependency-aware startup)

- Database migrations and static collection

- Deployment health verification

## Getting Started

### Prerequisites

- Docker & Docker Compose

- Python 3.11+ (for local development)

- (For deployment) Ansible and target Linux server

### Local Development

```
# 1. Clone the repository
git clone https://github.com/irvaniamirali/django-production-stack.git
cd django-production-stack

# 2. Create environment file
cp .env.example .env
# Edit .env with your values

# 3. Run with Docker Compose
docker compose -f docker/docker-compose.override.yml up -d

# 4. Access the application
open http://localhost
```

### Production Deployment

```
# 1. Install Ansible (on your control machine)
pip install ansible

# 2. Create encrypted vault file
ansible-vault create ansible/inventories/production/group_vars/vault.yml
# Add: vault_django_secret_key, vault_django_allowed_hosts, vault_db_password

# 3. Run server setup (first time only)
ansible-playbook -i ansible/inventories/production/hosts.yml ansible/playbooks/setup.yml --ask-vault-pass

# 4. Deploy the application
ansible-playbook -i ansible/inventories/production/hosts.yml ansible/playbooks/deploy.yml --ask-vault-pass
```

## License
Distributed under the MIT License. See `LICENSE` for more information.
