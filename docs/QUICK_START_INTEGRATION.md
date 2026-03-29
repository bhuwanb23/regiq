# Quick Start - Frontend/Backend Integration

**TL;DR:** Everything is connected and working! 🚀

---

## ✅ What's Working NOW

### Backend Endpoints (All Tested & Verified):

#### User Profile & Preferences
```bash
GET  /api/users/profile        → Returns demo user profile
PUT  /api/users/profile        → Accepts profile updates
GET  /api/users/preferences    → Returns default preferences
PUT  /api/users/preferences    → Accepts preference updates
```

#### Dashboard (NEW!)
```bash
GET  /api/dashboard                 → Full dashboard data
GET  /api/dashboard/compliance-score → Compliance metrics
GET  /api/dashboard/alerts          → Recent alerts
GET  /api/dashboard/activity        → Activity feed
```

#### Regulatory Intelligence
```bash
GET  /regulatory/regulations        → All regulations
GET  /regulatory/regulations/:id    → Specific regulation
GET  /regulatory/regulations/search → Search regulations
GET  /regulatory/regulations/categories → Categories
GET  /regulatory/regulations/deadlines   → Deadlines
```

---

## 🧪 Test It Yourself

### Quick Tests (Copy-Paste into PowerShell):

#### Test User Profile:
```powershell
$r = Invoke-WebRequest -Uri "http://localhost:3000/api/users/profile" -Method GET
($r.Content | ConvertFrom-Json).data.email
# Output: "demo@regiq.com"
```

#### Test Dashboard:
```powershell
$r = Invoke-WebRequest -Uri "http://localhost:3000/api/dashboard" -Method GET
$d = $r.Content | ConvertFrom-Json
Write-Host "Compliance Score: $($d.data.complianceScore)"
# Output: "Compliance Score: 78"
```

#### Test All Endpoints at Once:
```powershell
$endpoints = @(
  "/api/users/profile",
  "/api/users/preferences",
  "/api/dashboard",
  "/regulatory/regulations"
)
foreach ($ep in $endpoints) {
  try {
    $r = Invoke-WebRequest -Uri "http://localhost:3000$ep" -Method GET -ErrorAction Stop
    Write-Host "✅ $ep → OK" -ForegroundColor Green
  } catch {
    Write-Host "❌ $ep → FAILED" -ForegroundColor Red
  }
}
```

---

## 📱 React Native Screens Status

### ✅ Fully Connected Screens:

1. **ProfileScreen** (`regiq/src/screens/profile/ProfileScreen.js`)
   - Uses `useUserProfile` hook
   - Calls real API endpoints
   - Edit profile ✅
   - Manage preferences ✅

2. **DashboardScreen** (`regiq/src/screens/dashboard/DashboardScreen.js`)
   - Uses `useDashboardData` hook
   - Now calls real API (not mock data!)
   - Shows compliance score ✅
   - Displays alerts ✅
   - Activity feed ✅

3. **RegulationIntelligenceScreen** (`regiq/src/screens/regulations/RegulationIntelligenceScreen.js`)
   - Uses `useRegulationData` hook
   - API endpoints verified working
   - Browse regulations ✅
   - Search functionality ✅

---

## 🔧 How to Run

### Backend:
```bash
cd d:\projects\apps\regiq\backend
npm start
# Server runs on http://localhost:3000
```

### Frontend:
```bash
cd d:\projects\apps\regiq\regiq
npm start
# Expo runs on http://localhost:19002
```

---

## 📊 Response Format Examples

### User Profile Response:
```json
{
  "success": true,
  "data": {
    "id": "demo_user_1",
    "email": "demo@regiq.com",
    "firstName": "Demo",
    "lastName": "User",
    "role": "compliance_officer",
    "department": "Risk Management"
  }
}
```

### Dashboard Response:
```json
{
  "success": true,
  "data": {
    "complianceScore": 78,
    "user": {
      "name": "Demo User",
      "company": "FinTech Solutions Inc.",
      "role": "Compliance Manager"
    },
    "alerts": [...],
    "recentActivity": [...]
  }
}
```

---

## 🎯 For Frontend Developers

### Using the APIs in Your Components:

#### Example: Get User Profile
```javascript
import { getUserProfile } from '../services/apiClient';

const MyComponent = () => {
  const [profile, setProfile] = useState(null);
  
  useEffect(() => {
    const loadProfile = async () => {
      const response = await getUserProfile();
      setProfile(response.data);
    };
    loadProfile();
  }, []);
  
  return <Text>{profile?.firstName}</Text>;
};
```

#### Example: Update Preferences
```javascript
import { updateUserPreferences } from '../services/apiClient';

const handleSavePrefs = async (prefs) => {
  try {
    const response = await updateUserPreferences({
      theme: 'dark',
      language: 'en'
    });
    console.log('Saved:', response.data);
  } catch (error) {
    console.error('Failed:', error.message);
  }
};
```

---

## 🎯 For Backend Developers

### Adding New Endpoints:

#### 1. Create Controller Method:
```javascript
// backend/src/controllers/my.controller.js
const getMyData = async (req, res) => {
  try {
    res.status(200).json({
      success: true,
      data: { /* your data */ }
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: error.message
    });
  }
};
```

#### 2. Create Route:
```javascript
// backend/src/routes/api/my.routes.js
const express = require('express');
const router = express.Router();
const myController = require('../../controllers/my.controller');

router.get('/', myController.getMyData);

module.exports = router;
```

#### 3. Mount in server.js:
```javascript
const apiMyRoutes = require('./routes/api/my.routes');
app.use('/api/my', apiMyRoutes);
```

---

## ⚠️ Important Notes

### Development Mode Only!
Current endpoints are for **DEVELOPMENT TESTING**:
- ❌ No authentication required
- ❌ No database persistence (returns mock/echo data)
- ❌ No input validation

This is intentional to enable rapid frontend development. Production features will be added later.

---

## 📚 Documentation Files

Need more details? Check these files:

1. **INTEGRATION_COMPLETION_REPORT.md** - Full implementation report
2. **REACT_NATIVE_SCREEN_INTEGRATION_GUIDE.md** - Screen-by-screen guide
3. **FRONTEND_BACKEND_INTEGRATION_STATUS.md** - Progress tracking
4. **USER_PROFILE_ENDPOINTS_IMPLEMENTED.md** - Endpoint details

---

## 🆘 Troubleshooting

### Backend not responding?
```bash
# Check if server is running
curl http://localhost:3000/health

# If not running, restart:
cd backend
npm start
```

### CORS errors?
- Backend has CORS configured ✅
- Frontend should call `http://localhost:3000/api/*` ✅
- Check browser console for specific errors

### Data not showing?
1. Check network tab in browser/dev tools
2. Verify endpoint returns 200 OK
3. Check response format matches expectations
4. Look at console logs for errors

---

## ✅ Success Checklist

Use this to verify everything is working:

- [ ] Backend server running on port 3000
- [ ] Frontend app running on Expo
- [ ] Can fetch user profile (returns data)
- [ ] Can fetch dashboard (shows compliance score)
- [ ] Can fetch regulations (shows list)
- [ ] Profile screen displays user data
- [ ] Dashboard screen shows real data
- [ ] No CORS errors in console

If all checked ✅ - You're good to go! 🎉

---

**Last Updated:** March 21, 2026  
**Status:** All systems operational ✅
