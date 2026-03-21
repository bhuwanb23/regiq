// AI/ML Service Configuration
// Maps backend routes to Python FastAPI endpoints
const dotenv = require('dotenv');
dotenv.config();

module.exports = {
  // ── Core AI/ML Service Connection ────────────────────────────────────
  aiMlService: {
    baseUrl: process.env.AI_ML_SERVICE_BASE_URL || 'http://localhost:8000',
    apiKey:  process.env.AI_ML_SERVICE_API_KEY  || 'regiq-internal-api-key',
    timeout:    parseInt(process.env.AI_ML_SERVICE_TIMEOUT)    || 60000,
    maxRetries: parseInt(process.env.AI_ML_SERVICE_MAX_RETRIES) || 3,
  },

  // ── Endpoint Map (matches Python FastAPI routes exactly) ─────────────
  endpoints: {
    // Health
    health: '/health',

    // Bias Analysis Service  →  ai-ml/services/bias_analysis/
    bias: {
      analyze:     process.env.BIAS_ANALYZE_ENDPOINT  || '/api/v1/bias-analysis/analyze',
      score:       process.env.BIAS_SCORE_ENDPOINT    || '/api/v1/bias-analysis/score',
      metrics:     '/api/v1/bias-analysis/metrics',
      mitigation:  '/api/v1/bias-analysis/mitigate',
      explain:     '/api/v1/bias-analysis/explain',
      visualize:   '/api/v1/bias-analysis/visualize',
    },

    // Risk Simulator Service  →  ai-ml/services/risk_simulator/
    risk: {
      simulate:    process.env.RISK_MODEL_ENDPOINT    || '/api/v1/risk-simulator/simulate',
      monteCarlo:  '/api/v1/risk-simulator/monte-carlo',
      bayesian:    '/api/v1/risk-simulator/bayesian',
      stressTest:  '/api/v1/risk-simulator/stress-test',
      scenarios:   '/api/v1/risk-simulator/scenarios',
      frameworks:  '/api/v1/risk-simulator/frameworks',
    },

    // Regulatory Intelligence Service  →  ai-ml/services/regulatory_intelligence/
    regulatory: {
      analyze:     process.env.COMPLIANCE_MODEL_ENDPOINT || '/api/v1/regulatory-intelligence/documents/analyze',
      summarize:   '/api/v1/regulatory-intelligence/documents/summarize',
      search:      '/api/v1/regulatory-intelligence/search',
      qa:          '/api/v1/regulatory-intelligence/qa',
      entities:    '/api/v1/regulatory-intelligence/entities',
      seed:        '/api/v1/regulatory-intelligence/seed',
    },

    // Report Generator Service  →  ai-ml/services/report_generator/
    reports: {
      generate:    process.env.REPORT_GENERATE_ENDPOINT || '/api/v1/report-generator/generate',
      export:      '/api/v1/report-generator/export',
      glossary:    '/api/v1/report-generator/glossary',
      templates:   '/api/v1/report-generator/templates',
    },
  },

  // ── Legacy model config (kept for backwards compat) ──────────────────
  models: {
    complianceAnalysis: {
      name:     process.env.COMPLIANCE_MODEL_NAME    || 'regulatory-compliance-analyzer',
      version:  process.env.COMPLIANCE_MODEL_VERSION || 'v1',
      endpoint: process.env.COMPLIANCE_MODEL_ENDPOINT || '/api/v1/regulatory-intelligence/documents/analyze',
    },
    riskAssessment: {
      name:     process.env.RISK_MODEL_NAME    || 'financial-risk-assessor',
      version:  process.env.RISK_MODEL_VERSION || 'v1',
      endpoint: process.env.RISK_MODEL_ENDPOINT || '/api/v1/risk-simulator/simulate',
    },
    biasAnalysis: {
      name:     process.env.BIAS_MODEL_NAME    || 'bias-fairness-analyzer',
      version:  process.env.BIAS_MODEL_VERSION || 'v1',
      endpoint: process.env.BIAS_ANALYZE_ENDPOINT || '/api/v1/bias-analysis/analyze',
    },
    reportGenerator: {
      name:     process.env.REPORT_MODEL_NAME    || 'compliance-report-generator',
      version:  process.env.REPORT_MODEL_VERSION || 'v1',
      endpoint: process.env.REPORT_GENERATE_ENDPOINT || '/api/v1/report-generator/generate',
    },
  },

  // ── Job Queue ─────────────────────────────────────────────────────────
  jobQueue: {
    concurrency: parseInt(process.env.JOB_QUEUE_CONCURRENCY) || 5,
    timeout:     parseInt(process.env.JOB_QUEUE_TIMEOUT)     || 60000,
    retryDelay:  parseInt(process.env.JOB_QUEUE_RETRY_DELAY) || 5000,
    maxRetries:  parseInt(process.env.JOB_QUEUE_MAX_RETRIES) || 3,
  },

  // ── Caching ───────────────────────────────────────────────────────────
  cache: {
    ttl:      parseInt(process.env.CACHE_TTL)       || 300,
    maxItems: parseInt(process.env.CACHE_MAX_ITEMS) || 1000,
    enabled:  process.env.CACHE_ENABLED !== 'false',
  },

  // ── Rate Limiting ─────────────────────────────────────────────────────
  rateLimiting: {
    enabled:     process.env.RATE_LIMITING_ENABLED !== 'false',
    windowMs:    parseInt(process.env.RATE_LIMIT_WINDOW_MS)    || 60000,
    maxRequests: parseInt(process.env.RATE_LIMIT_MAX_REQUESTS) || 100,
    message:     process.env.RATE_LIMIT_MESSAGE || 'Too many requests, please try again later.',
  },

  // ── Monitoring ────────────────────────────────────────────────────────
  monitoring: {
    enabled:         process.env.MONITORING_ENABLED !== 'false',
    logLevel:        process.env.MONITORING_LOG_LEVEL || 'info',
    metricsEndpoint: process.env.METRICS_ENDPOINT    || '/metrics',
  },
};
