module.exports = (sequelize, DataTypes) => {
  const BiasNotification = sequelize.define('BiasNotification', {
    id: {
      type: DataTypes.UUID,
      defaultValue: DataTypes.UUIDV4,
      primaryKey: true
    },
    notificationName: {
      type: DataTypes.STRING,
      allowNull: false,
      field: 'notification_name'
    },
    description: {
      type: DataTypes.TEXT
    },
    triggerType: {
      type: DataTypes.STRING,
      allowNull: false,
      field: 'trigger_type'
    },
    triggerCondition: {
      type: DataTypes.JSON,
      field: 'trigger_condition'
    },
    severityThreshold: {
      type: DataTypes.FLOAT,
      field: 'severity_threshold'
    },
    metricType: {
      type: DataTypes.STRING,
      field: 'metric_type'
    },
    comparisonOperator: {
      type: DataTypes.STRING,
      field: 'comparison_operator'
    },
    recipients: {
      type: DataTypes.JSON
    },
    notificationType: {
      type: DataTypes.ENUM('email', 'slack', 'webhook'),
      defaultValue: 'email',
      field: 'notification_type'
    },
    notificationTemplate: {
      type: DataTypes.TEXT,
      field: 'notification_template'
    },
    isActive: {
      type: DataTypes.BOOLEAN,
      defaultValue: true,
      field: 'is_active'
    },
    lastTriggered: {
      type: DataTypes.DATE,
      field: 'last_triggered'
    },
    cooldownPeriod: {
      type: DataTypes.INTEGER,
      field: 'cooldown_period'
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
    tableName: 'bias_notifications',
    timestamps: true,
    underscored: true
  });

  return BiasNotification;
};