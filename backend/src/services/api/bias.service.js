/**
 * Bias Analysis Service (api layer)
 * Bridges the Node.js backend to the Python bias_analysis AI/ML service.
 *
 * Every method that requires AI computation calls the Python FastAPI service.
 * Database operations (CRUD) still hit Sequelize models directly.
 */

const {
  ModelAnalysis,
  DataBiasDetection,
  MitigationRecommendation,
  BiasResult,
  BiasTrend,
  ComparisonReport,
} = require('../../models');

const aiMlClient  = require('../ai-ml.service');
const { endpoints } = require('../../config/ai-ml.config');

class BiasService {

  // ── Bias Analysis ─────────────────────────────────────────────────── //

  /**
   * Run bias analysis via Python AI/ML service, then persist results.
   * @param {Object} analysisData - { modelFile, datasetFile, protectedAttributes, ... }
   */
  async analyzeBias(analysisData) {
    try {
      // 1. Call Python bias_analysis service
      const aiResult = await aiMlClient.makeRequest(
        'POST',
        endpoints.bias.analyze,
        analysisData
      );

      // 2. Persist to DB
      const analysis = await ModelAnalysis.create({
        modelId:            analysisData.modelId,
        datasetId:          analysisData.datasetId,
        protectedAttributes: analysisData.protectedAttributes,
        fairnessMetrics:    aiResult.fairness_metrics    || {},
        overallBiasScore:   aiResult.overall_bias_score  || 0,
        mitigationApplied:  aiResult.mitigation_applied  || null,
        shapValues:         aiResult.shap_values          || {},
        limeValues:         aiResult.lime_values          || {},
        status:             'completed',
        rawResult:          aiResult,
        createdAt:          new Date(),
        updatedAt:          new Date(),
      });

      return { ...analysis.toJSON(), aiResult };
    } catch (error) {
      throw new Error(`Failed to analyze bias: ${error.message}`);
    }
  }

  async listBiasAnalyses(filters = {}) {
    try {
      const whereClause = {};
      if (filters.modelId) whereClause.modelId = filters.modelId;
      if (filters.status)  whereClause.status  = filters.status;

      return await ModelAnalysis.findAll({
        where: whereClause,
        order: [['createdAt', 'DESC']],
        limit: parseInt(filters.limit) || 50,
      });
    } catch (error) {
      throw new Error(`Failed to list bias analyses: ${error.message}`);
    }
  }

  async getBiasAnalysis(analysisId) {
    try {
      const analysis = await ModelAnalysis.findByPk(analysisId);
      if (!analysis) throw new Error('Bias analysis not found');
      return analysis;
    } catch (error) {
      throw new Error(`Failed to get bias analysis: ${error.message}`);
    }
  }

  // ── Bias Scoring ──────────────────────────────────────────────────── //

  /**
   * Fetch real bias scores from Python service.
   * Falls back to last DB record if Python service is unavailable.
   */
  async getBiasScores(filters = {}) {
    try {
      // Try Python service first
      const aiResult = await aiMlClient.makeRequest(
        'POST',
        endpoints.bias.score,
        filters
      );

      return {
        demographicParity:  aiResult.demographic_parity  ?? aiResult.fairness_metrics?.demographic_parity,
        equalOpportunity:   aiResult.equalized_odds       ?? aiResult.fairness_metrics?.equalized_odds,
        disparateImpact:    aiResult.disparate_impact     ?? aiResult.fairness_metrics?.disparate_impact,
        statisticalParity:  aiResult.statistical_parity  ?? null,
        calibration:        aiResult.calibration          ?? aiResult.fairness_metrics?.calibration,
        consistencyScore:   aiResult.consistency_score   ?? null,
        overallBias:        aiResult.overall_bias_score  ?? null,
        source:             'python_ai_ml',
      };
    } catch (aiError) {
      // Fallback: return latest DB record if Python service is down
      const latest = await ModelAnalysis.findOne({
        order: [['createdAt', 'DESC']],
      });
      if (latest && latest.fairnessMetrics) {
        return { ...latest.fairnessMetrics, source: 'database_fallback' };
      }
      throw new Error(`Failed to get bias scores: ${aiError.message}`);
    }
  }

  // ── Fairness Metrics ──────────────────────────────────────────────── //

  async getFairnessMetrics(analysisId) {
    try {
      const aiResult = await aiMlClient.makeRequest(
        'GET',
        `${endpoints.bias.metrics}/${analysisId}`
      );
      return aiResult;
    } catch (error) {
      // Fall back to DB
      const analysis = await ModelAnalysis.findByPk(analysisId);
      if (!analysis) throw new Error('Analysis not found');
      return analysis.fairnessMetrics || {};
    }
  }

  // ── Mitigation ────────────────────────────────────────────────────── //

