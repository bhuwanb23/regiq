# REGIQ CI/CD Pipeline Documentation

## 📋 Overview

This document describes the complete CI/CD pipeline setup for both AI/ML and Backend services.

---

## 🏗️ Architecture

### Services
- **AI/ML Service** - Python FastAPI (port 8000)
- **Backend Service** - Node.js Express (port 3000)

### Environments
- **Development** - Local development
- **Staging** - Pre-production testing
- **Production** - Live environment

---

## 🚀 CI/CD Pipelines

### AI/ML Service Pipeline

**File:** `.github/workflows/ai-ml-cicd.yml`

#### Stages:

1. **🔍 Lint & Validate**
   - Code formatting check (Black)
   - Linting with Flake8
   - Type checking with MyPy

2. **🧪 Unit Tests**
   - Runs on Python 3.9, 3.10, 3.11
   - Coverage reporting to Codecov
   - Parallel execution across versions

3. **🔗 Integration Tests**
   - Requires PostgreSQL 14 and Redis 6
   - Tests database interactions
   - Tests service-to-service communication

4. **🐳 Build Docker Image**
   - Multi-architecture build
   - Push to GitHub Container Registry
   - Tagged with SHA and 'latest'

5. **🚀 Deploy to Staging**
   - Automatic deployment on main branch
   - Health check verification
   - Smoke tests execution

6. **🎯 Deploy to Production**
   - Manual approval required (GitHub Environment)
   - Blue-green deployment strategy
   - Rollback capability

### Backend Service Pipeline

**File:** `.github/workflows/backend-cicd.yml`

#### Stages:

1. **🔍 Lint & Validate**
   - ESLint code analysis
   - Prettier formatting check

2. **🧪 Unit Tests**
   - Runs on Node.js 18 and 20
   - Jest coverage reporting
   - Parallel execution

3. **🔗 Integration Tests**
   - PostgreSQL and Redis dependencies
   - API endpoint testing
   - Database migration testing

4. **🎯 E2E Tests**
   - Full system integration testing
   - Backend ↔ AI/ML communication tests
   - Performance benchmarks

5. **🐳 Build Docker Image**
   - Optimized multi-stage build
   - Security scanning
   - Registry push

6. **🚀 Deploy to Staging**
   - Automated deployment
   - Database migrations
   - Health verification

7. **🎯 Deploy to Production**
   - Requires manual approval
   - Zero-downtime deployment
   - Automated rollback on failure

---

## 📁 File Structure

```
regiq/
├── .github/
│   └── workflows/
│       ├── ai-ml-cicd.yml      # AI/ML pipeline
│       └── backend-cicd.yml     # Backend pipeline
├── ai-ml/
│   ├── scripts/
│   │   └── deploy.sh            # AI/ML deployment script
│   ├── .env.staging             # Staging environment variables
│   ├── .env.production          # Production environment variables
│   └── Dockerfile               # AI/ML Docker image
├── backend/
│   ├── scripts/
│   │   └── deploy.sh            # Backend deployment script
│   ├── .env.staging             # Staging environment variables
│   ├── .env.production          # Production environment variables
│   └── Dockerfile               # Backend Docker image
├── docker-compose.staging.yml    # Staging environment setup
└── docker-compose.production.yml # Production environment setup
```

---

## 🔧 Configuration

### GitHub Secrets Required

#### For AI/ML Service:
```bash
# Container Registry
GITHUB_TOKEN              # Auto-provided by GitHub Actions

# Deployment (if using external providers)
AWS_ACCESS_KEY_ID         # AWS credentials
AWS_SECRET_ACCESS_KEY     # AWS credentials
AWS_REGION                # AWS region

# Notification (optional)
SLACK_WEBHOOK_URL         # Slack notifications
DISCORD_WEBHOOK_URL       # Discord notifications
```

