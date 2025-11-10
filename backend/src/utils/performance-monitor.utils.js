const { performance } = require('perf_hooks');
const { monitoring } = require('../config/ai-ml.config');
const winston = require('winston');

/**
 * Performance Monitoring Utilities for AI/ML Service
 * Tracks and reports performance metrics for AI/ML operations
 */

class PerformanceMonitor {
  constructor() {
    this.metrics = new Map();
    this.requestCounts = new Map();
    this.errorCounts = new Map();
    this.responseTimes = new Map();
    this.enabled = monitoring.enabled;
    
    // Initialize logger
    this.logger = winston.createLogger({
      level: monitoring.logLevel,
      format: winston.format.json(),
      transports: [
        new winston.transports.Console(),
      ],
    });
    
    // Start metrics collection interval
    if (this.enabled) {
      this.startMetricsCollection();
    }
  }

  /**
   * Start timing an operation
   * @param {string} operationName - Name of the operation
   * @returns {number} Start time
   */
  startTiming(operationName) {
    if (!this.enabled) {
      return null;
    }
    
    const startTime = performance.now();
    this.logger.debug(`Starting operation: ${operationName}`);
    return startTime;
  }

  /**
   * End timing an operation and record metrics
   * @param {string} operationName - Name of the operation
   * @param {number} startTime - Start time from startTiming()
   * @param {boolean} success - Whether operation was successful
   */
  endTiming(operationName, startTime, success = true) {
    if (!this.enabled || startTime === null) {
      return;
    }
    
    const endTime = performance.now();
    const duration = endTime - startTime;
    
    // Update metrics
    this.updateMetrics(operationName, duration, success);
    
    this.logger.debug(`Operation completed: ${operationName}`, {
      duration: `${duration.toFixed(2)}ms`,
      success,
    });
  }

  /**
   * Update metrics for an operation
   * @param {string} operationName - Name of the operation
   * @param {number} duration - Duration in milliseconds
   * @param {boolean} success - Whether operation was successful
   */
  updateMetrics(operationName, duration, success) {
    // Update request count
    const requestCount = this.requestCounts.get(operationName) || 0;
    this.requestCounts.set(operationName, requestCount + 1);
    
    // Update error count if operation failed
    if (!success) {
      const errorCount = this.errorCounts.get(operationName) || 0;
      this.errorCounts.set(operationName, errorCount + 1);
    }
    
    // Update response times
    let responseTimes = this.responseTimes.get(operationName) || [];
    responseTimes.push(duration);
    
    // Keep only last 1000 response times to prevent memory issues
    if (responseTimes.length > 1000) {
      responseTimes = responseTimes.slice(-1000);
    }
    
    this.responseTimes.set(operationName, responseTimes);
  }

  /**
   * Record an error
   * @param {string} operationName - Name of the operation
   * @param {Error} error - Error object
   */
  recordError(operationName, error) {
    if (!this.enabled) {
      return;
    }
    
    const errorCount = this.errorCounts.get(operationName) || 0;
    this.errorCounts.set(operationName, errorCount + 1);
    
    this.logger.error(`Error in operation: ${operationName}`, {
      error: error.message,
      stack: error.stack,
    });
  }

