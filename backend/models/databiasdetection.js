'use strict';
const {
  Model
} = require('sequelize');
module.exports = (sequelize, DataTypes) => {
  class DataBiasDetection extends Model {
    /**
     * Helper method for defining associations.
     * This method is not a part of Sequelize lifecycle.
     * The `models/index` file will call this method automatically.
     */
    static associate(models) {
      // define association here
    }
  }
  DataBiasDetection.init({
    datasetId: DataTypes.UUID,
    datasetName: DataTypes.STRING,
    fileType: DataTypes.STRING,
    fileSize: DataTypes.INTEGER,
    rowCount: DataTypes.INTEGER,
    columnCount: DataTypes.INTEGER,
    protectedAttributes: DataTypes.JSON,
    biasMetrics: DataTypes.JSON,
    representationBias: DataTypes.JSON,
    measurementBias: DataTypes.JSON,
    evaluationBias: DataTypes.JSON,
    historicalBias: DataTypes.JSON,
    aggregationBias: DataTypes.JSON,
    selectionBias: DataTypes.JSON,
    survivorshipBias: DataTypes.JSON,
    severityScore: DataTypes.FLOAT,
    recommendations: DataTypes.JSON,
    status: DataTypes.STRING,
    analysisParameters: DataTypes.JSON
  }, {
    sequelize,
    modelName: 'DataBiasDetection',
  });
  return DataBiasDetection;
};