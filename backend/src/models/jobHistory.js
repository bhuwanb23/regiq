module.exports = (sequelize, DataTypes) => {
  const JobHistory = sequelize.define('JobHistory', {
    id: {
      type: DataTypes.UUID,
      defaultValue: DataTypes.UUIDV4,
      primaryKey: true
    },
    jobId: {
      type: DataTypes.STRING,
      allowNull: false,
      field: 'job_id'
    },
    jobType: {
      type: DataTypes.STRING,
      allowNull: false,
      field: 'job_type'
    },
    status: {
      type: DataTypes.ENUM('pending', 'queued', 'processing', 'retrying', 'completed', 'failed', 'cancelled'),
      allowNull: false
    },
    progress: {
      type: DataTypes.FLOAT,
      defaultValue: 0.0,
      validate: {
        min: 0,
        max: 100
      }
    },
    stage: {
      type: DataTypes.STRING
    },
    priority: {
      type: DataTypes.ENUM('low', 'normal', 'high'),
      defaultValue: 'normal'
    },
    startedAt: {
      type: DataTypes.DATE,
      field: 'started_at'
    },
    completedAt: {
      type: DataTypes.DATE,
      field: 'completed_at'
    },
    failedAt: {
      type: DataTypes.DATE,
      field: 'failed_at'
    },
    cancelledAt: {
      type: DataTypes.DATE,
      field: 'cancelled_at'
    },
    duration: {
      type: DataTypes.INTEGER,
      comment: 'Duration in milliseconds'
    },
    errorMessage: {
      type: DataTypes.TEXT,
      field: 'error_message'
    },
    errorStack: {
      type: DataTypes.TEXT,
      field: 'error_stack'
    },
    workerId: {
      type: DataTypes.STRING,
      field: 'worker_id'
    },
    nodeId: {
      type: DataTypes.STRING,
      field: 'node_id'
    },
    metadata: {
      type: DataTypes.JSON
    },
    inputParams: {
      type: DataTypes.JSON,
      field: 'input_params'
    },
    outputData: {
      type: DataTypes.JSON,
      field: 'output_data'
    },
    resourceUsage: {
      type: DataTypes.JSON,
      field: 'resource_usage'
    },
    throughput: {
      type: DataTypes.FLOAT
    },
    recordsProcessed: {
      type: DataTypes.INTEGER,
      field: 'records_processed'
    },
    totalRecords: {
      type: DataTypes.INTEGER,
      field: 'total_records'
    },
    retryCount: {
      type: DataTypes.INTEGER,
      defaultValue: 0,
      field: 'retry_count'
    }
  }, {
    tableName: 'job_histories',
    timestamps: true,
    underscored: true
  });

  return JobHistory;
};