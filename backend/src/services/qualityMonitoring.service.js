const { DataQualityMetric } = require('../models');

class QualityMonitoringService {
  async createQualityMetric(metricData) {
    try {
      const metric = await DataQualityMetric.create(metricData);
      return metric;
    } catch (error) {
      throw new Error(`Failed to create quality metric: ${error.message}`);
    }
  }

  async getQualityMetricById(id) {
    try {
      const metric = await DataQualityMetric.findByPk(id);
      if (!metric) {
        throw new Error('Quality metric not found');
      }
      return metric;
    } catch (error) {
      throw new Error(`Failed to get quality metric: ${error.message}`);
    }
  }

  async getAllQualityMetrics(limit = 10, offset = 0) {
    try {
      const { rows, count } = await DataQualityMetric.findAndCountAll({
        limit,
        offset,
        order: [['created_at', 'DESC']]
      });
      return { metrics: rows, count, limit, offset };
    } catch (error) {
      throw new Error(`Failed to list quality metrics: ${error.message}`);
    }
  }

  async updateQualityMetric(id, updateData) {
    try {
      const metric = await this.getQualityMetricById(id);
      const updatedMetric = await metric.update(updateData);
      return updatedMetric;
    } catch (error) {
      throw new Error(`Failed to update quality metric: ${error.message}`);
    }
  }

  async deleteQualityMetric(id) {
    try {
      const metric = await this.getQualityMetricById(id);
      await metric.destroy();
      return { success: true, message: 'Quality metric deleted successfully' };
    } catch (error) {
      throw new Error(`Failed to delete quality metric: ${error.message}`);
    }
  }

  async getQualityMetricsByJob(jobId, limit = 10, offset = 0) {
    try {
      const { rows, count } = await DataQualityMetric.findAndCountAll({
        where: { jobId },
        limit,
        offset,
        order: [['created_at', 'DESC']]
      });
      return { metrics: rows, count, limit, offset };
    } catch (error) {
      throw new Error(`Failed to get quality metrics by job: ${error.message}`);
    }
  }

  async calculateCompletenessMetric(jobId, totalRecords, nullRecords, fieldName = null) {
    try {
      const completeness = totalRecords > 0 ? 
        ((totalRecords - nullRecords) / totalRecords) * 100 : 0;
      
      const metric = await this.createQualityMetric({
        jobId: jobId,
        metricType: 'completeness',
        metricName: fieldName ? `Completeness - ${fieldName}` : 'Overall Completeness',
        metricValue: completeness,
        thresholdValue: 95.0, // Default threshold
        status: completeness >= 95.0 ? 'pass' : 'fail',
        dimension: fieldName || 'overall',
        recordCount: totalRecords,
        errorCount: nullRecords
      });

      return metric;
    } catch (error) {
      throw new Error(`Failed to calculate completeness metric: ${error.message}`);
    }
  }

  async calculateAccuracyMetric(jobId, totalRecords, invalidRecords, fieldName = null) {
    try {
      const accuracy = totalRecords > 0 ? 
        ((totalRecords - invalidRecords) / totalRecords) * 100 : 0;
      
      const metric = await this.createQualityMetric({
        jobId: jobId,
        metricType: 'accuracy',
        metricName: fieldName ? `Accuracy - ${fieldName}` : 'Overall Accuracy',
        metricValue: accuracy,
        thresholdValue: 98.0, // Default threshold
        status: accuracy >= 98.0 ? 'pass' : 'fail',
        dimension: fieldName || 'overall',
        recordCount: totalRecords,
        errorCount: invalidRecords
      });

      return metric;
    } catch (error) {
      throw new Error(`Failed to calculate accuracy metric: ${error.message}`);
    }
  }

  async calculateUniquenessMetric(jobId, totalRecords, duplicateRecords, fieldName = null) {
    try {
      const uniqueness = totalRecords > 0 ? 
        ((totalRecords - duplicateRecords) / totalRecords) * 100 : 0;
      
      const metric = await this.createQualityMetric({
        jobId: jobId,
        metricType: 'uniqueness',
        metricName: fieldName ? `Uniqueness - ${fieldName}` : 'Overall Uniqueness',
        metricValue: uniqueness,
        thresholdValue: 99.0, // Default threshold
        status: uniqueness >= 99.0 ? 'pass' : 'fail',
        dimension: fieldName || 'overall',
        recordCount: totalRecords,
        errorCount: duplicateRecords
      });

      return metric;
    } catch (error) {
      throw new Error(`Failed to calculate uniqueness metric: ${error.message}`);
    }
  }

  async getQualitySummary(jobId) {
    try {
      const metrics = await DataQualityMetric.findAll({
        where: { jobId },
        order: [['created_at', 'DESC']]
      });

      const summary = {
        jobId: jobId,
        totalMetrics: metrics.length,
        passCount: metrics.filter(m => m.status === 'pass').length,
        failCount: metrics.filter(m => m.status === 'fail').length,
        warningCount: metrics.filter(m => m.status === 'warning').length,
        averageScore: metrics.length > 0 ? 
          metrics.reduce((sum, m) => sum + parseFloat(m.metricValue || 0), 0) / metrics.length : 0,
        metricsByType: {}
      };

      // Group metrics by type
      for (const metric of metrics) {
        if (!summary.metricsByType[metric.metricType]) {
          summary.metricsByType[metric.metricType] = [];
        }
        summary.metricsByType[metric.metricType].push(metric);
      }

      return summary;
    } catch (error) {
      throw new Error(`Failed to get quality summary: ${error.message}`);
    }
  }

  async checkQualityThresholds(jobId) {
    try {
      const metrics = await DataQualityMetric.findAll({
        where: { jobId }
      });

      const failedMetrics = [];
      const warningMetrics = [];

      for (const metric of metrics) {
        if (metric.thresholdValue && metric.metricValue) {
          const value = parseFloat(metric.metricValue);
          const threshold = parseFloat(metric.thresholdValue);
          
          if (value < threshold * 0.8) { // Fail if below 80% of threshold
            failedMetrics.push(metric);
          } else if (value < threshold) { // Warning if below threshold but above 80%
            warningMetrics.push(metric);
          }
        }
      }

      return {
        failedMetrics: failedMetrics,
        warningMetrics: warningMetrics,
        totalCount: metrics.length
      };
    } catch (error) {
      throw new Error(`Failed to check quality thresholds: ${error.message}`);
    }
  }
}

module.exports = new QualityMonitoringService();