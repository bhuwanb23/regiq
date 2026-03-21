/**
 * Bias Analysis API Routes
 * Added: explainability, fairness metrics endpoints.
 */
const express          = require('express');
const biasController   = require('../../controllers/api/bias.controller');
const upload           = require('../../middleware/upload.middleware');

const router = express.Router();

// ── Bias Analysis ─────────────────────────────────────────────────────
router.post('/analysis',       biasController.analyzeBias);
router.get('/analysis',        biasController.listBiasAnalyses);
router.get('/analysis/:id',    biasController.getBiasAnalysis);

// ── Fairness Metrics ──────────────────────────────────────────────────
router.get('/analysis/:id/metrics', biasController.getFairnessMetrics);

// ── Explainability (SHAP / LIME) ──────────────────────────────────────
router.post('/explain',        biasController.getExplanation);

// ── Bias Reports ──────────────────────────────────────────────────────
router.get('/reports',         biasController.listBiasReports);
router.get('/reports/:id',     biasController.getBiasReport);

// ── Mitigation ────────────────────────────────────────────────────────
router.get('/mitigation',      biasController.listMitigationStrategies);
router.post('/mitigation',     biasController.applyMitigation);
router.get('/mitigation/:id',  biasController.getMitiagationStrategy);

// ── Model Upload ──────────────────────────────────────────────────────
router.post('/model-upload', upload.single('model'), biasController.uploadModel);

// ── Scoring & Visualization ───────────────────────────────────────────
router.get('/scoring',         biasController.getBiasScores);
router.get('/visualization',   biasController.getVisualizationData);
router.post('/visualization',  biasController.getVisualizationData);

module.exports = router;
