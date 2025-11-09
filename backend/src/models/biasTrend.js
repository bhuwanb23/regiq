module.exports = (sequelize, DataTypes) => {
  const BiasTrend = sequelize.define('BiasTrend', {
    id: {
      type: DataTypes.UUID,
      defaultValue: DataTypes.UUIDV4,
      primaryKey: true
    },
    modelId: {
      type: DataTypes.UUID,
      allowNull: false,
      field: 'model_id'
    },
    modelName: {
      type: DataTypes.STRING,
      allowNull: false,
      field: 'model_name'
    },
    metricType: {
      type: DataTypes.STRING,
      allowNull: false,
      field: 'metric_type'
    },
    metricValue: {
      type: DataTypes.FLOAT,
      field: 'metric_value'
    },
    threshold: {
      type: DataTypes.FLOAT
    },
    trendDirection: {
      type: DataTypes.ENUM('increasing', 'decreasing', 'stable'),
      field: 'trend_direction'
    },
    significance: {
      type: DataTypes.FLOAT
    },
    timePeriod: {
      type: DataTypes.STRING,
      field: 'time_period'
    },
    periodStart: {
      type: DataTypes.DATE,
      field: 'period_start'
    },
    periodEnd: {
      type: DataTypes.DATE,
      field: 'period_end'
    },
    comparisonBaseline: {
      type: DataTypes.FLOAT,
      field: 'comparison_baseline'
    },
    variance: {
      type: DataTypes.FLOAT
    },
    alertTriggered: {
      type: DataTypes.BOOLEAN,
      defaultValue: false,
      field: 'alert_triggered'
    },
    alertSeverity: {
      type: DataTypes.ENUM('low', 'medium', 'high', 'critical'),
      field: 'alert_severity'
    },
    createdAt: {
      type: DataTypes.DATE,
      field: 'created_at'
    },
    updatedAt: {
      type: DataTypes.DATE,
      field: 'updated_at'
    }
  }, {
    tableName: 'bias_trends',
    timestamps: true,
    underscored: true
  });

  return BiasTrend;
};