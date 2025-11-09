const batchProcessingService = require('../services/batchProcessing.service');

class DataPipelineJobController {
  async createBatchJob(req, res) {
    try {
      const job = await batchProcessingService.createBatchJob(req.body);
      res.status(201).json({
        success: true,
        message: 'Batch job created successfully',
        data: job
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  async getBatchJob(req, res) {
    try {
      const { id } = req.params;
      const job = await batchProcessingService.getBatchJobById(id);
      res.status(200).json({
        success: true,
        message: 'Batch job retrieved successfully',
        data: job
      });
    } catch (error) {
      res.status(404).json({
        success: false,
        message: error.message
      });
    }
  }

  async listBatchJobs(req, res) {
    try {
      const { limit = 10, offset = 0 } = req.query;
      const result = await batchProcessingService.getAllBatchJobs(
        parseInt(limit),
        parseInt(offset)
      );
      res.status(200).json({
        success: true,
        message: 'Batch jobs retrieved successfully',
        data: result
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }

  async updateBatchJob(req, res) {
    try {
      const { id } = req.params;
      const job = await batchProcessingService.updateBatchJob(id, req.body);
      res.status(200).json({
        success: true,
        message: 'Batch job updated successfully',
        data: job
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  async deleteBatchJob(req, res) {
    try {
      const { id } = req.params;
      const result = await batchProcessingService.deleteBatchJob(id);
      res.status(200).json({
        success: true,
        message: 'Batch job deleted successfully',
        data: result
      });
    } catch (error) {
      res.status(404).json({
        success: false,
        message: error.message
      });
    }
  }

  async startBatchProcessing(req, res) {
    try {
      const { jobId } = req.params;
      const result = await batchProcessingService.startBatchProcessing(
        jobId, 
        batchProcessingService.processBatchChunk.bind(batchProcessingService)
      );
      res.status(200).json({
        success: true,
        message: 'Batch processing started',
        data: result
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  async retryFailedBatchJob(req, res) {
    try {
      const { id } = req.params;
      const job = await batchProcessingService.retryFailedBatchJob(id);
      res.status(200).json({
        success: true,
        message: 'Batch job retry initiated successfully',
        data: job
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  async getPendingBatchJobs(req, res) {
    try {
      const jobs = await batchProcessingService.getPendingBatchJobs();
      res.status(200).json({
        success: true,
        message: 'Pending batch jobs retrieved successfully',
        data: jobs
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }
}

module.exports = new DataPipelineJobController();