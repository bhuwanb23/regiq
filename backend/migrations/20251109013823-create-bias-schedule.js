'use strict';
/** @type {import('sequelize-cli').Migration} */
module.exports = {
  async up(queryInterface, Sequelize) {
    await queryInterface.createTable('bias_schedules', {
      id: {
        allowNull: false,
        autoIncrement: true,
        primaryKey: true,
        type: Sequelize.INTEGER
      },
      schedule_name: {
        type: Sequelize.STRING
      },
      analysis_type: {
        type: Sequelize.STRING
      },
      entity_id: {
        type: Sequelize.UUID
      },
      entity_type: {
        type: Sequelize.STRING
      },
      schedule_type: {
        type: Sequelize.STRING
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
        type: Sequelize.BOOLEAN
      },
      timezone: {
        type: Sequelize.STRING
      },
      notification_emails: {
        type: Sequelize.JSON
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
  async down(queryInterface, Sequelize) {
    await queryInterface.dropTable('bias_schedules');
  }
};