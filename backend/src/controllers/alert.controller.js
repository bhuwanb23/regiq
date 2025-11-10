const alertService = require('../services/alert.service');

class AlertController {
  /**
   * Get all alerts with filtering and pagination
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   */
  async getAllAlerts(req, res) {
    try {
      const { page, limit, type, severity, jobId, resolved } = req.query;
      const filters = {};
      if (type) filters.type = type;
      if (severity) filters.severity = severity;
      if (jobId) filters.jobId = jobId;
      if (resolved !== undefined) filters.resolved = resolved === 'true';

      const pagination = {
        page: parseInt(page) || 1,
        limit: parseInt(limit) || 10
      };

      const result = await alertService.getAllAlerts(filters, pagination);
      res.json({
        success: true,
        data: result.data,
        pagination: {
          page: result.page,
          limit: result.limit,
          totalCount: result.totalCount,
          totalPages: Math.ceil(result.totalCount / result.limit)
        }
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }

  /**
   * Resolve an alert
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   */
  async resolveAlert(req, res) {
    try {
      const { alertId } = req.params;
      const result = await alertService.resolveAlert(alertId);
      res.json({
        success: true,
        data: result,
        message: 'Alert resolved successfully'
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  /**
   * Get alert statistics
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   */
  async getAlertStatistics(req, res) {
    try {
      const statistics = await alertService.getAlertStatistics();
      res.json({
        success: true,
        data: statistics
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }
}

module.exports = new AlertController();