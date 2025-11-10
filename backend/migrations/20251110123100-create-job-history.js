'use strict';
/** @type {import('sequelize-cli').Migration} */
module.exports = {
  async up(queryInterface, Sequelize) {
    await queryInterface.createTable('job_histories', {
      id: {
        allowNull: false,
        primaryKey: true,
        type: Sequelize.UUID,
        defaultValue: Sequelize.UUIDV4
      },
      jobId: {
        type: Sequelize.STRING,
        allowNull: false,
        field: 'job_id'
      },
      jobType: {
        type: Sequelize.STRING,
        allowNull: false,
        field: 'job_type'
      },
      status: {
        type: Sequelize.ENUM('pending', 'queued', 'processing', 'retrying', 'completed', 'failed', 'cancelled'),
        allowNull: false
      },
      progress: {
        type: Sequelize.FLOAT,
        defaultValue: 0.0
      },
      stage: {
        type: Sequelize.STRING
      },
      priority: {
        type: Sequelize.ENUM('low', 'normal', 'high'),
        defaultValue: 'normal'
      },
      startedAt: {
        type: Sequelize.DATE,
        field: 'started_at'
      },
      completedAt: {
        type: Sequelize.DATE,
        field: 'completed_at'
      },
      failedAt: {
        type: Sequelize.DATE,
        field: 'failed_at'
      },
      cancelledAt: {
        type: Sequelize.DATE,
        field: 'cancelled_at'
      },
      duration: {
        type: Sequelize.INTEGER,
        comment: 'Duration in milliseconds'
      },
      errorMessage: {
        type: Sequelize.TEXT,
        field: 'error_message'
      },
      errorStack: {
        type: Sequelize.TEXT,
        field: 'error_stack'
      },
      workerId: {
        type: Sequelize.STRING,
        field: 'worker_id'
      },
      nodeId: {
        type: Sequelize.STRING,
        field: 'node_id'
      },
      metadata: {
        type: Sequelize.JSON
      },
      inputParams: {
        type: Sequelize.JSON,
        field: 'input_params'
      },
      outputData: {
        type: Sequelize.JSON,
        field: 'output_data'
      },
      resourceUsage: {
        type: Sequelize.JSON,
        field: 'resource_usage'
      },
      throughput: {
        type: Sequelize.FLOAT
      },
      recordsProcessed: {
        type: Sequelize.INTEGER,
        field: 'records_processed'
      },
      totalRecords: {
        type: Sequelize.INTEGER,
        field: 'total_records'
      },
      retryCount: {
        type: Sequelize.INTEGER,
        defaultValue: 0,
        field: 'retry_count'
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
    await queryInterface.dropTable('job_histories');
  }
};