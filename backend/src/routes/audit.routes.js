const express = require('express');
const router = express.Router();
const auditController = require('../controllers/audit.controller');
const { authenticate, authorizeAdmin } = require('../middleware/auth.middleware');

// Apply authentication middleware to all routes
router.use(authenticate);

// Audit logs endpoints
router.get('/audit-logs', auditController.getAllAuditLogs);
router.get('/audit-logs/:auditLogId', auditController.getAuditLogById);

// System events tracking
router.get('/system-events', authorizeAdmin, auditController.getSystemEvents);

// Security event monitoring
router.get('/security-events', authorizeAdmin, auditController.getSecurityEvents);

// Audit trail generation
router.get('/audit-trail/:entityType/:entityId', auditController.generateAuditTrail);

// Audit statistics
router.get('/audit-statistics', authorizeAdmin, auditController.getAuditStatistics);

module.exports = router;