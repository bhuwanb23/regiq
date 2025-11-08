'use strict';
/** @type {import('sequelize-cli').Migration} */
module.exports = {
  async up(queryInterface, Sequelize) {
    await queryInterface.createTable('RegulatoryDocuments', {
      id: {
        allowNull: false,
        autoIncrement: true,
        primaryKey: true,
        type: Sequelize.INTEGER
      },
      title: {
        type: Sequelize.STRING
      },
      content: {
        type: Sequelize.TEXT
      },
      documentType: {
        type: Sequelize.STRING
      },
      source: {
        type: Sequelize.STRING
      },
      jurisdiction: {
        type: Sequelize.STRING
      },
      effectiveDate: {
        type: Sequelize.DATE
      },
      complianceScore: {
        type: Sequelize.FLOAT
      },
      keyFindings: {
        type: Sequelize.JSON
      },
      riskFactors: {
        type: Sequelize.JSON
      },
      recommendedActions: {
        type: Sequelize.JSON
      },
      tags: {
        type: Sequelize.JSON
      },
      status: {
        type: Sequelize.STRING
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
    await queryInterface.dropTable('RegulatoryDocuments');
  }
};