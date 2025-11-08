module.exports = (sequelize, DataTypes) => {
  const DataPipelineJob = sequelize.define('DataPipelineJob', {
    id: {
      type: DataTypes.UUID,
      defaultValue: DataTypes.UUIDV4,
      primaryKey: true
    },
    uploadId: {
      type: DataTypes.UUID,
      allowNull: false,
      field: 'upload_id'
    },
    fileName: {
      type: DataTypes.STRING,
      allowNull: false,
      field: 'file_name'
    },
    fileFormat: {
      type: DataTypes.STRING,
      allowNull: false,
      field: 'file_format'
    },
    fileSize: {
      type: DataTypes.INTEGER,
      field: 'file_size'
    },
    pipelineType: {
      type: DataTypes.STRING,
      allowNull: false,
      field: 'pipeline_type'
    },
    priority: {
      type: DataTypes.ENUM('low', 'normal', 'high'),
      defaultValue: 'normal'
    },
    configuration: {
      type: DataTypes.JSON
    },
    status: {
      type: DataTypes.ENUM('pending', 'in_progress', 'completed', 'failed', 'cancelled'),
      defaultValue: 'pending'
    },
    progress: {
      type: DataTypes.FLOAT,
      defaultValue: 0.0
    },
    stage: {
      type: DataTypes.STRING
    },
    estimatedCompletionTime: {
      type: DataTypes.DATE,
      field: 'estimated_completion_time'
    },
    recordsProcessed: {
      type: DataTypes.INTEGER,
      field: 'records_processed'
    },
    totalRecords: {
      type: DataTypes.INTEGER,
      field: 'total_records'
    },
    throughput: {
      type: DataTypes.FLOAT
    }
  }, {
    tableName: 'data_pipeline_jobs',
    timestamps: true,
    underscored: true
  });

  return DataPipelineJob;
};