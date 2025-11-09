const reportGenerationService = require('../services/reportGeneration.service');
const formatConversionService = require('../services/formatConversion.service');

class ReportGenerationController {
  async generateReport(req, res) {
    try {
      // For now, we'll use a test user ID
      // In a real implementation, this would come from authentication middleware
      const userId = 'test-user-id';
      const report = await reportGenerationService.generateReport(req.body, userId);
      res.status(201).json({
        success: true,
        message: 'Report generated successfully',
        data: report
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  async getReport(req, res) {
    try {
      const { id } = req.params;
      const report = await reportGenerationService.getReportById(id);
      res.status(200).json({
        success: true,
        message: 'Report retrieved successfully',
        data: report
      });
    } catch (error) {
      res.status(404).json({
        success: false,
        message: error.message
      });
    }
  }

  async listReports(req, res) {
    try {
      const { limit = 10, offset = 0 } = req.query;
      const result = await reportGenerationService.getAllReports(
        parseInt(limit),
        parseInt(offset)
      );
      res.status(200).json({
        success: true,
        message: 'Reports retrieved successfully',
        data: result
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }

  async updateReport(req, res) {
    try {
      const { id } = req.params;
      const report = await reportGenerationService.updateReport(id, req.body);
      res.status(200).json({
        success: true,
        message: 'Report updated successfully',
        data: report
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  async deleteReport(req, res) {
    try {
      const { id } = req.params;
      const result = await reportGenerationService.deleteReport(id);
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

  async getUserReports(req, res) {
    try {
      // For now, we'll use a test user ID
      // In a real implementation, this would come from authentication middleware
      const userId = 'test-user-id';
      const { limit = 10, offset = 0 } = req.query;
      const result = await reportGenerationService.getReportsByUser(
        userId,
        parseInt(limit),
        parseInt(offset)
      );
      res.status(200).json({
        success: true,
        message: 'User reports retrieved successfully',
        data: result
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }

  async getReportsByType(req, res) {
    try {
      const { reportType } = req.params;
      const { limit = 10, offset = 0 } = req.query;
      const result = await reportGenerationService.getReportsByType(
        reportType,
        parseInt(limit),
        parseInt(offset)
      );
      res.status(200).json({
        success: true,
        message: 'Reports by type retrieved successfully',
        data: result
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }

  async convertReport(req, res) {
    try {
      const { id } = req.params;
      const { format } = req.query;
      
      if (!format) {
        return res.status(400).json({
          success: false,
          message: 'Format parameter is required'
        });
      }

      const report = await reportGenerationService.getReportById(id);
      const converted = await formatConversionService.convert(report.content, format);
      
      res.status(200).json({
        success: true,
        message: `Report converted to ${format} successfully`,
        data: {
          ...converted,
          originalReportId: id
        }
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }
}

module.exports = new ReportGenerationController();