module.exports = (sequelize, DataTypes) => {
  const FileUpload = sequelize.define('FileUpload', {
    id: {
      type: DataTypes.UUID,
      defaultValue: DataTypes.UUIDV4,
      primaryKey: true
    },
    userId: {
      type: DataTypes.UUID,
      allowNull: false,
      field: 'user_id'
    },
    fileName: {
      type: DataTypes.STRING,
      allowNull: false,
      field: 'file_name'
    },
    originalName: {
      type: DataTypes.STRING,
      allowNull: false,
      field: 'original_name'
    },
    fileExtension: {
      type: DataTypes.STRING,
      field: 'file_extension'
    },
    mimeType: {
      type: DataTypes.STRING,
      field: 'mime_type'
    },
    fileSize: {
      type: DataTypes.BIGINT,
      field: 'file_size'
    },
    filePath: {
      type: DataTypes.STRING,
      field: 'file_path'
    },
    bucketName: {
      type: DataTypes.STRING,
      field: 'bucket_name'
    },
    uploadStatus: {
      type: DataTypes.ENUM('pending', 'uploading', 'uploaded', 'processing', 'completed', 'failed'),
      defaultValue: 'pending',
      field: 'upload_status'
    },
    processingStatus: {
      type: DataTypes.ENUM('pending', 'in_progress', 'completed', 'failed'),
      defaultValue: 'pending',
      field: 'processing_status'
    },
    checksum: {
      type: DataTypes.STRING
    },
    encoding: {
      type: DataTypes.STRING
    },
    delimiter: {
      type: DataTypes.STRING
    },
    hasHeader: {
      type: DataTypes.BOOLEAN,
      defaultValue: true,
      field: 'has_header'
    },
    rowCount: {
      type: DataTypes.INTEGER,
      field: 'row_count'
    },
    columnCount: {
      type: DataTypes.INTEGER,
      field: 'column_count'
    },
    errorCount: {
      type: DataTypes.INTEGER,
      field: 'error_count'
    },
    errorMessage: {
      type: DataTypes.TEXT,
      field: 'error_message'
    }
  }, {
    tableName: 'file_uploads',
    timestamps: true,
    underscored: true
  });

  return FileUpload;
};