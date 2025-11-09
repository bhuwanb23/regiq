const { DataPipelineJob } = require('../models');

class BatchProcessingService {
  async createBatchJob(jobData) {
    try {
      const job = await DataPipelineJob.create({
        ...jobData,
        pipelineType: 'batch',
        status: 'pending'
      });
      return job;
    } catch (error) {
      throw new Error(`Failed to create batch processing job: ${error.message}`);
    }
  }

  async getBatchJobById(id) {
    try {
      const job = await DataPipelineJob.findByPk(id);
      if (!job) {
        throw new Error('Batch processing job not found');
      }
      return job;
    } catch (error) {
      throw new Error(`Failed to get batch processing job: ${error.message}`);
    }
  }

  async getAllBatchJobs(limit = 10, offset = 0) {
    try {
      const { rows, count } = await DataPipelineJob.findAndCountAll({
        where: { pipelineType: 'batch' },
        limit,
        offset,
        order: [['created_at', 'DESC']]
      });
      return { jobs: rows, count, limit, offset };
    } catch (error) {
      throw new Error(`Failed to list batch processing jobs: ${error.message}`);
    }
  }

  async updateBatchJob(id, updateData) {
    try {
      const job = await this.getBatchJobById(id);
      const updatedJob = await job.update(updateData);
      return updatedJob;
    } catch (error) {
      throw new Error(`Failed to update batch processing job: ${error.message}`);
    }
  }

  async deleteBatchJob(id) {
    try {
      const job = await this.getBatchJobById(id);
      await job.destroy();
      return { success: true, message: 'Batch processing job deleted successfully' };
    } catch (error) {
      throw new Error(`Failed to delete batch processing job: ${error.message}`);
    }
  }

  async startBatchProcessing(jobId, processDataFunction) {
    try {
      // Update job status to in_progress
      let job = await this.getBatchJobById(jobId);
      await job.update({
        status: 'in_progress',
        startTime: new Date()
      });

      // Process data in batches
      const batchSize = job.configuration?.batchSize || 1000;
      const totalRecords = job.totalRecords || 0;
      let recordsProcessed = 0;

      // Simulate batch processing
      while (recordsProcessed < totalRecords) {
        const currentBatchSize = Math.min(batchSize, totalRecords - recordsProcessed);
        
        // Process the batch
        await processDataFunction(job, recordsProcessed, currentBatchSize);
        
        recordsProcessed += currentBatchSize;
        
        // Update progress
        const progress = (recordsProcessed / totalRecords) * 100;
        job = await job.update({
          recordsProcessed: recordsProcessed,
          progress: progress,
          stage: `Processing batch ${Math.ceil(recordsProcessed / batchSize)}`
        });

        // Simulate processing time
        await new Promise(resolve => setTimeout(resolve, 100));
      }

      // Update job status to completed
      await job.update({
        status: 'completed',
        endTime: new Date(),
        progress: 100.0
      });

      return { success: true, message: 'Batch processing completed successfully' };
    } catch (error) {
      // Update job status to failed
      try {
        const job = await this.getBatchJobById(jobId);
        await job.update({
          status: 'failed',
          endTime: new Date(),
          errorMessage: error.message
        });
      } catch (updateError) {
        console.error(`Failed to update job status to failed: ${updateError.message}`);
      }
      
      throw new Error(`Failed to process batch: ${error.message}`);
    }
  }

  async processBatchChunk(job, startIndex, batchSize) {
    try {
      // This is where the actual batch processing logic would go
      // For now, we'll just simulate processing
      console.log(`Processing batch ${startIndex} to ${startIndex + batchSize} for job ${job.id}`);
      
      // Simulate some processing work
      await new Promise(resolve => setTimeout(resolve, 50));
      
      return { 
        success: true, 
        processedCount: batchSize,
        startIndex: startIndex
      };
    } catch (error) {
      throw new Error(`Failed to process batch chunk: ${error.message}`);
    }
  }

  async getPendingBatchJobs() {
    try {
      const jobs = await DataPipelineJob.findAll({
        where: { 
          pipelineType: 'batch',
          status: 'pending'
        },
        order: [['priority', 'DESC'], ['created_at', 'ASC']]
      });
      return jobs;
    } catch (error) {
      throw new Error(`Failed to get pending batch jobs: ${error.message}`);
    }
  }

  async retryFailedBatchJob(jobId) {
    try {
      const job = await this.getBatchJobById(jobId);
      
      if (job.status !== 'failed') {
        throw new Error('Only failed jobs can be retried');
      }

      // Reset job for retry
      await job.update({
        status: 'pending',
        progress: 0.0,
        recordsProcessed: 0,
        errorMessage: null,
        retryCount: (job.retryCount || 0) + 1
      });

      return job;
    } catch (error) {
      throw new Error(`Failed to retry batch job: ${error.message}`);
    }
  }
}

module.exports = new BatchProcessingService();