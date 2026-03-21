/**
 * Risk Simulation Service (api layer)
 * Bridges the Node.js backend to the Python risk_simulator AI/ML service.
 *
 * Monte Carlo, Bayesian, and stress testing all delegate to Python.
 * CRUD (simulation records, scenarios) hits Sequelize directly.
 */

const { RiskSimulation, RiskScenario } = require('../../models');
const aiMlClient  = require('../ai-ml.service');
const { endpoints } = require('../../config/ai-ml.config');

class RiskService {

  // ── Simulation CRUD ───────────────────────────────────────────────── //

  async createSimulation(simulationData) {
    try {
      const simulation = await RiskSimulation.create({
        ...simulationData,
        status:    'configured',
        createdAt: new Date(),
        updatedAt: new Date(),
      });
      return simulation;
    } catch (error) {
      throw new Error(`Failed to create simulation: ${error.message}`);
    }
  }

  async listSimulations(filters = {}) {
    try {
      const whereClause = {};
      if (filters.scenarioId) whereClause.scenarioId = filters.scenarioId;
      if (filters.status)     whereClause.status     = filters.status;

      return await RiskSimulation.findAll({
        where: whereClause,
        order: [['createdAt', 'DESC']],
        limit: parseInt(filters.limit) || 50,
      });
    } catch (error) {
      throw new Error(`Failed to list simulations: ${error.message}`);
    }
  }

  async getSimulation(simulationId) {
    try {
      const simulation = await RiskSimulation.findByPk(simulationId);
      if (!simulation) throw new Error('Risk simulation not found');
      return simulation;
    } catch (error) {
      throw new Error(`Failed to get simulation: ${error.message}`);
    }
  }

  async updateSimulation(simulationId, updateData) {
    try {
      const simulation = await RiskSimulation.findByPk(simulationId);
      if (!simulation) throw new Error('Risk simulation not found');
      await simulation.update(updateData);
      return simulation;
    } catch (error) {
      throw new Error(`Failed to update simulation: ${error.message}`);
    }
  }

  async deleteSimulation(simulationId) {
    try {
      const simulation = await RiskSimulation.findByPk(simulationId);
      if (!simulation) throw new Error('Risk simulation not found');
      await simulation.destroy();
      return { success: true, message: 'Risk simulation deleted successfully' };
    } catch (error) {
      throw new Error(`Failed to delete simulation: ${error.message}`);
    }
  }

  // ── Scenario CRUD ─────────────────────────────────────────────────── //

  async createScenario(scenarioData) {
    try {
      const scenario = await RiskScenario.create({
        ...scenarioData,
        isActive:  true,
        createdAt: new Date(),
        updatedAt: new Date(),
      });
      return scenario;
    } catch (error) {
      throw new Error(`Failed to create scenario: ${error.message}`);
    }
  }

  async listScenarios(filters = {}) {
    try {
      const whereClause = { isActive: true };
      if (filters.scenarioType) whereClause.scenarioType = filters.scenarioType;
      if (filters.severity)     whereClause.severity     = filters.severity;

      return await RiskScenario.findAll({
        where: whereClause,
        order: [['createdAt', 'DESC']],
        limit: parseInt(filters.limit) || 50,
      });
    } catch (error) {
      throw new Error(`Failed to list scenarios: ${error.message}`);
    }
  }

  async getScenario(scenarioId) {
    try {
      const scenario = await RiskScenario.findByPk(scenarioId);
      if (!scenario) throw new Error('Risk scenario not found');
      return scenario;
    } catch (error) {
      throw new Error(`Failed to get scenario: ${error.message}`);
    }
  }

  async updateScenario(scenarioId, updateData) {
    try {
      const scenario = await RiskScenario.findByPk(scenarioId);
      if (!scenario) throw new Error('Risk scenario not found');
      await scenario.update(updateData);
      return scenario;
    } catch (error) {
      throw new Error(`Failed to update scenario: ${error.message}`);
    }
  }

  async deleteScenario(scenarioId) {
    try {
      const scenario = await RiskScenario.findByPk(scenarioId);
      if (!scenario) throw new Error('Risk scenario not found');
      await scenario.update({ isActive: false });
      return { success: true, message: 'Risk scenario deactivated successfully' };
    } catch (error) {
      throw new Error(`Failed to delete scenario: ${error.message}`);
    }
  }

  // ── Monte Carlo (Python AI/ML) ────────────────────────────────────── //

