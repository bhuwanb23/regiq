# 🔄 REGIQ Integration Guide

This guide provides detailed instructions for integrating the three core components of the REGIQ platform:
1. **Frontend** (React Native Mobile App)
2. **Backend** (Node.js API Gateway + FastAPI Services)
3. **AI/ML Engine** (Python-based AI Services)

## 🏗️ Architecture Overview

```mermaid
graph TB
    A[📱 React Native App] --> B[⚡ Node.js API Gateway]
    B --> C[🐍 FastAPI Backend]
    C --> D[🤖 AI/ML Services]
    C --> E[(PostgreSQL)]
    D --> F[🧠 Google Gemini AI]
    B --> G[(Redis Cache)]
    
    style A fill:#61DAFB,stroke:#20232A,color:#fff
    style B fill:#68D391,stroke:#38A169,color:#fff
    style C fill:#009688,stroke:#004D40,color:#fff
    style D fill:#FF6B6B,stroke:#C92A2A,color:#fff
    style F fill:#4285F4,stroke:#1565C0,color:#fff
```

## 📁 Project Structure

```
regiq/
├── regiq/                 # React Native Frontend
│   ├── src/
│   │   ├── components/    # UI Components
│   │   ├── screens/       # App Screens
│   │   ├── hooks/         # Custom Hooks
│   │   └── navigation/    # App Navigation
│   └── package.json
│
├── backend/               # Node.js + FastAPI Backend
│   ├── src/
│   │   ├── controllers/   # Request Handlers
│   │   ├── routes/        # API Endpoints
│   │   ├── services/      # Business Logic
│   │   ├── models/        # Database Models
│   │   └── config/        # Configuration
│   ├── services/          # FastAPI Services
│   │   ├── api/           # API Layer
│   │   ├── regulatory_intelligence/
│   │   ├── bias_analysis/
│   │   ├── risk_simulator/
│   │   └── report_generator/
│   └── package.json
│
├── ai-ml/                 # AI/ML Engine
│   ├── services/
│   │   ├── api/           # FastAPI Layer
│   │   ├── regulatory_intelligence/
│   │   ├── bias_analysis/
│   │   ├── risk_simulator/
│   │   └── report_generator/
│   ├── models/            # ML Models
│   └── requirements.txt
│
├── docker-compose.yml     # Production Setup
└── docker-compose.dev.yml # Development Setup
```

## 🔗 Component Integration

### 1. Frontend ↔ Backend Communication

The React Native frontend communicates with the Node.js API Gateway through RESTful APIs.

**Base URLs:**
- Development: `http://localhost:3000`
- Production: `https://api.yourdomain.com`

**Example API Calls:**
```javascript
// Fetch regulations
const response = await fetch('/api/regulations', {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  }
});

// Create a new regulation
const response = await fetch('/api/regulations', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    title: 'New Regulation',
    description: 'Regulation details...'
  })
});
```

### 2. Backend ↔ AI/ML Communication

The Node.js backend communicates with the FastAPI-based AI/ML services through internal API calls.

**Configuration:**
- AI/ML Service URL: `http://localhost:8000` (development) or `http://fastapi-backend:8000` (Docker)
- Authentication: Bearer token in headers

**Service Integration Example:**
```javascript
// ai-ml.service.js
const axios = require('axios');

class AIClient {
  constructor() {
    this.baseUrl = process.env.AI_ML_SERVICE_BASE_URL || 'http://localhost:8000';
    this.client = axios.create({
      baseURL: this.baseUrl,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${process.env.AI_ML_SERVICE_API_KEY}`
      }
    });
  }

  async analyzeCompliance(data) {
    const response = await this.client.post('/api/v1/regulatory-intelligence/documents/analyze', data);
    return response.data;
  }
}
```

### 3. AI/ML Services Architecture

The AI/ML engine consists of four core services:

1. **Regulatory Intelligence** - Parses and analyzes regulatory documents
2. **Bias Analysis** - Evaluates AI models for fairness and bias
3. **Risk Simulator** - Predicts compliance risks using Monte Carlo simulations
4. **Report Generator** - Creates comprehensive compliance reports

**API Endpoints:**
```http
# Regulatory Intelligence
POST /api/v1/regulatory-intelligence/documents/analyze
POST /api/v1/regulatory-intelligence/summarize
POST /api/v1/regulatory-intelligence/qa
POST /api/v1/regulatory-intelligence/search

