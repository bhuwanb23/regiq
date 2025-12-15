const auditService = require('../services/audit.service');

class AuditController {
  /**
   * Get all audit logs with filtering and pagination
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   */
  async getAllAuditLogs(req, res) {
    try {
      const { page, limit, action, entityType, startDate, endDate } = req.query;
      const filters = {};
      if (action) filters.action = action;
      if (entityType) filters.entityType = entityType;
      if (startDate) filters.startDate = startDate;
      if (endDate) filters.endDate = endDate;

      const pagination = {
        page: parseInt(page) || 1,
        limit: parseInt(limit) || 10
      };

      const result = await auditService.getAuditLogs(filters, pagination);
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
   * Get audit log by ID
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   */
  async getAuditLogById(req, res) {
    try {
      const { auditLogId } = req.params;
      const auditLog = await auditService.getAuditLogById(auditLogId);
      res.json({
        success: true,
        data: auditLog
      });
    } catch (error) {
      res.status(404).json({
        success: false,
        message: error.message
      });
    }
  }

  /**
   * Get system events
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   */
  async getSystemEvents(req, res) {
    try {
      const { page, limit, startDate, endDate } = req.query;
      const filters = {};
      if (startDate) filters.startDate = startDate;
      if (endDate) filters.endDate = endDate;

      const pagination = {
        page: parseInt(page) || 1,
        limit: parseInt(limit) || 10
      };

      const result = await auditService.getSystemEvents(filters, pagination);
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
   * Get security events
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   */
  async getSecurityEvents(req, res) {
    try {
      const { page, limit, startDate, endDate } = req.query;
      const filters = {};
      if (startDate) filters.startDate = startDate;
      if (endDate) filters.endDate = endDate;

      const pagination = {
        page: parseInt(page) || 1,
        limit: parseInt(limit) || 10
      };

      const result = await auditService.getSecurityEvents(filters, pagination);
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
   * Generate audit trail for an entity
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   */
  async generateAuditTrail(req, res) {
    try {
      const { entityType, entityId } = req.params;
      const auditTrail = await auditService.generateAuditTrail(entityType, entityId);
      res.json({
        success: true,
        data: auditTrail
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }

  /**
   * Get audit statistics
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   */
  async getAuditStatistics(req, res) {
    try {
      const statistics = await auditService.getAuditStatistics();
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

module.exports = new AuditController();