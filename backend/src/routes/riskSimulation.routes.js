const express = require('express');
const riskSimulationController = require('../controllers/riskSimulation.controller');

const router = express.Router();

// Risk Scenario Creation Endpoints
router.post('/scenarios', riskSimulationController.createRiskScenario);
router.get('/scenarios/:id', riskSimulationController.getRiskScenario);
router.get('/scenarios', riskSimulationController.listRiskScenarios);
router.put('/scenarios/:id', riskSimulationController.updateRiskScenario);
router.delete('/scenarios/:id', riskSimulationController.deleteRiskScenario);

// Risk Simulation Execution Endpoints
router.post('/simulations', riskSimulationController.setupSimulation);
router.post('/simulations/:id/run', riskSimulationController.runSimulation);
router.get('/simulations/:id', riskSimulationController.getSimulation);
router.get('/simulations', riskSimulationController.listSimulations);

// Risk Alert Generation Endpoints
router.post('/alerts', riskSimulationController.createRiskAlert);
router.get('/alerts', riskSimulationController.listRiskAlerts);
router.post('/alerts/:id/resolve', riskSimulationController.resolveRiskAlert);

// Risk Visualization Data Endpoints
router.post('/visualizations', riskSimulationController.createVisualization);
router.get('/visualizations/:id', riskSimulationController.getVisualization);
router.get('/visualizations', riskSimulationController.listVisualizations);

// Risk Comparison Functionality Endpoints
router.post('/comparisons', riskSimulationController.compareSimulations);
router.get('/comparisons/:id', riskSimulationController.getComparison);
router.get('/comparisons', riskSimulationController.listComparisons);

// Risk Simulation Scheduling Endpoints
router.post('/schedules', riskSimulationController.scheduleSimulation);
router.get('/schedules', riskSimulationController.listSchedules);
router.put('/schedules/:id', riskSimulationController.updateSchedule);
router.delete('/schedules/:id', riskSimulationController.deleteSchedule);

module.exports = router;