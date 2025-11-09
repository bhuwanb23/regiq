const express = require('express');
const biasAnalysisController = require('../controllers/biasAnalysis.controller');

const router = express.Router();

// Model Bias Analysis Endpoints
router.post('/analysis/model', biasAnalysisController.analyzeModel);
router.get('/analysis/model/:id', biasAnalysisController.getModelAnalysis);
router.get('/analysis/model', biasAnalysisController.listModelAnalyses);
router.delete('/analysis/model/:id', biasAnalysisController.deleteModelAnalysis);

// Data Bias Detection Services
router.post('/detection/data', biasAnalysisController.detectDataBias);
router.get('/detection/data/:id', biasAnalysisController.getDataBiasDetection);
router.get('/detection/data', biasAnalysisController.listDataBiasDetections);
router.post('/detection/data/batch', biasAnalysisController.batchDataBiasDetection);

// Bias Mitigation Recommendations
router.get('/mitigation/:analysisId', biasAnalysisController.getMitigationRecommendations);
router.post('/mitigation/apply/:analysisId', biasAnalysisController.applyMitigation);
router.get('/mitigation/templates', biasAnalysisController.getMitigationTemplates);

// Bias Analysis Result Storage
router.post('/results', biasAnalysisController.storeBiasResults);
router.get('/results/:id', biasAnalysisController.getBiasResults);
router.get('/results', biasAnalysisController.listBiasResults);
router.put('/results/:id', biasAnalysisController.updateBiasResults);

// Bias Trend Monitoring
router.get('/trends', biasAnalysisController.getBiasTrends);
router.get('/trends/model/:modelId', biasAnalysisController.getModelBiasTrends);
router.post('/trends/alerts', biasAnalysisController.createTrendAlerts);

// Bias Comparison Reports
router.post('/reports/compare', biasAnalysisController.generateComparisonReport);
router.get('/reports/compare/:id', biasAnalysisController.getComparisonReport);
router.get('/reports/compare', biasAnalysisController.listComparisonReports);

// Bias Analysis Scheduling
router.post('/schedule', biasAnalysisController.scheduleBiasAnalysis);
router.get('/schedule/:id', biasAnalysisController.getScheduledAnalysis);
router.get('/schedule', biasAnalysisController.listScheduledAnalyses);
router.put('/schedule/:id', biasAnalysisController.updateScheduledAnalysis);
router.delete('/schedule/:id', biasAnalysisController.cancelScheduledAnalysis);

// Bias Analysis Notifications
router.post('/notifications', biasAnalysisController.createNotificationRule);
router.get('/notifications/:id', biasAnalysisController.getNotificationRule);
router.get('/notifications', biasAnalysisController.listNotificationRules);
router.put('/notifications/:id', biasAnalysisController.updateNotificationRule);
router.delete('/notifications/:id', biasAnalysisController.deleteNotificationRule);

module.exports = router;