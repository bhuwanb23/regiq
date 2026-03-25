const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const dotenv = require('dotenv');
const cookieParser = require('cookie-parser');

// Load environment variables
dotenv.config();

// Create Express app
const app = express();
const PORT = process.env.PORT || 3000;
const NODE_ENV = process.env.NODE_ENV || 'development';

// CORS Configuration
const corsOptions = {
  // Allow specific origins based on environment
  origin: function (origin, callback) {
    // Allowed origins for different environments
    const allowedOrigins = [
      'http://localhost:19000', // Expo Go
      'http://localhost:19002', // Expo Web
      'http://localhost:8081',  // React Native
      'http://localhost:3000',  // Web build
      'http://192.168.1.*:*',   // Local network (for mobile testing)
    ];
    
    // Add production origins from environment variable
    if (process.env.ALLOWED_ORIGINS) {
      const prodOrigins = process.env.ALLOWED_ORIGINS.split(',');
      allowedOrigins.push(...prodOrigins);
    }
    
    // Allow requests with no origin (mobile apps, curl, etc.)
    if (!origin) return callback(null, true);
    
    // Check if origin is allowed
    const isAllowed = allowedOrigins.some(allowed => {
      if (allowed.includes('*')) {
        const regex = new RegExp(allowed.replace('*', '.*'));
        return regex.test(origin);
      }
      return origin === allowed;
    });
    
    if (isAllowed) {
      callback(null, true);
    } else {
      console.warn(`CORS blocked: ${origin} is not in allowed origins`);
      callback(new Error('Not allowed by CORS'));
    }
  },
  
  // Allowed methods
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'],
  
  // Allowed headers
  allowedHeaders: ['Content-Type', 'Authorization', 'X-Requested-With', 'Accept', 'Origin'],
  
  // Exposed headers (for client to access)
  exposedHeaders: ['Content-Length', 'X-Request-Id'],
  
  // Allow credentials (cookies, authorization headers)
  credentials: true,
  
  // Max age for preflight caching (10 minutes)
  maxAge: 600,
};

// Apply CORS middleware with configuration
app.use(cors(corsOptions));

// Security headers (after CORS)
app.use(helmet());

// Parse bodies
app.use(express.json({ limit: '10mb' })); // Increased limit for file uploads
app.use(express.urlencoded({ extended: true, limit: '10mb' }));
app.use(cookieParser());

// Basic routes
app.get('/', (req, res) => {
  res.json({
    message: 'Welcome to REGIQ Backend API',
    version: '1.0.0',
    docs: '/docs',
    health: '/health'
  });
});

app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    uptime: process.uptime()
  });
});

// Auth routes
const authRoutes = require('./routes/auth.routes');
app.use('/auth', authRoutes);

// User routes
const userRoutes = require('./routes/user.routes');
app.use('/users', userRoutes);

// API User routes
const apiUserRoutes = require('./routes/api/user.routes');
app.use('/api/users', apiUserRoutes);

// Regulatory routes
const regulatoryRoutes = require('./routes/regulatory.routes');
app.use('/regulatory', regulatoryRoutes);

// Bias Analysis routes
const biasAnalysisRoutes = require('./routes/biasAnalysis.routes');
app.use('/bias', biasAnalysisRoutes);

// API Bias Analysis routes
const apiBiasRoutes = require('./routes/api/bias.routes');
app.use('/api/bias', apiBiasRoutes);

// Risk Simulation routes
const riskSimulationRoutes = require('./routes/riskSimulation.routes');
app.use('/risk', riskSimulationRoutes);

// API Risk Simulation routes
const apiRiskRoutes = require('./routes/api/risk.routes');
app.use('/api/risk', apiRiskRoutes);

// Report Generation routes
const reportGenerationRoutes = require('./routes/reportGeneration.routes');
app.use('/reports', reportGenerationRoutes);

// API Report Generation routes
const apiReportsRoutes = require('./routes/api/reports.routes');
app.use('/api/reports', apiReportsRoutes);

// Data Ingestion routes
const dataIngestionRoutes = require('./routes/dataIngestion.routes');
app.use('/data', dataIngestionRoutes);

// AI/ML routes
const aiMlRoutes = require('./routes/ai-ml.routes');
app.use('/ai-ml', aiMlRoutes);

// Job Status routes
const jobStatusRoutes = require('./routes/jobStatus.routes');
app.use('/status', jobStatusRoutes);

// Alert routes
const alertRoutes = require('./routes/alert.routes');
app.use('/alerts', alertRoutes);

// Search routes
const searchRoutes = require('./routes/search.routes');
app.use('/search', searchRoutes);

// Notification routes
const notificationRoutes = require('./routes/notification.routes');
app.use('/notifications', notificationRoutes);

// API Notification routes
const apiNotificationRoutes = require('./routes/api/notification.routes');
app.use('/api/notifications', apiNotificationRoutes);

// Audit routes
const auditRoutes = require('./routes/audit.routes');
app.use('/audit', auditRoutes);

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({
    error: 'Something went wrong!',
    message: process.env.NODE_ENV === 'development' ? err.message : 'Internal server error'
  });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({
    error: 'Route not found'
  });
});

// Start server
const server = app.listen(PORT, () => {
  console.log(`REGIQ Backend Server is running on port ${PORT}`);
});

// Initialize WebSocket server
const websocketService = require('./services/websocket.service');
websocketService.initialize(server);

// Initialize notification scheduler
const notificationScheduler = require('./services/notification.scheduler');

module.exports = { app, server };