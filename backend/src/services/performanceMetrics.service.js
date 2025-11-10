const { JobStatus, JobHistory, sequelize } = require('../models');
const winston = require('winston');
const os = require('os');

class PerformanceMetricsService {
  constructor() {
    // Initialize logger
    this.logger = winston.createLogger({
      level: 'info',
      format: winston.format.json(),
      transports: [
        new winston.transports.Console(),
      ],
    });

    // Metrics storage
    this.metrics = new Map();
    this.resourceUsage = {
      cpu: 0,
      memory: 0,
      disk: 0
    };

    // Start collecting metrics
    this.startMetricsCollection();
  }

  /**
   * Start metrics collection interval
   */
  startMetricsCollection() {
    // Collect system metrics every 30 seconds
    setInterval(() => {
      this.collectSystemMetrics();
    }, 30000);

    // Collect job metrics every minute
    setInterval(() => {
      this.collectJobMetrics();
    }, 60000);
  }

  /**
   * Collect system resource metrics
   */
  collectSystemMetrics() {
    try {
      // CPU usage
      const cpus = os.cpus();
      let totalIdle = 0;
      let totalTick = 0;
      
      for (let i = 0; i < cpus.length; i++) {
        const cpu = cpus[i];
        for (const type in cpu.times) {
          totalTick += cpu.times[type];
        }
        totalIdle += cpu.times.idle;
      }
      
      const idle = totalIdle / cpus.length;
      const total = totalTick / cpus.length;
      const usage = (1 - idle / total) * 100;
      
      this.resourceUsage.cpu = Math.round(usage * 100) / 100;

      // Memory usage
      const memoryUsage = process.memoryUsage();
      this.resourceUsage.memory = Math.round((memoryUsage.heapUsed / memoryUsage.heapTotal) * 100 * 100) / 100;

      // Disk usage (simplified)
      try {
        const diskInfo = os.freemem() / os.totalmem();
        this.resourceUsage.disk = Math.round((1 - diskInfo) * 100 * 100) / 100;
      } catch (error) {
        this.logger.warn('Failed to get disk usage', { error: error.message });
      }

      this.logger.debug('System metrics collected', this.resourceUsage);
    } catch (error) {
      this.logger.error('Failed to collect system metrics', { error: error.message });
    }
  }

