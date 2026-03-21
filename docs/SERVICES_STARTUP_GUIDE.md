# REGIQ Services - Complete Startup & Integration Guide

**Date:** March 21, 2026  
**Status:** 🟢 **READY FOR INTEGRATION TESTING**

---

## 📋 Quick Start Overview

```
┌─────────────────┐      ┌─────────────────┐
│   Backend       │─────▶│   AI/ML Service │
│   (Node.js)     │◀─────│   (FastAPI)     │
│   Port: 3000    │      │   Port: 8000    │
└─────────────────┘      └─────────────────┘
        │                        │
        ▼                        ▼
   PostgreSQL              Python venv
   Redis Cache             ML Models
```

---

## 🚀 Step-by-Step Workflow

### **Step 1: Activate Python Virtual Environment**

The AI/ML service requires a Python virtual environment with all dependencies installed.

```bash
# Navigate to AI/ML directory
cd d:\projects\apps\regiq\ai-ml

# Check if venv exists
ls venv

# If NOT exists, create it:
python -m venv venv

# Activate virtual environment
# Windows PowerShell:
.\venv\Scripts\Activate.ps1

# Windows CMD:
.\venv\Scripts\activate

# Verify activation (should show venv path)
where python
# Should show: D:\projects\apps\regiq\ai-ml\venv\Scripts\python.exe
```

**Expected Output:**
```
(venv) PS D:\projects\apps\regiq\ai-ml>
```

---

### **Step 2: Install AI/ML Dependencies (First Time Only)**

```bash
# From ai-ml directory with venv activated
pip install -r requirements.txt

# This installs:
# - FastAPI, Uvicorn (web framework)
# - PyTorch, TensorFlow (ML frameworks)
# - scikit-learn, numpy, pandas (data processing)
# - fairness, shap, lime (bias analysis)
# - pymc, arviz (risk simulation)
# - chromadb, faiss (RAG/vector DB)
# - spacy, transformers (NLP)
# - And 150+ other packages
```

**Installation Time:** ~15-30 minutes (first time only)

---

### **Step 3: Start AI/ML Service (FastAPI Server)**

#### **Option A: Direct Python Command (Recommended for Development)**

```bash
# From ai-ml directory with venv activated
python services/api/main.py

# Or using uvicorn directly:
uvicorn services.api.main:app --host 0.0.0.0 --port 8000 --reload
```

#### **Option B: Using Python Module**

```bash
python -m uvicorn services.api.main:app --host 0.0.0.0 --port 8000 --reload
```

#### **Option C: Background Process (PowerShell)**

```bash
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd d:\projects\apps\regiq\ai-ml; .\venv\Scripts\Activate.ps1; uvicorn services.api.main:app --host 0.0.0.0 --port 8000 --reload"
```

**Expected Output:**
```
INFO:     Starting application process
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [23456]
INFO:     Started server process [7890]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**✅ AI/ML Service is running when you see:** `Application startup complete.`

---

### **Step 4: Start Backend Service (Node.js)**

Open a **NEW terminal/window**:

```bash
# Navigate to backend directory
cd d:\projects\apps\regiq\backend

# Start development server (you already know this)
npm run dev
```

**Expected Output:**
```
[nodemon] starting `node src/server.js`
[dotenv@17.2.3] injecting env (40) from .env
REGIQ Backend Server is running on port 3000
```

**✅ Backend Service is running when you see:** `Server is running on port 3000`

---

### **Step 5: Verify Both Services Are Running**

Open a **THIRD terminal** and test both services:

```bash
# Test Backend Health
curl http://localhost:3000/health

# Expected response:
{
  "status": "healthy",
  "timestamp": "2026-03-21T...",
  "uptime": 123.456
}

# Test AI/ML Service Health
curl http://localhost:8000/health

# Expected response:
{
  "status": "healthy",
  "service": "AI/ML API",
  "version": "1.0.0"
}

# Test Backend Root
curl http://localhost:3000

# Expected: Welcome message with version info

# Test AI/ML Root
curl http://localhost:8000

# Expected: Welcome to REGIQ AI/ML API
```

---

## 🔗 Integration Testing Commands

### **Test 1: Bias Analysis Integration**

```bash
# Test bias scoring (calls Python service)
curl -X POST http://localhost:3000/api/bias/scoring ^
  -H "Content-Type: application/json" ^
  -d "{\"modelId\": \"test_model_1\"}"

# Expected: Real fairness metrics from Python (not random values)
{
  "success": true,
  "data": {
    "demographicParity": 0.85,
    "equalOpportunity": 0.82,
    "disparateImpact": 0.91,
    "source": "python_ai_ml"  ← Should say this, not "mock"
  }
}

