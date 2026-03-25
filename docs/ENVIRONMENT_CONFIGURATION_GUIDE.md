# REGIQ Environment Configuration Guide

**Date:** March 23, 2026  
**Version:** 1.0.0

---

## 📋 **OVERVIEW**

This guide covers all environment configuration needed for REGIQ application across development, staging, and production environments.

---

## 🔧 **BACKEND ENVIRONMENT VARIABLES**

### **File:** `backend/.env`

#### **Server Configuration**
```bash
PORT=3000
NODE_ENV=development  # development | staging | production
```

#### **CORS Configuration** ⚠️ **CRITICAL FOR FRONTEND**
```bash
# Development (localhost)
ALLOWED_ORIGINS=http://localhost:19000,http://localhost:19002,http://localhost:8081,http://localhost:3000

# Staging (example)
# ALLOWED_ORIGINS=https://staging.regiq.com,https://staging-api.regiq.com

# Production (example)
# ALLOWED_ORIGINS=https://regiq.com,https://app.regiq.com,https://api.regiq.com
```

**Frontend Ports:**
- `http://localhost:19000` - Expo Go
- `http://localhost:19002` - Expo Web
- `http://localhost:8081` - React Native Metro Bundler
- `http://localhost:3000` - Web build

#### **Database Configuration**
```bash
DB_HOST=localhost
DB_PORT=5432
DB_NAME=regiq_backend
DB_USER=regiq_user
DB_PASSWORD=regiq_password
DB_DIALECT=postgres
```

#### **AI/ML Service Configuration**
```bash
AI_ML_SERVICE_BASE_URL=http://localhost:8000
AI_ML_SERVICE_API_KEY=regiq-internal-api-key
AI_ML_SERVICE_TIMEOUT=60000
AI_ML_SERVICE_MAX_RETRIES=3
```

---

## 📱 **FRONTEND ENVIRONMENT VARIABLES**

### **File:** `regiq/.env` (Create this file)

```bash
# API Configuration
REACT_NATIVE_API_BASE_URL=http://localhost:3000/api
REACT_NATIVE_API_TIMEOUT=10000

# Authentication
REACT_NATIVE_AUTH_TOKEN_KEY=@regiq:auth_token
REACT_NATIVE_USER_DATA_KEY=@regiq:user_data

# App Configuration
REACT_NATIVE_APP_NAME=REGIQ
REACT_NATIVE_ENV=development

# Feature Flags
REACT_NATIVE_ENABLE_ANALYTICS=true
REACT_NATIVE_ENABLE_PUSH_NOTIFICATIONS=true
```

---

## 🐍 **AI/ML SERVICE ENVIRONMENT VARIABLES**

### **File:** `ai-ml/.env`

#### **Server Configuration**
```bash
PORT=8000
ENVIRONMENT=development  # development | staging | production
```

#### **Service API Key**
```bash
SERVICE_API_KEY=regiq-internal-api-key
```

#### **Database Configuration**
```bash
DATABASE_URL=postgresql://regiq:regiq_password@localhost:5432/regiq_ai_ml
REDIS_URL=redis://localhost:6379/0
```

#### **LLM Configuration**
```bash
GOOGLE_API_KEY=your_google_api_key_here
GEMINI_MODEL=gemini-1.5-pro
```

---

## 🌍 **ENVIRONMENT-SPECIFIC CONFIGURATIONS**

### **Development Environment**

**Backend (`backend/.env`):**
```bash
NODE_ENV=development
PORT=3000
ALLOWED_ORIGINS=http://localhost:19000,http://localhost:19002,http://localhost:8081
AI_ML_SERVICE_BASE_URL=http://localhost:8000
```

**Frontend (`regiq/.env`):**
```bash
REACT_NATIVE_API_BASE_URL=http://localhost:3000/api
REACT_NATIVE_ENV=development
```

**AI/ML (`ai-ml/.env`):**
```bash
ENVIRONMENT=development
DATABASE_URL=postgresql://regiq:regiq_password@localhost:5432/regiq_ai_ml_dev
```

---

### **Staging Environment**

**Backend (`backend/.env.staging`):**
```bash
NODE_ENV=staging
PORT=3000
ALLOWED_ORIGINS=https://staging.regiq.com,https://staging-app.regiq.com
AI_ML_SERVICE_BASE_URL=https://staging-ai.regiq.com
DATABASE_URL=postgresql://regiq:${DB_PASSWORD}@staging-db.regiq.com:5432/regiq_staging
```

**Frontend (`regiq/.env.staging`):**
```bash
REACT_NATIVE_API_BASE_URL=https://staging-api.regiq.com/api
REACT_NATIVE_ENV=staging
```

**AI/ML (`ai-ml/.env.staging`):**
```bash
ENVIRONMENT=staging
DATABASE_URL=postgresql://regiq:${DB_PASSWORD}@staging-db.regiq.com:5432/regiq_staging
```