# Bias Analysis
POST /api/v1/bias/analyze
GET  /api/v1/bias/report/{model_id}
POST /api/v1/bias/mitigation

# Risk Simulation
POST /api/v1/risk/simulate
GET  /api/v1/risk/scenarios
POST /api/v1/risk/stress-test

# Report Generation
POST /api/v1/reports/generate
GET  /api/v1/reports/{report_id}
POST /api/v1/reports/schedule
```

## 🐳 Docker Integration

### Production Setup (`docker-compose.yml`)

```yaml
version: '3.8'

services:
  # PostgreSQL Database
  postgres:
    image: postgres:14
    environment:
      POSTGRES_DB: regiq
      POSTGRES_USER: regiq_user
      POSTGRES_PASSWORD: regiq_password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  # Redis Cache
  redis:
    image: redis:6-alpine

  # Node.js API Gateway
  api-gateway:
    build:
      context: ./backend
      dockerfile: Dockerfile.node
    environment:
      - DATABASE_URL=postgresql://regiq_user:regiq_password@postgres:5432/regiq
      - REDIS_URL=redis://redis:6379
      - FASTAPI_URL=http://fastapi-backend:8000
    depends_on:
      - postgres
      - redis

  # FastAPI Backend
  fastapi-backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.python
    environment:
      - DATABASE_URL=postgresql://regiq_user:regiq_password@postgres:5432/regiq
      - REDIS_URL=redis://redis:6379
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
    depends_on:
      - postgres
      - redis

  # AI/ML Services
  ai-ml-services:
    build:
      context: ./ai-ml
      dockerfile: Dockerfile
    environment:
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
      - FASTAPI_URL=http://fastapi-backend:8000
    depends_on:
      - fastapi-backend
```

### Development Setup (`docker-compose.dev.yml`)

The development setup includes additional tools:
- **pgAdmin** - PostgreSQL administration interface
- **Redis Commander** - Redis cache management interface

## ▶️ Running the Integrated System

### Option 1: Docker Deployment (Recommended)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-org/regiq.git
   cd regiq
   ```

2. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configurations
   ```

3. **Start all services:**
   ```bash
   # Production environment
   docker-compose up -d
   
   # Development environment (includes pgAdmin and Redis Commander)
   docker-compose -f docker-compose.dev.yml up -d
   ```

4. **Access the services:**
   - Frontend: `http://localhost:19000` (Expo DevTools)
   - API Gateway: `http://localhost:3000`
   - FastAPI Backend: `http://localhost:8000`
   - AI/ML Services: `http://localhost:8001`
   - pgAdmin: `http://localhost:5050`
   - Redis Commander: `http://localhost:8081`

### Option 2: Manual Setup

#### Frontend (React Native)
```bash
cd regiq
npm install
npx expo start
```

#### Backend (Node.js + FastAPI)
```bash
cd backend

# Install Node.js dependencies
npm install

# Install Python dependencies
pip install -r requirements.txt

# Start Node.js API Gateway
npm run dev

# Start FastAPI services
uvicorn services.api.main:app --host 0.0.0.0 --port 8000 --reload
```

#### AI/ML Engine
```bash
cd ai-ml
pip install -r requirements.txt
python -m services.api.main
```

## 🔧 Configuration

### Environment Variables

**Backend (.env):**
```bash
# Database
DATABASE_URL=postgresql://regiq_user:regiq_password@localhost:5432/regiq

# Redis
REDIS_URL=redis://localhost:6379

# AI/ML Service
AI_ML_SERVICE_BASE_URL=http://localhost:8000
AI_ML_SERVICE_API_KEY=your_api_key_here

# JWT
JWT_SECRET=your_jwt_secret_here
JWT_EXPIRES_IN=24h
```

**AI/ML (.env):**
```bash
# Google API
GOOGLE_API_KEY=your_google_api_key_here

# Database
DATABASE_URL=postgresql://regiq_user:regiq_password@localhost:5432/regiq

# Redis
REDIS_URL=redis://localhost:6379
```

## 🧪 Testing Integration

