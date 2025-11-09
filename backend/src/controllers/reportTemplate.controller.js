const reportTemplateService = require('../services/reportTemplate.service');

class ReportTemplateController {
  async createTemplate(req, res) {
    try {
      const template = await reportTemplateService.createTemplate(req.body);
      res.status(201).json({
        success: true,
        message: 'Report template created successfully',
        data: template
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  async getTemplate(req, res) {
    try {
      const { id } = req.params;
      const template = await reportTemplateService.getTemplateById(id);
      res.status(200).json({
        success: true,
        message: 'Report template retrieved successfully',
        data: template
      });
    } catch (error) {
      res.status(404).json({
        success: false,
        message: error.message
      });
    }
  }

  async listTemplates(req, res) {
    try {
      const { limit = 10, offset = 0 } = req.query;
      const result = await reportTemplateService.getAllTemplates(
        parseInt(limit),
        parseInt(offset)
      );
      res.status(200).json({
        success: true,
        message: 'Report templates retrieved successfully',
        data: result
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }

  async updateTemplate(req, res) {
    try {
      const { id } = req.params;
      const template = await reportTemplateService.updateTemplate(id, req.body);
      res.status(200).json({
        success: true,
        message: 'Report template updated successfully',
        data: template
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  async deleteTemplate(req, res) {
    try {
      const { id } = req.params;
      const result = await reportTemplateService.deleteTemplate(id);
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

  async getActiveTemplates(req, res) {
    try {
      const templates = await reportTemplateService.getActiveTemplates();
      res.status(200).json({
        success: true,
        message: 'Active report templates retrieved successfully',
        data: templates
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }
}

module.exports = new ReportTemplateController();