  /**
   * Run a proper Monte Carlo simulation via the Python risk_simulator service.
   * Uses Latin Hypercube Sampling + regulatory framework parameters.
   */
  async runMonteCarloSimulation(simulationId) {
    try {
      const simulation = await RiskSimulation.findByPk(simulationId);
      if (!simulation) throw new Error('Risk simulation not found');

      // Mark as running
      await simulation.update({ status: 'running' });

      // Call Python Monte Carlo engine
      const aiResult = await aiMlClient.makeRequest(
        'POST',
        endpoints.risk.monteCarlo,
        {
          simulation_id:    simulationId,
          framework_id:     simulation.frameworkId     || 'eu_ai_act',
          n_simulations:    simulation.iterations      || 10000,
          sampling_method:  simulation.samplingMethod  || 'lhs',
          risk_factors:     simulation.riskFactors     || {},
          parameters:       simulation.parameters      || {},
        }
      );

      // Persist results
      const summaryStatistics = {
        mean:        aiResult.mean         ?? aiResult.statistics?.mean,
        median:      aiResult.median       ?? aiResult.statistics?.median,
        stdDev:      aiResult.std_dev      ?? aiResult.statistics?.std_dev,
        min:         aiResult.min          ?? aiResult.statistics?.min,
        max:         aiResult.max          ?? aiResult.statistics?.max,
        percentile5: aiResult.percentile_5 ?? aiResult.statistics?.p5,
        percentile95:aiResult.percentile_95 ?? aiResult.statistics?.p95,
        var95:       aiResult.var_95       ?? null,
        riskProbability: aiResult.risk_probability ?? null,
        confidenceInterval: aiResult.confidence_interval ?? null,
        expectedLoss:    aiResult.expected_loss ?? null,
      };

      await simulation.update({
        status:           'completed',
        summaryStatistics: summaryStatistics,
        results: {
          rawData:   aiResult.samples?.slice(0, 100) || [],
          histogram: aiResult.histogram || [],
          heatmap:   aiResult.heatmap   || null,
        },
      });

      return {
        simulationId:     simulation.id,
        summaryStatistics,
        message:          'Monte Carlo simulation completed successfully',
        source:           'python_ai_ml',
      };
    } catch (error) {
      // Mark as failed
      try {
        const sim = await RiskSimulation.findByPk(simulationId);
        if (sim) await sim.update({ status: 'failed' });
      } catch (_) {}
      throw new Error(`Failed to run Monte Carlo simulation: ${error.message}`);
    }
  }

  // ── Bayesian Inference (Python AI/ML) ─────────────────────────────── //

  async runBayesianSimulation(simulationData) {
    try {
      const aiResult = await aiMlClient.makeRequest(
        'POST',
        endpoints.risk.bayesian,
        simulationData
      );
      return {
        posteriorMean:      aiResult.posterior_mean,
        posteriorStd:       aiResult.posterior_std,
        credibleInterval:   aiResult.credible_interval,
        convergenceDiags:   aiResult.convergence_diagnostics,
        rPhat:              aiResult.r_hat,
        effectiveSampleSize: aiResult.effective_sample_size,
        source:             'python_ai_ml',
      };
    } catch (error) {
      throw new Error(`Failed to run Bayesian simulation: ${error.message}`);
    }
  }

  // ── Stress Testing (Python AI/ML) ─────────────────────────────────── //

  /**
   * Run stress tests via Python risk_simulator scenarios engine.
   */
  async runStressTest(testData) {
    try {
      const aiResult = await aiMlClient.makeRequest(
        'POST',
        endpoints.risk.stressTest,
        testData
      );

      return {
        summary: {
          totalScenarios:          aiResult.total_scenarios         ?? testData.scenarios?.length,
          totalBaseRisk:           aiResult.total_base_risk         ?? null,
          totalStressedRisk:       aiResult.total_stressed_risk     ?? null,
          overallImpact:           aiResult.overall_impact          ?? null,
          stressRatio:             aiResult.stress_ratio            ?? null,
          riskIncreasePercentage:  aiResult.risk_increase_pct       ?? null,
        },
        scenarioResults: aiResult.scenario_results ?? [],
        vulnerabilities: aiResult.vulnerabilities  ?? [],
        recommendations: aiResult.recommendations  ?? [],
        timestamp:       new Date(),
        source:          'python_ai_ml',
      };
    } catch (aiError) {
      // JS fallback for when Python service is not running
      const scenarios = testData.scenarios || [];
      const results   = scenarios.map(scenario => {
        const stressFactor  = scenario.stressFactor || 1.0;
        const baseRisk      = scenario.baseRisk      || 50;
        const stressedRisk  = Math.min(100, baseRisk * stressFactor);
        return {
          scenarioId:   scenario.id,
          scenarioName: scenario.name,
          baseRisk,
          stressFactor,
          stressedRisk:  parseFloat(stressedRisk.toFixed(2)),
          impact:        parseFloat((stressedRisk - baseRisk).toFixed(2)),
        };
      });

      const totalBase     = results.reduce((s, r) => s + r.baseRisk, 0);
      const totalStressed = results.reduce((s, r) => s + r.stressedRisk, 0);

      return {
        summary: {
          totalScenarios:         results.length,
          totalBaseRisk:          parseFloat(totalBase.toFixed(2)),
          totalStressedRisk:      parseFloat(totalStressed.toFixed(2)),
          overallImpact:          parseFloat((totalStressed - totalBase).toFixed(2)),
          stressRatio:            parseFloat((totalStressed / (totalBase || 1)).toFixed(2)),
          riskIncreasePercentage: parseFloat((((totalStressed - totalBase) / (totalBase || 1)) * 100).toFixed(2)),
        },
        scenarioResults: results,
        timestamp: new Date(),
        source:    'js_fallback',
        warning:   `Python AI/ML service unavailable: ${aiError.message}`,
      };
    }
  }

  // ── Regulatory Frameworks ─────────────────────────────────────────── //

  async getFrameworks() {
    try {
      return await aiMlClient.makeRequest('GET', endpoints.risk.frameworks);
    } catch (error) {
      throw new Error(`Failed to get regulatory frameworks: ${error.message}`);
    }
  }
}

module.exports = new RiskService();
