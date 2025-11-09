const { 
  ModelAnalysis,
  DataBiasDetection,
  MitigationRecommendation,
  BiasResult,
  BiasTrend,
  ComparisonReport,
  BiasSchedule,
  BiasNotification
} = require('../models');

class BiasAnalysisService {
  /**
   * Model Bias Analysis
   */
  async analyzeModel(modelData, userId) {
    try {
      const analysis = await ModelAnalysis.create({
        ...modelData,
        status: 'completed'
      });
      return analysis;
    } catch (error) {
      throw new Error(`Failed to analyze model: ${error.message}`);
    }
  }

  async getModelAnalysis(analysisId) {
    try {
      const analysis = await ModelAnalysis.findByPk(analysisId);
      if (!analysis) {
        throw new Error('Model analysis not found');
      }
      return analysis;
    } catch (error) {
      throw new Error(`Failed to get model analysis: ${error.message}`);
    }
  }

  async listModelAnalyses(filters = {}) {
    try {
      const whereClause = {};
      
      if (filters.modelId) {
        whereClause.modelId = filters.modelId;
      }
      
      if (filters.modelName) {
        whereClause.modelName = filters.modelName;
      }
      
      if (filters.status) {
        whereClause.status = filters.status;
      }
      
      const analyses = await ModelAnalysis.findAll({
        where: whereClause,
        order: [['createdAt', 'DESC']],
        limit: filters.limit || 50
      });
      
      return analyses;
    } catch (error) {
      throw new Error(`Failed to list model analyses: ${error.message}`);
    }
  }

  async deleteModelAnalysis(analysisId) {
    try {
      const analysis = await ModelAnalysis.findByPk(analysisId);
      if (!analysis) {
        throw new Error('Model analysis not found');
      }
      
      await analysis.destroy();
      return { success: true, message: 'Model analysis deleted successfully' };
    } catch (error) {
      throw new Error(`Failed to delete model analysis: ${error.message}`);
    }
  }

  /**
   * Data Bias Detection
   */
  async detectDataBias(datasetData, userId) {
    try {
      const detection = await DataBiasDetection.create({
        ...datasetData,
        status: 'completed'
      });
      return detection;
    } catch (error) {
      throw new Error(`Failed to detect data bias: ${error.message}`);
    }
  }

  async getDataBiasDetection(detectionId) {
    try {
      const detection = await DataBiasDetection.findByPk(detectionId);
      if (!detection) {
        throw new Error('Data bias detection not found');
      }
      return detection;
    } catch (error) {
      throw new Error(`Failed to get data bias detection: ${error.message}`);
    }
  }

  async listDataBiasDetections(filters = {}) {
    try {
      const whereClause = {};
      
      if (filters.datasetId) {
        whereClause.datasetId = filters.datasetId;
      }
      
      if (filters.datasetName) {
        whereClause.datasetName = filters.datasetName;
      }
      
      if (filters.status) {
        whereClause.status = filters.status;
      }
      
      const detections = await DataBiasDetection.findAll({
        where: whereClause,
        order: [['createdAt', 'DESC']],
        limit: filters.limit || 50
      });
      
      return detections;
    } catch (error) {
      throw new Error(`Failed to list data bias detections: ${error.message}`);
    }
  }

  /**
   * Bias Mitigation Recommendations
   */
  async getMitigationRecommendations(analysisId) {
    try {
      const recommendations = await MitigationRecommendation.findAll({
        where: { analysisId },
        order: [['priority', 'ASC']]
      });
      return recommendations;
    } catch (error) {
      throw new Error(`Failed to get mitigation recommendations: ${error.message}`);
    }
  }

  async applyMitigation(analysisId, mitigationData) {
    try {
      // Simulate applying mitigation
      const result = {
        analysisId,
        status: 'applied',
        appliedAt: new Date(),
        ...mitigationData
      };
      return result;
    } catch (error) {
      throw new Error(`Failed to apply mitigation: ${error.message}`);
    }
  }

