'use strict';
const {
  Model
} = require('sequelize');
module.exports = (sequelize, DataTypes) => {
  class RiskSimulation extends Model {
    /**
     * Helper method for defining associations.
     * This method is not a part of Sequelize lifecycle.
     * The `models/index` file will call this method automatically.
     */
    static associate(models) {
      // define association here
    }
  }
  RiskSimulation.init({
    name: DataTypes.STRING,
    description: DataTypes.TEXT,
    scenarioId: DataTypes.UUID,
    simulationType: DataTypes.STRING,
    iterations: DataTypes.INTEGER,
    timeHorizon: DataTypes.INTEGER,
    modelParameters: DataTypes.JSON,
    status: DataTypes.STRING,
    summaryStatistics: DataTypes.JSON,
    results: DataTypes.JSON
  }, {
    sequelize,
    modelName: 'RiskSimulation',
  });
  return RiskSimulation;
};