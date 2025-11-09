'use strict';
/** @type {import('sequelize-cli').Migration} */
module.exports = {
  async up(queryInterface, Sequelize) {
    await queryInterface.createTable('mitigation_recommendations', {
      id: {
        allowNull: false,
        autoIncrement: true,
        primaryKey: true,
        type: Sequelize.INTEGER
      },
      analysis_id: {
        type: Sequelize.UUID
      },
      analysis_type: {
        type: Sequelize.STRING
      },
      bias_type: {
        type: Sequelize.STRING
      },
      severity: {
        type: Sequelize.STRING
      },
      recommendation_type: {
        type: Sequelize.STRING
      },
      title: {
        type: Sequelize.STRING
      },
      description: {
        type: Sequelize.TEXT
      },
      implementation_steps: {
        type: Sequelize.JSON
      },
      expected_impact: {
        type: Sequelize.FLOAT
      },
      confidence_score: {
        type: Sequelize.FLOAT
      },
      priority: {
        type: Sequelize.STRING
      },
      applicability: {
        type: Sequelize.JSON
      },
      resources: {
        type: Sequelize.JSON
      },
      estimated_effort: {
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
    await queryInterface.dropTable('mitigation_recommendations');
  }
};