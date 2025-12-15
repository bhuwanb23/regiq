const riskService = require('../../services/api/risk.service');

class RiskController {
  /**
   * Risk Simulation Endpoints
   */
  async createSimulation(req, res) {
    try {
      const simulation = await riskService.createSimulation(req.body);
      res.status(201).json({
        success: true,
        message: 'Risk simulation created successfully',
        data: simulation
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  async listSimulations(req, res) {
    try {
      const simulations = await riskService.listSimulations(req.query);
      res.status(200).json({
        success: true,
        data: simulations
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }

  async getSimulation(req, res) {
    try {
      const { id } = req.params;
      const simulation = await riskService.getSimulation(id);
      res.status(200).json({
        success: true,
        data: simulation
      });
    } catch (error) {
      res.status(404).json({
        success: false,
        message: error.message
      });
    }
  }

  async updateSimulation(req, res) {
    try {
      const { id } = req.params;
      const simulation = await riskService.updateSimulation(id, req.body);
      res.status(200).json({
        success: true,
        message: 'Risk simulation updated successfully',
        data: simulation
      });
    } catch (error) {
      res.status(404).json({
        success: false,
        message: error.message
      });
    }
  }

  async deleteSimulation(req, res) {
    try {
      const { id } = req.params;
      const result = await riskService.deleteSimulation(id);
      res.status(200).json({
        success: true,
        message: result.message
      });
    } catch (error) {
      res.status(404).json({
        success: false,
        message: error.message
      });
    }
  }

  /**
   * Risk Scenario Endpoints
   */
  async createScenario(req, res) {
    try {
      const scenario = await riskService.createScenario(req.body);
      res.status(201).json({
        success: true,
        message: 'Risk scenario created successfully',
        data: scenario
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  async listScenarios(req, res) {
    try {
      const scenarios = await riskService.listScenarios(req.query);
      res.status(200).json({
        success: true,
        data: scenarios
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }

  async getScenario(req, res) {
    try {
      const { id } = req.params;
      const scenario = await riskService.getScenario(id);
      res.status(200).json({
        success: true,
        data: scenario
      });
    } catch (error) {
      res.status(404).json({
        success: false,
        message: error.message
      });
    }
  }

  async updateScenario(req, res) {
    try {
      const { id } = req.params;
      const scenario = await riskService.updateScenario(id, req.body);
      res.status(200).json({
        success: true,
        message: 'Risk scenario updated successfully',
        data: scenario
      });
    } catch (error) {
      res.status(404).json({
        success: false,
        message: error.message
      });
    }
  }

  async deleteScenario(req, res) {
    try {
      const { id } = req.params;
      const result = await riskService.deleteScenario(id);
      res.status(200).json({
        success: true,
        message: result.message
      });
    } catch (error) {
      res.status(404).json({
        success: false,
        message: error.message
      });
    }
  }

  /**
   * Monte Carlo Simulation Trigger
   */
  async runMonteCarloSimulation(req, res) {
    try {
      const { id } = req.params;
      const result = await riskService.runMonteCarloSimulation(id);
      res.status(200).json({
        success: true,
        message: 'Monte Carlo simulation completed successfully',
        data: result
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }

  /**
   * Stress Testing Endpoint
   */
  async runStressTest(req, res) {
    try {
      const result = await riskService.runStressTest(req.body);
      res.status(200).json({
        success: true,
        message: 'Stress test completed successfully',
        data: result
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }
}

module.exports = new RiskController();