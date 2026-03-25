# 🚀 REGIQ Quick Reference Card

**For:** Frontend ↔ Backend Integration  
**Date:** March 23, 2026

---

## ⚡ START ALL SERVICES (Quick Commands)

### **Terminal 1 - AI/ML Service**
```bash
cd d:\projects\apps\regiq\ai-ml
venv\Scripts\activate
uvicorn services.api.main:app --reload --host 0.0.0.0 --port 8000
```

### **Terminal 2 - Backend**
```bash
cd d:\projects\apps\regiq\backend
npm run dev
```

### **Terminal 3 - Frontend**
```bash
cd d:\projects\apps\regiq\regiq
npm start
```

---

## ✅ VERIFICATION CHECKLIST

Run these tests in order:

### **1. Health Checks**
```bash
# AI/ML Service
curl http://localhost:8000/health

# Backend Service
curl http://localhost:3000/health
```

### **2. CORS Test**
```bash
cd backend
node test-cors-config.js
```

### **3. Frontend Connection**
In React Native app console:
```javascript
import apiClient from './services/api';
apiClient.get('/health')
  .then(res => console.log('✅ Connected:', res.data))
  .catch(err => console.error('❌ Error:', err));
```

---

## 🔧 ENVIRONMENT FILES

### **Backend `.env`**
```bash
PORT=3000
NODE_ENV=development
ALLOWED_ORIGINS=http://localhost:19000,http://localhost:19002,http://localhost:8081
AI_ML_SERVICE_BASE_URL=http://localhost:8000
DATABASE_URL=postgresql://regiq_user:regiq_password@localhost:5432/regiq_backend
REDIS_URL=redis://localhost:6379/0
```

### **Frontend `.env`**
```bash
REACT_NATIVE_API_BASE_URL=http://localhost:3000/api
REACT_NATIVE_API_TIMEOUT=10000
REACT_NATIVE_ENV=development
```

---

## 📊 SERVICE STATUS

| Service | URL | Port | Status Endpoint |
|---------|-----|------|-----------------|
| Frontend | http://localhost:19002 | 19002 | N/A |
| Backend | http://localhost:3000 | 3000 | `/health` |
| AI/ML | http://localhost:8000 | 8000 | `/health` |
| PostgreSQL | localhost | 5432 | N/A |
| Redis | localhost | 6379 | N/A |

---

## 🐛 QUICK TROUBLESHOOTING

### **CORS Error**
```
Error: Access blocked by CORS policy
```
**Fix:** Check `ALLOWED_ORIGINS` in `backend/.env`, restart backend

### **Connection Refused**
```
Error: Network request failed
```
**Fix:** Verify service is running: `curl http://localhost:PORT/health`

### **Database Error**
```
Error: Unable to connect to database
```
**Fix:** Start PostgreSQL, check credentials in `.env`

### **Port Already in Use**
```
Error: EADDRINUSE :::3000
```
**Fix:** Kill process: `netstat -ano | findstr :3000`, then `taskkill /PID <PID> /F`

---

## 📁 KEY FILES

| File | Purpose |
|------|---------|
| `backend/src/server.js` | CORS configuration |
| `backend/.env` | Backend environment |
| `regiq/src/services/api.js` | Frontend API client |
| `regiq/.env` | Frontend environment |
| `backend/test-cors-config.js` | CORS testing tool |

---

## 📖 DOCUMENTATION

- **Full Guide:** `docs/ENVIRONMENT_CONFIGURATION_GUIDE.md`
- **Quick Start:** `docs/INTEGRATION_QUICKSTART.md`
- **Summary:** `docs/ENVIRONMENT_CONFIG_COMPLETE.md`

---

## 🎯 COMMON API CALLS

```javascript
// Import in React Native component
import { 
  getRegulations, 
  getRiskSimulations, 
  getBiasReports 
} from './services/apiClient';

// Use in useEffect or event handler
useEffect(() => {
  const loadData = async () => {
    const regulations = await getRegulations();
    const simulations = await getRiskSimulations();
    const biasReports = await getBiasReports();
    // Update state with data...
  };
  loadData();
}, []);
```

---

## 🔍 DEBUGGING TIPS

1. **Check all services are running:**
   ```bash
   netstat -ano | findstr ":3000 :8000 :19002"
   ```

2. **View real-time logs:**
   - Backend: `tail -f backend/logs/application/*.log`
   - AI/ML: Watch uvicorn output
   - Frontend: Check Expo terminal

3. **Test individual endpoints:**
   ```bash
   curl -H "Origin: http://localhost:19000" \
        http://localhost:3000/api/regulatory/regulations -v
   ```

4. **Verify environment loaded:**
   ```javascript
   console.log('API URL:', process.env.REACT_NATIVE_API_BASE_URL);
   ```

---

## ✅ INTEGRATION FLOW

```
Frontend (React Native)
  ↓ HTTP (port 3000)
Backend (Node.js Express)
  ↓ REST (port 8000)
AI/ML Service (Python FastAPI)
  ↓ SQL
PostgreSQL Database
  ↓ Cache
Redis
```

---

**Last Updated:** March 23, 2026  
**Status:** ✅ Ready for Integration
