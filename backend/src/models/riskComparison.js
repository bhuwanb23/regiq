module.exports = (sequelize, DataTypes) => {
  const RiskComparison = sequelize.define('RiskComparison', {
    id: {
      type: DataTypes.UUID,
      defaultValue: DataTypes.UUIDV4,
      primaryKey: true
    },
    comparisonName: {
      type: DataTypes.STRING,
      allowNull: false,
      field: 'comparison_name'
    },
    description: {
      type: DataTypes.TEXT
    },
    simulationsCompared: {
      type: DataTypes.JSON,
      field: 'simulations_compared'
    },
    scenariosCompared: {
      type: DataTypes.JSON,
      field: 'scenarios_compared'
    },
    metricsCompared: {
      type: DataTypes.JSON,
      field: 'metrics_compared'
    },
    comparisonType: {
      type: DataTypes.STRING,
      field: 'comparison_type'
    },
    timeRange: {
      type: DataTypes.JSON,
      field: 'time_range'
    },
    baselineSimulationId: {
      type: DataTypes.UUID,
      field: 'baseline_simulation_id'
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
      field: 'report_format'
    },
    status: {
      type: DataTypes.STRING,
      defaultValue: 'completed'
    },
    generatedBy: {
      type: DataTypes.UUID,
      field: 'generated_by'
    }
  }, {
    tableName: 'risk_comparisons',
    timestamps: true,
    underscored: true
  });

  return RiskComparison;
};