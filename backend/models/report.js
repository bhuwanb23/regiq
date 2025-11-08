'use strict';
const {
  Model
} = require('sequelize');
module.exports = (sequelize, DataTypes) => {
  class Report extends Model {
    /**
     * Helper method for defining associations.
     * This method is not a part of Sequelize lifecycle.
     * The `models/index` file will call this method automatically.
     */
    static associate(models) {
      // define association here
    }
  }
  Report.init({
    reportType: DataTypes.STRING,
    title: DataTypes.STRING,
    content: DataTypes.JSON,
    templateId: DataTypes.UUID,
    parameters: DataTypes.JSON,
    status: DataTypes.STRING,
    format: DataTypes.STRING,
    downloadUrl: DataTypes.STRING
  }, {
    sequelize,
    modelName: 'Report',
  });
  return Report;
};