const { jobQueue } = require('../config/ai-ml.config');
const winston = require('winston');

/**
 * Job Queue Utilities for AI/ML Service
 * Handles asynchronous processing of AI/ML tasks
 */

class JobQueue {
  constructor() {
    this.queue = [];
    this.processing = [];
    this.completed = [];
    this.failed = [];
    this.concurrency = jobQueue.concurrency;
    this.timeout = jobQueue.timeout;
    this.retryDelay = jobQueue.retryDelay;
    this.maxRetries = jobQueue.maxRetries;
    
    // Initialize logger
    this.logger = winston.createLogger({
      level: 'info',
      format: winston.format.json(),
      transports: [
        new winston.transports.Console(),
      ],
    });
    
    // Start processing queue
    this.startProcessing();
  }

  /**
   * Add a job to the queue
   * @param {string} type - Type of job (compliance, risk, sentiment, anomaly)
   * @param {Object} data - Job data
   * @param {Function} callback - Callback function to execute when job completes
   * @returns {string} Job ID
   */
  addJob(type, data, callback) {
    const jobId = this.generateJobId();
    const job = {
      id: jobId,
      type,
      data,
      callback,
      status: 'queued',
      createdAt: new Date(),
      retries: 0,
    };
    
    this.queue.push(job);
    this.logger.info(`Job added to queue`, { jobId, type });
    
    return jobId;
  }

  /**
   * Process jobs in the queue
   */
  async processQueue() {
    // Check if we can process more jobs
    if (this.processing.length >= this.concurrency) {
      return;
    }
    
    // Process jobs while we have capacity
    while (this.queue.length > 0 && this.processing.length < this.concurrency) {
      const job = this.queue.shift();
      job.status = 'processing';
      job.startedAt = new Date();
      this.processing.push(job);
      
      this.logger.info(`Starting job processing`, { jobId: job.id, type: job.type });
      
      // Process the job
      this.processJob(job);
    }
  }

  /**
   * Process a single job
   * @param {Object} job - Job to process
   */
  async processJob(job) {
    try {
      // Set timeout for job processing
      const timeoutPromise = new Promise((_, reject) => {
        setTimeout(() => reject(new Error('Job timeout')), this.timeout);
      });
      
      // Execute job with timeout
      const result = await Promise.race([
        job.callback(job.data),
        timeoutPromise
      ]);
      
      // Job completed successfully
      job.status = 'completed';
      job.completedAt = new Date();
      job.result = result;
      
      // Move job from processing to completed
      this.moveToCompleted(job);
      
      this.logger.info(`Job completed successfully`, { jobId: job.id, type: job.type });
    } catch (error) {
      this.logger.error(`Job failed`, { jobId: job.id, type: job.type, error: error.message });
      
      // Check if we should retry
      if (job.retries < this.maxRetries) {
        job.retries++;
        job.status = 'retrying';
        this.logger.info(`Retrying job`, { jobId: job.id, retry: job.retries });
        
        // Wait before retrying
        setTimeout(() => {
          job.status = 'queued';
          this.queue.unshift(job);
        }, this.retryDelay);
      } else {
        // Job failed permanently
        job.status = 'failed';
        job.failedAt = new Date();
        job.error = error.message;
        
        // Move job from processing to failed
        this.moveToFailed(job);
        
        this.logger.error(`Job failed permanently`, { jobId: job.id, type: job.type, error: error.message });
      }
    }
  }

  /**
   * Move job from processing to completed
   * @param {Object} job - Job to move
   */
  moveToCompleted(job) {
    const index = this.processing.findIndex(j => j.id === job.id);
    if (index !== -1) {
      this.processing.splice(index, 1);
      this.completed.push(job);
      
      // Keep only recent completed jobs
      if (this.completed.length > 1000) {
        this.completed.shift();
      }
    }
    
    // Process next job in queue
    this.processQueue();
  }

  /**
   * Move job from processing to failed
   * @param {Object} job - Job to move
   */
  moveToFailed(job) {
    const index = this.processing.findIndex(j => j.id === job.id);
    if (index !== -1) {
      this.processing.splice(index, 1);
      this.failed.push(job);
      
      // Keep only recent failed jobs
      if (this.failed.length > 1000) {
        this.failed.shift();
      }
    }
    
    // Process next job in queue
    this.processQueue();
  }

  /**
   * Start processing queue
   */
  startProcessing() {
    setInterval(() => {
      this.processQueue();
    }, 1000); // Check queue every second
  }

  /**
   * Get job status
   * @param {string} jobId - Job ID
   * @returns {Object|null} Job status or null if not found
   */
  getJobStatus(jobId) {
    // Check in all queues
    const allJobs = [...this.queue, ...this.processing, ...this.completed, ...this.failed];
    const job = allJobs.find(j => j.id === jobId);
    
    if (!job) {
      return null;
    }
    
    return {
      id: job.id,
      type: job.type,
      status: job.status,
      createdAt: job.createdAt,
      startedAt: job.startedAt,
      completedAt: job.completedAt,
      failedAt: job.failedAt,
      retries: job.retries,
    };
  }

  /**
   * Get all jobs of a specific type
   * @param {string} type - Job type
   * @returns {Array} Array of jobs
   */
  getJobsByType(type) {
    const allJobs = [...this.queue, ...this.processing, ...this.completed, ...this.failed];
    return allJobs.filter(job => job.type === type);
  }

  /**
   * Get queue statistics
   * @returns {Object} Queue statistics
   */
  getStats() {
    return {
      queued: this.queue.length,
      processing: this.processing.length,
      completed: this.completed.length,
      failed: this.failed.length,
      concurrency: this.concurrency,
      maxRetries: this.maxRetries,
    };
  }

  /**
   * Generate a unique job ID
   * @returns {string} Unique job ID
   */
  generateJobId() {
    return `job_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  /**
   * Cancel a job
   * @param {string} jobId - Job ID to cancel
   * @returns {boolean} True if job was cancelled, false otherwise
   */
  cancelJob(jobId) {
    // Check if job is in queue
    const queueIndex = this.queue.findIndex(j => j.id === jobId);
    if (queueIndex !== -1) {
      this.queue.splice(queueIndex, 1);
      this.logger.info(`Job cancelled from queue`, { jobId });
      return true;
    }
    
    // Check if job is processing
    const processingIndex = this.processing.findIndex(j => j.id === jobId);
    if (processingIndex !== -1) {
      // We can't actually stop a running job, but we can mark it as cancelled
      const job = this.processing[processingIndex];
      job.status = 'cancelled';
      this.logger.info(`Job marked as cancelled`, { jobId });
      return true;
    }
    
    return false;
  }
}

// Export singleton instance
module.exports = new JobQueue();