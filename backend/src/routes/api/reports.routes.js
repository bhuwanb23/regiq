const express = require('express');
const reportController = require('../../controllers/api/reports.controller');

const router = express.Router();

// Report CRUD Endpoints
router.post('/', reportController.createReport);
router.get('/', reportController.listReports);

// Report Template Management Endpoints
router.post('/templates', reportController.createTemplate);
router.get('/templates', reportController.listTemplates);
router.get('/templates/:id', reportController.getTemplate);
router.put('/templates/:id', reportController.updateTemplate);
router.delete('/templates/:id', reportController.deleteTemplate);

// Report Scheduling Endpoints
router.post('/schedules', reportController.createSchedule);
router.get('/schedules', reportController.listSchedules);
router.get('/schedules/:id', reportController.getSchedule);
router.put('/schedules/:id', reportController.updateSchedule);
router.delete('/schedules/:id', reportController.deleteSchedule);
router.post('/schedules/:id/execute', reportController.executeSchedule);

// Report Generation Endpoint
router.post('/generate', reportController.generateReport);

// Report Export Endpoints
router.get('/:id/export/pdf', reportController.exportReportPdf);
router.get('/:id/export/csv', reportController.exportReportCsv);
router.get('/:id/export/json', reportController.exportReportJson);

// Individual Report Endpoints (must be last)
router.get('/:id', reportController.getReport);
router.put('/:id', reportController.updateReport);
router.delete('/:id', reportController.deleteReport);

// Report Generation Endpoint
router.post('/generate', reportController.generateReport);

// Report Export Endpoints
router.get('/:id/export/pdf', reportController.exportReportPdf);
router.get('/:id/export/csv', reportController.exportReportCsv);
router.get('/:id/export/json', reportController.exportReportJson);

// Report Template Management Endpoints
router.post('/templates', reportController.createTemplate);
router.get('/templates', reportController.listTemplates);
router.get('/templates/:id', reportController.getTemplate);
router.put('/templates/:id', reportController.updateTemplate);
router.delete('/templates/:id', reportController.deleteTemplate);

// Report Scheduling Endpoints
router.post('/schedules', reportController.createSchedule);
router.get('/schedules', reportController.listSchedules);
router.get('/schedules/:id', reportController.getSchedule);
router.put('/schedules/:id', reportController.updateSchedule);
router.delete('/schedules/:id', reportController.deleteSchedule);
router.post('/schedules/:id/execute', reportController.executeSchedule);

module.exports = router;