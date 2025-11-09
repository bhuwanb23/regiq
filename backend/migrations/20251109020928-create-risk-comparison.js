'use strict';
/** @type {import('sequelize-cli').Migration} */
module.exports = {
  async up(queryInterface, Sequelize) {
    await queryInterface.createTable('risk_comparisons', {
      id: {
        type: Sequelize.UUID,
        defaultValue: Sequelize.UUIDV4,
        primaryKey: true,
        allowNull: false
      },
      comparison_name: {
        type: Sequelize.STRING,
        allowNull: false
      },
      description: {
        type: Sequelize.TEXT
      },
      simulations_compared: {
        type: Sequelize.JSON
      },
      scenarios_compared: {
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
      baseline_simulation_id: {
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
        type: Sequelize.STRING,
        defaultValue: 'completed'
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
    await queryInterface.dropTable('risk_comparisons');
  }
};