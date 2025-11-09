'use strict';
/** @type {import('sequelize-cli').Migration} */
module.exports = {
  async up(queryInterface, Sequelize) {
    await queryInterface.createTable('data_quality_metrics', {
      id: {
        allowNull: false,
        primaryKey: true,
        type: Sequelize.UUID,
        defaultValue: Sequelize.UUIDV4
      },
      jobId: {
        type: Sequelize.UUID,
        allowNull: false,
        field: 'job_id'
      },
      metricType: {
        type: Sequelize.ENUM('completeness', 'accuracy', 'consistency', 'timeliness', 'uniqueness', 'validity'),
        allowNull: false,
        field: 'metric_type'
      },
      metricName: {
        type: Sequelize.STRING,
        allowNull: false,
        field: 'metric_name'
      },
      metricValue: {
        type: Sequelize.DECIMAL(10, 4),
        field: 'metric_value'
      },
      thresholdValue: {
        type: Sequelize.DECIMAL(10, 4),
        field: 'threshold_value'
      },
      status: {
        type: Sequelize.ENUM('pass', 'fail', 'warning'),
        defaultValue: 'pass'
      },
      dimension: {
        type: Sequelize.STRING
      },
      dataSource: {
        type: Sequelize.STRING,
        field: 'data_source'
      },
      tableName: {
        type: Sequelize.STRING,
        field: 'table_name'
      },
      columnName: {
        type: Sequelize.STRING,
        field: 'column_name'
      },
      recordCount: {
        type: Sequelize.INTEGER,
        field: 'record_count'
      },
      errorCount: {
        type: Sequelize.INTEGER,
        field: 'error_count'
      },
      errorMessage: {
        type: Sequelize.TEXT,
        field: 'error_message'
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
    await queryInterface.dropTable('data_quality_metrics');
  }
};