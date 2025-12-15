const { 
  Report,
  ReportTemplate,
  ReportSchedule
} = require('../../models');

class ReportService {
  /**
   * Report CRUD Methods
   */
  async createReport(reportData) {
    try {
      const report = await Report.create({
        ...reportData,
        status: 'completed',
        createdAt: new Date(),
        updatedAt: new Date()
      });
      return report;
    } catch (error) {
      throw new Error(`Failed to create report: ${error.message}`);
    }
  }

  async listReports(filters = {}) {
    try {
      const whereClause = {};
      
      if (filters.reportType) {
        whereClause.reportType = filters.reportType;
      }
      
      if (filters.status) {
        whereClause.status = filters.status;
      }
      
      const limit = filters.limit ? parseInt(filters.limit) : 50;
      const offset = filters.offset ? parseInt(filters.offset) : 0;
      
      const { rows: reports, count } = await Report.findAndCountAll({
        where: whereClause,
        order: [['createdAt', 'DESC']],
        limit: limit,
        offset: offset
      });
      
      return {
        reports: reports,
        count: count,
        limit: limit,
        offset: offset
      };
    } catch (error) {
      throw new Error(`Failed to list reports: ${error.message}`);
    }
  }

  async getReport(reportId) {
    try {
      const report = await Report.findByPk(reportId);
      if (!report) {
        throw new Error('Report not found');
      }
      return report;
    } catch (error) {
      throw new Error(`Failed to get report: ${error.message}`);
    }
  }

  async updateReport(reportId, updateData) {
    try {
      const report = await Report.findByPk(reportId);
      if (!report) {
        throw new Error('Report not found');
      }
      
      await report.update(updateData);
      return report;
    } catch (error) {
      throw new Error(`Failed to update report: ${error.message}`);
    }
  }

  async deleteReport(reportId) {
    try {
      const report = await Report.findByPk(reportId);
      if (!report) {
        throw new Error('Report not found');
      }
      
      await report.destroy();
      return { success: true, message: 'Report deleted successfully' };
    } catch (error) {
      throw new Error(`Failed to delete report: ${error.message}`);
    }
  }

  /**
   * Report Generation Method
   */
  async generateReport(generationData) {
    try {
      // Simulate report generation
      const reportContent = {
        title: generationData.title || 'Generated Report',
        generatedAt: new Date(),
        data: generationData.data || {},
        summary: generationData.summary || {},
        metadata: {
          generatedBy: 'system',
          version: '1.0'
        }
      };
      
      const report = await Report.create({
        reportType: generationData.reportType || 'generic',
        title: reportContent.title,
        content: reportContent,
        status: 'completed',
        format: generationData.format || 'pdf',
        createdAt: new Date(),
        updatedAt: new Date()
      });
      
      return report;
    } catch (error) {
      throw new Error(`Failed to generate report: ${error.message}`);
    }
  }

  /**
   * Report Export Methods
   */
  async exportReportPdf(reportId) {
    try {
      const report = await this.getReport(reportId);
      
      // Simulate PDF generation
      const pdfContent = `
        Report Title: ${report.title}
        Report Type: ${report.reportType}
        Generated At: ${report.createdAt}
        
        Content:
        ${JSON.stringify(report.content, null, 2)}
      `;
      
      // In a real implementation, we would use a library like pdfkit or puppeteer
      // For now, we'll return a Buffer with the text content
      return Buffer.from(pdfContent, 'utf-8');
    } catch (error) {
      throw new Error(`Failed to export report as PDF: ${error.message}`);
    }
  }

  async exportReportCsv(reportId) {
    try {
      const report = await this.getReport(reportId);
      
      // Simulate CSV generation
      let csvContent = 'Title,Report Type,Generated At,Status\n';
      csvContent += `"${report.title}","${report.reportType}","${report.createdAt}","${report.status}"\n`;
      
      // Add data rows if available
      if (report.content && report.content.data) {
        csvContent += '\nData:\n';
        const data = report.content.data;
        if (Array.isArray(data)) {
          // If data is an array, create CSV rows
          data.forEach((item, index) => {
            csvContent += `${index},${JSON.stringify(item)}\n`;
          });
        } else {
          // If data is an object, flatten it
          Object.entries(data).forEach(([key, value]) => {
            csvContent += `"${key}","${value}"\n`;
          });
        }
      }
      
      return csvContent;
    } catch (error) {
      throw new Error(`Failed to export report as CSV: ${error.message}`);
    }
  }

  async exportReportJson(reportId) {
    try {
      const report = await this.getReport(reportId);
      return report;
    } catch (error) {
      throw new Error(`Failed to export report as JSON: ${error.message}`);
    }
  }

  /**
   * Report Template Management Methods
   */
  async createTemplate(templateData) {
    try {
      const template = await ReportTemplate.create({
        ...templateData,
        isActive: true,
        createdAt: new Date(),
        updatedAt: new Date()
      });
      return template;
    } catch (error) {
      throw new Error(`Failed to create template: ${error.message}`);
    }
  }

