const { ReportDistribution, ReportGeneration } = require('../models');

class ReportDistributionService {
  async createDistribution(distributionData) {
    try {
      // Validate report exists
      const report = await ReportGeneration.findByPk(distributionData.reportId);
      if (!report) {
        throw new Error('Report not found');
      }

      const distribution = await ReportDistribution.create(distributionData);
      return distribution;
    } catch (error) {
      throw new Error(`Failed to create report distribution: ${error.message}`);
    }
  }

  async getDistributionById(id) {
    try {
      const distribution = await ReportDistribution.findByPk(id);
      if (!distribution) {
        throw new Error('Report distribution not found');
      }
      return distribution;
    } catch (error) {
      throw new Error(`Failed to get report distribution: ${error.message}`);
    }
  }

  async getAllDistributions(limit = 10, offset = 0) {
    try {
      const { rows, count } = await ReportDistribution.findAndCountAll({
        limit,
        offset,
        order: [['created_at', 'DESC']]
      });
      return { distributions: rows, count, limit, offset };
    } catch (error) {
      throw new Error(`Failed to list report distributions: ${error.message}`);
    }
  }

  async updateDistribution(id, updateData) {
    try {
      const distribution = await this.getDistributionById(id);
      const updatedDistribution = await distribution.update(updateData);
      
      // If status was updated to sent, update sentAt timestamp
      if (updateData.status === 'sent' && !distribution.sentAt) {
        await updatedDistribution.update({ sentAt: new Date() });
      }
      
      // If status was updated to delivered, update deliveredAt timestamp
      if (updateData.status === 'delivered' && !distribution.deliveredAt) {
        await updatedDistribution.update({ deliveredAt: new Date() });
      }
      
      return updatedDistribution;
    } catch (error) {
      throw new Error(`Failed to update report distribution: ${error.message}`);
    }
  }

  async deleteDistribution(id) {
    try {
      const distribution = await this.getDistributionById(id);
      await distribution.destroy();
      return { success: true, message: 'Report distribution deleted successfully' };
    } catch (error) {
      throw new Error(`Failed to delete report distribution: ${error.message}`);
    }
  }

  async getDistributionsByReport(reportId, limit = 10, offset = 0) {
    try {
      const { rows, count } = await ReportDistribution.findAndCountAll({
        where: { reportId },
        limit,
        offset,
        order: [['created_at', 'DESC']]
      });
      return { distributions: rows, count, limit, offset };
    } catch (error) {
      throw new Error(`Failed to get report distributions: ${error.message}`);
    }
  }

  async getDistributionsByStatus(status, limit = 10, offset = 0) {
    try {
      const { rows, count } = await ReportDistribution.findAndCountAll({
        where: { status },
        limit,
        offset,
        order: [['created_at', 'DESC']]
      });
      return { distributions: rows, count, limit, offset };
    } catch (error) {
      throw new Error(`Failed to get distributions by status: ${error.message}`);
    }
  }

  async sendDistribution(id) {
    try {
      const distribution = await this.getDistributionById(id);
      
      // In a real implementation, we would actually send the report via the specified delivery method
      // For now, we'll just update the status to sent
      const updatedDistribution = await distribution.update({
        status: 'sent',
        sentAt: new Date()
      });
      
      return updatedDistribution;
    } catch (error) {
      throw new Error(`Failed to send report distribution: ${error.message}`);
    }
  }

  async markAsDelivered(id) {
    try {
      const distribution = await this.getDistributionById(id);
      
      // Update status to delivered
      const updatedDistribution = await distribution.update({
        status: 'delivered',
        deliveredAt: new Date()
      });
      
      return updatedDistribution;
    } catch (error) {
      throw new Error(`Failed to mark distribution as delivered: ${error.message}`);
    }
  }
}

module.exports = new ReportDistributionService();