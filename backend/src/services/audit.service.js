const { AuditLog, sequelize } = require('../models');
const { Op } = require('sequelize');
const winston = require('winston');

class AuditService {
  constructor() {
    // Initialize logger
    this.logger = winston.createLogger({
      level: 'info',
      format: winston.format.json(),
      transports: [
        new winston.transports.Console(),
      ],
    });
  }

  /**
   * Log user activity
   * @param {Object} logData - Audit log data
   * @returns {Object} Created audit log
   */
  async logActivity(logData) {
    try {
      const auditLog = await AuditLog.create(logData);
      
      this.logger.info('User activity logged', { 
        auditLogId: auditLog.id, 
        userId: auditLog.userId,
        action: auditLog.action
      });

      return auditLog;
    } catch (error) {
      this.logger.error('Failed to log user activity', { error: error.message, logData });
      throw new Error(`Failed to log user activity: ${error.message}`);
    }
  }

  /**
   * Get audit logs with filtering and pagination
   * @param {Object} filters - Filter criteria
   * @param {Object} pagination - Pagination options
   * @returns {Array} Audit logs
   */
  async getAuditLogs(filters = {}, pagination = {}) {
    try {
      const { page = 1, limit = 10 } = pagination;
      const offset = (page - 1) * limit;

      const whereClause = {};
      if (filters.userId) whereClause.userId = filters.userId;
      if (filters.action) whereClause.action = filters.action;
      if (filters.entityType) whereClause.entityType = filters.entityType;
      
      // Date range filtering
      if (filters.startDate || filters.endDate) {
        whereClause.createdAt = {};
        if (filters.startDate) {
          whereClause.createdAt[Op.gte] = new Date(filters.startDate);
        }
        if (filters.endDate) {
          whereClause.createdAt[Op.lte] = new Date(filters.endDate);
        }
      }

      const auditLogs = await AuditLog.findAndCountAll({
        where: whereClause,
        limit,
        offset,
        order: [['createdAt', 'DESC']]
      });

      return {
        data: auditLogs.rows,
        totalCount: auditLogs.count,
        page,
        limit
      };
    } catch (error) {
      this.logger.error('Failed to get audit logs', { error: error.message });
      throw new Error(`Failed to get audit logs: ${error.message}`);
    }
  }

  /**
   * Get audit log by ID
   * @param {string} auditLogId - Audit log ID
   * @returns {Object} Audit log
   */
  async getAuditLogById(auditLogId) {
    try {
      const auditLog = await AuditLog.findByPk(auditLogId);
      
      if (!auditLog) {
        throw new Error('Audit log not found');
      }

      return auditLog;
    } catch (error) {
      this.logger.error('Failed to get audit log', { error: error.message, auditLogId });
      throw new Error(`Failed to get audit log: ${error.message}`);
    }
  }

  /**
   * Get system event tracking data
   * @param {Object} filters - Filter criteria
   * @param {Object} pagination - Pagination options
   * @returns {Array} System events
   */
  async getSystemEvents(filters = {}, pagination = {}) {
    try {
      const { page = 1, limit = 10 } = pagination;
      const offset = (page - 1) * limit;

      // Filter for system-related actions
      const whereClause = {
        action: {
          [Op.in]: ['SYSTEM_START', 'SYSTEM_SHUTDOWN', 'CONFIG_CHANGE', 'MAINTENANCE']
        }
      };

      if (filters.startDate || filters.endDate) {
        whereClause.createdAt = {};
        if (filters.startDate) {
          whereClause.createdAt[Op.gte] = new Date(filters.startDate);
        }
        if (filters.endDate) {
          whereClause.createdAt[Op.lte] = new Date(filters.endDate);
        }
      }

      const systemEvents = await AuditLog.findAndCountAll({
        where: whereClause,
        limit,
        offset,
        order: [['createdAt', 'DESC']]
      });

      return {
        data: systemEvents.rows,
        totalCount: systemEvents.count,
        page,
        limit
      };
    } catch (error) {
      this.logger.error('Failed to get system events', { error: error.message });
      throw new Error(`Failed to get system events: ${error.message}`);
    }
  }

