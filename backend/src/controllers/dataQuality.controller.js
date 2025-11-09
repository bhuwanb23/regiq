const qualityMonitoringService = require('../services/qualityMonitoring.service');

class DataQualityController {
  async createQualityMetric(req, res) {
    try {
      const metric = await qualityMonitoringService.createQualityMetric(req.body);
      res.status(201).json({
        success: true,
        message: 'Quality metric created successfully',
        data: metric
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  async getQualityMetric(req, res) {
    try {
      const { id } = req.params;
      const metric = await qualityMonitoringService.getQualityMetricById(id);
      res.status(200).json({
        success: true,
        message: 'Quality metric retrieved successfully',
        data: metric
      });
    } catch (error) {
      res.status(404).json({
        success: false,
        message: error.message
      });
    }
  }

  async listQualityMetrics(req, res) {
    try {
      const { limit = 10, offset = 0 } = req.query;
      const result = await qualityMonitoringService.getAllQualityMetrics(
        parseInt(limit),
        parseInt(offset)
      );
      res.status(200).json({
        success: true,
        message: 'Quality metrics retrieved successfully',
        data: result
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }

  async updateQualityMetric(req, res) {
    try {
      const { id } = req.params;
      const metric = await qualityMonitoringService.updateQualityMetric(id, req.body);
      res.status(200).json({
        success: true,
        message: 'Quality metric updated successfully',
        data: metric
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  async deleteQualityMetric(req, res) {
    try {
      const { id } = req.params;
      const result = await qualityMonitoringService.deleteQualityMetric(id);
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

  async getQualityMetricsByJob(req, res) {
    try {
      const { jobId } = req.params;
      const { limit = 10, offset = 0 } = req.query;
      const result = await qualityMonitoringService.getQualityMetricsByJob(
        jobId,
        parseInt(limit),
        parseInt(offset)
      );
      res.status(200).json({
        success: true,
        message: 'Quality metrics by job retrieved successfully',
        data: result
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }

  async calculateCompletenessMetric(req, res) {
    try {
      const { jobId, totalRecords, nullRecords, fieldName } = req.body;
      const metric = await qualityMonitoringService.calculateCompletenessMetric(
        jobId, 
        totalRecords, 
        nullRecords, 
        fieldName
      );
      res.status(201).json({
        success: true,
        message: 'Completeness metric calculated successfully',
        data: metric
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  async calculateAccuracyMetric(req, res) {
    try {
      const { jobId, totalRecords, invalidRecords, fieldName } = req.body;
      const metric = await qualityMonitoringService.calculateAccuracyMetric(
        jobId, 
        totalRecords, 
        invalidRecords, 
        fieldName
      );
      res.status(201).json({
        success: true,
        message: 'Accuracy metric calculated successfully',
        data: metric
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  async calculateUniquenessMetric(req, res) {
    try {
      const { jobId, totalRecords, duplicateRecords, fieldName } = req.body;
      const metric = await qualityMonitoringService.calculateUniquenessMetric(
        jobId, 
        totalRecords, 
        duplicateRecords, 
        fieldName
      );
      res.status(201).json({
        success: true,
        message: 'Uniqueness metric calculated successfully',
        data: metric
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  async getQualitySummary(req, res) {
    try {
      const { jobId } = req.params;
      const summary = await qualityMonitoringService.getQualitySummary(jobId);
      res.status(200).json({
        success: true,
        message: 'Quality summary retrieved successfully',
        data: summary
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }

  async checkQualityThresholds(req, res) {
    try {
      const { jobId } = req.params;
      const result = await qualityMonitoringService.checkQualityThresholds(jobId);
      res.status(200).json({
        success: true,
        message: 'Quality thresholds checked successfully',
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

module.exports = new DataQualityController();