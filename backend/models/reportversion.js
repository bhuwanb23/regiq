'use strict';
const {
  Model
} = require('sequelize');
module.exports = (sequelize, DataTypes) => {
  class ReportVersion extends Model {
    /**
     * Helper method for defining associations.
     * This method is not a part of Sequelize lifecycle.
     * The `models/index` file will call this method automatically.
     */
    static associate(models) {
      // define association here
    }
  }
  ReportVersion.init({
    reportId: DataTypes.UUID,
    versionNumber: DataTypes.INTEGER,
    title: DataTypes.STRING,
    content: DataTypes.TEXT,
    createdBy: DataTypes.UUID,
    changeLog: DataTypes.TEXT
  }, {
    sequelize,
    modelName: 'ReportVersion',
  });
  return ReportVersion;
};