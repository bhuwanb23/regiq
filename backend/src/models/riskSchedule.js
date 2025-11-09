module.exports = (sequelize, DataTypes) => {
  const RiskSchedule = sequelize.define('RiskSchedule', {
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
    description: {
      type: DataTypes.TEXT
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
    }
  }, {
    tableName: 'risk_schedules',
    timestamps: true,
    underscored: true
  });

  return RiskSchedule;
};