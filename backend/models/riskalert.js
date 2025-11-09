'use strict';
const {
  Model
} = require('sequelize');
module.exports = (sequelize, DataTypes) => {
  class RiskAlert extends Model {
    /**
     * Helper method for defining associations.
     * This method is not a part of Sequelize lifecycle.
     * The `models/index` file will call this method automatically.
     */
    static associate(models) {
      // define association here
    }
  }
  RiskAlert.init({
    alertName: DataTypes.STRING,
    description: DataTypes.TEXT,
    alertType: DataTypes.STRING,
    severity: DataTypes.STRING,
    threshold: DataTypes.FLOAT,
    currentValue: DataTypes.FLOAT,
    triggeredAt: DataTypes.DATE,
    resolvedAt: DataTypes.DATE,
    isActive: DataTypes.BOOLEAN,
    simulationId: DataTypes.UUID,
    scenarioId: DataTypes.UUID,
    recipients: DataTypes.JSON,
    metadata: DataTypes.JSON
  }, {
    sequelize,
    modelName: 'RiskAlert',
  });
  return RiskAlert;
};