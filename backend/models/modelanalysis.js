'use strict';
const {
  Model
} = require('sequelize');
module.exports = (sequelize, DataTypes) => {
  class ModelAnalysis extends Model {
    /**
     * Helper method for defining associations.
     * This method is not a part of Sequelize lifecycle.
     * The `models/index` file will call this method automatically.
     */
    static associate(models) {
      // define association here
    }
  }
  ModelAnalysis.init({
    modelId: DataTypes.UUID,
    modelName: DataTypes.STRING,
    modelType: DataTypes.STRING,
    framework: DataTypes.STRING,
    version: DataTypes.STRING,
    targetVariable: DataTypes.STRING,
    protectedAttributes: DataTypes.JSON,
    trainingDataSize: DataTypes.INTEGER,
    performanceMetrics: DataTypes.JSON,
    demographicParityDifference: DataTypes.FLOAT,
    equalOpportunityDifference: DataTypes.FLOAT,
    disparateImpact: DataTypes.FLOAT,
    statisticalParityDifference: DataTypes.FLOAT,
    consistencyScore: DataTypes.FLOAT,
    featureImportanceBias: DataTypes.JSON,
    groupMetrics: DataTypes.JSON,
    status: DataTypes.STRING,
    analysisParameters: DataTypes.JSON
  }, {
    sequelize,
    modelName: 'ModelAnalysis',
  });
  return ModelAnalysis;
};