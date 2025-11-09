'use strict';
/** @type {import('sequelize-cli').Migration} */
module.exports = {
  async up(queryInterface, Sequelize) {
    await queryInterface.createTable('comparison_reports', {
      id: {
        allowNull: false,
        autoIncrement: true,
        primaryKey: true,
        type: Sequelize.INTEGER
      },
      report_name: {
        type: Sequelize.STRING
      },
      description: {
        type: Sequelize.TEXT
      },
      models_compared: {
        type: Sequelize.JSON
      },
      datasets_compared: {
        type: Sequelize.JSON
      },
      metrics_compared: {
        type: Sequelize.JSON
      },
      comparison_type: {
        type: Sequelize.STRING
      },
      time_range: {
        type: Sequelize.JSON
      },
      baseline_model_id: {
        type: Sequelize.UUID
      },
      comparison_results: {
        type: Sequelize.JSON
      },
      summary: {
        type: Sequelize.JSON
      },
      recommendations: {
        type: Sequelize.JSON
      },
      visualization_data: {
        type: Sequelize.JSON
      },
      report_format: {
        type: Sequelize.STRING
      },
      status: {
        type: Sequelize.STRING
      },
      generated_by: {
        type: Sequelize.UUID
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
    await queryInterface.dropTable('comparison_reports');
  }
};