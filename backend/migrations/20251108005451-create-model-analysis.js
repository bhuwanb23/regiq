'use strict';
/** @type {import('sequelize-cli').Migration} */
module.exports = {
  async up(queryInterface, Sequelize) {
    await queryInterface.createTable('model_analyses', {
      id: {
        type: Sequelize.UUID,
        defaultValue: Sequelize.UUIDV4,
        primaryKey: true,
        allowNull: false
      },
      model_id: {
        type: Sequelize.UUID,
        allowNull: false
      },
      model_name: {
        type: Sequelize.STRING,
        allowNull: false
      },
      model_type: {
        type: Sequelize.STRING,
        allowNull: false
      },
      framework: {
        type: Sequelize.STRING,
        allowNull: false
      },
      version: {
        type: Sequelize.STRING,
        allowNull: false
      },
      target_variable: {
        type: Sequelize.STRING,
        allowNull: false
      },
      protected_attributes: {
        type: Sequelize.JSON,
        allowNull: false
      },
      training_data_size: {
        type: Sequelize.INTEGER
      },
      performance_metrics: {
        type: Sequelize.JSON
      },
      demographic_parity_difference: {
        type: Sequelize.FLOAT
      },
      equal_opportunity_difference: {
        type: Sequelize.FLOAT
      },
      disparate_impact: {
        type: Sequelize.FLOAT
      },
      statistical_parity_difference: {
        type: Sequelize.FLOAT
      },
      consistency_score: {
        type: Sequelize.FLOAT
      },
      feature_importance_bias: {
        type: Sequelize.JSON
      },
      group_metrics: {
        type: Sequelize.JSON
      },
      status: {
        type: Sequelize.ENUM('pending', 'in_progress', 'completed', 'failed'),
        defaultValue: 'pending'
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
    await queryInterface.dropTable('model_analyses');
  }
};