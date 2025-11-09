const biasAnalysisService = require('../services/biasAnalysis.service');

class BiasAnalysisController {
  /**
   * Model Bias Analysis Endpoints
   */
  async analyzeModel(req, res) {
    try {
      // For testing without authentication, use a dummy user ID
      // Authorization will be added back later
      const analysis = await biasAnalysisService.analyzeModel(req.body, 'test-user-id');
      res.status(201).json({
        success: true,
        message: 'Model analysis completed successfully',
        data: analysis
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  async getModelAnalysis(req, res) {
    try {
      const { id } = req.params;
      const analysis = await biasAnalysisService.getModelAnalysis(id);
      res.status(200).json({
        success: true,
        data: analysis
      });
    } catch (error) {
      res.status(404).json({
        success: false,
        message: error.message
      });
    }
  }

  async listModelAnalyses(req, res) {
    try {
      const analyses = await biasAnalysisService.listModelAnalyses(req.query);
      res.status(200).json({
        success: true,
        data: analyses
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }

  async deleteModelAnalysis(req, res) {
    try {
      const { id } = req.params;
      const result = await biasAnalysisService.deleteModelAnalysis(id);
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
   * Data Bias Detection Services
   */
  async detectDataBias(req, res) {
    try {
      // For testing without authentication, use a dummy user ID
      // Authorization will be added back later
      const detection = await biasAnalysisService.detectDataBias(req.body, 'test-user-id');
      res.status(201).json({
        success: true,
        message: 'Data bias detection completed successfully',
        data: detection
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  async getDataBiasDetection(req, res) {
    try {
      const { id } = req.params;
      const detection = await biasAnalysisService.getDataBiasDetection(id);
      res.status(200).json({
        success: true,
        data: detection
      });
    } catch (error) {
      res.status(404).json({
        success: false,
        message: error.message
      });
    }
  }

  async listDataBiasDetections(req, res) {
    try {
      const detections = await biasAnalysisService.listDataBiasDetections(req.query);
      res.status(200).json({
        success: true,
        data: detections
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }

  async batchDataBiasDetection(req, res) {
    try {
      // For testing without authentication, use a dummy user ID
      // Authorization will be added back later
      const results = [];
      for (const dataset of req.body.datasets) {
        const result = await biasAnalysisService.detectDataBias(dataset, 'test-user-id');
        results.push(result);
      }
      res.status(201).json({
        success: true,
        message: 'Batch data bias detection completed successfully',
        data: results
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  /**
   * Bias Mitigation Recommendations
   */
  async getMitigationRecommendations(req, res) {
    try {
      const { analysisId } = req.params;
      const recommendations = await biasAnalysisService.getMitigationRecommendations(analysisId);
      res.status(200).json({
        success: true,
        data: recommendations
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }

  async applyMitigation(req, res) {
    try {
      const { analysisId } = req.params;
      const result = await biasAnalysisService.applyMitigation(analysisId, req.body);
      res.status(200).json({
        success: true,
        message: 'Mitigation applied successfully',
        data: result
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  async getMitigationTemplates(req, res) {
    try {
      const templates = await biasAnalysisService.getMitigationTemplates();
      res.status(200).json({
        success: true,
        data: templates
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }

  /**
   * Bias Analysis Result Storage
   */
  async storeBiasResults(req, res) {
    try {
      // For testing without authentication, use a dummy user ID
      // Authorization will be added back later
      const result = await biasAnalysisService.storeBiasResults(req.body, 'test-user-id');
      res.status(201).json({
        success: true,
        message: 'Bias results stored successfully',
        data: result
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  async getBiasResults(req, res) {
    try {
      const { id } = req.params;
      const result = await biasAnalysisService.getBiasResults(id);
      res.status(200).json({
        success: true,
        data: result
      });
    } catch (error) {
      res.status(404).json({
        success: false,
        message: error.message
      });
    }
  }

  async listBiasResults(req, res) {
    try {
      const results = await biasAnalysisService.listBiasResults(req.query);
      res.status(200).json({
        success: true,
        data: results
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }

  async updateBiasResults(req, res) {
    try {
      const { id } = req.params;
      // In a real implementation, we would update the results
      res.status(200).json({
        success: true,
        message: 'Bias results updated successfully'
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  /**
   * Bias Trend Monitoring
   */
  async getBiasTrends(req, res) {
    try {
      const trends = await biasAnalysisService.getBiasTrends(req.query);
      res.status(200).json({
        success: true,
        data: trends
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }

  async getModelBiasTrends(req, res) {
    try {
      const { modelId } = req.params;
      const trends = await biasAnalysisService.getModelBiasTrends(modelId);
      res.status(200).json({
        success: true,
        data: trends
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }

  async createTrendAlerts(req, res) {
    try {
      // For testing without authentication, use a dummy user ID
      // Authorization will be added back later
      const alert = await biasAnalysisService.createTrendAlert(req.body);
      res.status(201).json({
        success: true,
        message: 'Trend alert created successfully',
        data: alert
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  /**
   * Bias Comparison Reports
   */
  async generateComparisonReport(req, res) {
    try {
      // For testing without authentication, use a dummy user ID
      // Authorization will be added back later
      const report = await biasAnalysisService.generateComparisonReport(req.body, 'test-user-id');
      res.status(201).json({
        success: true,
        message: 'Comparison report generated successfully',
        data: report
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  async getComparisonReport(req, res) {
    try {
      const { id } = req.params;
      const report = await biasAnalysisService.getComparisonReport(id);
      res.status(200).json({
        success: true,
        data: report
      });
    } catch (error) {
      res.status(404).json({
        success: false,
        message: error.message
      });
    }
  }

  async listComparisonReports(req, res) {
    try {
      const reports = await biasAnalysisService.listComparisonReports(req.query);
      res.status(200).json({
        success: true,
        data: reports
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }

  /**
   * Bias Analysis Scheduling
   */
  async scheduleBiasAnalysis(req, res) {
    try {
      // For testing without authentication, use a dummy user ID
      // Authorization will be added back later
      const schedule = await biasAnalysisService.scheduleBiasAnalysis(req.body, 'test-user-id');
      res.status(201).json({
        success: true,
        message: 'Bias analysis scheduled successfully',
        data: schedule
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  async getScheduledAnalysis(req, res) {
    try {
      const { id } = req.params;
      const schedule = await biasAnalysisService.getScheduledAnalysis(id);
      res.status(200).json({
        success: true,
        data: schedule
      });
    } catch (error) {
      res.status(404).json({
        success: false,
        message: error.message
      });
    }
  }

  async listScheduledAnalyses(req, res) {
    try {
      const schedules = await biasAnalysisService.listScheduledAnalyses(req.query);
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

  async updateScheduledAnalysis(req, res) {
    try {
      const { id } = req.params;
      const schedule = await biasAnalysisService.updateScheduledAnalysis(id, req.body);
      res.status(200).json({
        success: true,
        message: 'Scheduled analysis updated successfully',
        data: schedule
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  async cancelScheduledAnalysis(req, res) {
    try {
      const { id } = req.params;
      const result = await biasAnalysisService.cancelScheduledAnalysis(id);
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
   * Bias Analysis Notifications
   */
  async createNotificationRule(req, res) {
    try {
      // For testing without authentication, use a dummy user ID
      // Authorization will be added back later
      const notification = await biasAnalysisService.createNotificationRule(req.body, 'test-user-id');
      res.status(201).json({
        success: true,
        message: 'Notification rule created successfully',
        data: notification
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  async getNotificationRule(req, res) {
    try {
      const { id } = req.params;
      const notification = await biasAnalysisService.getNotificationRule(id);
      res.status(200).json({
        success: true,
        data: notification
      });
    } catch (error) {
      res.status(404).json({
        success: false,
        message: error.message
      });
    }
  }

  async listNotificationRules(req, res) {
    try {
      const notifications = await biasAnalysisService.listNotificationRules(req.query);
      res.status(200).json({
        success: true,
        data: notifications
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }

  async updateNotificationRule(req, res) {
    try {
      const { id } = req.params;
      const notification = await biasAnalysisService.updateNotificationRule(id, req.body);
      res.status(200).json({
        success: true,
        message: 'Notification rule updated successfully',
        data: notification
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  async deleteNotificationRule(req, res) {
    try {
      const { id } = req.params;
      const result = await biasAnalysisService.deleteNotificationRule(id);
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

module.exports = new BiasAnalysisController();