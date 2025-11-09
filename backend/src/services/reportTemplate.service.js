const { ReportTemplate } = require('../models');

class ReportTemplateService {
  async createTemplate(templateData) {
    try {
      const template = await ReportTemplate.create(templateData);
      return template;
    } catch (error) {
      throw new Error(`Failed to create report template: ${error.message}`);
    }
  }

  async getTemplateById(id) {
    try {
      const template = await ReportTemplate.findByPk(id);
      if (!template) {
        throw new Error('Report template not found');
      }
      return template;
    } catch (error) {
      throw new Error(`Failed to get report template: ${error.message}`);
    }
  }

  async getAllTemplates(limit = 10, offset = 0) {
    try {
      const { rows, count } = await ReportTemplate.findAndCountAll({
        limit,
        offset,
        order: [['created_at', 'DESC']]
      });
      return { templates: rows, count, limit, offset };
    } catch (error) {
      throw new Error(`Failed to list report templates: ${error.message}`);
    }
  }

  async updateTemplate(id, updateData) {
    try {
      const template = await this.getTemplateById(id);
      const updatedTemplate = await template.update(updateData);
      return updatedTemplate;
    } catch (error) {
      throw new Error(`Failed to update report template: ${error.message}`);
    }
  }

  async deleteTemplate(id) {
    try {
      const template = await this.getTemplateById(id);
      await template.destroy();
      return { success: true, message: 'Report template deleted successfully' };
    } catch (error) {
      throw new Error(`Failed to delete report template: ${error.message}`);
    }
  }

  async getActiveTemplates() {
    try {
      const templates = await ReportTemplate.findAll({
        where: { isActive: true },
        order: [['created_at', 'DESC']]
      });
      return templates;
    } catch (error) {
      throw new Error(`Failed to get active report templates: ${error.message}`);
    }
  }
}

module.exports = new ReportTemplateService();