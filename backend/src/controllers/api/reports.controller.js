const reportService = require('../../services/api/reports.service');

class ReportController {
  /**
   * Report CRUD Endpoints
   */
  async createReport(req, res) {
    try {
      const report = await reportService.createReport(req.body);
      res.status(201).json({
        success: true,
        message: 'Report created successfully',
        data: report
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  async listReports(req, res) {
    try {
      const reports = await reportService.listReports(req.query);
      res.status(200).json({
        success: true,
        data: reports
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }

  async getReport(req, res) {
    try {
      const { id } = req.params;
      const report = await reportService.getReport(id);
      res.status(200).json({
        success: true,
        data: report
      });
    } catch (error) {
      res.status(404).json({
        success: false,
        message: error.message
      });
    }
  }

  async updateReport(req, res) {
    try {
      const { id } = req.params;
      const report = await reportService.updateReport(id, req.body);
      res.status(200).json({
        success: true,
        message: 'Report updated successfully',
        data: report
      });
    } catch (error) {
      res.status(404).json({
        success: false,
        message: error.message
      });
    }
  }

  async deleteReport(req, res) {
    try {
      const { id } = req.params;
      const result = await reportService.deleteReport(id);
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

  /**
   * Report Generation Endpoint
   */
  async generateReport(req, res) {
    try {
      const report = await reportService.generateReport(req.body);
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

  /**
   * Report Export Endpoints
   */
  async exportReportPdf(req, res) {
    try {
      const { id } = req.params;
      const pdfBuffer = await reportService.exportReportPdf(id);
      
      res.setHeader('Content-Type', 'application/pdf');
      res.setHeader('Content-Disposition', `attachment; filename="report-${id}.pdf"`);
      res.status(200).send(pdfBuffer);
    } catch (error) {
      res.status(404).json({
        success: false,
        message: error.message
      });
    }
  }

  async exportReportCsv(req, res) {
    try {
      const { id } = req.params;
      const csvData = await reportService.exportReportCsv(id);
      
      res.setHeader('Content-Type', 'text/csv');
      res.setHeader('Content-Disposition', `attachment; filename="report-${id}.csv"`);
      res.status(200).send(csvData);
    } catch (error) {
      res.status(404).json({
        success: false,
        message: error.message
      });
    }
  }

  async exportReportJson(req, res) {
    try {
      const { id } = req.params;
      const jsonData = await reportService.exportReportJson(id);
      
      res.setHeader('Content-Type', 'application/json');
      res.setHeader('Content-Disposition', `attachment; filename="report-${id}.json"`);
      res.status(200).send(JSON.stringify(jsonData, null, 2));
    } catch (error) {
      res.status(404).json({
        success: false,
        message: error.message
      });
    }
  }

  /**
   * Report Template Management Endpoints
   */
  async createTemplate(req, res) {
    try {
      const template = await reportService.createTemplate(req.body);
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

  async listTemplates(req, res) {
    try {
      const templates = await reportService.listTemplates(req.query);
      res.status(200).json({
        success: true,
        data: templates
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }

  async getTemplate(req, res) {
    try {
      const { id } = req.params;
      const template = await reportService.getTemplate(id);
      res.status(200).json({
        success: true,
        data: template
      });
    } catch (error) {
      res.status(404).json({
        success: false,
        message: error.message
      });
    }
  }

  async updateTemplate(req, res) {
    try {
      const { id } = req.params;
      const template = await reportService.updateTemplate(id, req.body);
      res.status(200).json({
        success: true,
        message: 'Report template updated successfully',
        data: template
      });
    } catch (error) {
      res.status(404).json({
        success: false,
        message: error.message
      });
    }
  }

  async deleteTemplate(req, res) {
    try {
      const { id } = req.params;
      const result = await reportService.deleteTemplate(id);
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

  /**
   * Report Scheduling Endpoints
   */
  async createSchedule(req, res) {
    try {
      const schedule = await reportService.createSchedule(req.body);
      res.status(201).json({
        success: true,
        message: 'Report schedule created successfully',
        data: schedule
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  async listSchedules(req, res) {
    try {
      const schedules = await reportService.listSchedules(req.query);
      res.status(200).json({
        success: true,
        data: schedules
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }

  async getSchedule(req, res) {
    try {
      const { id } = req.params;
      const schedule = await reportService.getSchedule(id);
      res.status(200).json({
        success: true,
        data: schedule
      });
    } catch (error) {
      res.status(404).json({
        success: false,
        message: error.message
      });
    }
  }

  async updateSchedule(req, res) {
    try {
      const { id } = req.params;
      const schedule = await reportService.updateSchedule(id, req.body);
      res.status(200).json({
        success: true,
        message: 'Report schedule updated successfully',
        data: schedule
      });
    } catch (error) {
      res.status(404).json({
        success: false,
        message: error.message
      });
    }
  }

  async deleteSchedule(req, res) {
    try {
      const { id } = req.params;
      const result = await reportService.deleteSchedule(id);
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

  async executeSchedule(req, res) {
    try {
      const { id } = req.params;
      const result = await reportService.executeSchedule(id);
      res.status(200).json({
        success: true,
        message: 'Report schedule executed successfully',
        data: result
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }

  /**
   * Get compliance glossary
   */
  async getGlossary(req, res) {
    try {
      // Call Python service to get glossary
      const aiMlClient = require('../../services/ai-ml.service');
      const glossary = await aiMlClient.makeRequest('GET', '/api/v1/report-generator/glossary');
      
      res.status(200).json({
        success: true,
        message: 'Compliance glossary retrieved successfully',
        data: glossary
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }
}

module.exports = new ReportController();