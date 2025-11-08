'use strict';
/** @type {import('sequelize-cli').Migration} */
module.exports = {
  async up(queryInterface, Sequelize) {
    await queryInterface.createTable('ModelAnalyses', {
      id: {
        allowNull: false,
        autoIncrement: true,
        primaryKey: true,
        type: Sequelize.INTEGER
      },
      modelId: {
        type: Sequelize.UUID
      },
      modelName: {
        type: Sequelize.STRING
      },
      modelType: {
        type: Sequelize.STRING
      },
      framework: {
        type: Sequelize.STRING
      },
      version: {
        type: Sequelize.STRING
      },
      targetVariable: {
        type: Sequelize.STRING
      },
      protectedAttributes: {
        type: Sequelize.JSON
      },
      trainingDataSize: {
        type: Sequelize.INTEGER
      },
      performanceMetrics: {
        type: Sequelize.JSON
      },
      demographicParityDifference: {
        type: Sequelize.FLOAT
      },
      equalOpportunityDifference: {
        type: Sequelize.FLOAT
      },
      disparateImpact: {
        type: Sequelize.FLOAT
      },
      statisticalParityDifference: {
        type: Sequelize.FLOAT
      },
      consistencyScore: {
        type: Sequelize.FLOAT
      },
      featureImportanceBias: {
        type: Sequelize.JSON
      },
      groupMetrics: {
        type: Sequelize.JSON
      },
      status: {
        type: Sequelize.STRING
      },
      analysisParameters: {
        type: Sequelize.JSON
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
    await queryInterface.dropTable('ModelAnalyses');
  }
};