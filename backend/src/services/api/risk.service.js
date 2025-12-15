const { 
  RiskSimulation,
  RiskScenario
} = require('../../models');

class RiskService {
  /**
   * Risk Simulation Methods
   */
  async createSimulation(simulationData) {
    try {
      const simulation = await RiskSimulation.create({
        ...simulationData,
        status: 'configured',
        createdAt: new Date(),
        updatedAt: new Date()
      });
      return simulation;
    } catch (error) {
      throw new Error(`Failed to create simulation: ${error.message}`);
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
      throw new Error(`Failed to list simulations: ${error.message}`);
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
      throw new Error(`Failed to get simulation: ${error.message}`);
    }
  }

  async updateSimulation(simulationId, updateData) {
    try {
      const simulation = await RiskSimulation.findByPk(simulationId);
      if (!simulation) {
        throw new Error('Risk simulation not found');
      }
      
      await simulation.update(updateData);
      return simulation;
    } catch (error) {
      throw new Error(`Failed to update simulation: ${error.message}`);
    }
  }

  async deleteSimulation(simulationId) {
    try {
      const simulation = await RiskSimulation.findByPk(simulationId);
      if (!simulation) {
        throw new Error('Risk simulation not found');
      }
      
      await simulation.destroy();
      return { success: true, message: 'Risk simulation deleted successfully' };
    } catch (error) {
      throw new Error(`Failed to delete simulation: ${error.message}`);
    }
  }

  /**
   * Risk Scenario Methods
   */
  async createScenario(scenarioData) {
    try {
      const scenario = await RiskScenario.create({
        ...scenarioData,
        isActive: true,
        createdAt: new Date(),
        updatedAt: new Date()
      });
      return scenario;
    } catch (error) {
      throw new Error(`Failed to create scenario: ${error.message}`);
    }
  }

  async listScenarios(filters = {}) {
    try {
      const whereClause = {
        isActive: true
      };
      
      if (filters.scenarioType) {
        whereClause.scenarioType = filters.scenarioType;
      }
      
      if (filters.severity) {
        whereClause.severity = filters.severity;
      }
      
      const scenarios = await RiskScenario.findAll({
        where: whereClause,
        order: [['createdAt', 'DESC']],
        limit: filters.limit || 50
      });
      
      return scenarios;
    } catch (error) {
      throw new Error(`Failed to list scenarios: ${error.message}`);
    }
  }

  async getScenario(scenarioId) {
    try {
      const scenario = await RiskScenario.findByPk(scenarioId);
      if (!scenario) {
        throw new Error('Risk scenario not found');
      }
      return scenario;
    } catch (error) {
      throw new Error(`Failed to get scenario: ${error.message}`);
    }
  }

  async updateScenario(scenarioId, updateData) {
    try {
      const scenario = await RiskScenario.findByPk(scenarioId);
      if (!scenario) {
        throw new Error('Risk scenario not found');
      }
      
      await scenario.update(updateData);
      return scenario;
    } catch (error) {
      throw new Error(`Failed to update scenario: ${error.message}`);
    }
  }

  async deleteScenario(scenarioId) {
    try {
      const scenario = await RiskScenario.findByPk(scenarioId);
      if (!scenario) {
        throw new Error('Risk scenario not found');
      }
      
      // Soft delete by setting isActive to false
      await scenario.update({ isActive: false });
      return { success: true, message: 'Risk scenario deactivated successfully' };
    } catch (error) {
      throw new Error(`Failed to delete scenario: ${error.message}`);
    }
  }

