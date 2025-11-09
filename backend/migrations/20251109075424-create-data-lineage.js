'use strict';
/** @type {import('sequelize-cli').Migration} */
module.exports = {
  async up(queryInterface, Sequelize) {
    await queryInterface.createTable('data_lineage', {
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
      sourceSystem: {
        type: Sequelize.STRING,
        allowNull: false,
        field: 'source_system'
      },
      targetSystem: {
        type: Sequelize.STRING,
        allowNull: false,
        field: 'target_system'
      },
      sourceTable: {
        type: Sequelize.STRING,
        field: 'source_table'
      },
      targetTable: {
        type: Sequelize.STRING,
        field: 'target_table'
      },
      sourceColumn: {
        type: Sequelize.STRING,
        field: 'source_column'
      },
      targetColumn: {
        type: Sequelize.STRING,
        field: 'target_column'
      },
      transformationType: {
        type: Sequelize.STRING,
        field: 'transformation_type'
      },
      transformationLogic: {
        type: Sequelize.TEXT,
        field: 'transformation_logic'
      },
      lineageType: {
        type: Sequelize.STRING,
        field: 'lineage_type'
      },
      status: {
        type: Sequelize.STRING,
        defaultValue: 'active'
      },
      startTime: {
        type: Sequelize.DATE,
        field: 'start_time'
      },
      endTime: {
        type: Sequelize.DATE,
        field: 'end_time'
      },
      duration: {
        type: Sequelize.INTEGER
      },
      recordCount: {
        type: Sequelize.INTEGER,
        field: 'record_count'
      },
      errorCount: {
        type: Sequelize.INTEGER,
        field: 'error_count'
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
    await queryInterface.dropTable('data_lineage');
  }
};