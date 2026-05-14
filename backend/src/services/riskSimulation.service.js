const {
  RiskSimulation,
  RiskScenario,
  RiskAlert,
  RiskVisualization,
  RiskSchedule,
  RiskComparison
} = require('../models');

let aiMlService;
try {
  aiMlService = require('./ai-ml.service');
} catch (err) {
  aiMlService = null;
}

class RiskSimulationService {
  /**
   * Risk Scenario Creation
   */
  async createRiskScenario(scenarioData, userId) {
    try {
      const scenario = await RiskScenario.create({
        ...scenarioData,
        createdBy: userId
      });
      return scenario;
    } catch (error) {
      throw new Error(`Failed to create risk scenario: ${error.message}`);
    }
  }

  async getRiskScenario(scenarioId) {
    try {
      const scenario = await RiskScenario.findByPk(scenarioId);
      if (!scenario) {
        throw new Error('Risk scenario not found');
      }
      return scenario;
    } catch (error) {
      throw new Error(`Failed to get risk scenario: ${error.message}`);
    }
  }

  async listRiskScenarios(filters = {}) {
    try {
      const whereClause = {};
      
      if (filters.scenarioType) {
        whereClause.scenarioType = filters.scenarioType;
      }
      
      if (filters.severity) {
        whereClause.severity = filters.severity;
      }
      
      if (filters.isActive !== undefined) {
        whereClause.isActive = filters.isActive;
      }
      
      const scenarios = await RiskScenario.findAll({
        where: whereClause,
        order: [['createdAt', 'DESC']],
        limit: filters.limit || 50
      });
      
      return scenarios;
    } catch (error) {
      throw new Error(`Failed to list risk scenarios: ${error.message}`);
    }
  }

  async updateRiskScenario(scenarioId, updateData) {
    try {
      const scenario = await RiskScenario.findByPk(scenarioId);
      if (!scenario) {
        throw new Error('Risk scenario not found');
      }
      
      await scenario.update(updateData);
      return scenario;
    } catch (error) {
      throw new Error(`Failed to update risk scenario: ${error.message}`);
    }
  }

  async deleteRiskScenario(scenarioId) {
    try {
      const scenario = await RiskScenario.findByPk(scenarioId);
      if (!scenario) {
        throw new Error('Risk scenario not found');
      }
      
      await scenario.destroy();
      return { success: true, message: 'Risk scenario deleted successfully' };
    } catch (error) {
      throw new Error(`Failed to delete risk scenario: ${error.message}`);
    }
  }

  /**
   * Risk Simulation Execution
   */
  async setupSimulation(simulationData, userId) {
    try {
      const simulation = await RiskSimulation.create({
        ...simulationData,
        status: 'configured'
      });
      return simulation;
    } catch (error) {
      throw new Error(`Failed to setup risk simulation: ${error.message}`);
    }
  }