  async getMitigationTemplates() {
    try {
      // Return predefined templates
      const templates = [
        {
          id: 'preprocessing',
          name: 'Preprocessing Techniques',
          description: 'Data preprocessing methods to reduce bias',
          techniques: ['reweighing', 'disparate_impact_remover', 'lfr']
        },
        {
          id: 'inprocessing',
          name: 'In-processing Techniques',
          description: 'Model training methods that address bias during training',
          techniques: ['prejudice_remover', 'adversarial_debiasing', 'meta_fair_classifier']
        },
        {
          id: 'postprocessing',
          name: 'Post-processing Techniques',
          description: 'Methods to adjust model outputs to reduce bias',
          techniques: ['calibrated_eq_odds_postprocessing', 'eq_odds_postprocessing', 'reject_option_classification']
        }
      ];
      return templates;
    } catch (error) {
      throw new Error(`Failed to get mitigation templates: ${error.message}`);
    }
  }

  /**
   * Bias Analysis Result Storage
   */
  async storeBiasResults(resultData, userId) {
    try {
      const result = await BiasResult.create({
        ...resultData,
        createdAt: new Date()
      });
      return result;
    } catch (error) {
      throw new Error(`Failed to store bias results: ${error.message}`);
    }
  }

  async getBiasResults(resultId) {
    try {
      const result = await BiasResult.findByPk(resultId);
      if (!result) {
        throw new Error('Bias result not found');
      }
      return result;
    } catch (error) {
      throw new Error(`Failed to get bias results: ${error.message}`);
    }
  }

  async listBiasResults(filters = {}) {
    try {
      const whereClause = {};
      
      if (filters.analysisId) {
        whereClause.analysisId = filters.analysisId;
      }
      
      if (filters.entityId) {
        whereClause.entityId = filters.entityId;
      }
      
      if (filters.entityType) {
        whereClause.entityType = filters.entityType;
      }
      
      const results = await BiasResult.findAll({
        where: whereClause,
        order: [['createdAt', 'DESC']],
        limit: filters.limit || 50
      });
      
      return results;
    } catch (error) {
      throw new Error(`Failed to list bias results: ${error.message}`);
    }
  }

  /**
   * Bias Trend Monitoring
   */
  async getBiasTrends(filters = {}) {
    try {
      const whereClause = {};
      
      if (filters.modelId) {
        whereClause.modelId = filters.modelId;
      }
      
      if (filters.metricType) {
        whereClause.metricType = filters.metricType;
      }
      
      if (filters.alertTriggered !== undefined) {
        whereClause.alertTriggered = filters.alertTriggered;
      }
      
      const trends = await BiasTrend.findAll({
        where: whereClause,
        order: [['createdAt', 'DESC']],
        limit: filters.limit || 50
      });
      
      return trends;
    } catch (error) {
      throw new Error(`Failed to get bias trends: ${error.message}`);
    }
  }

  async getModelBiasTrends(modelId) {
    try {
      const trends = await BiasTrend.findAll({
        where: { modelId },
        order: [['createdAt', 'DESC']]
      });
      return trends;
    } catch (error) {
      throw new Error(`Failed to get model bias trends: ${error.message}`);
    }
  }

  async createTrendAlert(alertData) {
    try {
      const alert = await BiasTrend.create({
        ...alertData,
        alertTriggered: true,
        createdAt: new Date()
      });
      return alert;
    } catch (error) {
      throw new Error(`Failed to create trend alert: ${error.message}`);
    }
  }

  /**
   * Bias Comparison Reports
   */
  async generateComparisonReport(reportData, userId) {
    try {
      const report = await ComparisonReport.create({
        ...reportData,
        status: 'completed',
        generatedBy: userId,
        createdAt: new Date()
      });
      return report;
    } catch (error) {
      throw new Error(`Failed to generate comparison report: ${error.message}`);
    }
  }

  async getComparisonReport(reportId) {
    try {
      const report = await ComparisonReport.findByPk(reportId);
      if (!report) {
        throw new Error('Comparison report not found');
      }
      return report;
    } catch (error) {
      throw new Error(`Failed to get comparison report: ${error.message}`);
    }
  }

  async listComparisonReports(filters = {}) {
    try {
      const whereClause = {};
      
      if (filters.status) {
        whereClause.status = filters.status;
      }
      
      if (filters.comparisonType) {
        whereClause.comparisonType = filters.comparisonType;
      }
      
      const reports = await ComparisonReport.findAll({
        where: whereClause,
        order: [['createdAt', 'DESC']],
        limit: filters.limit || 50
      });
      
      return reports;
    } catch (error) {
      throw new Error(`Failed to list comparison reports: ${error.message}`);
    }
  }

