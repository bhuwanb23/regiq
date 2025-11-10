const { JobStatus, JobHistory, sequelize } = require('../models');
const winston = require('winston');
const websocketService = require('./websocket.service');

class JobStatusService {
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
   * Create a new job status record
   * @param {Object} jobData - Job data
   * @returns {Object} Created job status
   */
  async createJobStatus(jobData) {
    try {
      const jobStatus = await JobStatus.create({
        jobId: jobData.jobId,
        jobType: jobData.jobType,
        status: jobData.status || 'pending',
        priority: jobData.priority || 'normal',
        metadata: jobData.metadata || {},
        inputParams: jobData.inputParams || {},
        ...jobData
      });

      this.logger.info('Job status created', { jobId: jobStatus.jobId, status: jobStatus.status });
      return jobStatus;
    } catch (error) {
      this.logger.error('Failed to create job status', { error: error.message, jobId: jobData.jobId });
      throw new Error(`Failed to create job status: ${error.message}`);
    }
  }

  /**
   * Get job status by job ID
   * @param {string} jobId - Job ID
   * @returns {Object} Job status
   */
  async getJobStatus(jobId) {
    try {
      const jobStatus = await JobStatus.findOne({
        where: { jobId }
      });

      if (!jobStatus) {
        throw new Error('Job not found');
      }

      return jobStatus;
    } catch (error) {
      this.logger.error('Failed to get job status', { error: error.message, jobId });
      throw new Error(`Failed to get job status: ${error.message}`);
    }
  }

  /**
   * Update job status
   * @param {string} jobId - Job ID
   * @param {Object} updateData - Data to update
   * @returns {Object} Updated job status
   */
  async updateJobStatus(jobId, updateData) {
    try {
      const jobStatus = await JobStatus.findOne({
        where: { jobId }
      });

      if (!jobStatus) {
        throw new Error('Job not found');
      }

      // If job is completing, move to history
      if (updateData.status === 'completed' || updateData.status === 'failed' || updateData.status === 'cancelled') {
        await this.moveToHistory(jobStatus);
      }

      const updatedJobStatus = await jobStatus.update(updateData);
      this.logger.info('Job status updated', { jobId, status: updatedJobStatus.status });
      
      // Broadcast update via WebSocket
      websocketService.broadcastJobUpdate(jobId, {
        status: updatedJobStatus.status,
        progress: updatedJobStatus.progress,
        stage: updatedJobStatus.stage,
        updatedAt: updatedJobStatus.updatedAt
      });
      
      return updatedJobStatus;
    } catch (error) {
      this.logger.error('Failed to update job status', { error: error.message, jobId });
      throw new Error(`Failed to update job status: ${error.message}`);
    }
  }

  /**
   * Get all job statuses with filtering and pagination
   * @param {Object} filters - Filter criteria
   * @param {Object} pagination - Pagination options
   * @returns {Array} Job statuses
   */
  async getAllJobStatuses(filters = {}, pagination = {}) {
    try {
      const { page = 1, limit = 10 } = pagination;
      const offset = (page - 1) * limit;

      const whereClause = {};
      if (filters.jobType) whereClause.jobType = filters.jobType;
      if (filters.status) whereClause.status = filters.status;
      if (filters.priority) whereClause.priority = filters.priority;

      const jobStatuses = await JobStatus.findAndCountAll({
        where: whereClause,
        limit,
        offset,
        order: [['createdAt', 'DESC']]
      });

      return {
        data: jobStatuses.rows,
        totalCount: jobStatuses.count,
        page,
        limit
      };
    } catch (error) {
      this.logger.error('Failed to get job statuses', { error: error.message });
      throw new Error(`Failed to get job statuses: ${error.message}`);
    }
  }

  /**
   * Cancel a job
   * @param {string} jobId - Job ID
   * @param {string} reason - Cancellation reason
   * @returns {Object} Updated job status
   */
  async cancelJob(jobId, reason = '') {
    try {
      const jobStatus = await JobStatus.findOne({
        where: { jobId }
      });

      if (!jobStatus) {
        throw new Error('Job not found');
      }

      if (jobStatus.status === 'completed' || jobStatus.status === 'failed') {
        throw new Error('Cannot cancel completed or failed job');
      }

      const updatedJobStatus = await jobStatus.update({
        status: 'cancelled',
        cancelledAt: new Date(),
        errorMessage: reason
      });

      this.logger.info('Job cancelled', { jobId, reason });
      
      // Broadcast cancellation update via WebSocket
      websocketService.broadcastJobUpdate(jobId, {
        status: 'cancelled',
        reason,
        cancelledAt: updatedJobStatus.cancelledAt,
        updatedAt: updatedJobStatus.updatedAt
      });
      
      return updatedJobStatus;
    } catch (error) {
      this.logger.error('Failed to cancel job', { error: error.message, jobId });
      throw new Error(`Failed to cancel job: ${error.message}`);
    }
  }

