'use strict';
/** @type {import('sequelize-cli').Migration} */
module.exports = {
  async up(queryInterface, Sequelize) {
    await queryInterface.createTable('data_pipeline_jobs', {
      id: {
        allowNull: false,
        primaryKey: true,
        type: Sequelize.UUID,
        defaultValue: Sequelize.UUIDV4
      },
      uploadId: {
        type: Sequelize.UUID,
        field: 'upload_id'
      },
      fileName: {
        type: Sequelize.STRING,
        field: 'file_name'
      },
      fileFormat: {
        type: Sequelize.STRING,
        field: 'file_format'
      },
      fileSize: {
        type: Sequelize.INTEGER,
        field: 'file_size'
      },
      pipelineType: {
        type: Sequelize.STRING,
        field: 'pipeline_type'
      },
      priority: {
        type: Sequelize.ENUM('low', 'normal', 'high'),
        defaultValue: 'normal'
      },
      configuration: {
        type: Sequelize.JSON
      },
      status: {
        type: Sequelize.ENUM('pending', 'in_progress', 'completed', 'failed', 'cancelled'),
        defaultValue: 'pending'
      },
      progress: {
        type: Sequelize.FLOAT,
        defaultValue: 0.0
      },
      stage: {
        type: Sequelize.STRING
      },
      estimatedCompletionTime: {
        type: Sequelize.DATE,
        field: 'estimated_completion_time'
      },
      recordsProcessed: {
        type: Sequelize.INTEGER,
        field: 'records_processed'
      },
      totalRecords: {
        type: Sequelize.INTEGER,
        field: 'total_records'
      },
      throughput: {
        type: Sequelize.FLOAT
      },
      createdAt: {
        allowNull: false,
        type: Sequelize.DATE,
        field: 'created_at'
      },
      updatedAt: {
        allowNull: false,
        type: Sequelize.DATE,
        field: 'updated_at'
      }
    });
  },
  async down(queryInterface, Sequelize) {
    await queryInterface.dropTable('data_pipeline_jobs');
  }
};