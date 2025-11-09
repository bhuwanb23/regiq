module.exports = (sequelize, DataTypes) => {
  const RiskVisualization = sequelize.define('RiskVisualization', {
    id: {
      type: DataTypes.UUID,
      defaultValue: DataTypes.UUIDV4,
      primaryKey: true
    },
    visualizationName: {
      type: DataTypes.STRING,
      allowNull: false,
      field: 'visualization_name'
    },
    description: {
      type: DataTypes.TEXT
    },
    visualizationType: {
      type: DataTypes.STRING,
      allowNull: false,
      field: 'visualization_type'
    },
    dataType: {
      type: DataTypes.STRING,
      allowNull: false,
      field: 'data_type'
    },
    data: {
      type: DataTypes.JSON,
      allowNull: false
    },
    xAxisLabel: {
      type: DataTypes.STRING,
      field: 'x_axis_label'
    },
    yAxisLabel: {
      type: DataTypes.STRING,
      field: 'y_axis_label'
    },
    chartTitle: {
      type: DataTypes.STRING,
      field: 'chart_title'
    },
    simulationId: {
      type: DataTypes.UUID,
      allowNull: false,
      field: 'simulation_id'
    },
    scenarioId: {
      type: DataTypes.UUID,
      field: 'scenario_id'
    },
    metadata: {
      type: DataTypes.JSON
    }
  }, {
    tableName: 'risk_visualizations',
    timestamps: true,
    underscored: true
  });

  return RiskVisualization;
};