module.exports = (sequelize, DataTypes) => {
  const ReportSchedule = sequelize.define('ReportSchedule', {
    id: {
      type: DataTypes.UUID,
      defaultValue: DataTypes.UUIDV4,
      primaryKey: true
    },
    scheduleName: {
      type: DataTypes.STRING,
      allowNull: false
    },
    description: {
      type: DataTypes.TEXT
    },
    reportType: {
      type: DataTypes.STRING,
      allowNull: false
    },
    frequency: {
      type: DataTypes.STRING
    },
    cronExpression: {
      type: DataTypes.STRING
    },
    nextRunTime: {
      type: DataTypes.DATE
    },
    lastRunTime: {
      type: DataTypes.DATE
    },
    lastRunStatus: {
      type: DataTypes.STRING
    },
    parameters: {
      type: DataTypes.JSON
    },
    isActive: {
      type: DataTypes.BOOLEAN,
      defaultValue: true
    },
    timezone: {
      type: DataTypes.STRING
    },
    notificationEmails: {
      type: DataTypes.JSON
    },
    createdBy: {
      type: DataTypes.UUID,
      allowNull: false
    }
  }, {
    tableName: 'report_schedules',
    timestamps: true,
    underscored: true
  });

  ReportSchedule.associate = function(models) {
    // Associations can be defined here if needed
  };

  return ReportSchedule;
};