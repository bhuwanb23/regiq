const express = require('express');
const riskController = require('../../controllers/api/risk.controller');

const router = express.Router();

// Risk Simulation Endpoints
router.post('/simulations', riskController.createSimulation);
router.get('/simulations', riskController.listSimulations);
router.get('/simulations/:id', riskController.getSimulation);
router.put('/simulations/:id', riskController.updateSimulation);
router.delete('/simulations/:id', riskController.deleteSimulation);

// Risk Scenario Endpoints
router.post('/scenarios', riskController.createScenario);
router.get('/scenarios', riskController.listScenarios);
router.get('/scenarios/:id', riskController.getScenario);
router.put('/scenarios/:id', riskController.updateScenario);
router.delete('/scenarios/:id', riskController.deleteScenario);

// Monte Carlo Simulation Trigger
router.post('/simulations/:id/monte-carlo', riskController.runMonteCarloSimulation);

// Stress Testing Endpoint
router.post('/stress-test', riskController.runStressTest);

module.exports = router;