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

// Middleware
app.use(helmet()); // Security headers
app.use(cors()); // Cross-origin resource sharing
app.use(express.json()); // Parse JSON bodies
app.use(express.urlencoded({ extended: true })); // Parse URL-encoded bodies
app.use(cookieParser()); // Parse cookies

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

// Regulatory routes
const regulatoryRoutes = require('./routes/regulatory.routes');
app.use('/regulatory', regulatoryRoutes);

// Bias Analysis routes
const biasAnalysisRoutes = require('./routes/biasAnalysis.routes');
app.use('/bias', biasAnalysisRoutes);

// Risk Simulation routes
const riskSimulationRoutes = require('./routes/riskSimulation.routes');
app.use('/risk', riskSimulationRoutes);

// Report Generation routes
const reportGenerationRoutes = require('./routes/reportGeneration.routes');
app.use('/reports', reportGenerationRoutes);

// Data Ingestion routes
const dataIngestionRoutes = require('./routes/dataIngestion.routes');
app.use('/data', dataIngestionRoutes);

// AI/ML routes
const aiMlRoutes = require('./routes/ai-ml.routes');
app.use('/ai-ml', aiMlRoutes);

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
app.listen(PORT, () => {
  console.log(`REGIQ Backend Server is running on port ${PORT}`);
});

module.exports = app;