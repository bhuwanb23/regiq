const express = require('express');
const regulatoryController = require('../controllers/regulatory.controller');
const { authenticate } = require('../middleware/auth.middleware');
const {
  validateRegulationQuery,
  validateRegulationSearch,
  validateDeadlinesQuery,
  validateRegulationId
} = require('../middleware/regulatoryValidation.middleware');

const router = express.Router();

// Document upload and processing endpoints
// Write operations require auth so `req.user.id` is populated.
router.post('/documents/upload', authenticate, regulatoryController.uploadDocument);
router.post('/documents/:id/process', authenticate, regulatoryController.processDocument);
router.get('/documents/:id/status', regulatoryController.getDocumentProcessingStatus);

// Regulatory document search and filtering (read-only, public)
router.get('/documents', regulatoryController.searchDocuments);
router.get('/documents/:id', regulatoryController.getDocumentById);

// New regulatory intelligence endpoints (read-only, public)
router.get('/regulations/search', validateRegulationSearch, regulatoryController.searchRegulations);
router.get('/regulations/categories', regulatoryController.getRegulationCategories);
router.get('/regulations/deadlines', validateDeadlinesQuery, regulatoryController.getUpcomingDeadlines);
router.get('/regulations', validateRegulationQuery, regulatoryController.getRegulations);
router.get('/regulations/:id', validateRegulationId, regulatoryController.getRegulationById);

// Compliance checking endpoints
router.post('/compliance/check', authenticate, regulatoryController.checkCompliance);
router.get('/compliance/results/:id', regulatoryController.getComplianceResult);

// Regulatory alert generation
router.post('/alerts', authenticate, regulatoryController.createAlert);
router.get('/alerts', regulatoryController.getAlerts);
router.put('/alerts/:id', authenticate, regulatoryController.updateAlertStatus);

// Document versioning system
router.post('/documents/:id/versions', authenticate, regulatoryController.createDocumentVersion);
router.get('/documents/:id/versions', regulatoryController.getDocumentVersions);

// Document metadata management
router.put('/documents/:id/metadata', authenticate, regulatoryController.updateDocumentMetadata);
router.get('/documents/:id/metadata', regulatoryController.getDocumentMetadata);

// Document sharing capabilities
router.post('/documents/:id/share', authenticate, regulatoryController.shareDocument);
router.get('/documents/shared', authenticate, regulatoryController.getSharedDocuments);

// Document analysis results storage
router.post('/analysis', authenticate, regulatoryController.storeAnalysisResult);
router.get('/analysis/:id', regulatoryController.getAnalysisResult);
router.get('/analysis/document/:documentId', regulatoryController.getDocumentAnalysisResults);

module.exports = router;