const { 
  Report,
  ReportTemplate,
  ReportSchedule
} = require('../../models');
const puppeteer = require('puppeteer');
const Handlebars = require('handlebars');

// Register Handlebars helpers
Handlebars.registerHelper('json', function(context) {
  return JSON.stringify(context, null, 2);
});

Handlebars.registerHelper('ifEquals', function(arg1, arg2, options) {
  return (arg1 == arg2) ? options.fn(this) : options.inverse(this);
});

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
      // Use the content directly from generationData or create a default structure
      const reportContent = generationData.content || {
        title: generationData.title || 'Generated Report',
        generatedAt: new Date(),
        data: {},
        summary: {},
        metadata: {
          generatedBy: 'system',
          version: '1.0'
        }
      };
      
      const report = await Report.create({
        reportType: generationData.reportType || 'generic',
        title: generationData.title || reportContent.title || 'Generated Report',
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
      
      // Debug: Log report data
      console.log('DEBUG: Report data:', JSON.stringify(report, null, 2));
      
      // Get the template for this report type
      const template = await ReportTemplate.findOne({
        where: { 
          templateType: report.reportType,
          isActive: true,
          contentType: 'html'
        },
        order: [['createdAt', 'DESC']]
      });
      
      // Debug: Log template info
      if (template) {
        console.log('DEBUG: Using template:', template.name, 'ID:', template.id);
      } else {
        console.log('DEBUG: No template found, using fallback');
      }
      
      let htmlContent;
      
      if (template) {
        const templateData = {
          title: report.title,
          reportType: report.reportType,
          generatedAt: report.createdAt,
          content: report.content,
          reportId: report.id
        };
        
        // Debug: Log template data
        console.log('DEBUG: Template data:', JSON.stringify(templateData, null, 2));
        
        // Render the HTML template with report data
        htmlContent = this.renderHtmlTemplate(template.content, templateData);
      } else {
        // Fallback to simple HTML if no template found
        htmlContent = `
          <!DOCTYPE html>
          <html>
          <head>
            <meta charset="UTF-8">
            <title>${report.title}</title>
            <style>
              body { font-family: Arial, sans-serif; margin: 40px; }
              h1 { color: #333; }
              .meta { color: #666; margin-bottom: 20px; }
              pre { background: #f5f5f5; padding: 15px; overflow-x: auto; }
            </style>
          </head>
          <body>
            <h1>${report.title}</h1>
            <div class="meta">
              <p><strong>Report Type:</strong> ${report.reportType}</p>
              <p><strong>Generated At:</strong> ${report.createdAt}</p>
              <p><strong>Report ID:</strong> ${report.id}</p>
            </div>
            <pre>${JSON.stringify(report.content, null, 2)}</pre>
          </body>
          </html>
        `;
      }
      
      // Debug: Log generated HTML (first 1000 chars)
      console.log('DEBUG: Generated HTML (first 1000 chars):', htmlContent.substring(0, 1000));
      
      // Convert HTML to PDF using Puppeteer
      const pdfBuffer = await this.htmlToPdf(htmlContent);
      return pdfBuffer;
    } catch (error) {
      console.error('ERROR in exportReportPdf:', error);
      throw new Error(`Failed to export report as PDF: ${error.message}`);
    }
  }
  
  /**
   * Render HTML template with Handlebars
   */
  renderHtmlTemplate(templateContent, data) {
    try {
      // Ensure data is properly formatted
      const formattedData = {
        ...data,
        // Format dates properly
        generatedAt: data.generatedAt instanceof Date ? data.generatedAt.toString() : data.generatedAt,
        // Ensure content is properly structured
        content: data.content || {}
      };
      
      const template = Handlebars.compile(templateContent);
      return template(formattedData);
    } catch (error) {
      throw new Error(`Failed to render HTML template: ${error.message}`);
    }
  }
  
  /**
   * Convert HTML to PDF using Puppeteer
   */
  async htmlToPdf(htmlContent) {
    try {
      const browser = await puppeteer.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
      });
      
      const page = await browser.newPage();
      await page.setContent(htmlContent, { waitUntil: 'networkidle0' });
      
      const pdf = await page.pdf({
        format: 'A4',
        printBackground: true,
        margin: {
          top: '20px',
          bottom: '20px',
          left: '20px',
          right: '20px'
        }
      });
      
      await browser.close();
      return pdf;
    } catch (error) {
      throw new Error(`Failed to convert HTML to PDF: ${error.message}`);
    }
  }

  async exportReportCsv(reportId) {
    try {
      const report = await this.getReport(reportId);
      
      // Create CSV header
      let csvContent = 'Title,Report Type,Generated At,Status,Total Regulations,Compliant,Non-Compliant,Pending\n';
      
      // Add summary row
      const summary = report.content?.summary || {};
      csvContent += `"${report.title}","${report.reportType}","${report.createdAt}","${report.status}","${summary.totalRegulations || 0}","${summary.compliant || 0}","${summary.nonCompliant || 0}","${summary.pending || 0}"\n`;
      
      // Add detailed data rows if available
      if (report.content && report.content.data && Array.isArray(report.content.data)) {
        csvContent += '\nJurisdiction,Regulation,Status,Action Required\n';
        report.content.data.forEach(item => {
          csvContent += `"${item.jurisdiction || ''}","${item.regulation || ''}","${item.status || ''}","${item.action || ''}"\n`;
        });
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