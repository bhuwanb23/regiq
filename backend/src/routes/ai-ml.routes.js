const express = require('express');
const aiMlController = require('../controllers/ai-ml.controller');
const { aiMlRateLimiter } = require('../middleware/rate-limit.middleware');

const router = express.Router();

// Apply rate limiting to all AI/ML routes
router.use(aiMlRateLimiter);

// AI/ML Analysis Endpoints
/**
 * @route POST /ai-ml/compliance
 * @desc Analyze regulatory compliance using AI/ML
 * @access Public
 */
router.post('/compliance', aiMlController.analyzeCompliance);

/**
 * @route POST /ai-ml/risk
 * @desc Assess financial risk using AI/ML
 * @access Public
 */
router.post('/risk', aiMlController.assessRisk);

/**
 * @route POST /ai-ml/sentiment
 * @desc Analyze market sentiment using AI/ML
 * @access Public
 */
router.post('/sentiment', aiMlController.analyzeSentiment);

/**
 * @route POST /ai-ml/anomalies
 * @desc Detect anomalies in data using AI/ML
 * @access Public
 */
router.post('/anomalies', aiMlController.detectAnomalies);

// Async Job Processing Endpoints
/**
 * @route POST /ai-ml/jobs
 * @desc Process AI/ML job asynchronously
 * @access Public
 */
router.post('/jobs', aiMlController.processJobAsync);

/**
 * @route GET /ai-ml/jobs/:jobId
 * @desc Get job status
 * @access Public
 */
router.get('/jobs/:jobId', aiMlController.getJobStatus);

// Health and Metrics Endpoints
/**
 * @route GET /ai-ml/health
 * @desc Get AI/ML service health status
 * @access Public
 */
router.get('/health', aiMlController.getHealthStatus);

/**
 * @route GET /ai-ml/metrics
 * @desc Get performance metrics
 * @access Public
 */
router.get('/metrics', aiMlController.getMetrics);

module.exports = router;