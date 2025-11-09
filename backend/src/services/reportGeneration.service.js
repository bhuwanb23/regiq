const { ReportGeneration, ReportTemplate } = require('../models');

class ReportGenerationService {
  async generateReport(reportData, userId) {
    try {
      // Validate template if provided
      if (reportData.templateId) {
        const template = await ReportTemplate.findByPk(reportData.templateId);
        if (!template) {
          throw new Error('Report template not found');
        }
      }

      const report = await ReportGeneration.create({
        ...reportData,
        generatedBy: userId,
        status: 'pending'
      });

      // In a real implementation, we would generate the actual report content here
      // For now, we'll just update the status to completed
      await report.update({ status: 'completed' });

      return report;
    } catch (error) {
      throw new Error(`Failed to generate report: ${error.message}`);
    }
  }

  async getReportById(id) {
    try {
      const report = await ReportGeneration.findByPk(id);
      if (!report) {
        throw new Error('Report not found');
      }
      return report;
    } catch (error) {
      throw new Error(`Failed to get report: ${error.message}`);
    }
  }

  async getAllReports(limit = 10, offset = 0) {
    try {
      const { rows, count } = await ReportGeneration.findAndCountAll({
        limit,
        offset,
        order: [['created_at', 'DESC']]
      });
      return { reports: rows, count, limit, offset };
    } catch (error) {
      throw new Error(`Failed to list reports: ${error.message}`);
    }
  }

  async updateReport(id, updateData) {
    try {
      const report = await this.getReportById(id);
      const updatedReport = await report.update(updateData);
      return updatedReport;
    } catch (error) {
      throw new Error(`Failed to update report: ${error.message}`);
    }
  }

  async deleteReport(id) {
    try {
      const report = await this.getReportById(id);
      await report.destroy();
      return { success: true, message: 'Report deleted successfully' };
    } catch (error) {
      throw new Error(`Failed to delete report: ${error.message}`);
    }
  }

  async getReportsByUser(userId, limit = 10, offset = 0) {
    try {
      const { rows, count } = await ReportGeneration.findAndCountAll({
        where: { generatedBy: userId },
        limit,
        offset,
        order: [['created_at', 'DESC']]
      });
      return { reports: rows, count, limit, offset };
    } catch (error) {
      throw new Error(`Failed to get user reports: ${error.message}`);
    }
  }

  async getReportsByType(reportType, limit = 10, offset = 0) {
    try {
      const { rows, count } = await ReportGeneration.findAndCountAll({
        where: { reportType },
        limit,
        offset,
        order: [['created_at', 'DESC']]
      });
      return { reports: rows, count, limit, offset };
    } catch (error) {
      throw new Error(`Failed to get reports by type: ${error.message}`);
    }
  }
}

module.exports = new ReportGenerationService();