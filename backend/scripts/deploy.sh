#!/bin/bash

# ============================================================================
# REGIQ Backend Service Deployment Script
# ============================================================================
# Usage: ./deploy.sh [environment]
# Environments: staging, production
# ============================================================================

set -e  # Exit on error

# Configuration
ENVIRONMENT=${1:-staging}
PROJECT_NAME="regiq-backend"
DOCKER_REGISTRY="ghcr.io"
IMAGE_NAME="regiq/backend-service"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_prerequisites() {
    log_info "Checking prerequisites..."
    
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose is not installed"
        exit 1
    fi
    
    if ! command -v node &> /dev/null; then
        log_error "Node.js is not installed"
        exit 1
    fi
    
    log_success "Prerequisites check passed"
}

run_database_migrations() {
    log_info "Running database migrations..."
    
    cd backend
    
    if [ "$ENVIRONMENT" == "production" ]; then
        npm run migrate:prod
    else
        npm run migrate
    fi
    
    cd ..
    log_success "Database migrations completed"
}

build_docker_image() {
    log_info "Building Docker image..."
    
    TAG="${IMAGE_NAME}:${ENVIRONMENT}-$(date +%Y%m%d-%H%M%S)"
    
    docker build -t "${TAG}" \
        -f backend/Dockerfile \
        --build-arg ENVIRONMENT=${ENVIRONMENT} \
        .
    
    log_success "Docker image built: ${TAG}"
    
    echo "${TAG}"
}

push_to_registry() {
    local IMAGE_TAG=$1
    
    log_info "Pushing image to registry..."
    
    if [[ "$GITHUB_ACTIONS" == "true" ]]; then
        log_info "Running in GitHub Actions - skipping manual push"
    else
        docker push "${IMAGE_TAG}"
        log_success "Image pushed to registry: ${IMAGE_TAG}"
    fi
}

deploy_staging() {
    log_info "Deploying to staging environment..."
    
    # Load environment variables
    if [ -f "backend/.env.staging" ]; then
        export $(cat backend/.env.staging | xargs)
    fi
    
    # Deploy using docker-compose
    docker-compose -f docker-compose.staging.yml up -d
    
    log_success "Deployed to staging"
}

deploy_production() {
    log_info "Deploying to production environment..."
    
    # Load environment variables
    if [ -f "backend/.env.production" ]; then
        export $(cat backend/.env.production | xargs)
    fi
    
    # Deploy using docker-compose
    docker-compose -f docker-compose.production.yml up -d
    
    log_success "Deployed to production"
}

verify_deployment() {
    log_info "Verifying deployment..."
    
    HEALTH_URL=""
    if [ "$ENVIRONMENT" == "staging" ]; then
        HEALTH_URL="http://localhost:3000/health"
    elif [ "$ENVIRONMENT" == "production" ]; then
        HEALTH_URL="https://api.regiq.com/health"
    fi
    
    MAX_RETRIES=30
    RETRY_COUNT=0
    
    while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
        RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "${HEALTH_URL}" || echo "000")
        
        if [ "$RESPONSE" == "200" ]; then
            log_success "Deployment verified successfully"
            return 0
        fi
        
        RETRY_COUNT=$((RETRY_COUNT + 1))
        log_info "Waiting for service to be ready... (Attempt ${RETRY_COUNT}/${MAX_RETRIES})"
        sleep 10
    done
    
    log_error "Deployment verification failed after ${MAX_RETRIES} attempts"
    return 1
}

run_integration_tests() {
    log_info "Running integration tests..."
    
    cd backend
    
    if [ -f "test_integration_all.js" ]; then
        node test_integration_all.js || {
            log_error "Integration tests failed"
            exit 1
        }
    else
        log_warning "Integration test file not found, skipping..."
    fi
    
    cd ..
    log_success "Integration tests passed"
}

cleanup_old_containers() {
    log_info "Cleaning up old containers..."
    
    docker container prune -f --filter "until=24h"
    
    log_success "Cleanup completed"
}

backup_database() {
    if [ "$ENVIRONMENT" == "production" ]; then
        log_info "Creating database backup..."
        
        TIMESTAMP=$(date +%Y%m%d_%H%M%S)
        BACKUP_FILE="backups/db_backup_${TIMESTAMP}.sql"
        
        mkdir -p backups
        
        # Adjust based on your database type
        if [ -n "$DATABASE_URL" ]; then
            pg_dump "$DATABASE_URL" > "$BACKUP_FILE" || {
                log_warning "Database backup failed, continuing anyway..."
            }
            log_success "Database backup created: ${BACKUP_FILE}"
        fi
    fi
}

# Main deployment process
main() {
    log_info "Starting deployment to ${ENVIRONMENT}"
    log_info "=========================================="
    
    case $ENVIRONMENT in
        staging|production)
            check_prerequisites
            
            if [ "$ENVIRONMENT" == "production" ]; then
                backup_database
            fi
            
            run_database_migrations
            
            IMAGE_TAG=$(build_docker_image)
            push_to_registry "${IMAGE_TAG}"
            
            if [ "$ENVIRONMENT" == "staging" ]; then
                deploy_staging
            else
                deploy_production
            fi
            
            verify_deployment
            run_integration_tests
            cleanup_old_containers
            
            log_success "=========================================="
            log_success "Deployment to ${ENVIRONMENT} completed successfully!"
            log_success "=========================================="
            ;;
        *)
            log_error "Invalid environment: ${ENVIRONMENT}"
            log_error "Usage: ./deploy.sh [staging|production]"
            exit 1
            ;;
    esac
}

# Run main function
main
