const { DataPipelineJob } = require('../models');

class ErrorHandlingService {
  async logError(jobId, error, context = {}) {
    try {
      console.error(`Data Pipeline Error - Job: ${jobId}`, {
        error: error.message,
        stack: error.stack,
        context: context,
        timestamp: new Date().toISOString()
      });

      // Update job with error information
      if (jobId) {
        const job = await DataPipelineJob.findByPk(jobId);
        if (job) {
          await job.update({
            status: 'failed',
            errorMessage: error.message,
            endTime: new Date()
          });
        }
      }

      return { 
        success: true, 
        message: 'Error logged successfully',
        errorId: this.generateErrorId()
      };
    } catch (logError) {
      console.error('Failed to log error:', logError);
      throw new Error(`Failed to log error: ${logError.message}`);
    }
  }

  generateErrorId() {
    return 'err_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
  }

  async retryJob(jobId, maxRetries = 3) {
    try {
      const job = await DataPipelineJob.findByPk(jobId);
      if (!job) {
        throw new Error('Job not found');
      }

      if (job.retryCount >= maxRetries) {
        throw new Error(`Maximum retries (${maxRetries}) exceeded`);
      }

      // Reset job for retry
      await job.update({
        status: 'pending',
        progress: 0.0,
        recordsProcessed: 0,
        errorMessage: null,
        retryCount: (job.retryCount || 0) + 1,
        startTime: null,
        endTime: null
      });

      return { 
        success: true, 
        message: `Job ${jobId} reset for retry (${job.retryCount + 1}/${maxRetries})` 
      };
    } catch (error) {
      throw new Error(`Failed to retry job: ${error.message}`);
    }
  }

  async handleValidationError(jobId, validationErrors) {
    try {
      console.warn(`Validation errors in job ${jobId}:`, validationErrors);
      
      // Update job with validation error information
      if (jobId) {
        const job = await DataPipelineJob.findByPk(jobId);
        if (job) {
          await job.update({
            status: 'failed',
            errorMessage: `Validation failed: ${validationErrors.map(e => e.message).join(', ')}`
          });
        }
      }

      return { 
        success: true, 
        message: 'Validation errors handled successfully' 
      };
    } catch (error) {
      throw new Error(`Failed to handle validation errors: ${error.message}`);
    }
  }

  async handleProcessingError(jobId, error, recordIndex = null) {
    try {
      console.error(`Processing error in job ${jobId} at record ${recordIndex}:`, error);
      
      // Update job with processing error information
      if (jobId) {
        const job = await DataPipelineJob.findByPk(jobId);
        if (job) {
          const errorCount = (job.errorCount || 0) + 1;
          await job.update({
            errorCount: errorCount,
            errorMessage: error.message
          });
        }
      }

      return { 
        success: true, 
        message: 'Processing error handled successfully' 
      };
    } catch (handleError) {
      throw new Error(`Failed to handle processing error: ${handleError.message}`);
    }
  }

  async getJobErrors(jobId, limit = 10, offset = 0) {
    try {
      const job = await DataPipelineJob.findByPk(jobId);
      if (!job) {
        throw new Error('Job not found');
      }

      // In a real implementation, we would query an errors table
      // For now, we'll return the job's error information
      const errors = [];
      
      if (job.errorMessage) {
        errors.push({
          id: this.generateErrorId(),
          jobId: job.id,
          message: job.errorMessage,
          timestamp: job.updated_at,
          type: 'job_error',
          severity: 'error'
        });
      }

      return { 
        errors: errors.slice(offset, offset + limit),
        count: errors.length,
        limit: limit,
        offset: offset
      };
    } catch (error) {
      throw new Error(`Failed to get job errors: ${error.message}`);
    }
  }

  async createErrorReport(jobId) {
    try {
      const job = await DataPipelineJob.findByPk(jobId);
      if (!job) {
        throw new Error('Job not found');
      }

      const errorReport = {
        jobId: job.id,
        jobName: job.fileName,
        status: job.status,
        errorMessage: job.errorMessage,
        startTime: job.startTime,
        endTime: job.endTime,
        duration: job.endTime && job.startTime ? 
          job.endTime.getTime() - job.startTime.getTime() : null,
        recordsProcessed: job.recordsProcessed,
        totalRecords: job.totalRecords,
        errorCount: job.errorCount,
        retryCount: job.retryCount,
        generatedAt: new Date()
      };

      return errorReport;
    } catch (error) {
      throw new Error(`Failed to create error report: ${error.message}`);
    }
  }

  async notifyOnError(jobId, notificationConfig = {}) {
    try {
      const job = await DataPipelineJob.findByPk(jobId);
      if (!job || job.status !== 'failed') {
        return { success: true, message: 'No error to notify about' };
      }

      // In a real implementation, this would send notifications
      // via email, Slack, SMS, etc. based on notificationConfig
      console.log(`Notification: Job ${jobId} failed with error: ${job.errorMessage}`);
      
      // Log notification
      console.log(`Error notification sent for job ${jobId}`, {
        jobId: jobId,
        error: job.errorMessage,
        notificationType: notificationConfig.type || 'console',
        timestamp: new Date().toISOString()
      });

      return { 
        success: true, 
        message: 'Error notification sent successfully' 
      };
    } catch (error) {
      throw new Error(`Failed to send error notification: ${error.message}`);
    }
  }

  async recoverFromError(jobId, recoveryStrategy = 'retry') {
    try {
      const job = await DataPipelineJob.findByPk(jobId);
      if (!job) {
        throw new Error('Job not found');
      }

      switch (recoveryStrategy) {
        case 'retry':
          return await this.retryJob(jobId);
          
        case 'skip':
          await job.update({
            status: 'completed',
            progress: 100.0,
            endTime: new Date()
          });
          return { success: true, message: 'Job marked as completed (skipped)' };
          
        case 'partial':
          // In a real implementation, this would attempt partial recovery
          await job.update({
            status: 'completed',
            progress: 100.0,
            endTime: new Date()
          });
          return { success: true, message: 'Job marked as completed (partial recovery)' };
          
        default:
          throw new Error(`Unknown recovery strategy: ${recoveryStrategy}`);
      }
    } catch (error) {
      throw new Error(`Failed to recover from error: ${error.message}`);
    }
  }
}

module.exports = new ErrorHandlingService();