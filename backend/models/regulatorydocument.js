'use strict';
const {
  Model
} = require('sequelize');
module.exports = (sequelize, DataTypes) => {
  class RegulatoryDocument extends Model {
    /**
     * Helper method for defining associations.
     * This method is not a part of Sequelize lifecycle.
     * The `models/index` file will call this method automatically.
     */
    static associate(models) {
      // define association here
    }
  }
  RegulatoryDocument.init({
    title: DataTypes.STRING,
    content: DataTypes.TEXT,
    documentType: DataTypes.STRING,
    source: DataTypes.STRING,
    jurisdiction: DataTypes.STRING,
    effectiveDate: DataTypes.DATE,
    complianceScore: DataTypes.FLOAT,
    keyFindings: DataTypes.JSON,
    riskFactors: DataTypes.JSON,
    recommendedActions: DataTypes.JSON,
    tags: DataTypes.JSON,
    status: DataTypes.STRING
  }, {
    sequelize,
    modelName: 'RegulatoryDocument',
  });
  return RegulatoryDocument;
};