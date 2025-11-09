module.exports = (sequelize, DataTypes) => {
  const RiskAlert = sequelize.define('RiskAlert', {
    id: {
      type: DataTypes.UUID,
      defaultValue: DataTypes.UUIDV4,
      primaryKey: true
    },
    alertName: {
      type: DataTypes.STRING,
      allowNull: false,
      field: 'alert_name'
    },
    description: {
      type: DataTypes.TEXT
    },
    alertType: {
      type: DataTypes.STRING,
      allowNull: false,
      field: 'alert_type'
    },
    severity: {
      type: DataTypes.ENUM('low', 'medium', 'high', 'critical'),
      defaultValue: 'medium'
    },
    threshold: {
      type: DataTypes.FLOAT
    },
    currentValue: {
      type: DataTypes.FLOAT,
      field: 'current_value'
    },
    triggeredAt: {
      type: DataTypes.DATE,
      field: 'triggered_at'
    },
    resolvedAt: {
      type: DataTypes.DATE,
      field: 'resolved_at'
    },
    isActive: {
      type: DataTypes.BOOLEAN,
      defaultValue: true,
      field: 'is_active'
    },
    simulationId: {
      type: DataTypes.UUID,
      field: 'simulation_id'
    },
    scenarioId: {
      type: DataTypes.UUID,
      field: 'scenario_id'
    },
    recipients: {
      type: DataTypes.JSON
    },
    metadata: {
      type: DataTypes.JSON
    }
  }, {
    tableName: 'risk_alerts',
    timestamps: true,
    underscored: true
  });

  return RiskAlert;
};