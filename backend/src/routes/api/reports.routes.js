/**
 * Reports API Routes
 * Fixed: removed duplicate route definitions that existed in original file.
 * Each route is defined exactly once.
 */
const express        = require('express');
const reportController = require('../../controllers/api/reports.controller');

const router = express.Router();

// ── Report CRUD ───────────────────────────────────────────────────────
router.post('/',     reportController.createReport);
router.get('/',      reportController.listReports);

// ── Report Generation (AI/ML) ─────────────────────────────────────────
router.post('/generate', reportController.generateReport);

// ── Report Templates ──────────────────────────────────────────────────
router.post('/templates',      reportController.createTemplate);
router.get('/templates',       reportController.listTemplates);
router.get('/templates/:id',   reportController.getTemplate);
router.put('/templates/:id',   reportController.updateTemplate);
router.delete('/templates/:id',reportController.deleteTemplate);

// ── Report Schedules ──────────────────────────────────────────────────
router.post('/schedules',           reportController.createSchedule);
router.get('/schedules',            reportController.listSchedules);
router.get('/schedules/:id',        reportController.getSchedule);
router.put('/schedules/:id',        reportController.updateSchedule);
router.delete('/schedules/:id',     reportController.deleteSchedule);
router.post('/schedules/:id/execute', reportController.executeSchedule);

// ── Individual Report + Exports (must come AFTER named sub-routes) ────
router.get('/:id',              reportController.getReport);
router.put('/:id',              reportController.updateReport);
router.delete('/:id',           reportController.deleteReport);
router.get('/:id/export/pdf',   reportController.exportReportPdf);
router.get('/:id/export/csv',   reportController.exportReportCsv);
router.get('/:id/export/json',  reportController.exportReportJson);

// Glossary endpoint
router.get('/glossary',         reportController.getGlossary);

module.exports = router;