#### For Backend Service:
```bash
# Same as AI/ML plus:
DATABASE_URL              # Production database connection string
REDIS_URL                 # Production Redis connection string
```

### GitHub Environments

Create these environments in GitHub repository settings:

1. **staging**
   - Auto-deploy enabled
   - No approval required

2. **production**
   - Manual approval required
   - Protected branches
   - Deployment branches: `main` only

---

## 🚦 Usage

### Manual Deployment

#### AI/ML Service

```bash
# Deploy to staging
cd ai-ml
chmod +x scripts/deploy.sh
./scripts/deploy.sh staging

# Deploy to production
./scripts/deploy.sh production
```

#### Backend Service

```bash
# Deploy to staging
cd backend
chmod +x scripts/deploy.sh
./scripts/deploy.sh staging

# Deploy to production
./scripts/deploy.sh production
```

### Local Testing

```bash
# Test AI/ML service locally
cd ai-ml
docker-compose -f docker-compose.staging.yml up --build

# Test Backend service locally
cd backend
docker-compose -f docker-compose.staging.yml up --build
```

---

## 📊 Monitoring & Verification

### Health Check Endpoints

- **AI/ML Service:** `http://localhost:8000/health`
- **Backend Service:** `http://localhost:3000/health`

### Logs

Access container logs:

```bash
# View all logs
docker-compose -f docker-compose.staging.yml logs -f

# View specific service
docker-compose -f docker-compose.staging.yml logs -f ai-ml-service
```

### Metrics

The pipelines track:
- ✅ Build success/failure rates
- ✅ Test coverage percentages
- ✅ Deployment duration
- ✅ Rollback frequency
- ✅ Health check response times

---

## 🔄 Rollback Strategy

### Automatic Rollback Triggers
1. Health check failures (> 3 consecutive)
2. Error rate spikes (> 5% of requests)
3. Response time degradation (> 5s average)

### Manual Rollback

```bash
# Rollback to previous version
docker-compose -f docker-compose.production.yml down
docker-compose -f docker-compose.production.yml up -d --force-recreate
```

---

## 🛡️ Security Considerations

### Best Practices Implemented
1. ✅ Secrets stored in GitHub Secrets (not in code)
2. ✅ Container images scanned for vulnerabilities
3. ✅ Network isolation between services
4. ✅ Health checks prevent unhealthy deployments
5. ✅ Environment-specific configurations
6. ✅ Database backups before production deployments

### Recommended Enhancements
- Enable Dependabot for automated security updates
- Implement container image signing
- Add SAST/DAST scanning in pipelines
- Use OIDC for cloud provider authentication

---

## 📈 Optimization Tips

### Build Time Optimization
1. Leverage Docker layer caching
2. Use multi-stage builds
3. Minimize context size
4. Parallel test execution

### Cost Optimization
1. Use spot instances for CI runners
2. Clean up old Docker images
3. Right-size container resources
4. Auto-scale based on demand

---

## 🆘 Troubleshooting

### Common Issues

**Pipeline fails at "Lint & Validate"**
```bash
# Fix formatting issues
cd ai-ml
black services/ scripts/
cd backend
npx prettier --write "src/**/*.js"
```

**Integration tests timeout**
```bash
# Increase service startup timeouts in workflow
# Check database/redis health checks
```

**Deployment fails health check**
```bash
# Check service logs
docker-compose logs -f ai-ml-service

# Verify environment variables
docker-compose config
```

---

## 📞 Support

For issues or questions:
1. Check pipeline run logs in GitHub Actions
2. Review service logs via docker-compose
3. Contact DevOps team via Slack

---

## 🎯 Next Steps

1. ✅ Configure GitHub secrets
2. ✅ Create GitHub environments (staging, production)
3. ✅ Test staging deployment
4. ✅ Verify health checks
5. ✅ Run smoke tests
6. ✅ Approve production deployment

---

**Last Updated:** March 23, 2026  
**Version:** 1.0.0
