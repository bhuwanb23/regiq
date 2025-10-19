# REGIQ Project Structure

## Root Directory Structure
```
regiq/
├── frontend/                 # React Native Expo App
│   ├── src/
│   │   ├── components/       # Reusable UI components
│   │   │   ├── common/       # Common components (buttons, inputs, cards)
│   │   │   ├── charts/       # Chart components for visualizations
│   │   │   ├── forms/        # Form components
│   │   │   └── navigation/   # Navigation components
│   │   ├── screens/          # App screens
│   │   │   ├── onboarding/   # Welcome, signup, profile setup
│   │   │   ├── dashboard/    # Main dashboard
│   │   │   ├── regulations/  # Regulation intelligence
│   │   │   ├── ai-audit/     # AI model audit
│   │   │   ├── simulation/   # Risk simulation
│   │   │   ├── alerts/       # Notifications & alerts
│   │   │   ├── reports/      # Reports & audit
│   │   │   └── settings/     # Settings & integrations
│   │   ├── navigation/       # Navigation configuration
│   │   ├── services/         # API services
│   │   ├── utils/            # Utility functions
│   │   ├── hooks/            # Custom React hooks
│   │   ├── context/          # React context providers
│   │   ├── constants/        # App constants
│   │   └── styles/           # Global styles and theme
│   ├── assets/               # Images, fonts, icons
│   ├── App.js               # Main app component
│   └── package.json         # Dependencies
│
├── backend/                  # FastAPI Backend
│   ├── app/
│   │   ├── api/              # API routes
│   │   │   ├── v1/           # API version 1
│   │   │   │   ├── auth/     # Authentication endpoints
│   │   │   │   ├── regulations/ # Regulation endpoints
│   │   │   │   ├── models/   # AI model endpoints
│   │   │   │   ├── simulation/ # Risk simulation endpoints
│   │   │   │   ├── reports/  # Reports endpoints
│   │   │   │   └── alerts/   # Alerts endpoints
│   │   │   └── __init__.py
│   │   ├── core/             # Core functionality
│   │   │   ├── config.py     # Configuration
│   │   │   ├── security.py   # Security utilities
│   │   │   └── database.py   # Database connection
│   │   ├── models/           # Database models
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── services/         # Business logic
│   │   └── utils/            # Utility functions
│   ├── requirements.txt      # Python dependencies
│   ├── Dockerfile           # Docker configuration
│   └── main.py              # FastAPI app entry point
│
├── ai-ml/                    # AI/ML Services
│   ├── services/
│   │   ├── gemini/           # Gemini AI integration
│   │   ├── explainability/   # SHAP, LIME implementations
│   │   ├── bias_detection/   # Bias analysis
│   │   ├── synthetic_data/   # Synthetic data generation
│   │   └── regulation_parser/ # Legal text processing
│   ├── models/               # ML model definitions
│   ├── data/                 # Training data and datasets
│   ├── notebooks/            # Jupyter notebooks for experimentation
│   ├── requirements.txt      # Python ML dependencies
│   └── config/               # ML service configurations
│
├── shared/                   # Shared utilities and types
│   ├── types/                # TypeScript type definitions
│   ├── constants/            # Shared constants
│   └── utils/                # Shared utility functions
│
├── docs/                     # Documentation
│   ├── api/                  # API documentation
│   ├── frontend/             # Frontend documentation
│   └── deployment/           # Deployment guides
│
├── scripts/                  # Build and deployment scripts
├── docker-compose.yml        # Multi-service Docker setup
├── .gitignore               # Git ignore rules
└── README.md                # Project overview
```

## Frontend Screen Structure

### 1. Onboarding Flow
- `WelcomeScreen.js` - Landing page with tagline
- `AuthScreen.js` - Login/Signup with OAuth
- `ProfileSetupScreen.js` - Company info and preferences
- `ModelIntegrationScreen.js` - Optional AI model setup

### 2. Main App Screens
- `DashboardScreen.js` - Compliance health score & overview
- `RegulationFeedScreen.js` - Regulation intelligence
- `ModelAuditScreen.js` - AI model analysis
- `RiskSimulationScreen.js` - Synthetic risk simulation
- `AlertsScreen.js` - Notifications center
- `ReportsScreen.js` - Audit reports
- `SettingsScreen.js` - App settings & integrations

### 3. Component Library
- `ComplianceGauge.js` - Circular compliance score
- `RegulationCard.js` - Regulation display card
- `BiasHeatmap.js` - Model bias visualization
- `RiskChart.js` - Risk simulation charts
- `AlertBadge.js` - Notification indicators
- `ActionButton.js` - Primary action buttons

## Technology Stack Integration

### Frontend Dependencies (to be added)
- Navigation: `@react-navigation/native`, `@react-navigation/bottom-tabs`
- UI Components: `react-native-elements`, `react-native-vector-icons`
- Charts: `react-native-chart-kit`, `react-native-svg`
- State Management: `@reduxjs/toolkit`, `react-redux`
- API: `axios`, `@tanstack/react-query`
- Authentication: `expo-auth-session`
- Notifications: `expo-notifications`

### Backend Dependencies
- FastAPI, Uvicorn, Pydantic
- SQLAlchemy, Alembic (database)
- JWT authentication
- Celery (background tasks)
- Redis (caching)

### AI-ML Dependencies
- Google Generative AI (Gemini)
- SHAP, LIME (explainability)
- Pandas, NumPy (data processing)
- Scikit-learn (ML utilities)
- Transformers (NLP)
