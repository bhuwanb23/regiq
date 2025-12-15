const cron = require('node-cron');
const notificationService = require('./notification.service');
const winston = require('winston');

class NotificationScheduler {
  constructor() {
    // Initialize logger
    this.logger = winston.createLogger({
      level: 'info',
      format: winston.format.json(),
      transports: [
        new winston.transports.Console(),
      ],
    });

    // Start scheduler
    this.start();
  }

  /**
   * Start the notification scheduler
   */
  start() {
    // Check for scheduled notifications every minute
    cron.schedule('* * * * *', async () => {
      try {
        this.logger.info('Checking for scheduled notifications');
        await notificationService.sendScheduledNotifications();
      } catch (error) {
        this.logger.error('Failed to process scheduled notifications', { error: error.message });
      }
    });

    this.logger.info('Notification scheduler started');
  }
}

module.exports = new NotificationScheduler();