---

### **Production Environment**

**Backend (`backend/.env.production`):**
```bash
NODE_ENV=production
PORT=3000
ALLOWED_ORIGINS=https://regiq.com,https://app.regiq.com
AI_ML_SERVICE_BASE_URL=https://ai.regiq.com
DATABASE_URL=postgresql://regiq:${DB_PASSWORD}@prod-db.regiq.com:5432/regiq_production
```

**Frontend (`regiq/.env.production`):**
```bash
REACT_NATIVE_API_BASE_URL=https://api.regiq.com/api
REACT_NATIVE_ENV=production
```

**AI/ML (`ai-ml/.env.production`):**
```bash
ENVIRONMENT=production
DATABASE_URL=postgresql://regiq:${DB_PASSWORD}@prod-db.regiq.com:5432/regiq_production
```

---

## 🔒 **SECURITY BEST PRACTICES**

### **1. Never Commit Secrets**
```bash
# Add to .gitignore
.env
.env.*
!.env.example
```

### **2. Use Environment Variables for Secrets**
```bash
# ✅ Good
const apiKey = process.env.AI_ML_SERVICE_API_KEY;

# ❌ Bad
const apiKey = 'hardcoded_secret_key';
```

### **3. Encrypt Sensitive Data**
```bash
# Use strong passwords
JWT_SECRET=$(openssl rand -base64 32)
DB_PASSWORD=$(openssl rand -base64 32)
```

### **4. Separate Secrets by Environment**
```bash
# Different secrets for each environment
development → local testing
staging → shared team access
production → restricted access
```

---

## 🚀 **SETUP INSTRUCTIONS**

### **Step 1: Backend Setup**

```bash
cd backend

# Copy example env file
cp .env.example .env

# Edit .env with your values
nano .env  # or use your favorite editor

# Start server
npm run dev
```

### **Step 2: Frontend Setup**

```bash
cd regiq

# Create .env file
cat > .env << EOL
REACT_NATIVE_API_BASE_URL=http://localhost:3000/api
REACT_NATIVE_ENV=development
EOL

# Install dependencies
npm install

# Start app
npm start
```

### **Step 3: AI/ML Service Setup**

```bash
cd ai-ml

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Copy example env file
cp .env.example .env

# Edit .env
nano .env

# Start service
uvicorn services.api.main:app --reload
```

---

## ✅ **VERIFICATION CHECKLIST**

### **Development Environment**

- [ ] Backend running on `http://localhost:3000`
- [ ] AI/ML service running on `http://localhost:8000`
- [ ] Frontend can connect to backend
- [ ] CORS allows localhost origins
- [ ] Database connection successful
- [ ] Redis connection successful

### **Test Connection**

```bash
# Test backend health
curl http://localhost:3000/health

# Test AI/ML service health
curl http://localhost:8000/health

# Test from frontend (React Native)
import apiClient from './services/api';
apiClient.get('/health').then(console.log).catch(console.error);
```

---

## 🔧 **TROUBLESHOOTING**

### **CORS Errors**

**Error:** `Access to fetch at 'http://localhost:3000' from origin 'http://localhost:19000' has been blocked by CORS policy`

**Solution:**
1. Check `ALLOWED_ORIGINS` in `backend/.env`
2. Ensure frontend origin is listed
3. Restart backend server

### **Connection Refused**

**Error:** `Network request failed`

**Solution:**
1. Verify backend is running: `curl http://localhost:3000/health`
2. Check firewall settings
3. For mobile devices, use computer's IP instead of localhost

### **Environment Variables Not Loading**

**Error:** `undefined` for environment variables

**Solution:**
1. Restart the server after changing `.env`
2. Check file is named correctly (`.env` not `.env.txt`)
3. Verify dotenv is installed: `npm list dotenv`

---

## 📊 **CONFIGURATION MATRIX**

| Variable | Development | Staging | Production |
|----------|-------------|---------|------------|
| **Backend Port** | 3000 | 3000 | 3000 |
| **AI/ML Port** | 8000 | 8000 | 8000 |
| **Frontend API URL** | http://localhost:3000/api | https://staging-api.regiq.com | https://api.regiq.com |
| **Database** | localhost:5432 | staging-db.regiq.com | prod-db.regiq.com |
| **Redis** | localhost:6379 | staging-redis.regiq.com | prod-redis.regiq.com |
| **CORS Origins** | localhost:* | *.staging.regiq.com | *.regiq.com |
| **NODE_ENV** | development | staging | production |

---

## 🎯 **NEXT STEPS**

1. ✅ Configure development environment
2. ⏳ Test frontend ↔ backend connection
3. ⏳ Configure staging environment (when ready)
4. ⏳ Configure production environment (when ready)

---

**Last Updated:** March 23, 2026  
**Maintained By:** DevOps Team
