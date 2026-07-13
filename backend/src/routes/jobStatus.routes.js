const express = require('express');
const router = express.Router();
const jobStatusController = require('../controllers/jobStatus.controller');
const { authenticate } = require('../middleware/auth.middleware');

// Apply authentication middleware to all routes
router.use(authenticate);

// Job status tracking endpoints
router.get('/jobs/:jobId', jobStatusController.getJobStatus);
router.get('/jobs', jobStatusController.getAllJobStatuses);
router.put('/jobs/:jobId/cancel', jobStatusController.cancelJob);
router.put('/jobs/:jobId/progress', jobStatusController.updateProgress);

// Job history management
router.get('/jobs/history', jobStatusController.getJobHistory);

// Performance metrics collection
router.get('/metrics/performance', jobStatusController.getPerformanceMetrics);
router.get('/metrics/realtime', jobStatusController.getRealTimeMetrics);

// System health and resource utilization tracking
router.get('/system/health', jobStatusController.getSystemHealth);

module.exports = router;