  async listTemplates(filters = {}) {
    try {
      const whereClause = {
        isActive: true
      };
      
      if (filters.templateType) {
        whereClause.templateType = filters.templateType;
      }
      
      const limit = filters.limit ? parseInt(filters.limit) : 50;
      const offset = filters.offset ? parseInt(filters.offset) : 0;
      
      const { rows: templates, count } = await ReportTemplate.findAndCountAll({
        where: whereClause,
        order: [['createdAt', 'DESC']],
        limit: limit,
        offset: offset
      });
      
      return {
        templates: templates,
        count: count,
        limit: limit,
        offset: offset
      };
    } catch (error) {
      throw new Error(`Failed to list templates: ${error.message}`);
    }
  }

  async getTemplate(templateId) {
    try {
      const template = await ReportTemplate.findByPk(templateId);
      if (!template) {
        throw new Error('Report template not found');
      }
      return template;
    } catch (error) {
      throw new Error(`Failed to get template: ${error.message}`);
    }
  }

  async updateTemplate(templateId, updateData) {
    try {
      const template = await ReportTemplate.findByPk(templateId);
      if (!template) {
        throw new Error('Report template not found');
      }
      
      await template.update(updateData);
      return template;
    } catch (error) {
      throw new Error(`Failed to update template: ${error.message}`);
    }
  }

  async deleteTemplate(templateId) {
    try {
      const template = await ReportTemplate.findByPk(templateId);
      if (!template) {
        throw new Error('Report template not found');
      }
      
      // Soft delete by setting isActive to false
      await template.update({ isActive: false });
      return { success: true, message: 'Report template deactivated successfully' };
    } catch (error) {
      throw new Error(`Failed to delete template: ${error.message}`);
    }
  }

  /**
   * Report Scheduling Methods
   */
  async createSchedule(scheduleData) {
    try {
      const schedule = await ReportSchedule.create({
        ...scheduleData,
        isActive: true,
        nextRunTime: scheduleData.nextRunTime || new Date(Date.now() + 24 * 60 * 60 * 1000), // Default to 24 hours from now
        createdAt: new Date(),
        updatedAt: new Date()
      });
      return schedule;
    } catch (error) {
      throw new Error(`Failed to create schedule: ${error.message}`);
    }
  }

  async listSchedules(filters = {}) {
    try {
      const whereClause = {
        isActive: true
      };
      
      if (filters.reportType) {
        whereClause.reportType = filters.reportType;
      }
      
      const limit = filters.limit ? parseInt(filters.limit) : 50;
      const offset = filters.offset ? parseInt(filters.offset) : 0;
      
      const { rows: schedules, count } = await ReportSchedule.findAndCountAll({
        where: whereClause,
        order: [['nextRunTime', 'ASC']],
        limit: limit,
        offset: offset
      });
      
      return {
        schedules: schedules,
        count: count,
        limit: limit,
        offset: offset
      };
    } catch (error) {
      throw new Error(`Failed to list schedules: ${error.message}`);
    }
  }

  async getSchedule(scheduleId) {
    try {
      const schedule = await ReportSchedule.findByPk(scheduleId);
      if (!schedule) {
        throw new Error('Report schedule not found');
      }
      return schedule;
    } catch (error) {
      throw new Error(`Failed to get schedule: ${error.message}`);
    }
  }

  async updateSchedule(scheduleId, updateData) {
    try {
      const schedule = await ReportSchedule.findByPk(scheduleId);
      if (!schedule) {
        throw new Error('Report schedule not found');
      }
      
      await schedule.update(updateData);
      return schedule;
    } catch (error) {
      throw new Error(`Failed to update schedule: ${error.message}`);
    }
  }

  async deleteSchedule(scheduleId) {
    try {
      const schedule = await ReportSchedule.findByPk(scheduleId);
      if (!schedule) {
        throw new Error('Report schedule not found');
      }
      
      // Soft delete by setting isActive to false
      await schedule.update({ isActive: false });
      return { success: true, message: 'Report schedule deactivated successfully' };
    } catch (error) {
      throw new Error(`Failed to delete schedule: ${error.message}`);
    }
  }

  async executeSchedule(scheduleId) {
    try {
      const schedule = await this.getSchedule(scheduleId);
      
      // Simulate report generation based on schedule
      const reportData = {
        title: `${schedule.scheduleName || 'Scheduled'} Report`,
        reportType: schedule.reportType || 'scheduled',
        data: schedule.parameters || {},
        summary: {
          scheduledAt: new Date(),
          scheduleId: scheduleId
        }
      };
      
      const report = await this.generateReport(reportData);
      
      // Update next run time based on frequency
      const nextRunTime = new Date(Date.now() + this._calculateNextRunOffset(schedule.frequency));
      await this.updateSchedule(scheduleId, { nextRunTime });
      
      return {
        reportId: report.id,
        message: 'Scheduled report generated successfully',
        nextRunTime: nextRunTime
      };
    } catch (error) {
      throw new Error(`Failed to execute schedule: ${error.message}`);
    }
  }

  /**
   * Helper method to calculate next run offset based on frequency
   */
  _calculateNextRunOffset(frequency) {
    switch (frequency) {
      case 'daily':
        return 24 * 60 * 60 * 1000; // 24 hours
      case 'weekly':
        return 7 * 24 * 60 * 60 * 1000; // 7 days
      case 'monthly':
        return 30 * 24 * 60 * 60 * 1000; // 30 days
      default:
        return 24 * 60 * 60 * 1000; // Default to daily
    }
  }
}

module.exports = new ReportService();