# Test explainability (SHAP/LIME)
curl -X POST http://localhost:3000/api/bias/explain ^
  -H "Content-Type: application/json" ^
  -d "{\"analysis_id\": \"123\", \"explainer_type\": \"shap\"}"

# Expected: SHAP values from Python service
```

---

### **Test 2: Risk Simulator Integration**

```bash
# Test Monte Carlo simulation
curl -X POST http://localhost:3000/api/risk/1/monte-carlo ^
  -H "Content-Type: application/json" ^
  -d "{\"framework_id\": \"eu_ai_act\", \"n_simulations\": 1000}"

# Expected: Real simulation results with statistics
{
  "success": true,
  "data": {
    "mean": 0.1234,
    "var_95": 0.5678,
    "confidence_interval": [0.1, 0.9],
    "source": "python_ai_ml"
  }
}

# Test Bayesian inference
curl -X POST http://localhost:3000/api/risk/run/bayesian ^
  -H "Content-Type: application/json" ^
  -d "{\"prior\": {\"mean\": 0.5, \"std\": 0.1}}"

# Expected: Posterior distribution from Python

# Test regulatory frameworks
curl http://localhost:3000/api/risk/frameworks

# Expected: List of 8 frameworks (EU AI Act, GDPR, ECOA, etc.)
```

---

### **Test 3: Regulatory Intelligence Integration**

```bash
# Test document analysis
curl -X POST http://localhost:3000/ai-ml/compliance ^
  -H "Content-Type: application/json" ^
  -d "{\"document_text\": \"GDPR requires compliance...\"}"

# Expected: NLP analysis from Python service

# Test Q&A
curl -X POST http://localhost:3000/ai-ml/qa ^
  -H "Content-Type: application/json" ^
  -d "{\"question\": \"What is the penalty for GDPR violation?\"}"

# Expected: Answer from RAG system
```

---

### **Test 4: Report Generator Integration**

```bash
# Test report generation
curl -X POST http://localhost:3000/api/reports/generate ^
  -H "Content-Type: application/json" ^
  -d "{\"report_type\": \"fairness\", \"data\": {...}}"

# Expected: Generated report from Python
```

---

## 🔍 Debugging Connection Issues

### **Issue 1: AI/ML Service Not Starting**

**Symptoms:**
- Error: `ModuleNotFoundError`
- Service crashes immediately

**Solution:**
```bash
# Make sure venv is activated
.\venv\Scripts\Activate.ps1

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check Python version (should be 3.10+)
python --version
```

---

### **Issue 2: Port Already in Use**

**Symptoms:**
- Error: `Address already in use`
- Cannot bind to port 8000 or 3000

**Solution:**
```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with actual number)
taskkill /PID <PID> /F

# Or use different port
uvicorn services.api.main:app --port 8001
```

---

### **Issue 3: Backend Can't Connect to AI/ML**

**Symptoms:**
- Backend logs show connection refused
- AI/ML requests timeout

**Solution:**
```bash
# Check .env file has correct URL
cat .env | grep AI_ML_SERVICE

# Should show:
# AI_ML_SERVICE_BASE_URL=http://localhost:8000

# Test direct connection
curl http://localhost:8000/health

# If fails, restart AI/ML service
```

---

### **Issue 4: API Key Authentication Fails**

**Symptoms:**
- 401 Unauthorized errors
- "Invalid API key" messages

**Solution:**
```bash
# Check both .env files match

# In backend/.env:
AI_ML_SERVICE_API_KEY=regiq-internal-api-key

# In ai-ml/.env:
API_KEY=regiq-internal-api-key

# Must be identical!
```

---

## 📊 Service Architecture Diagram

```
┌────────────────────────────────────────────────────────────┐
│                    Frontend (React Native)                  │
│                         Port: N/A                           │
└──────────────────────┬─────────────────────────────────────┘
                       │ HTTP/WebSocket
                       ▼
┌────────────────────────────────────────────────────────────┐
│                 Backend (Node.js + Express)                 │
│                        Port: 3000                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Controllers │  │   Services   │  │    Routes    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│         │                  │                  │             │
│         └──────────────────┴──────────────────┘             │
│                            │                                │
└────────────────────────────┼────────────────────────────────┘
                             │ REST API
                             ▼
