module.exports = (sequelize, DataTypes) => {
  const ComparisonReport = sequelize.define('ComparisonReport', {
    id: {
      type: DataTypes.UUID,
      defaultValue: DataTypes.UUIDV4,
      primaryKey: true
    },
    reportName: {
      type: DataTypes.STRING,
      allowNull: false,
      field: 'report_name'
    },
    description: {
      type: DataTypes.TEXT
    },
    modelsCompared: {
      type: DataTypes.JSON,
      field: 'models_compared'
    },
    datasetsCompared: {
      type: DataTypes.JSON,
      field: 'datasets_compared'
    },
    metricsCompared: {
      type: DataTypes.JSON,
      field: 'metrics_compared'
    },
    comparisonType: {
      type: DataTypes.STRING,
      allowNull: false,
      field: 'comparison_type'
    },
    timeRange: {
      type: DataTypes.JSON,
      field: 'time_range'
    },
    baselineModelId: {
      type: DataTypes.UUID,
      field: 'baseline_model_id'
    },
    comparisonResults: {
      type: DataTypes.JSON,
      field: 'comparison_results'
    },
    summary: {
      type: DataTypes.JSON
    },
    recommendations: {
      type: DataTypes.JSON
    },
    visualizationData: {
      type: DataTypes.JSON,
      field: 'visualization_data'
    },
    reportFormat: {
      type: DataTypes.STRING,
      defaultValue: 'json',
      field: 'report_format'
    },
    status: {
      type: DataTypes.ENUM('pending', 'generating', 'completed', 'failed'),
      defaultValue: 'pending'
    },
    generatedBy: {
      type: DataTypes.UUID,
      field: 'generated_by'
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
    tableName: 'comparison_reports',
    timestamps: true,
    underscored: true
  });

  return ComparisonReport;
};