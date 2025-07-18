#!/bin/bash

# Production deployment script for face recognition system

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}🚀 Face Recognition System - Production Deployment${NC}"
echo "=================================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}❌ Docker is not running. Please start Docker first.${NC}"
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ docker-compose is not installed. Please install it first.${NC}"
    exit 1
fi

# Function to deploy with different profiles
deploy() {
    local profile=$1
    echo -e "${BLUE}📦 Deploying with profile: ${profile}${NC}"
    
    case $profile in
        "basic")
            docker-compose up -d face-recognition-app
            ;;
        "production")
            docker-compose --profile production up -d
            ;;
        "monitoring")
            docker-compose --profile production --profile monitoring up -d
            ;;
        *)
            echo -e "${RED}❌ Unknown profile: $profile${NC}"
            echo "Available profiles: basic, production, monitoring"
            exit 1
            ;;
    esac
}

# Parse command line arguments
PROFILE="basic"
BUILD=false
LOGS=false

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
        --logs)
            LOGS=true
            shift
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo "Options:"
            echo "  --profile PROFILE   Deployment profile (basic|production|monitoring)"
            echo "  --build            Force rebuild of images"
            echo "  --logs             Show logs after deployment"
            echo "  --help             Show this help message"
            exit 0
            ;;
        *)
            echo -e "${RED}❌ Unknown option: $1${NC}"
            exit 1
            ;;
    esac
done

# Build if requested
if [ "$BUILD" = true ]; then
    echo -e "${BLUE}🔨 Building Docker images...${NC}"
    docker-compose build --no-cache
fi

# Deploy
deploy $PROFILE

# Wait for services to be ready
echo -e "${BLUE}⏳ Waiting for services to be ready...${NC}"
sleep 10

# Health check
echo -e "${BLUE}🏥 Performing health check...${NC}"
if curl -f http://localhost:5000/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Application is healthy!${NC}"
else
    echo -e "${RED}❌ Application health check failed${NC}"
    echo -e "${YELLOW}📋 Checking logs...${NC}"
    docker-compose logs face-recognition-app
    exit 1
fi

# Show status
echo -e "${BLUE}📊 Service Status:${NC}"
docker-compose ps

# Show logs if requested
if [ "$LOGS" = true ]; then
    echo -e "${BLUE}📋 Service Logs:${NC}"
    docker-compose logs -f
fi

echo -e "${GREEN}🎉 Deployment completed successfully!${NC}"
echo -e "${BLUE}🌐 Access the application at: http://localhost:5000${NC}"

if [ "$PROFILE" = "production" ]; then
    echo -e "${BLUE}🌐 Nginx proxy available at: http://localhost${NC}"
fi

if [ "$PROFILE" = "monitoring" ]; then
    echo -e "${BLUE}📊 Prometheus: http://localhost:9090${NC}"
    echo -e "${BLUE}📈 Grafana: http://localhost:3000 (admin/admin)${NC}"
fi
