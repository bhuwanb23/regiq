'use strict';
const {
  Model
} = require('sequelize');
module.exports = (sequelize, DataTypes) => {
  class ReportSchedule extends Model {
    /**
     * Helper method for defining associations.
     * This method is not a part of Sequelize lifecycle.
     * The `models/index` file will call this method automatically.
     */
    static associate(models) {
      // define association here
    }
  }
  ReportSchedule.init({
    scheduleName: DataTypes.STRING,
    description: DataTypes.TEXT,
    reportType: DataTypes.STRING,
    frequency: DataTypes.STRING,
    cronExpression: DataTypes.STRING,
    nextRunTime: DataTypes.DATE,
    lastRunTime: DataTypes.DATE,
    lastRunStatus: DataTypes.STRING,
    parameters: DataTypes.JSON,
    isActive: DataTypes.BOOLEAN,
    timezone: DataTypes.STRING,
    notificationEmails: DataTypes.JSON,
    createdBy: DataTypes.UUID
  }, {
    sequelize,
    modelName: 'ReportSchedule',
  });
  return ReportSchedule;
};