  /**
   * Get performance metrics for an operation
   * @param {string} operationName - Name of the operation
   * @returns {Object} Performance metrics
   */
  getMetrics(operationName) {
    const requestCount = this.requestCounts.get(operationName) || 0;
    const errorCount = this.errorCounts.get(operationName) || 0;
    const responseTimes = this.responseTimes.get(operationName) || [];
    
    if (responseTimes.length === 0) {
      return {
        operationName,
        requestCount: 0,
        errorCount: 0,
        successRate: 100,
        avgResponseTime: 0,
        minResponseTime: 0,
        maxResponseTime: 0,
        p95ResponseTime: 0,
        p99ResponseTime: 0,
      };
    }
    
    // Calculate statistics
    const totalResponseTime = responseTimes.reduce((sum, time) => sum + time, 0);
    const avgResponseTime = totalResponseTime / responseTimes.length;
    const minResponseTime = Math.min(...responseTimes);
    const maxResponseTime = Math.max(...responseTimes);
    
    // Calculate percentiles
    const sortedTimes = [...responseTimes].sort((a, b) => a - b);
    const p95Index = Math.floor(sortedTimes.length * 0.95);
    const p99Index = Math.floor(sortedTimes.length * 0.99);
    const p95ResponseTime = sortedTimes[p95Index];
    const p99ResponseTime = sortedTimes[p99Index];
    
    const successRate = ((requestCount - errorCount) / requestCount) * 100;
    
    return {
      operationName,
      requestCount,
      errorCount,
      successRate: parseFloat(successRate.toFixed(2)),
      avgResponseTime: parseFloat(avgResponseTime.toFixed(2)),
      minResponseTime: parseFloat(minResponseTime.toFixed(2)),
      maxResponseTime: parseFloat(maxResponseTime.toFixed(2)),
      p95ResponseTime: parseFloat(p95ResponseTime.toFixed(2)),
      p99ResponseTime: parseFloat(p99ResponseTime.toFixed(2)),
    };
  }

  /**
   * Get all performance metrics
   * @returns {Array} Array of performance metrics for all operations
   */
  getAllMetrics() {
    const allOperations = new Set([
      ...this.requestCounts.keys(),
      ...this.errorCounts.keys(),
      ...this.responseTimes.keys(),
    ]);
    
    return Array.from(allOperations).map(operationName => 
      this.getMetrics(operationName)
    );
  }

  /**
   * Reset metrics for an operation
   * @param {string} operationName - Name of the operation
   */
  resetMetrics(operationName) {
    this.requestCounts.delete(operationName);
    this.errorCounts.delete(operationName);
    this.responseTimes.delete(operationName);
    
    this.logger.info(`Metrics reset for operation: ${operationName}`);
  }

  /**
   * Reset all metrics
   */
  resetAllMetrics() {
    this.requestCounts.clear();
    this.errorCounts.clear();
    this.responseTimes.clear();
    
    this.logger.info('All metrics reset');
  }

  /**
   * Start metrics collection interval
   */
  startMetricsCollection() {
    // Log summary metrics every 5 minutes
    setInterval(() => {
      const allMetrics = this.getAllMetrics();
      
      if (allMetrics.length > 0) {
        this.logger.info('Performance Metrics Summary', {
          timestamp: new Date().toISOString(),
          metrics: allMetrics,
        });
      }
    }, 300000); // 5 minutes
  }

  /**
   * Get system performance metrics
   * @returns {Object} System performance metrics
   */
  getSystemMetrics() {
    const memoryUsage = process.memoryUsage();
    const cpuUsage = process.cpuUsage();
    
    return {
      memory: {
        rss: Math.round(memoryUsage.rss / 1024 / 1024), // MB
        heapTotal: Math.round(memoryUsage.heapTotal / 1024 / 1024), // MB
        heapUsed: Math.round(memoryUsage.heapUsed / 1024 / 1024), // MB
        external: Math.round(memoryUsage.external / 1024 / 1024), // MB
      },
      cpu: {
        user: cpuUsage.user / 1000, // microseconds to milliseconds
        system: cpuUsage.system / 1000, // microseconds to milliseconds
      },
      uptime: process.uptime(),
    };
  }

  /**
   * Create a performance monitoring wrapper for async functions
   * @param {string} operationName - Name of the operation
   * @param {Function} asyncFunction - Async function to monitor
   * @returns {Function} Wrapped function
   */
  createMonitoredFunction(operationName, asyncFunction) {
    return async (...args) => {
      const startTime = this.startTiming(operationName);
      let success = true;
      
      try {
        const result = await asyncFunction(...args);
        this.endTiming(operationName, startTime, success);
        return result;
      } catch (error) {
        success = false;
        this.endTiming(operationName, startTime, success);
        this.recordError(operationName, error);
        throw error;
      }
    };
  }
}

// Export singleton instance
module.exports = new PerformanceMonitor();