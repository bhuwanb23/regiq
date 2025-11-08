'use strict';
/** @type {import('sequelize-cli').Migration} */
module.exports = {
  async up(queryInterface, Sequelize) {
    await queryInterface.createTable('DataPipelineJobs', {
      id: {
        allowNull: false,
        autoIncrement: true,
        primaryKey: true,
        type: Sequelize.INTEGER
      },
      uploadId: {
        type: Sequelize.UUID
      },
      fileName: {
        type: Sequelize.STRING
      },
      fileFormat: {
        type: Sequelize.STRING
      },
      fileSize: {
        type: Sequelize.INTEGER
      },
      pipelineType: {
        type: Sequelize.STRING
      },
      priority: {
        type: Sequelize.STRING
      },
      configuration: {
        type: Sequelize.JSON
      },
      status: {
        type: Sequelize.STRING
      },
      progress: {
        type: Sequelize.FLOAT
      },
      stage: {
        type: Sequelize.STRING
      },
      estimatedCompletionTime: {
        type: Sequelize.DATE
      },
      recordsProcessed: {
        type: Sequelize.INTEGER
      },
      totalRecords: {
        type: Sequelize.INTEGER
      },
      throughput: {
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
    await queryInterface.dropTable('DataPipelineJobs');
  }
};