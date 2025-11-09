'use strict';
/** @type {import('sequelize-cli').Migration} */
module.exports = {
  async up(queryInterface, Sequelize) {
    await queryInterface.createTable('data_bias_detections', {
      id: {
        allowNull: false,
        autoIncrement: true,
        primaryKey: true,
        type: Sequelize.INTEGER
      },
      dataset_id: {
        type: Sequelize.UUID
      },
      dataset_name: {
        type: Sequelize.STRING
      },
      file_type: {
        type: Sequelize.STRING
      },
      file_size: {
        type: Sequelize.INTEGER
      },
      row_count: {
        type: Sequelize.INTEGER
      },
      column_count: {
        type: Sequelize.INTEGER
      },
      protected_attributes: {
        type: Sequelize.JSON
      },
      bias_metrics: {
        type: Sequelize.JSON
      },
      representation_bias: {
        type: Sequelize.JSON
      },
      measurement_bias: {
        type: Sequelize.JSON
      },
      evaluation_bias: {
        type: Sequelize.JSON
      },
      historical_bias: {
        type: Sequelize.JSON
      },
      aggregation_bias: {
        type: Sequelize.JSON
      },
      selection_bias: {
        type: Sequelize.JSON
      },
      survivorship_bias: {
        type: Sequelize.JSON
      },
      severity_score: {
        type: Sequelize.FLOAT
      },
      recommendations: {
        type: Sequelize.JSON
      },
      status: {
        type: Sequelize.STRING
      },
      analysis_parameters: {
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
    await queryInterface.dropTable('data_bias_detections');
  }
};