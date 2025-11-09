'use strict';
const {
  Model
} = require('sequelize');
module.exports = (sequelize, DataTypes) => {
  class MitigationRecommendation extends Model {
    /**
     * Helper method for defining associations.
     * This method is not a part of Sequelize lifecycle.
     * The `models/index` file will call this method automatically.
     */
    static associate(models) {
      // define association here
    }
  }
  MitigationRecommendation.init({
    analysisId: DataTypes.UUID,
    analysisType: DataTypes.STRING,
    biasType: DataTypes.STRING,
    severity: DataTypes.STRING,
    recommendationType: DataTypes.STRING,
    title: DataTypes.STRING,
    description: DataTypes.TEXT,
    implementationSteps: DataTypes.JSON,
    expectedImpact: DataTypes.FLOAT,
    confidenceScore: DataTypes.FLOAT,
    priority: DataTypes.STRING,
    applicability: DataTypes.JSON,
    resources: DataTypes.JSON,
    estimatedEffort: DataTypes.STRING
  }, {
    sequelize,
    modelName: 'MitigationRecommendation',
  });
  return MitigationRecommendation;
};