/**
 * Risk Simulation API Routes
 * Added: Bayesian simulation, regulatory frameworks endpoints.
 */
const express        = require('express');
const riskController = require('../../controllers/api/risk.controller');

const router = express.Router();

// ── Risk Simulation CRUD ────────────────────────────────────────────── //
router.post('/',       riskController.createSimulation);   // was /simulations
router.get('/',        riskController.listSimulations);

// ── Regulatory Frameworks (from Python registry) ────────────────────── //
// MUST be before /:id or Express will match 'frameworks' as an ID
router.get('/frameworks', riskController.getFrameworks);

router.get('/:id',     riskController.getSimulation);
router.put('/:id',     riskController.updateSimulation);
router.delete('/:id',  riskController.deleteSimulation);

// ── Simulation Execution ──────────────────────────────────────────────
router.post('/:id/monte-carlo', riskController.runMonteCarloSimulation);
router.post('/run/bayesian',    riskController.runBayesianSimulation);

// ── Stress Testing ────────────────────────────────────────────────────
router.post('/stress-test', riskController.runStressTest);

// ── Scenarios ─────────────────────────────────────────────────────────
router.post('/scenarios',          riskController.createScenario);
router.get('/scenarios',           riskController.listScenarios);
router.get('/scenarios/:id',       riskController.getScenario);
router.put('/scenarios/:id',       riskController.updateScenario);
router.delete('/scenarios/:id',    riskController.deleteScenario);

// ── Regulatory Frameworks (from Python registry) ──────────────────────
router.get('/frameworks', riskController.getFrameworks);

module.exports = router;
