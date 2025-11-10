const express = require('express');
const router = express.Router();
const alertController = require('../controllers/alert.controller');
const { authenticate } = require('../middleware/auth.middleware');

// Apply authentication middleware to all routes
router.use(authenticate);

// Alert generation and management endpoints
router.get('/alerts', alertController.getAllAlerts);
router.put('/alerts/:alertId/resolve', alertController.resolveAlert);
router.get('/alerts/statistics', alertController.getAlertStatistics);

module.exports = router;