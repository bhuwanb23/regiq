const jobStatusService = require('../services/jobStatus.service');
const performanceMetricsService = require('../services/performanceMetrics.service');

class JobStatusController {
  /**
   * Get job status by ID
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   */
  async getJobStatus(req, res) {
    try {
      const { jobId } = req.params;
      const jobStatus = await jobStatusService.getJobStatus(jobId);
      res.json({
        success: true,
        data: jobStatus
      });
    } catch (error) {
      res.status(404).json({
        success: false,
        message: error.message
      });
    }
  }

  /**
   * Get all job statuses with filtering and pagination
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   */
  async getAllJobStatuses(req, res) {
    try {
      const { page, limit, jobType, status, priority } = req.query;
      const filters = {};
      if (jobType) filters.jobType = jobType;
      if (status) filters.status = status;
      if (priority) filters.priority = priority;

      const pagination = {
        page: parseInt(page) || 1,
        limit: parseInt(limit) || 10
      };

      const result = await jobStatusService.getAllJobStatuses(filters, pagination);
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
   * Get job history with filtering and pagination
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   */
  async getJobHistory(req, res) {
    try {
      const { page, limit, jobId, jobType, status } = req.query;
      const filters = {};
      if (jobId) filters.jobId = jobId;
      if (jobType) filters.jobType = jobType;
      if (status) filters.status = status;

      const pagination = {
        page: parseInt(page) || 1,
        limit: parseInt(limit) || 10
      };

      const result = await jobStatusService.getJobHistory(filters, pagination);
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
   * Cancel a job
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   */
  async cancelJob(req, res) {
    try {
      const { jobId } = req.params;
      const { reason } = req.body;
      const result = await jobStatusService.cancelJob(jobId, reason);
      res.json({
        success: true,
        data: result,
        message: 'Job cancelled successfully'
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  /**
   * Update job progress
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   */
  async updateProgress(req, res) {
    try {
      const { jobId } = req.params;
      const { progress, stage, resourceUsage } = req.body;
      const result = await jobStatusService.updateProgress(jobId, progress, {
        stage,
        resourceUsage
      });
      res.json({
        success: true,
        data: result,
        message: 'Job progress updated successfully'
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  /**
   * Get performance metrics
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   */
  async getPerformanceMetrics(req, res) {
    try {
      const metrics = await jobStatusService.getPerformanceMetrics();
      res.json({
        success: true,
        data: metrics
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }

  /**
   * Get real-time performance metrics
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   */
  async getRealTimeMetrics(req, res) {
    try {
      const [jobMetrics, resourceUsage] = await Promise.all([
        performanceMetricsService.getJobMetrics(),
        performanceMetricsService.getResourceUsage()
      ]);

      res.json({
        success: true,
        data: {
          resourceUsage,
          jobMetrics
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
   * Get system health status
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   */
  async getSystemHealth(req, res) {
    try {
      const health = performanceMetricsService.getSystemHealth();
      res.json({
        success: true,
        data: health
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }
}

module.exports = new JobStatusController();