  async listMitigationStrategies(filters = {}) {
    try {
      const whereClause = {};
      if (filters.analysisId) whereClause.analysisId = filters.analysisId;

      return await MitigationRecommendation.findAll({
        where: whereClause,
        order: [['priority', 'ASC']],
        limit: parseInt(filters.limit) || 50,
      });
    } catch (error) {
      throw new Error(`Failed to list mitigation strategies: ${error.message}`);
    }
  }

  /**
   * Apply a mitigation technique via Python service (reweighting, threshold adjustment, etc.)
   */
  async applyMitigation(mitigationData) {
    try {
      const aiResult = await aiMlClient.makeRequest(
        'POST',
        endpoints.bias.mitigation,
        mitigationData
      );

      return {
        status:          'applied',
        technique:        mitigationData.technique       || 'unknown',
        beforeMetrics:    aiResult.before_metrics        || {},
        afterMetrics:     aiResult.after_metrics         || {},
        improvement:      aiResult.improvement           || {},
        modelPath:        aiResult.saved_model_path      || null,
        appliedAt:        new Date(),
        raw:              aiResult,
      };
    } catch (error) {
      throw new Error(`Failed to apply mitigation: ${error.message}`);
    }
  }

  async getMitiagationStrategy(strategyId) {
    try {
      const strategy = await MitigationRecommendation.findByPk(strategyId);
      if (!strategy) throw new Error('Mitigation strategy not found');
      return strategy;
    } catch (error) {
      throw new Error(`Failed to get mitigation strategy: ${error.message}`);
    }
  }

  // ── Explainability ────────────────────────────────────────────────── //

  async getExplanation(analysisId, explainerType = 'shap') {
    try {
      const aiResult = await aiMlClient.makeRequest(
        'POST',
        endpoints.bias.explain,
        { analysis_id: analysisId, explainer_type: explainerType }
      );
      return aiResult;
    } catch (error) {
      throw new Error(`Failed to get explanation: ${error.message}`);
    }
  }

  // ── Visualization ─────────────────────────────────────────────────── //

  /**
   * Get visualization data from Python BiasVisualizer.
   * Returns base64 PNG charts or structured JSON for frontend rendering.
   */
  async getVisualizationData(filters = {}) {
    try {
      const aiResult = await aiMlClient.makeRequest(
        'GET',
        endpoints.bias.visualize,
        null
      );

      return {
        fairnessMetricsChart:    aiResult.fairness_metrics_chart    || null,
        groupComparisonChart:    aiResult.group_comparison_chart    || null,
        mitigationComparisonChart: aiResult.mitigation_comparison_chart || null,
        featureImportanceChart:  aiResult.feature_importance_chart  || null,
        summaryDashboard:        aiResult.summary_dashboard         || null,
        source: 'python_ai_ml',
      };
    } catch (aiError) {
      // Fallback: return structured placeholder data for frontend
      return {
        biasOverTime: [
          { date: '2025-10-01', score: 0.72 },
          { date: '2025-11-01', score: 0.78 },
          { date: '2025-12-01', score: 0.82 },
          { date: '2026-01-01', score: 0.85 },
          { date: '2026-02-01', score: 0.87 },
        ],
        featureImportance: [
          { feature: 'credit_score',     importance: 0.38 },
          { feature: 'annual_income',    importance: 0.29 },
          { feature: 'loan_amount',      importance: 0.18 },
          { feature: 'employment_years', importance: 0.14 },
          { feature: 'age',              importance: 0.11 },
        ],
        groupDisparities: [
          { group: 'Male',   rate: 0.72 },
          { group: 'Female', rate: 0.68 },
        ],
        source: 'fallback',
        error: aiError.message,
      };
    }
  }

  // ── Model Upload ──────────────────────────────────────────────────── //

  async uploadModel(file, metadata) {
    try {
      return {
        id:           `model_${Date.now()}`,
        fileName:     file.filename,
        originalName: file.originalname,
        mimeType:     file.mimetype,
        size:         file.size,
        path:         file.path,
        ...metadata,
        uploadedAt:   new Date(),
      };
    } catch (error) {
      throw new Error(`Failed to upload model: ${error.message}`);
    }
  }

  // ── Reports ───────────────────────────────────────────────────────── //

  async listBiasReports(filters = {}) {
    try {
      const whereClause = {};
      if (filters.modelId) whereClause.modelId = filters.modelId;

      return await ComparisonReport.findAll({
        where: whereClause,
        order: [['createdAt', 'DESC']],
        limit: parseInt(filters.limit) || 50,
      });
    } catch (error) {
      throw new Error(`Failed to list bias reports: ${error.message}`);
    }
  }

  async getBiasReport(reportId) {
    try {
      const report = await ComparisonReport.findByPk(reportId);
      if (!report) throw new Error('Bias report not found');
      return report;
    } catch (error) {
      throw new Error(`Failed to get bias report: ${error.message}`);
    }
  }
}

module.exports = new BiasService();
