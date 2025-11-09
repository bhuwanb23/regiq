const { ReportAnalytics, ReportGeneration } = require('../models');

class ReportAnalyticsService {
  async trackView(reportId, userId, metadata = {}) {
    try {
      // Check if report exists
      const report = await ReportGeneration.findByPk(reportId);
      if (!report) {
        throw new Error('Report not found');
      }

      // Check if analytics record already exists for this report and user
      let analytics = await ReportAnalytics.findOne({
        where: { reportId, userId }
      });

      if (analytics) {
        // Update existing record
        analytics.viewCount += 1;
        analytics.lastViewed = new Date();
        
        // Update device info if provided
        if (metadata.deviceType) analytics.deviceType = metadata.deviceType;
        if (metadata.ipAddress) analytics.ipAddress = metadata.ipAddress;
        if (metadata.userAgent) analytics.userAgent = metadata.userAgent;
        
        await analytics.save();
      } else {
        // Create new record
        analytics = await ReportAnalytics.create({
          reportId,
          userId,
          viewCount: 1,
          lastViewed: new Date(),
          deviceType: metadata.deviceType,
          ipAddress: metadata.ipAddress,
          userAgent: metadata.userAgent
        });
      }

      return analytics;
    } catch (error) {
      throw new Error(`Failed to track report view: ${error.message}`);
    }
  }

  async trackDownload(reportId, userId, metadata = {}) {
    try {
      // Check if report exists
      const report = await ReportGeneration.findByPk(reportId);
      if (!report) {
        throw new Error('Report not found');
      }

      // Check if analytics record already exists for this report and user
      let analytics = await ReportAnalytics.findOne({
        where: { reportId, userId }
      });

      if (analytics) {
        // Update existing record
        analytics.downloadCount += 1;
        analytics.lastViewed = new Date();
        
        // Update device info if provided
        if (metadata.deviceType) analytics.deviceType = metadata.deviceType;
        if (metadata.ipAddress) analytics.ipAddress = metadata.ipAddress;
        if (metadata.userAgent) analytics.userAgent = metadata.userAgent;
        
        await analytics.save();
      } else {
        // Create new record
        analytics = await ReportAnalytics.create({
          reportId,
          userId,
          downloadCount: 1,
          lastViewed: new Date(),
          deviceType: metadata.deviceType,
          ipAddress: metadata.ipAddress,
          userAgent: metadata.userAgent
        });
      }

      return analytics;
    } catch (error) {
      throw new Error(`Failed to track report download: ${error.message}`);
    }
  }

  async getAnalyticsById(id) {
    try {
      const analytics = await ReportAnalytics.findByPk(id);
      if (!analytics) {
        throw new Error('Report analytics not found');
      }
      return analytics;
    } catch (error) {
      throw new Error(`Failed to get report analytics: ${error.message}`);
    }
  }

  async getAnalyticsByReport(reportId, limit = 10, offset = 0) {
    try {
      const { rows, count } = await ReportAnalytics.findAndCountAll({
        where: { reportId },
        limit,
        offset,
        order: [['last_viewed', 'DESC']]
      });
      return { analytics: rows, count, limit, offset };
    } catch (error) {
      throw new Error(`Failed to get report analytics: ${error.message}`);
    }
  }

  async getReportSummary(reportId) {
    try {
      // Get all analytics for this report
      const analyticsRecords = await ReportAnalytics.findAll({
        where: { reportId }
      });

      // Calculate summary statistics
      let totalViews = 0;
      let totalDownloads = 0;
      const uniqueViewers = new Set();
      
      for (const record of analyticsRecords) {
        totalViews += record.viewCount;
        totalDownloads += record.downloadCount;
        if (record.userId) {
          uniqueViewers.add(record.userId);
        }
      }

      return {
        reportId,
        totalViews,
        totalDownloads,
        uniqueViewers: uniqueViewers.size,
        analyticsRecords: analyticsRecords.length
      };
    } catch (error) {
      throw new Error(`Failed to get report summary: ${error.message}`);
    }
  }

  async getTopReportsByViews(limit = 10) {
    try {
      // This would require a more complex query in a real implementation
      // For now, we'll return a simplified version
      const topReports = await ReportAnalytics.findAll({
        attributes: ['reportId'],
        group: ['reportId'],
        order: [['viewCount', 'DESC']],
        limit
      });

      return topReports;
    } catch (error) {
      throw new Error(`Failed to get top reports by views: ${error.message}`);
    }
  }

  async deleteAnalytics(id) {
    try {
      const analytics = await this.getAnalyticsById(id);
      await analytics.destroy();
      return { success: true, message: 'Report analytics deleted successfully' };
    } catch (error) {
      throw new Error(`Failed to delete report analytics: ${error.message}`);
    }
  }
}

module.exports = new ReportAnalyticsService();