'use strict';
/** @type {import('sequelize-cli').Migration} */
module.exports = {
  async up(queryInterface, Sequelize) {
    await queryInterface.createTable('RiskSimulations', {
      id: {
        allowNull: false,
        autoIncrement: true,
        primaryKey: true,
        type: Sequelize.INTEGER
      },
      name: {
        type: Sequelize.STRING
      },
      description: {
        type: Sequelize.TEXT
      },
      scenarioId: {
        type: Sequelize.UUID
      },
      simulationType: {
        type: Sequelize.STRING
      },
      iterations: {
        type: Sequelize.INTEGER
      },
      timeHorizon: {
        type: Sequelize.INTEGER
      },
      modelParameters: {
        type: Sequelize.JSON
      },
      status: {
        type: Sequelize.STRING
      },
      summaryStatistics: {
        type: Sequelize.JSON
      },
      results: {
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
    await queryInterface.dropTable('RiskSimulations');
  }
};