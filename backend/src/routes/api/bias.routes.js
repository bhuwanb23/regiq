const express = require('express');
const biasController = require('../../controllers/api/bias.controller');
const upload = require('../../middleware/upload.middleware');

const router = express.Router();

// Bias Analysis Endpoints
router.post('/analysis', biasController.analyzeBias);
router.get('/analysis', biasController.listBiasAnalyses);
router.get('/analysis/:id', biasController.getBiasAnalysis);

// Bias Reports Endpoints
router.get('/reports', biasController.listBiasReports);
router.get('/reports/:id', biasController.getBiasReport);

// Bias Mitigation Endpoints
router.get('/mitigation', biasController.listMitigationStrategies);
router.post('/mitigation', biasController.applyMitigation);
router.get('/mitigation/:id', biasController.getMitiagationStrategy);

// Model Upload Endpoint
router.post('/model-upload', upload.single('model'), biasController.uploadModel);

// Bias Scoring Endpoint
router.get('/scoring', biasController.getBiasScores);

// Visualization Data Endpoint
router.get('/visualization', biasController.getVisualizationData);

module.exports = router;