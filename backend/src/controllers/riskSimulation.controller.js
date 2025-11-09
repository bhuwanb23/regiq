const riskSimulationService = require('../services/riskSimulation.service');

class RiskSimulationController {
  /**
   * Risk Scenario Creation Endpoints
   */
  async createRiskScenario(req, res) {
    try {
      // For testing without authentication, use a dummy user ID
      // Authorization will be added back later
      const scenario = await riskSimulationService.createRiskScenario(req.body, 'test-user-id');
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

  async getRiskScenario(req, res) {
    try {
      const { id } = req.params;
      const scenario = await riskSimulationService.getRiskScenario(id);
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

  async listRiskScenarios(req, res) {
    try {
      const scenarios = await riskSimulationService.listRiskScenarios(req.query);
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

  async updateRiskScenario(req, res) {
    try {
      const { id } = req.params;
      const scenario = await riskSimulationService.updateRiskScenario(id, req.body);
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

  async deleteRiskScenario(req, res) {
    try {
      const { id } = req.params;
      const result = await riskSimulationService.deleteRiskScenario(id);
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
   * Risk Simulation Execution Endpoints
   */
  async setupSimulation(req, res) {
    try {
      const simulation = await riskSimulationService.setupSimulation(req.body, 'test-user-id');
      res.status(201).json({
        success: true,
        message: 'Risk simulation configured successfully',
        data: simulation
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  async runSimulation(req, res) {
    try {
      const { id } = req.params;
      const simulation = await riskSimulationService.runSimulation(id);
      res.status(200).json({
        success: true,
        message: 'Risk simulation completed successfully',
        data: simulation
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
      const simulation = await riskSimulationService.getSimulation(id);
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

  async listSimulations(req, res) {
    try {
      const simulations = await riskSimulationService.listSimulations(req.query);
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

  /**
   * Risk Alert Generation Endpoints
   */
  async createRiskAlert(req, res) {
    try {
      const alert = await riskSimulationService.createRiskAlert(req.body);
      res.status(201).json({
        success: true,
        message: 'Risk alert created successfully',
        data: alert
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  async listRiskAlerts(req, res) {
    try {
      const alerts = await riskSimulationService.listRiskAlerts(req.query);
      res.status(200).json({
        success: true,
        data: alerts
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }

  async resolveRiskAlert(req, res) {
    try {
      const { id } = req.params;
      const alert = await riskSimulationService.resolveRiskAlert(id);
      res.status(200).json({
        success: true,
        message: 'Risk alert resolved successfully',
        data: alert
      });
    } catch (error) {
      res.status(404).json({
        success: false,
        message: error.message
      });
    }
  }

  /**
   * Risk Visualization Data Endpoints
   */
  async createVisualization(req, res) {
    try {
      const visualization = await riskSimulationService.createVisualization(req.body);
      res.status(201).json({
        success: true,
        message: 'Risk visualization created successfully',
        data: visualization
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  async getVisualization(req, res) {
    try {
      const { id } = req.params;
      const visualization = await riskSimulationService.getVisualization(id);
      res.status(200).json({
        success: true,
        data: visualization
      });
    } catch (error) {
      res.status(404).json({
        success: false,
        message: error.message
      });
    }
  }

  async listVisualizations(req, res) {
    try {
      const visualizations = await riskSimulationService.listVisualizations(req.query);
      res.status(200).json({
        success: true,
        data: visualizations
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }

  /**
   * Risk Comparison Functionality Endpoints
   */
  async compareSimulations(req, res) {
    try {
      const comparison = await riskSimulationService.compareSimulations(req.body);
      res.status(201).json({
        success: true,
        message: 'Risk comparison completed successfully',
        data: comparison
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  async getComparison(req, res) {
    try {
      const { id } = req.params;
      const comparison = await riskSimulationService.getComparison(id);
      res.status(200).json({
        success: true,
        data: comparison
      });
    } catch (error) {
      res.status(404).json({
        success: false,
        message: error.message
      });
    }
  }

  async listComparisons(req, res) {
    try {
      const comparisons = await riskSimulationService.listComparisons(req.query);
      res.status(200).json({
        success: true,
        data: comparisons
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }

  /**
   * Risk Simulation Scheduling Endpoints
   */
  async scheduleSimulation(req, res) {
    try {
      const schedule = await riskSimulationService.scheduleSimulation(req.body);
      res.status(201).json({
        success: true,
        message: 'Risk simulation scheduled successfully',
        data: schedule
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  async listSchedules(req, res) {
    try {
      const schedules = await riskSimulationService.listSchedules(req.query);
      res.status(200).json({
        success: true,
        data: schedules
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }

  async updateSchedule(req, res) {
    try {
      const { id } = req.params;
      const schedule = await riskSimulationService.updateSchedule(id, req.body);
      res.status(200).json({
        success: true,
        message: 'Risk schedule updated successfully',
        data: schedule
      });
    } catch (error) {
      res.status(404).json({
        success: false,
        message: error.message
      });
    }
  }

  async deleteSchedule(req, res) {
    try {
      const { id } = req.params;
      const result = await riskSimulationService.deleteSchedule(id);
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
}

module.exports = new RiskSimulationController();