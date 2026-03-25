# 🚀 REGIQ Integration Quick Start Guide

**Date:** March 23, 2026  
**Status:** Ready for Testing

---

## 📋 **PREREQUISITES**

Before starting, ensure you have:
- ✅ Node.js 18+ installed
- ✅ Python 3.9+ installed
- ✅ PostgreSQL 14+ running
- ✅ Redis 6+ running
- ✅ All dependencies installed

---

## 🔧 **STEP 1: START ALL SERVICES**

### **Option A: Manual Startup (Recommended for Development)**

#### **1.1 Start PostgreSQL & Redis**

```bash
# Using Docker (recommended)
cd d:\projects\apps\regiq
docker-compose up -d postgres redis

# OR using native installations
# PostgreSQL should be running on port 5432
# Redis should be running on port 6379
```

#### **1.2 Start AI/ML Service (Python FastAPI)**

```bash
cd d:\projects\apps\regiq\ai-ml

# Activate virtual environment
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Linux/Mac

# Start the service
uvicorn services.api.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

#### **1.3 Start Backend Service (Node.js Express)**

```bash
cd d:\projects\apps\regiq\backend

# Install dependencies (if not done)
npm install

# Start development server
npm run dev
```

**Expected Output:**
```
REGIQ Backend Server is running on port 3000
Connected to PostgreSQL at localhost:5432
Connected to Redis at localhost:6379
AI/ML Service configured at http://localhost:8000
```

#### **1.4 Start Frontend App (React Native Expo)**

```bash
cd d:\projects\apps\regiq\regiq

# Install dependencies (if not done)
npm install

# Start Expo development server
npm start
# or
expo start
```

**Expected Output:**
```
┌─────────────────────────────────────┐
│  Your app is running at following   │
│  URL: http://localhost:19002        │
└─────────────────────────────────────┘

› Press a │ open Android
› Press i │ open iOS simulator
› Press w │ open web browser
```

---

### **Option B: Docker Compose (All-in-One)**

```bash
cd d:\projects\apps\regiq

# Start all services with Docker
docker-compose -f docker-compose.yml up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

---

## ✅ **STEP 2: VERIFY ALL SERVICES**

### **2.1 Test AI/ML Service Health**

```bash
curl http://localhost:8000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "service": "python_ai_ml",
  "timestamp": "2026-03-23T..."
}
```

### **2.2 Test Backend Service Health**

```bash
curl http://localhost:3000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-03-23T...",
  "uptime": 123.456
}
```

### **2.3 Test CORS Configuration**

```bash
cd d:\projects\apps\regiq\backend
node test-cors-config.js
```

**Expected Output:**
```
╔════════════════════════════════════════════╗
║   REGIQ CORS Configuration Test Suite     ║
╚════════════════════════════════════════════╝

✅ Backend health check: PASSED
✅ Expo Go: PASSED (allowed)
✅ Expo Web: PASSED (allowed)
✅ React Native Metro: PASSED (allowed)
✅ Web Build: PASSED (allowed)
✅ Unauthorized Origin: PASSED (correctly blocked)

🎉 All CORS tests passed!
```

---

## 🧪 **STEP 3: TEST FRONTEND ↔ BACKEND CONNECTION**

### **3.1 Simple Connection Test**

Create a test file in your React Native app:

```javascript
// Add to regiq/src/screens/dashboard/DashboardScreen.js
import React, { useEffect, useState } from 'react';
import apiClient from '../../services/api';

const DashboardScreen = () => {
  const [connectionStatus, setConnectionStatus] = useState('Testing...');

  useEffect(() => {
    const testConnection = async () => {
      try {
        const response = await apiClient.get('/health');
        setConnectionStatus(`✅ Connected: ${response.data.status}`);
        console.log('Backend connection successful:', response.data);
      } catch (error) {
        setConnectionStatus(`❌ Error: ${error.message}`);
        console.error('Backend connection failed:', error);
      }
    };
    
    testConnection();
  }, []);

  return (
    <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
      <Text>{connectionStatus}</Text>
    </View>
  );
};

export default DashboardScreen;
```

### **3.2 Test API Endpoints**

From the frontend, try fetching real data:

```javascript
import { getRiskSimulations, getBiasReports } from '../services/apiClient';

// In your screen component
useEffect(() => {
  const loadData = async () => {
    try {
      const simulations = await getRiskSimulations();
      console.log('Loaded simulations:', simulations);
      
      const biasReports = await getBiasReports();
      console.log('Loaded bias reports:', biasReports);
    } catch (error) {
      console.error('Error loading data:', error);
    }
  };
  
  loadData();
}, []);
```

