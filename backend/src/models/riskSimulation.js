module.exports = (sequelize, DataTypes) => {
  const RiskSimulation = sequelize.define('RiskSimulation', {
    id: {
      type: DataTypes.UUID,
      defaultValue: DataTypes.UUIDV4,
      primaryKey: true
    },
    name: {
      type: DataTypes.STRING,
      allowNull: false
    },
    description: {
      type: DataTypes.TEXT
    },
    scenarioId: {
      type: DataTypes.UUID,
      allowNull: false,
      field: 'scenario_id'
    },
    simulationType: {
      type: DataTypes.STRING,
      defaultValue: 'monte_carlo',
      field: 'simulation_type'
    },
    iterations: {
      type: DataTypes.INTEGER,
      defaultValue: 1000
    },
    timeHorizon: {
      type: DataTypes.INTEGER,
      field: 'time_horizon'
    },
    modelParameters: {
      type: DataTypes.JSON,
      field: 'model_parameters'
    },
    status: {
      type: DataTypes.ENUM('pending', 'configured', 'running', 'completed', 'failed'),
      defaultValue: 'pending'
    },
    summaryStatistics: {
      type: DataTypes.JSON,
      field: 'summary_statistics'
    },
    results: {
      type: DataTypes.JSON
    }
  }, {
    tableName: 'risk_simulations',
    timestamps: true,
    underscored: true
  });

  return RiskSimulation;
};