  async runSimulation(simulationId) {
    const simulation = await RiskSimulation.findByPk(simulationId);
    if (!simulation) {
      throw new Error('Risk simulation not found');
    }

    try {
      await simulation.update({ status: 'running' });

      // Delegate the actual numerical work to the FastAPI risk-simulator.
      // `aiMlService.assessRisk` walks the /setup → /run flow and returns
      // the raw service payload, which we map into our DB schema.
      let assessment = null;
      if (aiMlService && typeof aiMlService.assessRisk === 'function') {
        try {
          assessment = await aiMlService.assessRisk({
            simulation_id: simulation.id,
            scenario_id: simulation.scenarioId,
            parameters: simulation.parameters || {},
            sampling_method: simulation.samplingMethod || 'monte_carlo',
            num_iterations: simulation.numIterations || 10000,
          });
        } catch (svcErr) {
          // Surface, but allow a graceful degradation below.
          assessment = { error: svcErr.message };
        }
      }

      // Normalize the FastAPI payload (run.results may be on either branch).
      const exec = (assessment && assessment.execution) || {};
      const rawResults = exec.results || exec.result || {};
      const rawStats = exec.summary_statistics || exec.statistics || {};

      const results = {
        riskScore: Number(
          rawResults.risk_score ??
            rawResults.riskScore ??
            (typeof exec.var_95 === 'number' ? exec.var_95 : 0)
        ),
        confidence: Number(
          rawResults.confidence ?? exec.confidence ?? 0
        ),
        metrics: rawResults.metrics || {
          valueAtRisk: Number(exec.value_at_risk || exec.var_95 || 0),
          expectedShortfall: Number(exec.expected_shortfall || exec.es_95 || 0),
          volatility: Number(exec.volatility || 0),
        },
        raw: rawResults,
      };

      const summaryStatistics = Object.keys(rawStats).length
        ? rawStats
        : {
            mean: Number(exec.mean || 0),
            median: Number(exec.median || 0),
            stdDev: Number(exec.std_dev || exec.stdDev || 0),
            percentiles: exec.percentiles || {},
          };

      await simulation.update({
        status: assessment && !assessment.error ? 'completed' : 'failed',
        results,
        summaryStatistics,
      });

      return simulation;
    } catch (error) {
      try {
        await simulation.update({ status: 'failed' });
      } catch (_) {
        /* swallow */
      }
      throw new Error(`Failed to run risk simulation: ${error.message}`);
    }
  }

  async getSimulation(simulationId) {
    try {
      const simulation = await RiskSimulation.findByPk(simulationId);
      if (!simulation) {
        throw new Error('Risk simulation not found');
      }
      return simulation;
    } catch (error) {
      throw new Error(`Failed to get risk simulation: ${error.message}`);
    }
  }

  async listSimulations(filters = {}) {
    try {
      const whereClause = {};
      
      if (filters.scenarioId) {
        whereClause.scenarioId = filters.scenarioId;
      }
      
      if (filters.status) {
        whereClause.status = filters.status;
      }
      
      const simulations = await RiskSimulation.findAll({
        where: whereClause,
        order: [['createdAt', 'DESC']],
        limit: filters.limit || 50
      });
      
      return simulations;
    } catch (error) {
      throw new Error(`Failed to list risk simulations: ${error.message}`);
    }
  }

  /**
   * Risk Alert Generation
   */
  async createRiskAlert(alertData) {
    try {
      const alert = await RiskAlert.create({
        ...alertData,
        triggeredAt: new Date()
      });
      return alert;
    } catch (error) {
      throw new Error(`Failed to create risk alert: ${error.message}`);
    }
  }

  async listRiskAlerts(filters = {}) {
    try {
      const whereClause = {};
      
      if (filters.alertType) {
        whereClause.alertType = filters.alertType;
      }
      
      if (filters.severity) {
        whereClause.severity = filters.severity;
      }
      
      if (filters.isActive !== undefined) {
        whereClause.isActive = filters.isActive;
      }
      
      const alerts = await RiskAlert.findAll({
        where: whereClause,
        order: [['triggeredAt', 'DESC']],
        limit: filters.limit || 50
      });
      
      return alerts;
    } catch (error) {
      throw new Error(`Failed to list risk alerts: ${error.message}`);
    }
  }

  async resolveRiskAlert(alertId) {
    try {
      const alert = await RiskAlert.findByPk(alertId);
      if (!alert) {
        throw new Error('Risk alert not found');
      }
      
      await alert.update({
        isActive: false,
        resolvedAt: new Date()
      });
      
      return alert;
    } catch (error) {
      throw new Error(`Failed to resolve risk alert: ${error.message}`);
    }
  }

  /**
   * Risk Visualization Data
   */
  async createVisualization(visualizationData) {
    try {
      const visualization = await RiskVisualization.create(visualizationData);
      return visualization;
    } catch (error) {
      throw new Error(`Failed to create risk visualization: ${error.message}`);
    }
  }

  async getVisualization(visualizationId) {
    try {
      const visualization = await RiskVisualization.findByPk(visualizationId);
      if (!visualization) {
        throw new Error('Risk visualization not found');
      }
      return visualization;
    } catch (error) {
      throw new Error(`Failed to get risk visualization: ${error.message}`);
    }
  }

