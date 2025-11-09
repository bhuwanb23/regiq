'use strict';

/** @type {import('sequelize-cli').Migration} */
module.exports = {
  async up (queryInterface, Sequelize) {
    await queryInterface.createTable('report_schedules', {
      id: {
        type: Sequelize.UUID,
        defaultValue: Sequelize.UUIDV4,
        primaryKey: true
      },
      schedule_name: {
        type: Sequelize.STRING,
        allowNull: false
      },
      description: {
        type: Sequelize.TEXT
      },
      report_type: {
        type: Sequelize.STRING,
        allowNull: false
      },
      frequency: {
        type: Sequelize.STRING
      },
      cron_expression: {
        type: Sequelize.STRING
      },
      next_run_time: {
        type: Sequelize.DATE
      },
      last_run_time: {
        type: Sequelize.DATE
      },
      last_run_status: {
        type: Sequelize.STRING
      },
      parameters: {
        type: Sequelize.JSON
      },
      is_active: {
        type: Sequelize.BOOLEAN,
        defaultValue: true
      },
      timezone: {
        type: Sequelize.STRING
      },
      notification_emails: {
        type: Sequelize.JSON
      },
      created_by: {
        type: Sequelize.UUID,
        allowNull: false
      },
      created_at: {
        allowNull: false,
        type: Sequelize.DATE
      },
      updated_at: {
        allowNull: false,
        type: Sequelize.DATE
      }
    });
  },

  async down (queryInterface, Sequelize) {
    await queryInterface.dropTable('report_schedules');
  }
};