  /**
   * Bias Analysis Scheduling
   */
  async scheduleBiasAnalysis(scheduleData, userId) {
    try {
      const schedule = await BiasSchedule.create({
        ...scheduleData,
        isActive: true,
        createdAt: new Date()
      });
      return schedule;
    } catch (error) {
      throw new Error(`Failed to schedule bias analysis: ${error.message}`);
    }
  }

  async getScheduledAnalysis(scheduleId) {
    try {
      const schedule = await BiasSchedule.findByPk(scheduleId);
      if (!schedule) {
        throw new Error('Scheduled analysis not found');
      }
      return schedule;
    } catch (error) {
      throw new Error(`Failed to get scheduled analysis: ${error.message}`);
    }
  }

  async listScheduledAnalyses(filters = {}) {
    try {
      const whereClause = {};
      
      if (filters.isActive !== undefined) {
        whereClause.isActive = filters.isActive;
      }
      
      if (filters.analysisType) {
        whereClause.analysisType = filters.analysisType;
      }
      
      if (filters.entityType) {
        whereClause.entityType = filters.entityType;
      }
      
      const schedules = await BiasSchedule.findAll({
        where: whereClause,
        order: [['createdAt', 'DESC']],
        limit: filters.limit || 50
      });
      
      return schedules;
    } catch (error) {
      throw new Error(`Failed to list scheduled analyses: ${error.message}`);
    }
  }

  async updateScheduledAnalysis(scheduleId, updateData) {
    try {
      const schedule = await BiasSchedule.findByPk(scheduleId);
      if (!schedule) {
        throw new Error('Scheduled analysis not found');
      }
      
      await schedule.update(updateData);
      return schedule;
    } catch (error) {
      throw new Error(`Failed to update scheduled analysis: ${error.message}`);
    }
  }

  async cancelScheduledAnalysis(scheduleId) {
    try {
      const schedule = await BiasSchedule.findByPk(scheduleId);
      if (!schedule) {
        throw new Error('Scheduled analysis not found');
      }
      
      await schedule.update({ isActive: false });
      return { success: true, message: 'Scheduled analysis cancelled successfully' };
    } catch (error) {
      throw new Error(`Failed to cancel scheduled analysis: ${error.message}`);
    }
  }

  /**
   * Bias Analysis Notifications
   */
  async createNotificationRule(notificationData, userId) {
    try {
      const notification = await BiasNotification.create({
        ...notificationData,
        isActive: true,
        createdAt: new Date()
      });
      return notification;
    } catch (error) {
      throw new Error(`Failed to create notification rule: ${error.message}`);
    }
  }

  async getNotificationRule(notificationId) {
    try {
      const notification = await BiasNotification.findByPk(notificationId);
      if (!notification) {
        throw new Error('Notification rule not found');
      }
      return notification;
    } catch (error) {
      throw new Error(`Failed to get notification rule: ${error.message}`);
    }
  }

  async listNotificationRules(filters = {}) {
    try {
      const whereClause = {};
      
      if (filters.isActive !== undefined) {
        whereClause.isActive = filters.isActive;
      }
      
      if (filters.triggerType) {
        whereClause.triggerType = filters.triggerType;
      }
      
      if (filters.notificationType) {
        whereClause.notificationType = filters.notificationType;
      }
      
      const notifications = await BiasNotification.findAll({
        where: whereClause,
        order: [['createdAt', 'DESC']],
        limit: filters.limit || 50
      });
      
      return notifications;
    } catch (error) {
      throw new Error(`Failed to list notification rules: ${error.message}`);
    }
  }

  async updateNotificationRule(notificationId, updateData) {
    try {
      const notification = await BiasNotification.findByPk(notificationId);
      if (!notification) {
        throw new Error('Notification rule not found');
      }
      
      await notification.update(updateData);
      return notification;
    } catch (error) {
      throw new Error(`Failed to update notification rule: ${error.message}`);
    }
  }

  async deleteNotificationRule(notificationId) {
    try {
      const notification = await BiasNotification.findByPk(notificationId);
      if (!notification) {
        throw new Error('Notification rule not found');
      }
      
      await notification.destroy();
      return { success: true, message: 'Notification rule deleted successfully' };
    } catch (error) {
      throw new Error(`Failed to delete notification rule: ${error.message}`);
    }
  }
}

module.exports = new BiasAnalysisService();