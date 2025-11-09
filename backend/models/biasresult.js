'use strict';
const {
  Model
} = require('sequelize');
module.exports = (sequelize, DataTypes) => {
  class BiasResult extends Model {
    /**
     * Helper method for defining associations.
     * This method is not a part of Sequelize lifecycle.
     * The `models/index` file will call this method automatically.
     */
    static associate(models) {
      // define association here
    }
  }
  BiasResult.init({
    analysisId: DataTypes.UUID,
    analysisType: DataTypes.STRING,
    entityId: DataTypes.UUID,
    entityType: DataTypes.STRING,
    biasMetrics: DataTypes.JSON,
    overallScore: DataTypes.FLOAT,
    demographicParity: DataTypes.FLOAT,
    equalOpportunity: DataTypes.FLOAT,
    disparateImpact: DataTypes.FLOAT,
    statisticalParity: DataTypes.FLOAT,
    consistency: DataTypes.FLOAT,
    groupFairness: DataTypes.JSON,
    individualFairness: DataTypes.JSON,
    biasCategories: DataTypes.JSON,
    confidenceInterval: DataTypes.JSON,
    statisticalSignificance: DataTypes.FLOAT
  }, {
    sequelize,
    modelName: 'BiasResult',
  });
  return BiasResult;
};