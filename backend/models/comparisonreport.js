'use strict';
const {
  Model
} = require('sequelize');
module.exports = (sequelize, DataTypes) => {
  class ComparisonReport extends Model {
    /**
     * Helper method for defining associations.
     * This method is not a part of Sequelize lifecycle.
     * The `models/index` file will call this method automatically.
     */
    static associate(models) {
      // define association here
    }
  }
  ComparisonReport.init({
    reportName: DataTypes.STRING,
    description: DataTypes.TEXT,
    modelsCompared: DataTypes.JSON,
    datasetsCompared: DataTypes.JSON,
    metricsCompared: DataTypes.JSON,
    comparisonType: DataTypes.STRING,
    timeRange: DataTypes.JSON,
    baselineModelId: DataTypes.UUID,
    comparisonResults: DataTypes.JSON,
    summary: DataTypes.JSON,
    recommendations: DataTypes.JSON,
    visualizationData: DataTypes.JSON,
    reportFormat: DataTypes.STRING,
    status: DataTypes.STRING,
    generatedBy: DataTypes.UUID
  }, {
    sequelize,
    modelName: 'ComparisonReport',
  });
  return ComparisonReport;
};