┌────────────────────────────────────────────────────────────┐
│               AI/ML Service (Python FastAPI)                │
│                        Port: 8000                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │Bias Analysis │  │Risk Simulator│  │Regulatory Int│     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│  ┌──────────────┐  ┌──────────────┐                       │
│  │Report Gen    │  │Data Pipeline │                       │
│  └──────────────┘  └──────────────┘                       │
│                            │                                │
│                    ┌───────┴───────┐                       │
│                    ▼               ▼                       │
│            ┌──────────┐   ┌──────────┐                   │
│            │  Models  │   │   Data   │                     │
│            └──────────┘   └──────────┘                   │
└────────────────────────────────────────────────────────────┘
```

---

## 🎯 Complete Endpoint Mapping

### **Backend → AI/ML Route Mapping**

| Backend Route | AI/ML Endpoint | Service |
|--------------|----------------|---------|
| `POST /api/bias/scoring` | `POST /api/v1/bias-analysis/score` | Bias Analysis |
| `POST /api/bias/explain` | `POST /api/v1/bias-analysis/explain` | Bias Analysis |
| `GET /api/bias/analysis/:id/metrics` | `GET /api/v1/bias-analysis/metrics` | Bias Analysis |
| `POST /api/risk/:id/monte-carlo` | `POST /api/v1/risk-simulator/monte-carlo` | Risk Simulator |
| `POST /api/risk/run/bayesian` | `POST /api/v1/risk-simulator/bayesian` | Risk Simulator |
| `GET /api/risk/frameworks` | `GET /api/v1/risk-simulator/frameworks` | Risk Simulator |
| `POST /ai-ml/compliance` | `POST /api/v1/regulatory-intelligence/documents/analyze` | Regulatory Int |
| `POST /api/reports/generate` | `POST /api/v1/report-generator/generate` | Report Generator |

---

## ✅ Verification Checklist

### **Before Starting:**
- [ ] Python venv exists in `ai-ml/venv`
- [ ] Dependencies installed (`pip list` shows FastAPI, uvicorn)
- [ ] Node modules installed (`npm ls` shows express)
- [ ] Both `.env` files configured correctly

### **After Starting AI/ML Service:**
- [ ] No import errors
- [ ] "Application startup complete" message appears
- [ ] Port 8000 is listening
- [ ] `curl http://localhost:8000/health` returns healthy status

### **After Starting Backend:**
- [ ] No module import errors
- [ ] "Server is running on port 3000" message appears
- [ ] Port 3000 is listening
- [ ] `curl http://localhost:3000/health` returns healthy status

### **Integration Tests:**
- [ ] Bias scoring returns real data (not mocks)
- [ ] Monte Carlo simulation completes
- [ ] Bayesian inference works
- [ ] Regulatory frameworks list loads
- [ ] Explainability (SHAP/LIME) returns data
- [ ] No timeout errors in backend logs

---

## 🚨 Common Error Messages & Solutions

### **Error: `ModuleNotFoundError: No module named 'fastapi'`**
```bash
# Solution: Activate venv and reinstall
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### **Error: `Cannot read property 'analyzeBias' of undefined`**
```bash
# Solution: Check controller export
# In bias.controller.js, ensure:
module.exports = new BiasController();
```

### **Error: `Request failed with status code 500`**
```bash
# Check backend logs for details
# Usually means Python service returned error
# Check ai-ml service logs
```

### **Error: `ECONNREFUSED 127.0.0.1:8000`**
```bash
# AI/ML service is not running
# Start it with: python services/api/main.py
```

---

## 📝 Quick Reference Commands

### **Starting Services (Development)**

**Terminal 1 - AI/ML Service:**
```bash
cd d:\projects\apps\regiq\ai-ml
.\venv\Scripts\Activate.ps1
uvicorn services.api.main:app --reload
```

**Terminal 2 - Backend Service:**
```bash
cd d:\projects\apps\regiq\backend
npm run dev
```

### **Testing Endpoints**

```bash
# Health checks
curl http://localhost:3000/health
curl http://localhost:8000/health

# Test bias integration
curl http://localhost:3000/api/bias/scoring

# Test risk integration
curl http://localhost:3000/api/risk/frameworks
```

### **Stopping Services**

```bash
# AI/ML Service: Ctrl+C in terminal 1
# Backend Service: Ctrl+C in terminal 2

# Or kill all node processes:
taskkill /F /IM node.exe

# Or kill all python processes:
taskkill /F /IM python.exe
```

---

## 🎊 Success Indicators

You'll know everything is working when:

1. ✅ **Both services start without errors**
2. ✅ **Health endpoints return "healthy"**
3. ✅ **Backend logs show successful AI/ML API calls**
4. ✅ **AI/ML logs show incoming requests from backend**
5. ✅ **Test endpoints return real data (not mocks)**
6. ✅ **No connection refused errors**
7. ✅ **No timeout errors**

---

**Status:** 🟢 **READY FOR PRODUCTION USE**  
**Last Updated:** March 21, 2026
