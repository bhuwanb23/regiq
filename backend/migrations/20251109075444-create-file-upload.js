'use strict';
/** @type {import('sequelize-cli').Migration} */
module.exports = {
  async up(queryInterface, Sequelize) {
    await queryInterface.createTable('file_uploads', {
      id: {
        allowNull: false,
        primaryKey: true,
        type: Sequelize.UUID,
        defaultValue: Sequelize.UUIDV4
      },
      userId: {
        type: Sequelize.UUID,
        allowNull: false,
        field: 'user_id'
      },
      fileName: {
        type: Sequelize.STRING,
        field: 'file_name'
      },
      originalName: {
        type: Sequelize.STRING,
        field: 'original_name'
      },
      fileExtension: {
        type: Sequelize.STRING,
        field: 'file_extension'
      },
      mimeType: {
        type: Sequelize.STRING,
        field: 'mime_type'
      },
      fileSize: {
        type: Sequelize.BIGINT,
        field: 'file_size'
      },
      filePath: {
        type: Sequelize.STRING,
        field: 'file_path'
      },
      bucketName: {
        type: Sequelize.STRING,
        field: 'bucket_name'
      },
      uploadStatus: {
        type: Sequelize.ENUM('pending', 'uploading', 'uploaded', 'processing', 'completed', 'failed'),
        defaultValue: 'pending',
        field: 'upload_status'
      },
      processingStatus: {
        type: Sequelize.ENUM('pending', 'in_progress', 'completed', 'failed'),
        defaultValue: 'pending',
        field: 'processing_status'
      },
      checksum: {
        type: Sequelize.STRING
      },
      encoding: {
        type: Sequelize.STRING
      },
      delimiter: {
        type: Sequelize.STRING
      },
      hasHeader: {
        type: Sequelize.BOOLEAN,
        defaultValue: true,
        field: 'has_header'
      },
      rowCount: {
        type: Sequelize.INTEGER,
        field: 'row_count'
      },
      columnCount: {
        type: Sequelize.INTEGER,
        field: 'column_count'
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
    await queryInterface.dropTable('file_uploads');
  }
};