  /**
   * Collect job-related metrics
   */
  async collectJobMetrics() {
    try {
      // Get job status counts
      const statusCounts = await JobStatus.findAll({
        attributes: ['status', [sequelize.fn('COUNT', sequelize.col('status')), 'count']],
        group: ['status'],
        raw: true
      });

      // Get recent job completion times
      const recentJobs = await JobHistory.findAll({
        where: {
          status: 'completed',
          createdAt: {
            [sequelize.Op.gte]: new Date(Date.now() - 60 * 60 * 1000) // Last hour
          }
        },
        order: [['createdAt', 'DESC']],
        limit: 50
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

      // Store metrics
      this.metrics.set('jobMetrics', {
        statusCounts,
        avgCompletionTime,
        failureRate,
        totalJobs,
        failedJobs,
        recentJobs: recentJobs.length,
        timestamp: new Date()
      });

      this.logger.debug('Job metrics collected', {
        avgCompletionTime,
        failureRate,
        totalJobs,
        recentJobs: recentJobs.length
      });
    } catch (error) {
      this.logger.error('Failed to collect job metrics', { error: error.message });
    }
  }

  /**
   * Record job execution time
   * @param {string} jobId - Job ID
   * @param {number} executionTime - Execution time in milliseconds
   */
  recordJobExecutionTime(jobId, executionTime) {
    try {
      const jobMetrics = this.metrics.get('jobExecutionTimes') || [];
      jobMetrics.push({
        jobId,
        executionTime,
        timestamp: new Date()
      });

      // Keep only last 1000 entries
      if (jobMetrics.length > 1000) {
        jobMetrics.shift();
      }

      this.metrics.set('jobExecutionTimes', jobMetrics);
      this.logger.debug('Job execution time recorded', { jobId, executionTime });
    } catch (error) {
      this.logger.error('Failed to record job execution time', { error: error.message, jobId });
    }
  }

  /**
   * Record throughput metric
   * @param {string} jobId - Job ID
   * @param {number} recordsProcessed - Number of records processed
   * @param {number} executionTime - Execution time in milliseconds
   */
  recordThroughput(jobId, recordsProcessed, executionTime) {
    try {
      const throughput = recordsProcessed / (executionTime / 1000); // records per second
      const throughputMetrics = this.metrics.get('throughput') || [];
      throughputMetrics.push({
        jobId,
        throughput,
        recordsProcessed,
        executionTime,
        timestamp: new Date()
      });

      // Keep only last 1000 entries
      if (throughputMetrics.length > 1000) {
        throughputMetrics.shift();
      }

      this.metrics.set('throughput', throughputMetrics);
      this.logger.debug('Throughput recorded', { jobId, throughput });
    } catch (error) {
      this.logger.error('Failed to record throughput', { error: error.message, jobId });
    }
  }

  /**
   * Get current system resource usage
   * @returns {Object} Resource usage metrics
   */
  getResourceUsage() {
    return {
      ...this.resourceUsage,
      timestamp: new Date()
    };
  }

  /**
   * Get job metrics
   * @returns {Object} Job metrics
   */
  async getJobMetrics() {
    return this.metrics.get('jobMetrics') || {};
  }

  /**
   * Get recent job execution times
   * @param {number} limit - Number of recent entries to return
   * @returns {Array} Recent job execution times
   */
  getRecentJobExecutionTimes(limit = 50) {
    const jobExecutionTimes = this.metrics.get('jobExecutionTimes') || [];
    return jobExecutionTimes.slice(-limit);
  }

  /**
   * Get recent throughput metrics
   * @param {number} limit - Number of recent entries to return
   * @returns {Array} Recent throughput metrics
   */
  getRecentThroughput(limit = 50) {
    const throughput = this.metrics.get('throughput') || [];
    return throughput.slice(-limit);
  }

  /**
   * Get all performance metrics
   * @returns {Object} All performance metrics
   */
  async getAllMetrics() {
    return {
      resourceUsage: this.getResourceUsage(),
      jobMetrics: await this.getJobMetrics(),
      jobExecutionTimes: this.getRecentJobExecutionTimes(),
      throughput: this.getRecentThroughput()
    };
  }

  /**
   * Get percentile metrics for job execution times
   * @param {number} percentile - Percentile to calculate (e.g., 95 for 95th percentile)
   * @returns {Object} Percentile metrics
   */
  getExecutionTimePercentiles(percentile = 95) {
    try {
      const jobExecutionTimes = this.metrics.get('jobExecutionTimes') || [];
      if (jobExecutionTimes.length === 0) {
        return { percentile, value: 0 };
      }

      // Sort execution times
      const sortedTimes = [...jobExecutionTimes].sort((a, b) => a.executionTime - b.executionTime);
      
      // Calculate percentile
      const index = Math.floor((percentile / 100) * (sortedTimes.length - 1));
      const value = sortedTimes[index].executionTime;
      
      return { percentile, value };
    } catch (error) {
      this.logger.error('Failed to calculate execution time percentiles', { error: error.message });
      return { percentile, value: 0 };
    }
  }

  /**
   * Get system health status
   * @returns {Object} System health status
   */
  getSystemHealth() {
    const resourceUsage = this.getResourceUsage();
    
    let status = 'healthy';
    let issues = [];
    
    if (resourceUsage.cpu > 80) {
      status = 'warning';
      issues.push('High CPU usage');
    }
    
    if (resourceUsage.memory > 80) {
      status = 'warning';
      issues.push('High memory usage');
    }
    
    if (resourceUsage.disk > 90) {
      status = 'critical';
      issues.push('High disk usage');
    }
    
    return {
      status,
      resourceUsage,
      issues,
      timestamp: new Date()
    };
  }
}

module.exports = new PerformanceMetricsService();