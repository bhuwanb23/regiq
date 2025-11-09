const lineageTrackingService = require('../services/lineageTracking.service');

class DataLineageController {
  async createLineageRecord(req, res) {
    try {
      const lineage = await lineageTrackingService.createLineageRecord(req.body);
      res.status(201).json({
        success: true,
        message: 'Lineage record created successfully',
        data: lineage
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  async getLineageRecord(req, res) {
    try {
      const { id } = req.params;
      const lineage = await lineageTrackingService.getLineageRecordById(id);
      res.status(200).json({
        success: true,
        message: 'Lineage record retrieved successfully',
        data: lineage
      });
    } catch (error) {
      res.status(404).json({
        success: false,
        message: error.message
      });
    }
  }

  async listLineageRecords(req, res) {
    try {
      const { limit = 10, offset = 0 } = req.query;
      const result = await lineageTrackingService.getAllLineageRecords(
        parseInt(limit),
        parseInt(offset)
      );
      res.status(200).json({
        success: true,
        message: 'Lineage records retrieved successfully',
        data: result
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }

  async updateLineageRecord(req, res) {
    try {
      const { id } = req.params;
      const lineage = await lineageTrackingService.updateLineageRecord(id, req.body);
      res.status(200).json({
        success: true,
        message: 'Lineage record updated successfully',
        data: lineage
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  async deleteLineageRecord(req, res) {
    try {
      const { id } = req.params;
      const result = await lineageTrackingService.deleteLineageRecord(id);
      res.status(200).json({
        success: true,
        message: result.message
      });
    } catch (error) {
      res.status(404).json({
        success: false,
        message: error.message
      });
    }
  }

  async getLineageByJob(req, res) {
    try {
      const { jobId } = req.params;
      const { limit = 10, offset = 0 } = req.query;
      const result = await lineageTrackingService.getLineageByJob(
        jobId,
        parseInt(limit),
        parseInt(offset)
      );
      res.status(200).json({
        success: true,
        message: 'Lineage by job retrieved successfully',
        data: result
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }

  async createTransformationLineage(req, res) {
    try {
      const { jobId, sourceInfo, targetInfo, transformationInfo } = req.body;
      const lineage = await lineageTrackingService.createTransformationLineage(
        jobId, 
        sourceInfo, 
        targetInfo, 
        transformationInfo
      );
      res.status(201).json({
        success: true,
        message: 'Transformation lineage created successfully',
        data: lineage
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  async completeTransformationLineage(req, res) {
    try {
      const { lineageId } = req.params;
      const { recordCount, errorCount } = req.body;
      const lineage = await lineageTrackingService.completeTransformationLineage(
        lineageId, 
        recordCount, 
        errorCount
      );
      res.status(200).json({
        success: true,
        message: 'Transformation lineage completed successfully',
        data: lineage
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  async getLineageGraph(req, res) {
    try {
      const { jobId } = req.params;
      const graph = await lineageTrackingService.getLineageGraph(jobId);
      res.status(200).json({
        success: true,
        message: 'Lineage graph retrieved successfully',
        data: graph
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }

  async getLineagePath(req, res) {
    try {
      const { jobId } = req.params;
      const { sourceSystem, targetSystem } = req.query;
      const path = await lineageTrackingService.getLineagePath(jobId, sourceSystem, targetSystem);
      res.status(200).json({
        success: true,
        message: 'Lineage path retrieved successfully',
        data: path
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }

  async getImpactAnalysis(req, res) {
    try {
      const { jobId } = req.params;
      const { system, table } = req.query;
      const analysis = await lineageTrackingService.getImpactAnalysis(jobId, system, table);
      res.status(200).json({
        success: true,
        message: 'Impact analysis completed successfully',
        data: analysis
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }
}

module.exports = new DataLineageController();