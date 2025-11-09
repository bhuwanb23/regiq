const { ReportSchedule } = require('../models');
const cron = require('node-cron');

class ReportSchedulingService {
  constructor() {
    this.scheduledTasks = new Map();
  }

  async createSchedule(scheduleData) {
    try {
      // Validate cron expression if provided
      if (scheduleData.cronExpression) {
        if (!cron.validate(scheduleData.cronExpression)) {
          throw new Error('Invalid cron expression');
        }
      }

      const schedule = await ReportSchedule.create(scheduleData);
      
      // If the schedule is active, start it
      if (schedule.isActive) {
        this.startSchedule(schedule.id);
      }

      return schedule;
    } catch (error) {
      throw new Error(`Failed to create report schedule: ${error.message}`);
    }
  }

  async getScheduleById(id) {
    try {
      const schedule = await ReportSchedule.findByPk(id);
      if (!schedule) {
        throw new Error('Report schedule not found');
      }
      return schedule;
    } catch (error) {
      throw new Error(`Failed to get report schedule: ${error.message}`);
    }
  }

  async getAllSchedules(limit = 10, offset = 0) {
    try {
      const { rows, count } = await ReportSchedule.findAndCountAll({
        limit,
        offset,
        order: [['created_at', 'DESC']]
      });
      return { schedules: rows, count, limit, offset };
    } catch (error) {
      throw new Error(`Failed to list report schedules: ${error.message}`);
    }
  }

  async updateSchedule(id, updateData) {
    try {
      const schedule = await this.getScheduleById(id);
      
      // Validate cron expression if provided
      if (updateData.cronExpression) {
        if (!cron.validate(updateData.cronExpression)) {
          throw new Error('Invalid cron expression');
        }
      }

      const updatedSchedule = await schedule.update(updateData);
      
      // If the schedule was updated to be active, start it
      // If it was updated to be inactive, stop it
      if (updateData.isActive !== undefined) {
        if (updateData.isActive) {
          this.startSchedule(schedule.id);
        } else {
          this.stopSchedule(schedule.id);
        }
      }

      return updatedSchedule;
    } catch (error) {
      throw new Error(`Failed to update report schedule: ${error.message}`);
    }
  }

  async deleteSchedule(id) {
    try {
      const schedule = await this.getScheduleById(id);
      
      // Stop the scheduled task if it's running
      this.stopSchedule(schedule.id);
      
      await schedule.destroy();
      return { success: true, message: 'Report schedule deleted successfully' };
    } catch (error) {
      throw new Error(`Failed to delete report schedule: ${error.message}`);
    }
  }

  async getActiveSchedules() {
    try {
      const schedules = await ReportSchedule.findAll({
        where: { isActive: true },
        order: [['created_at', 'DESC']]
      });
      return schedules;
    } catch (error) {
      throw new Error(`Failed to get active report schedules: ${error.message}`);
    }
  }

  startSchedule(scheduleId) {
    try {
      // In a real implementation, we would set up the actual cron job
      // For now, we'll just store the schedule ID in our map
      this.scheduledTasks.set(scheduleId, true);
      console.log(`Started schedule: ${scheduleId}`);
    } catch (error) {
      console.error(`Failed to start schedule ${scheduleId}: ${error.message}`);
    }
  }

  stopSchedule(scheduleId) {
    try {
      // In a real implementation, we would stop the actual cron job
      // For now, we'll just remove the schedule ID from our map
      this.scheduledTasks.delete(scheduleId);
      console.log(`Stopped schedule: ${scheduleId}`);
    } catch (error) {
      console.error(`Failed to stop schedule ${scheduleId}: ${error.message}`);
    }
  }

  async executeSchedule(scheduleId) {
    try {
      const schedule = await this.getScheduleById(scheduleId);
      
      // Update last run time and status
      await schedule.update({
        lastRunTime: new Date(),
        lastRunStatus: 'executing'
      });

      // In a real implementation, we would generate the report here
      // For now, we'll just update the status to completed
      await schedule.update({
        lastRunStatus: 'completed'
      });

      return { success: true, message: 'Schedule executed successfully' };
    } catch (error) {
      // Update status to failed
      try {
        const schedule = await this.getScheduleById(scheduleId);
        await schedule.update({
          lastRunStatus: 'failed'
        });
      } catch (updateError) {
        console.error(`Failed to update schedule status: ${updateError.message}`);
      }
      
      throw new Error(`Failed to execute schedule: ${error.message}`);
    }
  }
}

module.exports = new ReportSchedulingService();