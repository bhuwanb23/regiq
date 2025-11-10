const { JobStatus, JobHistory, Alert, sequelize } = require('../models');
const { Op } = require('sequelize');
const winston = require('winston');
const websocketService = require('./websocket.service');

class AlertService {
  constructor() {
    // Initialize logger
    this.logger = winston.createLogger({
      level: 'info',
      format: winston.format.json(),
      transports: [
        new winston.transports.Console(),
      ],
    });

    // Start monitoring for alerts
    this.startAlertMonitoring();
  }

  /**
   * Start alert monitoring interval
   */
  startAlertMonitoring() {
    // Check for failed jobs every minute
    setInterval(() => {
      this.checkForFailedJobs();
    }, 60000);

    // Check for stuck jobs every 5 minutes
    setInterval(() => {
      this.checkForStuckJobs();
    }, 300000);

    // Check system health every 30 seconds
    setInterval(() => {
      this.checkSystemHealth();
    }, 30000);
  }

  /**
   * Check for recently failed jobs and generate alerts
   */
  async checkForFailedJobs() {
    try {
      const oneMinuteAgo = new Date(Date.now() - 60000);
      
      // Find recently failed jobs
      const failedJobs = await JobStatus.findAll({
        where: {
          status: 'failed',
          failedAt: {
            [Op.gte]: oneMinuteAgo
          }
        }
      });

      for (const job of failedJobs) {
        await this.createAlert({
          type: 'JOB_FAILURE',
          severity: 'HIGH',
          jobId: job.jobId,
          jobType: job.jobType,
          message: `Job ${job.jobId} of type ${job.jobType} failed`,
          details: {
            errorMessage: job.errorMessage,
            errorStack: job.errorStack,
            nodeId: job.nodeId
          }
        });
      }
    } catch (error) {
      this.logger.error('Failed to check for failed jobs', { error: error.message });
    }
  }

  /**
   * Check for stuck jobs (jobs that haven't progressed in a while)
   */
  async checkForStuckJobs() {
    try {
      const fiveMinutesAgo = new Date(Date.now() - 300000);
      
      // Find processing jobs that haven't updated in 5 minutes
      const stuckJobs = await JobStatus.findAll({
        where: {
          status: 'processing',
          updatedAt: {
            [Op.lt]: fiveMinutesAgo
          }
        }
      });

      for (const job of stuckJobs) {
        await this.createAlert({
          type: 'JOB_STUCK',
          severity: 'MEDIUM',
          jobId: job.jobId,
          jobType: job.jobType,
          message: `Job ${job.jobId} of type ${job.jobType} appears to be stuck`,
          details: {
            progress: job.progress,
            stage: job.stage,
            nodeId: job.nodeId
          }
        });
      }
    } catch (error) {
      this.logger.error('Failed to check for stuck jobs', { error: error.message });
    }
  }

  /**
   * Check system health and generate alerts for resource issues
   */
  async checkSystemHealth() {
    try {
      // This would integrate with a system monitoring service
      // For now, we'll simulate basic checks
      const healthCheck = await this.performHealthCheck();
      
      if (healthCheck.status === 'critical') {
        await this.createAlert({
          type: 'SYSTEM_CRITICAL',
          severity: 'CRITICAL',
          message: 'System is in critical state',
          details: healthCheck.issues
        });
      } else if (healthCheck.status === 'warning') {
        await this.createAlert({
          type: 'SYSTEM_WARNING',
          severity: 'HIGH',
          message: 'System has warnings',
          details: healthCheck.issues
        });
      }
    } catch (error) {
      this.logger.error('Failed to check system health', { error: error.message });
    }
  }

  /**
   * Perform basic system health check
   * @returns {Object} Health status
   */
  async performHealthCheck() {
    // In a real implementation, this would check actual system metrics
    // For now, we'll return a basic status
    return {
      status: 'healthy',
      issues: []
    };
  }

  /**
   * Create a new alert
   * @param {Object} alertData - Alert data
   * @returns {Object} Created alert
   */
  async createAlert(alertData) {
    try {
      // Create alert in database
      const alert = await Alert.create({
        type: alertData.type,
        severity: alertData.severity,
        jobId: alertData.jobId || null,
        jobType: alertData.jobType || null,
        message: alertData.message,
        details: alertData.details || {},
        resolved: false
      });

      this.logger.info('Alert created', { 
        alertId: alert.id, 
        type: alert.type, 
        severity: alert.severity 
      });

      // Broadcast alert via WebSocket
      websocketService.broadcastJobUpdate('system', {
        type: 'ALERT',
        alert: {
          id: alert.id,
          type: alert.type,
          severity: alert.severity,
          message: alert.message,
          createdAt: alert.createdAt
        }
      });

      // In a real implementation, this would also send notifications
      // via email, SMS, or other channels based on severity
      
      return alert;
    } catch (error) {
      this.logger.error('Failed to create alert', { error: error.message, alertData });
      throw new Error(`Failed to create alert: ${error.message}`);
    }
  }

  /**
   * Get all alerts with filtering and pagination
   * @param {Object} filters - Filter criteria
   * @param {Object} pagination - Pagination options
   * @returns {Array} Alerts
   */
  async getAllAlerts(filters = {}, pagination = {}) {
    try {
      const { page = 1, limit = 10 } = pagination;
      const offset = (page - 1) * limit;

      const whereClause = {};
      if (filters.type) whereClause.type = filters.type;
      if (filters.severity) whereClause.severity = filters.severity;
      if (filters.jobId) whereClause.jobId = filters.jobId;
      if (filters.resolved !== undefined) whereClause.resolved = filters.resolved;

      const alerts = await Alert.findAndCountAll({
        where: whereClause,
        limit,
        offset,
        order: [['createdAt', 'DESC']]
      });

      return {
        data: alerts.rows,
        totalCount: alerts.count,
        page,
        limit
      };
    } catch (error) {
      this.logger.error('Failed to get alerts', { error: error.message });
      throw new Error(`Failed to get alerts: ${error.message}`);
    }
  }

  /**
   * Resolve an alert
   * @param {string} alertId - Alert ID
   * @returns {Object} Updated alert
   */
  async resolveAlert(alertId) {
    try {
      const alert = await Alert.findByPk(alertId);
      
      if (!alert) {
        throw new Error('Alert not found');
      }

      const updatedAlert = await alert.update({
        resolved: true,
        resolvedAt: new Date()
      });

      this.logger.info('Alert resolved', { alertId });
      return updatedAlert;
    } catch (error) {
      this.logger.error('Failed to resolve alert', { error: error.message, alertId });
      throw new Error(`Failed to resolve alert: ${error.message}`);
    }
  }

  /**
   * Get alert statistics
   * @returns {Object} Alert statistics
   */
  async getAlertStatistics() {
    try {
      const totalAlerts = await Alert.count();
      const unresolvedAlerts = await Alert.count({
        where: { resolved: false }
      });
      
      const alertsByType = await Alert.findAll({
        attributes: ['type', [sequelize.fn('COUNT', sequelize.col('type')), 'count']],
        where: { resolved: false },
        group: ['type']
      });

      const alertsBySeverity = await Alert.findAll({
        attributes: ['severity', [sequelize.fn('COUNT', sequelize.col('severity')), 'count']],
        where: { resolved: false },
        group: ['severity']
      });

      return {
        totalAlerts,
        unresolvedAlerts,
        alertsByType,
        alertsBySeverity
      };
    } catch (error) {
      this.logger.error('Failed to get alert statistics', { error: error.message });
      throw new Error(`Failed to get alert statistics: ${error.message}`);
    }
  }
}

module.exports = new AlertService();