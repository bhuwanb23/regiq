module.exports = (sequelize, DataTypes) => {
  const DataQualityMetric = sequelize.define('DataQualityMetric', {
    id: {
      type: DataTypes.UUID,
      defaultValue: DataTypes.UUIDV4,
      primaryKey: true
    },
    jobId: {
      type: DataTypes.UUID,
      allowNull: false,
      field: 'job_id'
    },
    metricType: {
      type: DataTypes.ENUM('completeness', 'accuracy', 'consistency', 'timeliness', 'uniqueness', 'validity'),
      allowNull: false,
      field: 'metric_type'
    },
    metricName: {
      type: DataTypes.STRING,
      allowNull: false,
      field: 'metric_name'
    },
    metricValue: {
      type: DataTypes.DECIMAL(10, 4),
      field: 'metric_value'
    },
    thresholdValue: {
      type: DataTypes.DECIMAL(10, 4),
      field: 'threshold_value'
    },
    status: {
      type: DataTypes.ENUM('pass', 'fail', 'warning'),
      defaultValue: 'pass'
    },
    dimension: {
      type: DataTypes.STRING
    },
    dataSource: {
      type: DataTypes.STRING,
      field: 'data_source'
    },
    tableName: {
      type: DataTypes.STRING,
      field: 'table_name'
    },
    columnName: {
      type: DataTypes.STRING,
      field: 'column_name'
    },
    recordCount: {
      type: DataTypes.INTEGER,
      field: 'record_count'
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
    tableName: 'data_quality_metrics',
    timestamps: true,
    underscored: true
  });

  return DataQualityMetric;
};