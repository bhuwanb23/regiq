const dataValidationService = require('../services/dataValidation.service');
const preprocessingService = require('../services/preprocessing.service');
const batchProcessingService = require('../services/batchProcessing.service');
const streamProcessingService = require('../services/streamProcessing.service');
const qualityMonitoringService = require('../services/qualityMonitoring.service');
const lineageTrackingService = require('../services/lineageTracking.service');
const errorHandlingService = require('../services/errorHandling.service');

class DataProcessingController {
  async validateData(req, res) {
    try {
      const { data, ruleIds } = req.body;
      const result = await dataValidationService.validateData(data, ruleIds);
      res.status(200).json({
        success: true,
        message: 'Data validation completed',
        data: result
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  async cleanData(req, res) {
    try {
      const { data, cleaningRules } = req.body;
      const result = await preprocessingService.cleanData(data, cleaningRules);
      res.status(200).json({
        success: true,
        message: 'Data cleaning completed',
        data: result
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }

  async transformData(req, res) {
    try {
      const { data, transformations } = req.body;
      const result = await preprocessingService.transformData(data, transformations);
      res.status(200).json({
        success: true,
        message: 'Data transformation completed',
        data: result
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }

  async standardizeData(req, res) {
    try {
      const { data, standardizationRules } = req.body;
      const result = await preprocessingService.standardizeData(data, standardizationRules);
      res.status(200).json({
        success: true,
        message: 'Data standardization completed',
        data: result
      });
    } catch (error) {
      res.status(500).json({
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
        batchProcessingService.processBatchChunk
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

  async createStreamProcessor(req, res) {
    try {
      const { streamId, config } = req.body;
      const processor = await streamProcessingService.createStreamProcessor(streamId, config);
      res.status(201).json({
        success: true,
        message: 'Stream processor created successfully',
        data: processor
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  async startStreamProcessing(req, res) {
    try {
      const { streamId } = req.params;
      const processor = await streamProcessingService.startStreamProcessing(
        streamId, 
        (data) => {
          // Process data here
          console.log('Processing stream data:', data);
          return Promise.resolve();
        }
      );
      res.status(200).json({
        success: true,
        message: 'Stream processing started',
        data: processor
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  async addDataToStream(req, res) {
    try {
      const { streamId } = req.params;
      const { data } = req.body;
      const result = await streamProcessingService.addDataToStream(streamId, data);
      res.status(200).json({
        success: true,
        message: 'Data added to stream',
        data: result
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  async stopStreamProcessing(req, res) {
    try {
      const { streamId } = req.params;
      const processor = await streamProcessingService.stopStreamProcessing(streamId);
      res.status(200).json({
        success: true,
        message: 'Stream processing stopped',
        data: processor
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  async getStreamProcessor(req, res) {
    try {
      const { streamId } = req.params;
      const processor = await streamProcessingService.getStreamProcessor(streamId);
      res.status(200).json({
        success: true,
        message: 'Stream processor retrieved',
        data: processor
      });
    } catch (error) {
      res.status(404).json({
        success: false,
        message: error.message
      });
    }
  }

  async getAllStreamProcessors(req, res) {
    try {
      const processors = await streamProcessingService.getAllStreamProcessors();
      res.status(200).json({
        success: true,
        message: 'Stream processors retrieved',
        data: processors
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }
}

module.exports = new DataProcessingController();