  async listVisualizations(filters = {}) {
    try {
      const whereClause = {};
      
      if (filters.simulationId) {
        whereClause.simulationId = filters.simulationId;
      }
      
      if (filters.visualizationType) {
        whereClause.visualizationType = filters.visualizationType;
      }
      
      const visualizations = await RiskVisualization.findAll({
        where: whereClause,
        order: [['createdAt', 'DESC']],
        limit: filters.limit || 50
      });
      
      return visualizations;
    } catch (error) {
      throw new Error(`Failed to list risk visualizations: ${error.message}`);
    }
  }

  /**
   * Risk Comparison Functionality
   */
  async compareSimulations(comparisonData) {
    try {
      // TODO: Implement actual comparison logic
      // For now, we'll create a placeholder
      const comparison = await RiskComparison.create({
        ...comparisonData,
        status: 'completed'
      });
      return comparison;
    } catch (error) {
      throw new Error(`Failed to compare risk simulations: ${error.message}`);
    }
  }

  async getComparison(comparisonId) {
    try {
      const comparison = await RiskComparison.findByPk(comparisonId);
      if (!comparison) {
        throw new Error('Risk comparison not found');
      }
      return comparison;
    } catch (error) {
      throw new Error(`Failed to get risk comparison: ${error.message}`);
    }
  }

  async listComparisons(filters = {}) {
    try {
      const whereClause = {};
      
      if (filters.status) {
        whereClause.status = filters.status;
      }
      
      const comparisons = await RiskComparison.findAll({
        where: whereClause,
        order: [['createdAt', 'DESC']],
        limit: filters.limit || 50
      });
      
      return comparisons;
    } catch (error) {
      throw new Error(`Failed to list risk comparisons: ${error.message}`);
    }
  }

  /**
   * Risk Simulation Scheduling
   */
  async scheduleSimulation(scheduleData) {
    try {
      const schedule = await RiskSchedule.create({
        ...scheduleData,
        nextRunTime: scheduleData.cronExpression ? this.calculateNextRun(scheduleData.cronExpression) : null
      });
      return schedule;
    } catch (error) {
      throw new Error(`Failed to schedule risk simulation: ${error.message}`);
    }
  }

  async listSchedules(filters = {}) {
    try {
      const whereClause = {};
      
      if (filters.scheduleType) {
        whereClause.scheduleType = filters.scheduleType;
      }
      
      if (filters.isActive !== undefined) {
        whereClause.isActive = filters.isActive;
      }
      
      const schedules = await RiskSchedule.findAll({
        where: whereClause,
        order: [['createdAt', 'DESC']],
        limit: filters.limit || 50
      });
      
      return schedules;
    } catch (error) {
      throw new Error(`Failed to list risk schedules: ${error.message}`);
    }
  }

  async updateSchedule(scheduleId, updateData) {
    try {
      const schedule = await RiskSchedule.findByPk(scheduleId);
      if (!schedule) {
        throw new Error('Risk schedule not found');
      }
      
      await schedule.update(updateData);
      return schedule;
    } catch (error) {
      throw new Error(`Failed to update risk schedule: ${error.message}`);
    }
  }

  async deleteSchedule(scheduleId) {
    try {
      const schedule = await RiskSchedule.findByPk(scheduleId);
      if (!schedule) {
        throw new Error('Risk schedule not found');
      }
      
      await schedule.destroy();
      return { success: true, message: 'Risk schedule deleted successfully' };
    } catch (error) {
      throw new Error(`Failed to delete risk schedule: ${error.message}`);
    }
  }

  // Helper method to calculate next run time from cron expression
  calculateNextRun(cronExpression) {
    // TODO: Implement proper cron parsing
    // For now, return a future date
    const now = new Date();
    return new Date(now.getTime() + 24 * 60 * 60 * 1000); // 24 hours from now
  }
}

module.exports = new RiskSimulationService();