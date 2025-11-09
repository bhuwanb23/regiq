const express = require('express');
const regulatoryController = require('../controllers/regulatory.controller');
const { authenticate, authorize } = require('../middleware/auth.middleware');

const router = express.Router();

// Apply authentication middleware to all routes
router.use(authenticate);

// Document upload and processing endpoints
router.post('/documents/upload', regulatoryController.uploadDocument);
router.post('/documents/:id/process', regulatoryController.processDocument);
router.get('/documents/:id/status', regulatoryController.getDocumentProcessingStatus);

// Regulatory document search and filtering
router.get('/documents', regulatoryController.searchDocuments);
router.get('/documents/:id', regulatoryController.getDocumentById);

// Compliance checking endpoints
router.post('/compliance/check', regulatoryController.checkCompliance);
router.get('/compliance/results/:id', regulatoryController.getComplianceResult);

// Regulatory alert generation
router.post('/alerts', regulatoryController.createAlert);
router.get('/alerts', regulatoryController.getAlerts);
router.put('/alerts/:id', regulatoryController.updateAlertStatus);

// Document versioning system
router.post('/documents/:id/versions', regulatoryController.createDocumentVersion);
router.get('/documents/:id/versions', regulatoryController.getDocumentVersions);

// Document metadata management
router.put('/documents/:id/metadata', regulatoryController.updateDocumentMetadata);
router.get('/documents/:id/metadata', regulatoryController.getDocumentMetadata);

// Document sharing capabilities
router.post('/documents/:id/share', regulatoryController.shareDocument);
router.get('/documents/shared', regulatoryController.getSharedDocuments);

// Document analysis results storage
router.post('/analysis', regulatoryController.storeAnalysisResult);
router.get('/analysis/:id', regulatoryController.getAnalysisResult);
router.get('/analysis/document/:documentId', regulatoryController.getDocumentAnalysisResults);

module.exports = router;