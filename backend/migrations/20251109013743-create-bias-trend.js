'use strict';
/** @type {import('sequelize-cli').Migration} */
module.exports = {
  async up(queryInterface, Sequelize) {
    await queryInterface.createTable('bias_trends', {
      id: {
        allowNull: false,
        autoIncrement: true,
        primaryKey: true,
        type: Sequelize.INTEGER
      },
      model_id: {
        type: Sequelize.UUID
      },
      model_name: {
        type: Sequelize.STRING
      },
      metric_type: {
        type: Sequelize.STRING
      },
      metric_value: {
        type: Sequelize.FLOAT
      },
      threshold: {
        type: Sequelize.FLOAT
      },
      trend_direction: {
        type: Sequelize.STRING
      },
      significance: {
        type: Sequelize.FLOAT
      },
      time_period: {
        type: Sequelize.STRING
      },
      period_start: {
        type: Sequelize.DATE
      },
      period_end: {
        type: Sequelize.DATE
      },
      comparison_baseline: {
        type: Sequelize.FLOAT
      },
      variance: {
        type: Sequelize.FLOAT
      },
      alert_triggered: {
        type: Sequelize.BOOLEAN
      },
      alert_severity: {
        type: Sequelize.STRING
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
    await queryInterface.dropTable('bias_trends');
  }
};