### Health Checks

1. **API Gateway Health:**
   ```bash
   curl http://localhost:3000/health
   ```

2. **FastAPI Backend Health:**
   ```bash
   curl http://localhost:8000/health
   ```

3. **AI/ML Services Health:**
   ```bash
   curl http://localhost:8001/health
   ```

### API Testing

1. **Test Backend ↔ AI/ML Integration:**
   ```bash
   # Test regulatory intelligence endpoint
   curl -X POST http://localhost:8000/api/v1/regulatory-intelligence/documents/analyze \
     -H "Content-Type: application/json" \
     -d '{"document_type": "regulation", "content": "Sample regulation content"}'
   ```

2. **Test Frontend ↔ Backend Integration:**
   ```bash
   # Test regulations endpoint
   curl -X GET http://localhost:3000/api/regulations \
     -H "Authorization: Bearer your_token_here"
   ```

## 🚀 Deployment

### Production Deployment

1. **Build Docker Images:**
   ```bash
   docker-compose build
   ```

2. **Deploy to Production:**
   ```bash
   docker-compose up -d
   ```

### Cloud Deployment Options

#### AWS ECS
```bash
# Create cluster
aws ecs create-cluster --cluster-name regiq-production

# Deploy services using task definitions
aws ecs run-task --cluster regiq-production --task-definition regiq-task
```

#### Google Cloud Run
```bash
# Deploy each service separately
gcloud run deploy regiq-api-gateway --source ./backend
gcloud run deploy regiq-ai-ml --source ./ai-ml
```

#### Azure Container Instances
```bash
# Deploy services
az container create --resource-group regiq --name api-gateway --image your-registry/regiq-api-gateway
az container create --resource-group regiq --name ai-ml-services --image your-registry/regiq-ai-ml
```

## 📈 Monitoring & Observability

### Logging
- **Application Logs**: Winston (Node.js), Python logging (FastAPI)
- **Structured Logging**: JSON format for easy parsing
- **Log Levels**: DEBUG, INFO, WARN, ERROR

### Metrics
- **API Performance**: Response times, throughput
- **AI/ML Performance**: Processing times, accuracy metrics
- **System Health**: CPU, memory, disk usage

### Alerting
- **Service Downtime**: Immediate notifications
- **Performance Degradation**: Threshold-based alerts
- **Error Rates**: Anomaly detection for error spikes

## 🔒 Security Considerations

### Authentication
- **JWT Tokens**: Secure authentication between services
- **API Keys**: Service-to-service authentication
- **OAuth 2.0**: User authentication for frontend

### Data Protection
- **Encryption**: TLS for data in transit
- **Database**: Encrypted storage for sensitive data
- **PII Handling**: GDPR-compliant data processing

### Rate Limiting
- **API Rate Limits**: Prevent abuse and DDoS attacks
- **Quotas**: Fair usage policies for services
- **Throttling**: Adaptive rate limiting based on load

## 🆘 Troubleshooting

### Common Issues

1. **Services Not Communicating:**
   - Check Docker network connectivity
   - Verify service URLs in environment variables
   - Ensure ports are properly exposed

2. **Database Connection Issues:**
   - Verify database credentials
   - Check PostgreSQL service status
   - Ensure database migrations are applied

3. **AI/ML Service Failures:**
   - Check Google API key validity
   - Verify model dependencies are installed
   - Monitor resource usage (CPU/memory)

### Debugging Commands

```bash
# Check running containers
docker ps

# View service logs
docker-compose logs api-gateway
docker-compose logs fastapi-backend
docker-compose logs ai-ml-services

# Check network connectivity between services
docker-compose exec api-gateway ping fastapi-backend
docker-compose exec fastapi-backend ping ai-ml-services

# Restart specific services
docker-compose restart api-gateway
```

## 📚 Additional Resources

- [API Documentation](http://localhost:3000/docs) - Auto-generated API docs
- [AI/ML Documentation](http://localhost:8001/docs) - AI service API docs
- [Database Schema](./docs/database-schema.md) - Entity relationship diagrams
- [Deployment Guide](./docs/deployment.md) - Detailed deployment instructions
- [Troubleshooting Guide](./docs/troubleshooting.md) - Common issues and solutions