  /**
   * Move job to history when completed/failed/cancelled
   * @param {Object} jobStatus - Job status object
   */
  async moveToHistory(jobStatus) {
    try {
      // Calculate duration if started
      let duration = null;
      if (jobStatus.startedAt) {
        const endTime = jobStatus.completedAt || jobStatus.failedAt || jobStatus.cancelledAt || new Date();
        duration = endTime.getTime() - jobStatus.startedAt.getTime();
      }

      // Create history record
      await JobHistory.create({
        jobId: jobStatus.jobId,
        jobType: jobStatus.jobType,
        status: jobStatus.status,
        progress: jobStatus.progress,
        stage: jobStatus.stage,
        priority: jobStatus.priority,
        startedAt: jobStatus.startedAt,
        completedAt: jobStatus.completedAt,
        failedAt: jobStatus.failedAt,
        cancelledAt: jobStatus.cancelledAt,
        duration,
        errorMessage: jobStatus.errorMessage,
        errorStack: jobStatus.errorStack,
        workerId: jobStatus.workerId,
        nodeId: jobStatus.nodeId,
        metadata: jobStatus.metadata,
        inputParams: jobStatus.inputParams,
        outputData: jobStatus.outputData,
        resourceUsage: jobStatus.resourceUsage,
        throughput: jobStatus.throughput,
        recordsProcessed: jobStatus.recordsProcessed,
        totalRecords: jobStatus.totalRecords,
        retryCount: jobStatus.retryCount
      });

      this.logger.info('Job moved to history', { jobId: jobStatus.jobId });
    } catch (error) {
      this.logger.error('Failed to move job to history', { error: error.message, jobId: jobStatus.jobId });
      // Don't throw error here as this is a background operation
    }
  }

  /**
   * Get job history with filtering and pagination
   * @param {Object} filters - Filter criteria
   * @param {Object} pagination - Pagination options
   * @returns {Array} Job histories
   */
  async getJobHistory(filters = {}, pagination = {}) {
    try {
      const { page = 1, limit = 10 } = pagination;
      const offset = (page - 1) * limit;

      const whereClause = {};
      if (filters.jobId) whereClause.jobId = filters.jobId;
      if (filters.jobType) whereClause.jobType = filters.jobType;
      if (filters.status) whereClause.status = filters.status;

      const jobHistories = await JobHistory.findAndCountAll({
        where: whereClause,
        limit,
        offset,
        order: [['createdAt', 'DESC']]
      });

      return {
        data: jobHistories.rows,
        totalCount: jobHistories.count,
        page,
        limit
      };
    } catch (error) {
      this.logger.error('Failed to get job history', { error: error.message });
      throw new Error(`Failed to get job history: ${error.message}`);
    }
  }

  /**
   * Update job progress
   * @param {string} jobId - Job ID
   * @param {number} progress - Progress percentage (0-100)
   * @param {Object} additionalData - Additional data to update
   */
  async updateProgress(jobId, progress, additionalData = {}) {
    try {
      const jobStatus = await JobStatus.findOne({
        where: { jobId }
      });

      if (!jobStatus) {
        throw new Error('Job not found');
      }

      const updateData = {
        progress,
        ...additionalData
      };

      // Update estimated completion time if not already set
      if (!jobStatus.estimatedCompletionTime && progress > 0 && progress < 100) {
        const elapsed = Date.now() - (jobStatus.startedAt || jobStatus.createdAt).getTime();
        const estimatedTotal = elapsed / (progress / 100);
        const estimatedCompletionTime = new Date(Date.now() + (estimatedTotal - elapsed));
        updateData.estimatedCompletionTime = estimatedCompletionTime;
      }

      const updatedJobStatus = await jobStatus.update(updateData);
      this.logger.info('Job progress updated', { jobId, progress });
      
      // Broadcast progress update via WebSocket
      websocketService.broadcastJobUpdate(jobId, {
        status: updatedJobStatus.status,
        progress: updatedJobStatus.progress,
        stage: updatedJobStatus.stage,
        updatedAt: updatedJobStatus.updatedAt
      });
      
      return updatedJobStatus;
    } catch (error) {
      this.logger.error('Failed to update job progress', { error: error.message, jobId });
      throw new Error(`Failed to update job progress: ${error.message}`);
    }
  }

  /**
   * Get performance metrics
   * @returns {Object} Performance metrics
   */
  async getPerformanceMetrics() {
    try {
      // Get counts by status
      const statusCounts = await JobStatus.findAll({
        attributes: ['status', [sequelize.fn('COUNT', sequelize.col('status')), 'count']],
        group: ['status']
      });

      // Get recent job completion times
      const recentJobs = await JobHistory.findAll({
        where: {
          status: 'completed',
          createdAt: {
            [sequelize.Op.gte]: new Date(Date.now() - 24 * 60 * 60 * 1000) // Last 24 hours
          }
        },
        order: [['createdAt', 'DESC']],
        limit: 100
      });

      // Calculate average completion time
      let avgCompletionTime = 0;
      if (recentJobs.length > 0) {
        const totalDuration = recentJobs.reduce((sum, job) => sum + (job.duration || 0), 0);
        avgCompletionTime = totalDuration / recentJobs.length;
      }

      // Get failure rate
      const totalJobs = await JobHistory.count();
      const failedJobs = await JobHistory.count({
        where: { status: 'failed' }
      });
      const failureRate = totalJobs > 0 ? (failedJobs / totalJobs) * 100 : 0;

      return {
        statusCounts,
        avgCompletionTime,
        failureRate,
        totalJobs,
        failedJobs,
        recentJobs: recentJobs.length
      };
    } catch (error) {
      this.logger.error('Failed to get performance metrics', { error: error.message });
      throw new Error(`Failed to get performance metrics: ${error.message}`);
    }
  }
}

module.exports = new JobStatusService();