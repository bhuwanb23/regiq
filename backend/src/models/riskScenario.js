module.exports = (sequelize, DataTypes) => {
  const RiskScenario = sequelize.define('RiskScenario', {
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
    scenarioType: {
      type: DataTypes.STRING,
      allowNull: false,
      field: 'scenario_type'
    },
    parameters: {
      type: DataTypes.JSON
    },
    probability: {
      type: DataTypes.FLOAT,
      validate: {
        min: 0,
        max: 1
      }
    },
    impact: {
      type: DataTypes.FLOAT,
      validate: {
        min: 0,
        max: 100
      }
    },
    severity: {
      type: DataTypes.ENUM('low', 'medium', 'high', 'critical'),
      defaultValue: 'medium'
    },
    timeHorizon: {
      type: DataTypes.INTEGER,
      field: 'time_horizon'
    },
    jurisdiction: {
      type: DataTypes.STRING
    },
    isActive: {
      type: DataTypes.BOOLEAN,
      defaultValue: true,
      field: 'is_active'
    },
    createdBy: {
      type: DataTypes.UUID,
      field: 'created_by'
    },
    metadata: {
      type: DataTypes.JSON
    }
  }, {
    tableName: 'risk_scenarios',
    timestamps: true,
    underscored: true
  });

  return RiskScenario;
};