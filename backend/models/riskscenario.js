'use strict';
const {
  Model
} = require('sequelize');
module.exports = (sequelize, DataTypes) => {
  class RiskScenario extends Model {
    /**
     * Helper method for defining associations.
     * This method is not a part of Sequelize lifecycle.
     * The `models/index` file will call this method automatically.
     */
    static associate(models) {
      // define association here
    }
  }
  RiskScenario.init({
    name: DataTypes.STRING,
    description: DataTypes.TEXT,
    scenarioType: DataTypes.STRING,
    parameters: DataTypes.JSON,
    probability: DataTypes.FLOAT,
    impact: DataTypes.FLOAT,
    severity: DataTypes.STRING,
    timeHorizon: DataTypes.INTEGER,
    jurisdiction: DataTypes.STRING,
    isActive: DataTypes.BOOLEAN,
    createdBy: DataTypes.UUID,
    metadata: DataTypes.JSON
  }, {
    sequelize,
    modelName: 'RiskScenario',
  });
  return RiskScenario;
};