const express = require('express');
const router = express.Router();
const jobStatusController = require('../controllers/jobStatus.controller');
const { authenticate } = require('../middleware/auth.middleware');

// Apply authentication middleware to all routes
router.use(authenticate);

// Job status tracking endpoints
// IMPORTANT: specific routes (e.g. /jobs/history) must precede the
// generic /:jobId catcher, otherwise Express captures them as IDs.
router.get('/jobs', jobStatusController.getAllJobStatuses);
router.get('/jobs/history', jobStatusController.getJobHistory);
router.get('/jobs/:jobId', jobStatusController.getJobStatus);
router.put('/jobs/:jobId/cancel', jobStatusController.cancelJob);
router.put('/jobs/:jobId/progress', jobStatusController.updateProgress);

// Performance metrics collection
router.get('/metrics/performance', jobStatusController.getPerformanceMetrics);
router.get('/metrics/realtime', jobStatusController.getRealTimeMetrics);

// System health and resource utilization tracking
router.get('/system/health', jobStatusController.getSystemHealth);

module.exports = router;