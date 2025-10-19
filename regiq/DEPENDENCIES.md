# REGIQ Frontend Dependencies

## Required Dependencies to Install

Run the following commands to install all necessary dependencies:

```bash
# Navigation
npm install @react-navigation/native @react-navigation/bottom-tabs @react-navigation/stack

# Navigation dependencies for Expo
npx expo install react-native-screens react-native-safe-area-context

# UI Components and Icons
npm install react-native-elements react-native-vector-icons
npx expo install @expo/vector-icons

# Charts and Visualizations
npm install react-native-svg react-native-chart-kit
npx expo install react-native-svg

# State Management
npm install @reduxjs/toolkit react-redux

# API and Data Fetching
npm install axios @tanstack/react-query

# Authentication
npx expo install expo-auth-session expo-crypto

# Notifications
npx expo install expo-notifications

# Additional Expo modules
npx expo install expo-linear-gradient expo-blur

# Development Dependencies
npm install --save-dev @babel/core @babel/preset-env
```

## Current Package.json Structure

The current package.json needs to be updated with these dependencies. Here's what should be added:

```json
{
  "dependencies": {
    "expo": "~54.0.13",
    "expo-status-bar": "~3.0.8",
    "react": "19.1.0",
    "react-native": "0.81.4",
    
    // Navigation
    "@react-navigation/native": "^6.1.9",
    "@react-navigation/bottom-tabs": "^6.5.11",
    "@react-navigation/stack": "^6.3.20",
    "react-native-screens": "~4.0.0",
    "react-native-safe-area-context": "~5.0.0",
    
    // UI & Icons
    "react-native-elements": "^3.4.3",
    "react-native-vector-icons": "^10.0.3",
    "@expo/vector-icons": "^14.0.0",
    
    // Charts
    "react-native-svg": "~15.7.0",
    "react-native-chart-kit": "^6.12.0",
    
    // State Management
    "@reduxjs/toolkit": "^2.0.1",
    "react-redux": "^9.0.4",
    
    // API
    "axios": "^1.6.2",
    "@tanstack/react-query": "^5.17.1",
    
    // Auth & Notifications
    "expo-auth-session": "~6.0.0",
    "expo-crypto": "~14.0.0",
    "expo-notifications": "~1.0.0",
    
    // Additional
    "expo-linear-gradient": "~14.0.0",
    "expo-blur": "~14.0.0"
  }
}
```

## Backend Dependencies (FastAPI)

Create `backend/requirements.txt`:

```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
sqlalchemy==2.0.23
alembic==1.13.1
psycopg2-binary==2.9.9
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
celery==5.3.4
redis==5.0.1
httpx==0.25.2
```

## AI-ML Dependencies

Create `ai-ml/requirements.txt`:

```txt
google-generativeai==0.3.2
openai==1.3.7
shap==0.43.0
lime==0.2.0.1
pandas==2.1.4
numpy==1.25.2
scikit-learn==1.3.2
transformers==4.36.2
torch==2.1.2
matplotlib==3.8.2
seaborn==0.13.0
jupyter==1.0.0
fastapi==0.104.1
uvicorn==0.24.0
```
