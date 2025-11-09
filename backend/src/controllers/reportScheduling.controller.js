const reportSchedulingService = require('../services/reportScheduling.service');

class ReportSchedulingController {
  async createSchedule(req, res) {
    try {
      const schedule = await reportSchedulingService.createSchedule(req.body);
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

  async getSchedule(req, res) {
    try {
      const { id } = req.params;
      const schedule = await reportSchedulingService.getScheduleById(id);
      res.status(200).json({
        success: true,
        message: 'Report schedule retrieved successfully',
        data: schedule
      });
    } catch (error) {
      res.status(404).json({
        success: false,
        message: error.message
      });
    }
  }

  async listSchedules(req, res) {
    try {
      const { limit = 10, offset = 0 } = req.query;
      const result = await reportSchedulingService.getAllSchedules(
        parseInt(limit),
        parseInt(offset)
      );
      res.status(200).json({
        success: true,
        message: 'Report schedules retrieved successfully',
        data: result
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }

  async updateSchedule(req, res) {
    try {
      const { id } = req.params;
      const schedule = await reportSchedulingService.updateSchedule(id, req.body);
      res.status(200).json({
        success: true,
        message: 'Report schedule updated successfully',
        data: schedule
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  async deleteSchedule(req, res) {
    try {
      const { id } = req.params;
      const result = await reportSchedulingService.deleteSchedule(id);
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

  async getActiveSchedules(req, res) {
    try {
      const schedules = await reportSchedulingService.getActiveSchedules();
      res.status(200).json({
        success: true,
        message: 'Active report schedules retrieved successfully',
        data: schedules
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }

  async executeSchedule(req, res) {
    try {
      const { id } = req.params;
      const result = await reportSchedulingService.executeSchedule(id);
      res.status(200).json({
        success: true,
        message: result.message
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }
}

module.exports = new ReportSchedulingController();