const express = require('express');
const router = express.Router();

// Controllers
const fileUploadController = require('../controllers/fileUpload.controller');
const dataProcessingController = require('../controllers/dataProcessing.controller');
const dataQualityController = require('../controllers/dataQuality.controller');
const dataLineageController = require('../controllers/dataLineage.controller');
const dataValidationController = require('../controllers/dataValidation.controller');
const dataPipelineJobController = require('../controllers/dataPipelineJob.controller');

// File Upload Routes
router.post('/upload', fileUploadController.getUploadMiddleware(), fileUploadController.uploadFile);
router.get('/uploads/:id', fileUploadController.getFileUpload);
router.get('/uploads', fileUploadController.listFileUploads);
router.put('/uploads/:id', fileUploadController.updateFileUpload);
router.delete('/uploads/:id', fileUploadController.deleteFileUpload);
router.get('/uploads-user', fileUploadController.getUserFileUploads);
router.put('/uploads/:id/status', fileUploadController.updateUploadStatus);

// Data Validation Routes
router.post('/validation-rules', dataValidationController.createValidationRule);
router.get('/validation-rules/:id', dataValidationController.getValidationRule);
router.get('/validation-rules', dataValidationController.listValidationRules);
router.put('/validation-rules/:id', dataValidationController.updateValidationRule);
router.delete('/validation-rules/:id', dataValidationController.deleteValidationRule);
router.get('/validation-rules-active', dataValidationController.getActiveValidationRules);

router.post('/validate', dataProcessingController.validateData);

// Data Preprocessing Routes
router.post('/clean', dataProcessingController.cleanData);
router.post('/transform', dataProcessingController.transformData);
router.post('/standardize', dataProcessingController.standardizeData);

// Batch Processing Routes
router.post('/batch', dataPipelineJobController.createBatchJob);
router.get('/batch/:id', dataPipelineJobController.getBatchJob);
router.get('/batch', dataPipelineJobController.listBatchJobs);
router.put('/batch/:id', dataPipelineJobController.updateBatchJob);
router.delete('/batch/:id', dataPipelineJobController.deleteBatchJob);
router.post('/batch/:jobId/start', dataPipelineJobController.startBatchProcessing);
router.post('/batch/:id/retry', dataPipelineJobController.retryFailedBatchJob);
router.get('/batch-pending', dataPipelineJobController.getPendingBatchJobs);

// Stream Processing Routes
router.post('/stream', dataProcessingController.createStreamProcessor);
router.post('/stream/:streamId/start', dataProcessingController.startStreamProcessing);
router.post('/stream/:streamId/data', dataProcessingController.addDataToStream);
router.post('/stream/:streamId/stop', dataProcessingController.stopStreamProcessing);
router.get('/stream/:streamId', dataProcessingController.getStreamProcessor);
router.get('/streams', dataProcessingController.getAllStreamProcessors);

// Data Quality Routes
router.post('/quality/metrics', dataQualityController.createQualityMetric);
router.get('/quality/metrics/:id', dataQualityController.getQualityMetric);
router.get('/quality/metrics', dataQualityController.listQualityMetrics);
router.put('/quality/metrics/:id', dataQualityController.updateQualityMetric);
router.delete('/quality/metrics/:id', dataQualityController.deleteQualityMetric);
router.get('/quality/job/:jobId', dataQualityController.getQualityMetricsByJob);
router.post('/quality/completeness', dataQualityController.calculateCompletenessMetric);
router.post('/quality/accuracy', dataQualityController.calculateAccuracyMetric);
router.post('/quality/uniqueness', dataQualityController.calculateUniquenessMetric);
router.get('/quality/summary/:jobId', dataQualityController.getQualitySummary);
router.get('/quality/thresholds/:jobId', dataQualityController.checkQualityThresholds);

// Data Lineage Routes
router.post('/lineage', dataLineageController.createLineageRecord);
router.get('/lineage/:id', dataLineageController.getLineageRecord);
router.get('/lineage', dataLineageController.listLineageRecords);
router.put('/lineage/:id', dataLineageController.updateLineageRecord);
router.delete('/lineage/:id', dataLineageController.deleteLineageRecord);
router.get('/lineage/job/:jobId', dataLineageController.getLineageByJob);
router.post('/lineage/transformation', dataLineageController.createTransformationLineage);
router.post('/lineage/transformation/:lineageId/complete', dataLineageController.completeTransformationLineage);
router.get('/lineage/graph/:jobId', dataLineageController.getLineageGraph);
router.get('/lineage/path/:jobId', dataLineageController.getLineagePath);
router.get('/lineage/impact/:jobId', dataLineageController.getImpactAnalysis);

module.exports = router;