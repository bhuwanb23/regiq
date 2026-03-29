const express = require('express');
const dashboardController = require('../../controllers/dashboard.controller');

const router = express.Router();

/**
 * @route   GET /api/dashboard
 * @desc    Get comprehensive dashboard data 
 * @access  Public (for development)
 */
router.get('/', dashboardController.getDashboardData);

/**
 * @route   GET /api/dashboard/compliance-score
 * @desc    Get compliance score metrics
 * @access  Public
 */
router.get('/compliance-score', dashboardController.getComplianceScore);

/**
 * @route   GET /api/dashboard/alerts
 * @desc    Get dashboard alerts
 * @access  Public
 */
router.get('/alerts', dashboardController.getAlerts);

/**
 * @route   GET /api/dashboard/activity
 * @desc    Get activity feed
 * @access  Public
 */
router.get('/activity', dashboardController.getActivityFeed);

module.exports = router;
