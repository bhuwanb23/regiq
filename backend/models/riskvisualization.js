'use strict';
const {
  Model
} = require('sequelize');
module.exports = (sequelize, DataTypes) => {
  class RiskVisualization extends Model {
    /**
     * Helper method for defining associations.
     * This method is not a part of Sequelize lifecycle.
     * The `models/index` file will call this method automatically.
     */
    static associate(models) {
      // define association here
    }
  }
  RiskVisualization.init({
    visualizationName: DataTypes.STRING,
    description: DataTypes.TEXT,
    visualizationType: DataTypes.STRING,
    dataType: DataTypes.STRING,
    data: DataTypes.JSON,
    xAxisLabel: DataTypes.STRING,
    yAxisLabel: DataTypes.STRING,
    chartTitle: DataTypes.STRING,
    simulationId: DataTypes.UUID,
    scenarioId: DataTypes.UUID,
    metadata: DataTypes.JSON
  }, {
    sequelize,
    modelName: 'RiskVisualization',
  });
  return RiskVisualization;
};