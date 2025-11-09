'use strict';
const {
  Model
} = require('sequelize');
module.exports = (sequelize, DataTypes) => {
  class BiasNotification extends Model {
    /**
     * Helper method for defining associations.
     * This method is not a part of Sequelize lifecycle.
     * The `models/index` file will call this method automatically.
     */
    static associate(models) {
      // define association here
    }
  }
  BiasNotification.init({
    notificationName: DataTypes.STRING,
    description: DataTypes.TEXT,
    triggerType: DataTypes.STRING,
    triggerCondition: DataTypes.JSON,
    severityThreshold: DataTypes.FLOAT,
    metricType: DataTypes.STRING,
    comparisonOperator: DataTypes.STRING,
    recipients: DataTypes.JSON,
    notificationType: DataTypes.STRING,
    notificationTemplate: DataTypes.TEXT,
    isActive: DataTypes.BOOLEAN,
    lastTriggered: DataTypes.DATE,
    cooldownPeriod: DataTypes.INTEGER
  }, {
    sequelize,
    modelName: 'BiasNotification',
  });
  return BiasNotification;
};