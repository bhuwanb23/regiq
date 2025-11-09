'use strict';
const {
  Model
} = require('sequelize');
module.exports = (sequelize, DataTypes) => {
  class ReportGeneration extends Model {
    /**
     * Helper method for defining associations.
     * This method is not a part of Sequelize lifecycle.
     * The `models/index` file will call this method automatically.
     */
    static associate(models) {
      // define association here
    }
  }
  ReportGeneration.init({
    title: DataTypes.STRING,
    description: DataTypes.TEXT,
    reportType: DataTypes.STRING,
    generatedBy: DataTypes.UUID,
    templateId: DataTypes.UUID,
    content: DataTypes.TEXT,
    format: DataTypes.STRING,
    fileSize: DataTypes.INTEGER,
    filePath: DataTypes.STRING,
    status: DataTypes.STRING,
    metadata: DataTypes.JSON
  }, {
    sequelize,
    modelName: 'ReportGeneration',
  });
  return ReportGeneration;
};