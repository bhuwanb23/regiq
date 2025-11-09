'use strict';
/** @type {import('sequelize-cli').Migration} */
module.exports = {
  async up(queryInterface, Sequelize) {
    await queryInterface.createTable('bias_notifications', {
      id: {
        allowNull: false,
        autoIncrement: true,
        primaryKey: true,
        type: Sequelize.INTEGER
      },
      notification_name: {
        type: Sequelize.STRING
      },
      description: {
        type: Sequelize.TEXT
      },
      trigger_type: {
        type: Sequelize.STRING
      },
      trigger_condition: {
        type: Sequelize.JSON
      },
      severity_threshold: {
        type: Sequelize.FLOAT
      },
      metric_type: {
        type: Sequelize.STRING
      },
      comparison_operator: {
        type: Sequelize.STRING
      },
      recipients: {
        type: Sequelize.JSON
      },
      notification_type: {
        type: Sequelize.STRING
      },
      notification_template: {
        type: Sequelize.TEXT
      },
      is_active: {
        type: Sequelize.BOOLEAN
      },
      last_triggered: {
        type: Sequelize.DATE
      },
      cooldown_period: {
        type: Sequelize.INTEGER
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
    await queryInterface.dropTable('bias_notifications');
  }
};