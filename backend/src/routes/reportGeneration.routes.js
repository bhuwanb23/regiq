const express = require('express');
const router = express.Router();

// Controllers
const reportTemplateController = require('../controllers/reportTemplate.controller');
const reportGenerationController = require('../controllers/reportGeneration.controller');
const reportSchedulingController = require('../controllers/reportScheduling.controller');
const reportDistributionController = require('../controllers/reportDistribution.controller');
const reportAnalyticsController = require('../controllers/reportAnalytics.controller');

// Report Analytics Routes
router.post('/analytics/:reportId/view', reportAnalyticsController.trackView);
router.post('/analytics/:reportId/download', reportAnalyticsController.trackDownload);
router.get('/analytics/:id', reportAnalyticsController.getAnalytics);
router.get('/analytics/report/:reportId', reportAnalyticsController.getAnalyticsByReport);
router.get('/analytics/summary/:reportId', reportAnalyticsController.getReportSummary);
router.get('/analytics/top-views', reportAnalyticsController.getTopReportsByViews);
router.delete('/analytics/:id', reportAnalyticsController.deleteAnalytics);

// Report Template Routes
router.post('/templates', reportTemplateController.createTemplate);
router.get('/templates/:id', reportTemplateController.getTemplate);
router.get('/templates', reportTemplateController.listTemplates);
router.put('/templates/:id', reportTemplateController.updateTemplate);
router.delete('/templates/:id', reportTemplateController.deleteTemplate);
router.get('/templates-active', reportTemplateController.getActiveTemplates);

// Report Generation Routes
router.post('/generate', reportGenerationController.generateReport);
router.get('/:id', reportGenerationController.getReport);
router.get('/', reportGenerationController.listReports);
router.put('/:id', reportGenerationController.updateReport);
router.delete('/:id', reportGenerationController.deleteReport);
router.get('/user/reports', reportGenerationController.getUserReports);
router.get('/type/:reportType', reportGenerationController.getReportsByType);
router.get('/:id/convert', reportGenerationController.convertReport);

// Report Scheduling Routes
router.post('/schedules', reportSchedulingController.createSchedule);
router.get('/schedules/:id', reportSchedulingController.getSchedule);
router.get('/schedules', reportSchedulingController.listSchedules);
router.put('/schedules/:id', reportSchedulingController.updateSchedule);
router.delete('/schedules/:id', reportSchedulingController.deleteSchedule);
router.get('/schedules-active', reportSchedulingController.getActiveSchedules);
router.post('/schedules/:id/execute', reportSchedulingController.executeSchedule);

// Report Distribution Routes
router.post('/distributions', reportDistributionController.createDistribution);
router.get('/distributions/:id', reportDistributionController.getDistribution);
router.get('/distributions', reportDistributionController.listDistributions);
router.put('/distributions/:id', reportDistributionController.updateDistribution);
router.delete('/distributions/:id', reportDistributionController.deleteDistribution);
router.get('/distributions/report/:reportId', reportDistributionController.getDistributionsByReport);
router.get('/distributions/status/:status', reportDistributionController.getDistributionsByStatus);
router.post('/distributions/:id/send', reportDistributionController.sendDistribution);
router.post('/distributions/:id/deliver', reportDistributionController.markAsDelivered);

module.exports = router;