  /**
   * Get security event monitoring data
   * @param {Object} filters - Filter criteria
   * @param {Object} pagination - Pagination options
   * @returns {Array} Security events
   */
  async getSecurityEvents(filters = {}, pagination = {}) {
    try {
      const { page = 1, limit = 10 } = pagination;
      const offset = (page - 1) * limit;

      // Filter for security-related actions
      const whereClause = {
        action: {
          [Op.in]: ['LOGIN_ATTEMPT', 'LOGIN_SUCCESS', 'LOGIN_FAILURE', 'LOGOUT', 'PASSWORD_CHANGE', 'PERMISSION_CHANGE', 'UNAUTHORIZED_ACCESS']
        }
      };

      if (filters.startDate || filters.endDate) {
        whereClause.createdAt = {};
        if (filters.startDate) {
          whereClause.createdAt[Op.gte] = new Date(filters.startDate);
        }
        if (filters.endDate) {
          whereClause.createdAt[Op.lte] = new Date(filters.endDate);
        }
      }

      const securityEvents = await AuditLog.findAndCountAll({
        where: whereClause,
        limit,
        offset,
        order: [['createdAt', 'DESC']]
      });

      return {
        data: securityEvents.rows,
        totalCount: securityEvents.count,
        page,
        limit
      };
    } catch (error) {
      this.logger.error('Failed to get security events', { error: error.message });
      throw new Error(`Failed to get security events: ${error.message}`);
    }
  }

  /**
   * Generate audit trail for a specific entity
   * @param {string} entityType - Entity type
   * @param {string} entityId - Entity ID
   * @returns {Array} Audit trail
   */
  async generateAuditTrail(entityType, entityId) {
    try {
      const auditTrail = await AuditLog.findAll({
        where: {
          entityType,
          entityId
        },
        order: [['createdAt', 'ASC']]
      });

      return auditTrail;
    } catch (error) {
      this.logger.error('Failed to generate audit trail', { error: error.message, entityType, entityId });
      throw new Error(`Failed to generate audit trail: ${error.message}`);
    }
  }

  /**
   * Get audit statistics
   * @returns {Object} Audit statistics
   */
  async getAuditStatistics() {
    try {
      const totalLogs = await AuditLog.count();
      
      const logsByAction = await AuditLog.findAll({
        attributes: ['action', [sequelize.fn('COUNT', sequelize.col('action')), 'count']],
        group: ['action']
      });

      const logsByEntityType = await AuditLog.findAll({
        attributes: ['entityType', [sequelize.fn('COUNT', sequelize.col('entityType')), 'count']],
        group: ['entityType']
      });

      const recentLogs = await AuditLog.findAll({
        limit: 10,
        order: [['createdAt', 'DESC']]
      });

      return {
        totalLogs,
        logsByAction,
        logsByEntityType,
        recentLogs
      };
    } catch (error) {
      this.logger.error('Failed to get audit statistics', { error: error.message });
      throw new Error(`Failed to get audit statistics: ${error.message}`);
    }
  }

  /**
   * Log system performance metrics
   * @param {Object} performanceData - Performance data
   * @returns {Object} Created audit log
   */
  async logPerformance(performanceData) {
    try {
      const logData = {
        userId: null, // System-generated log
        action: 'PERFORMANCE_METRIC',
        entityType: 'SYSTEM',
        entityId: 'SYSTEM_PERFORMANCE',
        details: performanceData,
        ipAddress: null,
        userAgent: null
      };

      const auditLog = await this.logActivity(logData);
      return auditLog;
    } catch (error) {
      this.logger.error('Failed to log performance metrics', { error: error.message, performanceData });
      throw new Error(`Failed to log performance metrics: ${error.message}`);
    }
  }

  /**
   * Log system errors
   * @param {Object} errorData - Error data
   * @returns {Object} Created audit log
   */
  async logError(errorData) {
    try {
      const logData = {
        userId: null, // System-generated log
        action: 'SYSTEM_ERROR',
        entityType: 'SYSTEM',
        entityId: 'SYSTEM_ERROR',
        details: errorData,
        ipAddress: null,
        userAgent: null
      };

      const auditLog = await this.logActivity(logData);
      return auditLog;
    } catch (error) {
      this.logger.error('Failed to log system error', { error: error.message, errorData });
      throw new Error(`Failed to log system error: ${error.message}`);
    }
  }
}

module.exports = new AuditService();