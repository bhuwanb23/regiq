/**
 * Risk Simulation API Routes
 * Added: Bayesian simulation, regulatory frameworks endpoints.
 */
const express        = require('express');
const riskController = require('../../controllers/api/risk.controller');

const router = express.Router();

// ── Risk Simulation CRUD ────────────────────────────────────────────── //
router.post('/',       riskController.createSimulation);
router.get('/',        riskController.listSimulations);

// ── Regulatory Frameworks (from Python registry) ────────────────────── //
// MUST be before /:id or Express will match 'frameworks' as an ID
router.get('/frameworks', riskController.getFrameworks);

// ── Scenarios ─────────────────────────────────────────────────────────
// MUST be before /:id or Express will match 'scenarios' as an ID
router.post('/scenarios',          riskController.createScenario);
router.get('/scenarios',           riskController.listScenarios);
router.get('/scenarios/:id',       riskController.getScenario);
router.put('/scenarios/:id',       riskController.updateScenario);
router.delete('/scenarios/:id',    riskController.deleteScenario);

// ── Simulation Execution ──────────────────────────────────────────────
// These must come after specific routes but before /:id
router.post('/run/bayesian',    riskController.runBayesianSimulation);
router.post('/stress-test',     riskController.runStressTest);
router.post('/:id/monte-carlo', riskController.runMonteCarloSimulation);

// ── Parameterized Routes (MUST come last) ───────────────────────────────
router.get('/:id',     riskController.getSimulation);
router.put('/:id',     riskController.updateSimulation);
router.delete('/:id',  riskController.deleteSimulation);

module.exports = router;
