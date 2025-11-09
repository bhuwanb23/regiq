module.exports = (sequelize, DataTypes) => {
  const BiasSchedule = sequelize.define('BiasSchedule', {
    id: {
      type: DataTypes.UUID,
      defaultValue: DataTypes.UUIDV4,
      primaryKey: true
    },
    scheduleName: {
      type: DataTypes.STRING,
      allowNull: false,
      field: 'schedule_name'
    },
    analysisType: {
      type: DataTypes.STRING,
      allowNull: false,
      field: 'analysis_type'
    },
    entityId: {
      type: DataTypes.UUID,
      allowNull: false,
      field: 'entity_id'
    },
    entityType: {
      type: DataTypes.STRING,
      allowNull: false,
      field: 'entity_type'
    },
    scheduleType: {
      type: DataTypes.STRING,
      allowNull: false,
      field: 'schedule_type'
    },
    frequency: {
      type: DataTypes.STRING
    },
    cronExpression: {
      type: DataTypes.STRING,
      field: 'cron_expression'
    },
    nextRunTime: {
      type: DataTypes.DATE,
      field: 'next_run_time'
    },
    lastRunTime: {
      type: DataTypes.DATE,
      field: 'last_run_time'
    },
    lastRunStatus: {
      type: DataTypes.STRING,
      field: 'last_run_status'
    },
    parameters: {
      type: DataTypes.JSON
    },
    isActive: {
      type: DataTypes.BOOLEAN,
      defaultValue: true,
      field: 'is_active'
    },
    timezone: {
      type: DataTypes.STRING
    },
    notificationEmails: {
      type: DataTypes.JSON,
      field: 'notification_emails'
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
    tableName: 'bias_schedules',
    timestamps: true,
    underscored: true
  });

  return BiasSchedule;
};