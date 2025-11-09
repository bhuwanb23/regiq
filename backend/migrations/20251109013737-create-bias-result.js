'use strict';
/** @type {import('sequelize-cli').Migration} */
module.exports = {
  async up(queryInterface, Sequelize) {
    await queryInterface.createTable('BiasResults', {
      id: {
        allowNull: false,
        autoIncrement: true,
        primaryKey: true,
        type: Sequelize.INTEGER
      },
      analysisId: {
        type: Sequelize.UUID
      },
      analysisType: {
        type: Sequelize.STRING
      },
      entityId: {
        type: Sequelize.UUID
      },
      entityType: {
        type: Sequelize.STRING
      },
      biasMetrics: {
        type: Sequelize.JSON
      },
      overallScore: {
        type: Sequelize.FLOAT
      },
      demographicParity: {
        type: Sequelize.FLOAT
      },
      equalOpportunity: {
        type: Sequelize.FLOAT
      },
      disparateImpact: {
        type: Sequelize.FLOAT
      },
      statisticalParity: {
        type: Sequelize.FLOAT
      },
      consistency: {
        type: Sequelize.FLOAT
      },
      groupFairness: {
        type: Sequelize.JSON
      },
      individualFairness: {
        type: Sequelize.JSON
      },
      biasCategories: {
        type: Sequelize.JSON
      },
      confidenceInterval: {
        type: Sequelize.JSON
      },
      statisticalSignificance: {
        type: Sequelize.FLOAT
      },
      createdAt: {
        allowNull: false,
        type: Sequelize.DATE
      },
      updatedAt: {
        allowNull: false,
        type: Sequelize.DATE
      }
    });
  },
  async down(queryInterface, Sequelize) {
    await queryInterface.dropTable('BiasResults');
  }
};