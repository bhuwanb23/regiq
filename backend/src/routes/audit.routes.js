const express = require('express');
const router = express.Router();
const auditController = require('../controllers/audit.controller');

// Audit logs endpoints
router.get('/audit-logs', auditController.getAllAuditLogs);
router.get('/audit-logs/:auditLogId', auditController.getAuditLogById);

// System events tracking
router.get('/system-events', auditController.getSystemEvents);

// Security event monitoring
router.get('/security-events', auditController.getSecurityEvents);

// Audit trail generation
router.get('/audit-trail/:entityType/:entityId', auditController.generateAuditTrail);

// Audit statistics
router.get('/audit-statistics', auditController.getAuditStatistics);

module.exports = router;