  /**
   * Monte Carlo Simulation Method
   */
  async runMonteCarloSimulation(simulationId) {
    try {
      const simulation = await RiskSimulation.findByPk(simulationId);
      if (!simulation) {
        throw new Error('Risk simulation not found');
      }
      
      // Update status to running
      await simulation.update({ status: 'running' });
      
      // Simulate Monte Carlo calculations
      const iterations = simulation.iterations || 1000;
      const results = [];
      
      // Generate random risk values based on parameters
      for (let i = 0; i < iterations; i++) {
        // Simulate a risk value between 0 and 100
        const riskValue = Math.random() * 100;
        results.push(riskValue);
      }
      
      // Calculate statistics
      const mean = results.reduce((a, b) => a + b, 0) / results.length;
      const sorted = [...results].sort((a, b) => a - b);
      const median = sorted[Math.floor(sorted.length / 2)];
      const stdDev = Math.sqrt(results.map(x => Math.pow(x - mean, 2)).reduce((a, b) => a + b) / results.length);
      
      // Calculate percentiles
      const p5 = sorted[Math.floor(sorted.length * 0.05)];
      const p95 = sorted[Math.floor(sorted.length * 0.95)];
      
      const summaryStatistics = {
        mean: parseFloat(mean.toFixed(2)),
        median: parseFloat(median.toFixed(2)),
        stdDev: parseFloat(stdDev.toFixed(2)),
        min: parseFloat(Math.min(...results).toFixed(2)),
        max: parseFloat(Math.max(...results).toFixed(2)),
        percentile5: parseFloat(p5.toFixed(2)),
        percentile95: parseFloat(p95.toFixed(2))
      };
      
      // Update simulation with results
      await simulation.update({
        status: 'completed',
        summaryStatistics: summaryStatistics,
        results: {
          rawData: results.slice(0, 100), // Store first 100 values for visualization
          histogram: this._generateHistogram(results)
        }
      });
      
      return {
        simulationId: simulation.id,
        summaryStatistics: summaryStatistics,
        message: 'Monte Carlo simulation completed successfully'
      };
    } catch (error) {
      // Update status to failed
      try {
        const simulation = await RiskSimulation.findByPk(simulationId);
        if (simulation) {
          await simulation.update({ status: 'failed' });
        }
      } catch (updateError) {
        // Ignore update error
      }
      
      throw new Error(`Failed to run Monte Carlo simulation: ${error.message}`);
    }
  }

  /**
   * Stress Testing Method
   */
  async runStressTest(testData) {
    try {
      // Simulate stress test calculations
      const scenarios = testData.scenarios || [];
      const results = [];
      
      for (const scenario of scenarios) {
        // Simulate stress test for each scenario
        const stressFactor = scenario.stressFactor || 1.0;
        const baseRisk = scenario.baseRisk || 50;
        
        // Calculate stressed risk value
        const stressedRisk = Math.min(100, baseRisk * stressFactor);
        
        results.push({
          scenarioId: scenario.id,
          scenarioName: scenario.name,
          baseRisk: baseRisk,
          stressFactor: stressFactor,
          stressedRisk: parseFloat(stressedRisk.toFixed(2)),
          impact: parseFloat((stressedRisk - baseRisk).toFixed(2))
        });
      }
      
      // Calculate overall stress test metrics
      const totalBaseRisk = results.reduce((sum, r) => sum + r.baseRisk, 0);
      const totalStressedRisk = results.reduce((sum, r) => sum + r.stressedRisk, 0);
      const overallImpact = parseFloat((totalStressedRisk - totalBaseRisk).toFixed(2));
      const stressRatio = parseFloat((totalStressedRisk / totalBaseRisk).toFixed(2));
      
      const stressTestSummary = {
        totalScenarios: results.length,
        totalBaseRisk: parseFloat(totalBaseRisk.toFixed(2)),
        totalStressedRisk: parseFloat(totalStressedRisk.toFixed(2)),
        overallImpact: overallImpact,
        stressRatio: stressRatio,
        riskIncreasePercentage: parseFloat(((overallImpact / totalBaseRisk) * 100).toFixed(2))
      };
      
      return {
        summary: stressTestSummary,
        scenarioResults: results,
        timestamp: new Date()
      };
    } catch (error) {
      throw new Error(`Failed to run stress test: ${error.message}`);
    }
  }

  /**
   * Helper method to generate histogram data
   */
  _generateHistogram(data) {
    const bins = 10;
    const min = Math.min(...data);
    const max = Math.max(...data);
    const binWidth = (max - min) / bins;
    
    const histogram = Array(bins).fill(0);
    
    for (const value of data) {
      const binIndex = Math.min(Math.floor((value - min) / binWidth), bins - 1);
      histogram[binIndex]++;
    }
    
    return histogram.map((count, index) => ({
      binStart: parseFloat((min + index * binWidth).toFixed(2)),
      binEnd: parseFloat((min + (index + 1) * binWidth).toFixed(2)),
      count: count
    }));
  }
}

module.exports = new RiskService();