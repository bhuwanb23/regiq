const reportAnalyticsService = require('../services/reportAnalytics.service');

class ReportAnalyticsController {
  async trackView(req, res) {
    try {
      // For now, we'll use a test user ID
      // In a real implementation, this would come from authentication middleware
      const userId = 'test-user-id';
      const { reportId } = req.params;
      const metadata = {
        deviceType: req.headers['user-agent'],
        ipAddress: req.ip,
        userAgent: req.headers['user-agent']
      };
      
      const analytics = await reportAnalyticsService.trackView(reportId, userId, metadata);
      res.status(200).json({
        success: true,
        message: 'Report view tracked successfully',
        data: analytics
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  async trackDownload(req, res) {
    try {
      // For now, we'll use a test user ID
      // In a real implementation, this would come from authentication middleware
      const userId = 'test-user-id';
      const { reportId } = req.params;
      const metadata = {
        deviceType: req.headers['user-agent'],
        ipAddress: req.ip,
        userAgent: req.headers['user-agent']
      };
      
      const analytics = await reportAnalyticsService.trackDownload(reportId, userId, metadata);
      res.status(200).json({
        success: true,
        message: 'Report download tracked successfully',
        data: analytics
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  async getAnalytics(req, res) {
    try {
      const { id } = req.params;
      const analytics = await reportAnalyticsService.getAnalyticsById(id);
      res.status(200).json({
        success: true,
        message: 'Report analytics retrieved successfully',
        data: analytics
      });
    } catch (error) {
      res.status(404).json({
        success: false,
        message: error.message
      });
    }
  }

  async getAnalyticsByReport(req, res) {
    try {
      const { reportId } = req.params;
      const { limit = 10, offset = 0 } = req.query;
      const result = await reportAnalyticsService.getAnalyticsByReport(
        reportId,
        parseInt(limit),
        parseInt(offset)
      );
      res.status(200).json({
        success: true,
        message: 'Report analytics retrieved successfully',
        data: result
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }

  async getReportSummary(req, res) {
    try {
      const { reportId } = req.params;
      const summary = await reportAnalyticsService.getReportSummary(reportId);
      res.status(200).json({
        success: true,
        message: 'Report summary retrieved successfully',
        data: summary
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }

  async getTopReportsByViews(req, res) {
    try {
      const { limit = 10 } = req.query;
      const topReports = await reportAnalyticsService.getTopReportsByViews(parseInt(limit));
      res.status(200).json({
        success: true,
        message: 'Top reports by views retrieved successfully',
        data: topReports
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }

  async deleteAnalytics(req, res) {
    try {
      const { id } = req.params;
      const result = await reportAnalyticsService.deleteAnalytics(id);
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
}

module.exports = new ReportAnalyticsController();