---

## 🔍 **STEP 4: DEBUGGING TOOLS**

### **Check Service Status**

```bash
# Check if ports are listening
netstat -ano | findstr :3000  # Backend
netstat -ano | findstr :8000  # AI/ML
netstat -ano | findstr :19002 # Frontend
```

### **View Logs**

```bash
# Backend logs
cd backend
npm run dev 2>&1 | tee backend.log

# AI/ML logs
cd ai-ml
uvicorn ... 2>&1 | tee aiml.log

# Frontend logs
cd regiq
npm start 2>&1 | tee frontend.log
```

### **Test Individual Endpoints**

```bash
# Test regulatory endpoint
curl http://localhost:3000/api/regulatory/regulations \
  -H "Origin: http://localhost:19000" \
  -v

# Test bias endpoint
curl http://localhost:3000/api/bias/scoring \
  -H "Origin: http://localhost:19000" \
  -v

# Test risk endpoint
curl http://localhost:3000/api/risk/simulations \
  -H "Origin: http://localhost:19000" \
  -v
```

---

## ⚠️ **COMMON ISSUES & SOLUTIONS**

### **Issue 1: CORS Error**

**Error:**
```
Access to fetch at 'http://localhost:3000' from origin 'http://localhost:19000' 
has been blocked by CORS policy
```

**Solution:**
1. Check `backend/.env` has correct `ALLOWED_ORIGINS`
2. Restart backend server
3. Clear browser/app cache

### **Issue 2: Connection Refused**

**Error:**
```
Network request failed
```

**Solution:**
```bash
# Verify backend is running
curl http://localhost:3000/health

# If not running, check logs
cd backend
npm run dev
```

### **Issue 3: Database Connection Error**

**Error:**
```
Unable to connect to database
```

**Solution:**
```bash
# Check PostgreSQL is running
docker ps | grep postgres

# Or start PostgreSQL
# Windows: pg_ctl start
# Linux: sudo systemctl start postgresql

# Test connection
psql -h localhost -U regiq_user -d regiq_backend
```

### **Issue 4: Environment Variables Not Loading**

**Error:**
```
undefined is not a valid environment variable
```

**Solution:**
1. Restart the server after changing `.env`
2. Check file encoding (should be UTF-8)
3. Verify no BOM characters in file

---

## 📊 **INTEGRATION CHECKLIST**

Use this checklist to verify everything is working:

### **Services Running**
- [ ] PostgreSQL running on port 5432
- [ ] Redis running on port 6379
- [ ] AI/ML service running on port 8000
- [ ] Backend service running on port 3000
- [ ] Frontend app running on port 19000/19002

### **Health Checks**
- [ ] `/health` endpoint responds on backend
- [ ] `/health` endpoint responds on AI/ML service
- [ ] Database connection successful
- [ ] Redis connection successful

### **CORS Configuration**
- [ ] CORS test script passes all tests
- [ ] Allowed origins configured correctly
- [ ] Preflight requests succeed
- [ ] Credentials allowed

### **Frontend Integration**
- [ ] Can connect to backend API
- [ ] Can fetch regulations data
- [ ] Can fetch bias analysis data
- [ ] Can fetch risk simulation data
- [ ] Can generate reports

### **Data Flow**
- [ ] Frontend → Backend → Database ✅
- [ ] Frontend → Backend → AI/ML ✅
- [ ] AI/ML → Database ✅
- [ ] Backend → Frontend ✅

---

## 🎯 **NEXT STEPS AFTER INTEGRATION**

Once integration is verified:

1. **Load Real Data in Screens**
   - Update dashboard with live metrics
   - Display regulation list
   - Show bias analysis results

2. **Implement User Authentication**
   - Login/logout flows
   - Token refresh
   - Protected routes

3. **Add Error Handling**
   - Network errors
   - API errors
   - Offline mode

4. **Performance Optimization**
   - Implement caching
   - Optimize API calls
   - Add loading states

---

## 📞 **SUPPORT**

If you encounter issues:

1. Check logs for error messages
2. Run the CORS test script
3. Verify all services are running
4. Check network connectivity
5. Review environment configuration

**Documentation:**
- Full Guide: `docs/ENVIRONMENT_CONFIGURATION_GUIDE.md`
- CORS Details: `backend/src/server.js` (lines 14-68)
- Frontend Config: `regiq/src/services/api.js`

---

**Last Updated:** March 23, 2026  
**Ready to integrate!** 🚀
