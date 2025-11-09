'use strict';
const {
  Model
} = require('sequelize');
module.exports = (sequelize, DataTypes) => {
  class RiskSchedule extends Model {
    /**
     * Helper method for defining associations.
     * This method is not a part of Sequelize lifecycle.
     * The `models/index` file will call this method automatically.
     */
    static associate(models) {
      // define association here
    }
  }
  RiskSchedule.init({
    scheduleName: DataTypes.STRING,
    description: DataTypes.TEXT,
    scheduleType: DataTypes.STRING,
    frequency: DataTypes.STRING,
    cronExpression: DataTypes.STRING,
    nextRunTime: DataTypes.DATE,
    lastRunTime: DataTypes.DATE,
    lastRunStatus: DataTypes.STRING,
    parameters: DataTypes.JSON,
    isActive: DataTypes.BOOLEAN,
    timezone: DataTypes.STRING,
    notificationEmails: DataTypes.JSON
  }, {
    sequelize,
    modelName: 'RiskSchedule',
  });
  return RiskSchedule;
};