const reportDistributionService = require('../services/reportDistribution.service');

class ReportDistributionController {
  async createDistribution(req, res) {
    try {
      const distribution = await reportDistributionService.createDistribution(req.body);
      res.status(201).json({
        success: true,
        message: 'Report distribution created successfully',
        data: distribution
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  async getDistribution(req, res) {
    try {
      const { id } = req.params;
      const distribution = await reportDistributionService.getDistributionById(id);
      res.status(200).json({
        success: true,
        message: 'Report distribution retrieved successfully',
        data: distribution
      });
    } catch (error) {
      res.status(404).json({
        success: false,
        message: error.message
      });
    }
  }

  async listDistributions(req, res) {
    try {
      const { limit = 10, offset = 0 } = req.query;
      const result = await reportDistributionService.getAllDistributions(
        parseInt(limit),
        parseInt(offset)
      );
      res.status(200).json({
        success: true,
        message: 'Report distributions retrieved successfully',
        data: result
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }

  async updateDistribution(req, res) {
    try {
      const { id } = req.params;
      const distribution = await reportDistributionService.updateDistribution(id, req.body);
      res.status(200).json({
        success: true,
        message: 'Report distribution updated successfully',
        data: distribution
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  async deleteDistribution(req, res) {
    try {
      const { id } = req.params;
      const result = await reportDistributionService.deleteDistribution(id);
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

  async getDistributionsByReport(req, res) {
    try {
      const { reportId } = req.params;
      const { limit = 10, offset = 0 } = req.query;
      const result = await reportDistributionService.getDistributionsByReport(
        reportId,
        parseInt(limit),
        parseInt(offset)
      );
      res.status(200).json({
        success: true,
        message: 'Report distributions retrieved successfully',
        data: result
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }

  async getDistributionsByStatus(req, res) {
    try {
      const { status } = req.params;
      const { limit = 10, offset = 0 } = req.query;
      const result = await reportDistributionService.getDistributionsByStatus(
        status,
        parseInt(limit),
        parseInt(offset)
      );
      res.status(200).json({
        success: true,
        message: 'Report distributions retrieved successfully',
        data: result
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }

  async sendDistribution(req, res) {
    try {
      const { id } = req.params;
      const distribution = await reportDistributionService.sendDistribution(id);
      res.status(200).json({
        success: true,
        message: 'Report distribution sent successfully',
        data: distribution
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  async markAsDelivered(req, res) {
    try {
      const { id } = req.params;
      const distribution = await reportDistributionService.markAsDelivered(id);
      res.status(200).json({
        success: true,
        message: 'Report distribution marked as delivered successfully',
        data: distribution
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }
}

module.exports = new ReportDistributionController();