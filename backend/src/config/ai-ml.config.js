// AI/ML Service Configuration
const dotenv = require('dotenv');
dotenv.config();

module.exports = {
  // AI/ML Service API Configuration
  aiMlService: {
    baseUrl: process.env.AI_ML_SERVICE_BASE_URL || 'http://localhost:8000',
    apiKey: process.env.AI_ML_SERVICE_API_KEY || 'default-api-key',
    timeout: parseInt(process.env.AI_ML_SERVICE_TIMEOUT) || 30000,
    maxRetries: parseInt(process.env.AI_ML_SERVICE_MAX_RETRIES) || 3,
  },

  // Model Configuration
  models: {
    // Regulatory Compliance Analysis Model
    complianceAnalysis: {
      name: process.env.COMPLIANCE_MODEL_NAME || 'regulatory-compliance-analyzer',
      version: process.env.COMPLIANCE_MODEL_VERSION || 'v1',
      endpoint: process.env.COMPLIANCE_MODEL_ENDPOINT || '/analyze/compliance',
    },
    
    // Risk Assessment Model
    riskAssessment: {
      name: process.env.RISK_MODEL_NAME || 'financial-risk-assessor',
      version: process.env.RISK_MODEL_VERSION || 'v1',
      endpoint: process.env.RISK_MODEL_ENDPOINT || '/analyze/risk',
    },
    
    // Market Sentiment Analysis Model
    sentimentAnalysis: {
      name: process.env.SENTIMENT_MODEL_NAME || 'market-sentiment-analyzer',
      version: process.env.SENTIMENT_MODEL_VERSION || 'v1',
      endpoint: process.env.SENTIMENT_MODEL_ENDPOINT || '/analyze/sentiment',
    },
    
    // Data Anomaly Detection Model
    anomalyDetection: {
      name: process.env.ANOMALY_MODEL_NAME || 'data-anomaly-detector',
      version: process.env.ANOMALY_MODEL_VERSION || 'v1',
      endpoint: process.env.ANOMALY_MODEL_ENDPOINT || '/detect/anomalies',
    },
  },

  // Job Queue Configuration
  jobQueue: {
    concurrency: parseInt(process.env.JOB_QUEUE_CONCURRENCY) || 5,
    timeout: parseInt(process.env.JOB_QUEUE_TIMEOUT) || 60000,
    retryDelay: parseInt(process.env.JOB_QUEUE_RETRY_DELAY) || 5000,
    maxRetries: parseInt(process.env.JOB_QUEUE_MAX_RETRIES) || 3,
  },

  // Caching Configuration
  cache: {
    ttl: parseInt(process.env.CACHE_TTL) || 300, // 5 minutes
    maxItems: parseInt(process.env.CACHE_MAX_ITEMS) || 1000,
    enabled: process.env.CACHE_ENABLED === 'true' || true,
  },

  // Rate Limiting Configuration
  rateLimiting: {
    enabled: process.env.RATE_LIMITING_ENABLED === 'true' || true,
    windowMs: parseInt(process.env.RATE_LIMIT_WINDOW_MS) || 60000, // 1 minute
    maxRequests: parseInt(process.env.RATE_LIMIT_MAX_REQUESTS) || 100,
    message: process.env.RATE_LIMIT_MESSAGE || 'Too many requests from this IP, please try again later.',
  },

  // Performance Monitoring
  monitoring: {
    enabled: process.env.MONITORING_ENABLED === 'true' || true,
    logLevel: process.env.MONITORING_LOG_LEVEL || 'info',
    metricsEndpoint: process.env.METRICS_ENDPOINT || '/metrics',
  },
};