const express = require('express');
const regulatoryController = require('../controllers/regulatory.controller');
const {
  validateRegulationQuery,
  validateRegulationSearch,
  validateDeadlinesQuery,
  validateRegulationId
} = require('../middleware/regulatoryValidation.middleware');

const router = express.Router();

// Document upload and processing endpoints
router.post('/documents/upload', regulatoryController.uploadDocument);
router.post('/documents/:id/process', regulatoryController.processDocument);
router.get('/documents/:id/status', regulatoryController.getDocumentProcessingStatus);

// Regulatory document search and filtering
router.get('/documents', regulatoryController.searchDocuments);
router.get('/documents/:id', regulatoryController.getDocumentById);

// New regulatory intelligence endpoints
router.get('/regulations/search', validateRegulationSearch, regulatoryController.searchRegulations);
router.get('/regulations/categories', regulatoryController.getRegulationCategories);
router.get('/regulations/deadlines', validateDeadlinesQuery, regulatoryController.getUpcomingDeadlines);
router.get('/regulations', validateRegulationQuery, regulatoryController.getRegulations);
router.get('/regulations/:id', validateRegulationId, regulatoryController.getRegulationById);

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