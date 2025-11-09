const dataValidationService = require('../services/dataValidation.service');

class DataValidationController {
  async createValidationRule(req, res) {
    try {
      const rule = await dataValidationService.createValidationRule(req.body);
      res.status(201).json({
        success: true,
        message: 'Validation rule created successfully',
        data: rule
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  async getValidationRule(req, res) {
    try {
      const { id } = req.params;
      const rule = await dataValidationService.getValidationRuleById(id);
      res.status(200).json({
        success: true,
        message: 'Validation rule retrieved successfully',
        data: rule
      });
    } catch (error) {
      res.status(404).json({
        success: false,
        message: error.message
      });
    }
  }

  async listValidationRules(req, res) {
    try {
      const { limit = 10, offset = 0 } = req.query;
      const result = await dataValidationService.getAllValidationRules(
        parseInt(limit),
        parseInt(offset)
      );
      res.status(200).json({
        success: true,
        message: 'Validation rules retrieved successfully',
        data: result
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }

  async updateValidationRule(req, res) {
    try {
      const { id } = req.params;
      const rule = await dataValidationService.updateValidationRule(id, req.body);
      res.status(200).json({
        success: true,
        message: 'Validation rule updated successfully',
        data: rule
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  async deleteValidationRule(req, res) {
    try {
      const { id } = req.params;
      const result = await dataValidationService.deleteValidationRule(id);
      res.status(200).json({
        success: true,
        message: 'Validation rule deleted successfully',
        data: result
      });
    } catch (error) {
      res.status(404).json({
        success: false,
        message: error.message
      });
    }
  }

  async getActiveValidationRules(req, res) {
    try {
      const rules = await dataValidationService.getActiveValidationRules();
      res.status(200).json({
        success: true,
        message: 'Active validation rules retrieved successfully',
        data: rules
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }
}

module.exports = new DataValidationController();