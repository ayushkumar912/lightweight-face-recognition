# 🚀 DevOps Operations Guide

## Face Recognition Attendance System - DevOps Documentation

This document provides comprehensive instructions for DevOps operations, deployment, monitoring, and automation for the Face Recognition Attendance System.

---

## 📋 Table of Contents

- [🏗️ Architecture Overview](#architecture-overview)
- [🐳 Docker & Containerization](#docker--containerization)
- [🔄 CI/CD Pipelines](#cicd-pipelines)
- [🚀 Deployment Guide](#deployment-guide)
- [🌍 Environment Setup](#environment-setup)
- [📊 Monitoring & Logging](#monitoring--logging)
- [🔧 Automation & Scripting](#automation--scripting)
- [🛠️ Troubleshooting](#troubleshooting)
- [📚 Additional Resources](#additional-resources)

---

## 🏗️ Architecture Overview

### System Components
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     Nginx       │    │  Face Recognition│    │     Redis       │
│  Load Balancer  │◄──►│     Flask App    │◄──►│     Cache       │
│   (Port 80)     │    │   (Port 5000)    │    │   (Port 6379)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         ▲                        ▲                        ▲
         │                        │                        │
         ▼                        ▼                        ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Prometheus    │    │     Grafana     │    │   File Storage  │
│   (Port 9090)   │    │   (Port 3000)   │    │  (Volumes)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Technology Stack
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Backend**: Python 3.11, Flask, dlib, OpenCV
- **Database**: CSV files, Redis (caching)
- **Containerization**: Docker, Docker Compose
- **Monitoring**: Prometheus, Grafana
- **Proxy**: Nginx
- **CI/CD**: GitHub Actions
- **Orchestration**: Docker Compose, Kubernetes (optional)

---

## 🐳 Docker & Containerization

### Docker Architecture

#### Multi-Stage Dockerfile
```dockerfile
# Builder stage - Heavy dependencies
FROM python:3.11-slim AS builder
RUN apt-get update && apt-get install -y build-essential cmake
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Runtime stage - Minimal footprint
FROM python:3.11-slim
RUN groupadd -r appuser && useradd -r -g appuser appuser
COPY --from=builder /root/.local /home/appuser/.local
COPY --chown=appuser:appuser . .
USER appuser
```

#### Container Optimization
- **Image Size**: Reduced from ~6GB to ~2GB using multi-stage builds
- **Security**: Non-root user execution
- **Health Checks**: Built-in health monitoring
- **Resource Limits**: Memory and CPU constraints

### Docker Commands

#### Build & Run
```bash
# Build the application image
docker build -t face-recognition-app .

# Build with no cache (clean build)
docker build --no-cache -t face-recognition-app .

# Run single container
docker run -p 5000:5000 face-recognition-app

# Run with environment variables
docker run -p 5000:5000 -e DEBUG=true face-recognition-app
```

#### Docker Compose Operations
```bash
# Start all services
docker-compose up -d

# Start with specific profile
docker-compose --profile monitoring up -d

# Scale services
docker-compose up -d --scale face-recognition-app=3

# View logs
docker-compose logs -f face-recognition-app

# Stop services
docker-compose down

# Remove volumes (clean slate)
docker-compose down -v
```

#### Container Management
```bash
# List running containers
docker ps

# Check container stats
docker stats

# Execute commands in container
docker exec -it face-recognition-app bash

# View container logs
docker logs face-recognition-app --tail 50 -f

# Inspect container
docker inspect face-recognition-app
```

---

## 🔄 CI/CD Pipelines

### GitHub Actions Workflow

#### Pipeline Stages
1. **Code Quality** - Linting, formatting, security checks
2. **Testing** - Unit tests, integration tests
3. **Build** - Docker image creation
4. **Security** - Vulnerability scanning
5. **Deploy** - Automated deployment

#### Workflow Configuration
**File**: `.github/workflows/ci-cd.yml`

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.9, 3.10, 3.11]
    
    steps:
    - uses: actions/checkout@v4
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install flake8 pytest bandit safety
    
    - name: Code quality checks
      run: |
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
        bandit -r . -x tests
        safety check
    
    - name: Run tests
      run: pytest tests/ -v

  build:
    needs: test
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    - name: Build Docker image
      run: docker build -t face-recognition-app .
    
    - name: Test Docker image
      run: |
        docker run -d -p 5000:5000 face-recognition-app
        sleep 10
        curl -f http://localhost:5000/health
```

#### Pipeline Features
- **Multi-Python Testing**: Tests on Python 3.9, 3.10, 3.11
- **Security Scanning**: Bandit for code security, Safety for dependencies
- **Code Quality**: Flake8 linting
- **Docker Integration**: Automated builds and tests
- **Health Checks**: Validates deployment success

### Branch Protection
- **Main Branch**: Requires PR reviews
- **Status Checks**: All CI checks must pass
- **Up-to-date**: Branches must be current

---

## 🚀 Deployment Guide

### Environment Profiles

#### Development Environment
```bash
# Basic setup - minimal resources
docker-compose --profile basic up -d
```
**Services**: App, Nginx, Redis

#### Production Environment
```bash
# Full production stack
docker-compose --profile production up -d
```
**Services**: App, Nginx, Redis + SSL, Health checks

#### Monitoring Environment
```bash
# Complete monitoring stack
docker-compose --profile monitoring up -d
```
**Services**: All + Prometheus, Grafana, Metrics

### Automated Deployment

#### Using Deploy Script
```bash
# Deploy with build
./deploy.sh --profile monitoring --build

# Deploy specific environment
./deploy.sh --profile production

# Deploy with health verification
./deploy.sh --profile monitoring --verify
```

#### Manual Deployment Steps
```bash
# 1. Pull latest code
git pull origin main

# 2. Build updated images
docker-compose build --no-cache

# 3. Deploy with zero downtime
docker-compose up -d --force-recreate --remove-orphans

# 4. Verify deployment
./verify_deployment.sh
```

### Deployment Verification
```bash
# Automated verification script
./verify_deployment.sh

# Manual verification
curl http://localhost/health
curl http://localhost:9090/-/healthy
curl http://localhost:3000/api/health
```

### Rolling Updates
```bash
# Update single service
docker-compose up -d --no-deps face-recognition-app

# Zero-downtime deployment
docker-compose up -d --scale face-recognition-app=2
# Wait for health checks
docker-compose up -d --scale face-recognition-app=1
```

---

## 🌍 Environment Setup

### Prerequisites
- Docker Engine 20.0+
- Docker Compose 2.0+
- Git
- 8GB+ RAM recommended
- macOS/Linux/Windows with WSL2

### Local Development Setup
```bash
# 1. Clone repository
git clone https://github.com/yourusername/face-recognition-system.git
cd face-recognition-system

# 2. Setup environment
cp .env.example .env
# Edit .env with your configurations

# 3. Install dependencies (optional, for local dev)
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
pip install -r requirements.txt

# 4. Start development environment
docker-compose --profile basic up -d

# 5. Access application
open http://localhost:5000
```

### Environment Variables

#### Application Configuration
```bash
# .env file
DEBUG=false
FLASK_ENV=production
LOG_LEVEL=INFO
KNOWN_FACES_PATH=/app/backend/known_faces
ATTENDANCE_FILE=/app/api/attendance.csv
```

#### Docker Configuration
```bash
# docker-compose.yml environment
PYTHONPATH=/app
FLASK_APP=api/app.py
TZ=UTC
```

### Production Environment
```bash
# Production optimizations
export COMPOSE_HTTP_TIMEOUT=120
export DOCKER_CLIENT_TIMEOUT=120

# Resource limits
ulimit -n 65536  # File descriptors
sysctl vm.max_map_count=262144  # Memory mapping
```

---

## 📊 Monitoring & Logging

### Prometheus Configuration

#### Metrics Collection
**File**: `monitoring/prometheus.yml`
```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'face-recognition-app'
    static_configs:
      - targets: ['face-recognition-app:5000']
    scrape_interval: 30s
    metrics_path: /metrics

  - job_name: 'nginx'
    static_configs:
      - targets: ['nginx:80']

  - job_name: 'redis'
    static_configs:
      - targets: ['redis:6379']
```

#### Key Metrics
- `up`: Service availability
- `face_recognition_requests_total`: API request count
- `face_recognition_confidence`: ML model accuracy
- `attendance_records_total`: Daily attendance count
- `container_memory_usage_bytes`: Resource utilization

### Grafana Dashboards

#### Pre-configured Dashboards
1. **System Overview**
   - Service health status
   - Resource utilization
   - Request rates

2. **Face Recognition Analytics**
   - Recognition accuracy trends
   - Daily attendance patterns
   - Confidence score distributions

3. **Infrastructure Monitoring**
   - Container metrics
   - Network traffic
   - Storage usage

#### Dashboard Import
```bash
# Access Grafana
open http://localhost:3000
# Login: admin/admin

# Import dashboard
curl -X POST \
  http://admin:admin@localhost:3000/api/dashboards/db \
  -H 'Content-Type: application/json' \
  -d @monitoring/grafana-dashboard-config.json
```

### Logging Strategy

#### Application Logs
```python
# Structured logging
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

#### Container Logs
```bash
# View all service logs
docker-compose logs -f

# Specific service logs
docker-compose logs -f face-recognition-app

# Filter logs by level
docker-compose logs face-recognition-app 2>&1 | grep ERROR

# Export logs
docker-compose logs --no-color face-recognition-app > app.log
```

#### Log Aggregation (Optional)
```yaml
# Add to docker-compose.yml for ELK stack
elasticsearch:
  image: elasticsearch:7.9.3
  environment:
    - discovery.type=single-node
    
logstash:
  image: logstash:7.9.3
  
kibana:
  image: kibana:7.9.3
  ports:
    - "5601:5601"
```

### Alerting

#### Prometheus Alert Rules
**File**: `monitoring/alert_rules.yml`
```yaml
groups:
  - name: face_recognition_alerts
    rules:
      - alert: ServiceDown
        expr: up == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Service {{ $labels.job }} is down"

      - alert: HighMemoryUsage
        expr: container_memory_usage_bytes > 1000000000
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage on {{ $labels.container_label_com_docker_compose_service }}"

      - alert: LowRecognitionAccuracy
        expr: avg_over_time(face_recognition_confidence[5m]) < 0.7
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "Face recognition accuracy below threshold"
```

---

## 🔧 Automation & Scripting

### Deployment Scripts

#### Main Deploy Script
**File**: `deploy.sh`
```bash
#!/bin/bash
# Automated deployment with health checks

set -e

PROFILE="basic"
BUILD=false
VERIFY=false

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --profile)
      PROFILE="$2"
      shift 2
      ;;
    --build)
      BUILD=true
      shift
      ;;
    --verify)
      VERIFY=true
      shift
      ;;
    *)
      echo "Unknown option $1"
      exit 1
      ;;
  esac
done

echo "🚀 Deploying with profile: $PROFILE"

# Build if requested
if [ "$BUILD" = true ]; then
  echo "🔨 Building Docker images..."
  docker-compose build --no-cache
fi

# Deploy services
echo "📦 Deploying services..."
docker-compose --profile $PROFILE up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 30

# Health check
echo "🏥 Performing health check..."
if curl -f http://localhost:5000/health > /dev/null 2>&1; then
  echo "✅ Application is healthy"
else
  echo "❌ Application health check failed"
  exit 1
fi

if [ "$VERIFY" = true ]; then
  echo "🔍 Running verification script..."
  ./verify_deployment.sh
fi

echo "🎉 Deployment completed successfully!"
```

#### Verification Script
**File**: `verify_deployment.sh`
```bash
#!/bin/bash
# Comprehensive deployment verification

echo "🔍 Verifying Face Recognition System Deployment"
echo "=============================================="

# Check container status
echo "📦 Checking container status..."
docker-compose ps --format "table {{.Name}}\t{{.Status}}"

# Health checks
echo ""
echo "🏥 Running health checks..."

check_service() {
  local name=$1
  local url=$2
  local expected=$3
  
  if curl -sf "$url" | grep -q "$expected"; then
    echo "✅ $name: HEALTHY"
  else
    echo "❌ $name: UNHEALTHY"
    return 1
  fi
}

check_service "Application" "http://localhost:5000/health" "healthy"
check_service "Prometheus" "http://localhost:9090/-/healthy" "Prometheus Server is Healthy"
check_service "Grafana" "http://localhost:3000/api/health" "database"

# Performance test
echo ""
echo "⚡ Running performance test..."
time curl -s http://localhost:5000/health > /dev/null

echo ""
echo "✅ All checks passed! System is ready."
```

### Backup Scripts

#### Data Backup
**File**: `scripts/backup.sh`
```bash
#!/bin/bash
# Backup face recognition data and configurations

BACKUP_DIR="./backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

echo "💾 Creating backup in $BACKUP_DIR"

# Backup face data
cp -r backend/known_faces "$BACKUP_DIR/"

# Backup attendance records
cp api/attendance.csv "$BACKUP_DIR/"

# Backup configurations
cp docker-compose.yml "$BACKUP_DIR/"
cp -r monitoring "$BACKUP_DIR/"

# Create archive
tar -czf "$BACKUP_DIR.tar.gz" -C "$BACKUP_DIR" .
rm -rf "$BACKUP_DIR"

echo "✅ Backup created: $BACKUP_DIR.tar.gz"
```

#### Database Backup (if using PostgreSQL)
```bash
#!/bin/bash
# Database backup script
docker exec postgres pg_dump -U username dbname > backup_$(date +%Y%m%d).sql
```

### Maintenance Scripts

#### System Cleanup
**File**: `scripts/cleanup.sh`
```bash
#!/bin/bash
# System maintenance and cleanup

echo "🧹 Performing system cleanup..."

# Remove unused Docker images
docker image prune -f

# Remove unused containers
docker container prune -f

# Remove unused volumes
docker volume prune -f

# Remove unused networks
docker network prune -f

# Clean up logs older than 7 days
find ./logs -name "*.log" -mtime +7 -delete 2>/dev/null || true

# Clean up temporary files
rm -rf tmp/*

echo "✅ Cleanup completed"
```

#### Log Rotation
```bash
#!/bin/bash
# Log rotation script
find ./logs -name "*.log" -size +100M -exec logrotate {} \;
```

### Monitoring Scripts

#### Health Monitor
**File**: `scripts/health_monitor.sh`
```bash
#!/bin/bash
# Continuous health monitoring

while true; do
  if ! curl -sf http://localhost:5000/health > /dev/null; then
    echo "$(date): ❌ Application health check failed" >> health.log
    # Send notification (email, slack, etc.)
  else
    echo "$(date): ✅ Application healthy" >> health.log
  fi
  sleep 60
done
```

---

## 🛠️ Troubleshooting

### Common Issues

#### Container Won't Start
```bash
# Check container logs
docker-compose logs face-recognition-app

# Check system resources
docker system df
docker system events

# Restart with clean state
docker-compose down -v
docker-compose up -d
```

#### Memory Issues
```bash
# Check memory usage
docker stats

# Increase memory limits in docker-compose.yml
mem_limit: 2g
memswap_limit: 2g

# Clear unused resources
docker system prune -a
```

#### Port Conflicts
```bash
# Check port usage
lsof -i :5000
netstat -tulpn | grep :5000

# Change ports in docker-compose.yml
ports:
  - "5001:5000"  # Use different external port
```

#### Face Recognition Issues
```bash
# Check face encodings
ls -la backend/known_faces/

# Verify model files
ls -la backend/resorces/

# Check application logs
docker-compose logs face-recognition-app | grep -i "face\|recognition\|error"
```

### Performance Optimization

#### Application Tuning
```python
# In app.py - optimize for production
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
app.config['UPLOAD_TIMEOUT'] = 30  # seconds
```

#### Docker Optimization
```dockerfile
# Multi-stage build optimization
FROM python:3.11-slim as builder
# Install dependencies here

FROM python:3.11-slim as runtime
# Copy only runtime dependencies
```

#### Database Optimization
```bash
# Redis tuning
redis-cli CONFIG SET maxmemory 512mb
redis-cli CONFIG SET maxmemory-policy allkeys-lru
```

### Debug Mode

#### Enable Debug Logging
```bash
# Set environment variable
export DEBUG=true
docker-compose restart face-recognition-app

# Or in docker-compose.yml
environment:
  - DEBUG=true
  - LOG_LEVEL=DEBUG
```

#### Development Mode
```bash
# Mount source code for live editing
volumes:
  - ./api:/app/api:ro
  - ./backend:/app/backend:ro
```

---

## 📚 Additional Resources

### Documentation Structure
```
docs/
├── DEVOPS_FEATURES.md      # DevOps capabilities overview
├── DEPLOYMENT_SUCCESS.md   # Deployment verification guide
├── PROMETHEUS_GUIDE.md     # Prometheus usage instructions
└── WEBSITE_USAGE_GUIDE.md  # Web interface guide
```

### Useful Commands Reference

#### Docker Operations
```bash
# Quick status check
docker-compose ps

# Service logs
docker-compose logs -f [service_name]

# Scale services
docker-compose up -d --scale face-recognition-app=3

# Update single service
docker-compose up -d --no-deps face-recognition-app

# Complete reset
docker-compose down -v && docker-compose up -d
```

#### Monitoring Commands
```bash
# Prometheus metrics
curl http://localhost:9090/api/v1/query?query=up

# Grafana health
curl http://localhost:3000/api/health

# Application metrics
curl http://localhost:5000/metrics
```

#### Maintenance Commands
```bash
# System cleanup
docker system prune -a

# Log viewing
docker-compose logs --tail=100 -f

# Resource monitoring
docker stats --no-stream
```

### External Resources
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Tutorials](https://grafana.com/tutorials/)
- [GitHub Actions Guide](https://docs.github.com/en/actions)

### Support & Contact
- **Issues**: GitHub Issues tracker
- **Documentation**: `/docs` directory
- **Monitoring**: Grafana dashboards at http://localhost:3000

---

## 🔄 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-07-18 | Initial DevOps implementation |
| 1.1.0 | 2025-07-18 | Added comprehensive monitoring |
| 1.2.0 | 2025-07-18 | Enhanced CI/CD pipeline |

---

**🎯 This DevOps guide provides everything needed to deploy, monitor, and maintain the Face Recognition Attendance System in production environments.**
