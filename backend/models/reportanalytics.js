'use strict';
const {
  Model
} = require('sequelize');
module.exports = (sequelize, DataTypes) => {
  class ReportAnalytics extends Model {
    /**
     * Helper method for defining associations.
     * This method is not a part of Sequelize lifecycle.
     * The `models/index` file will call this method automatically.
     */
    static associate(models) {
      // define association here
    }
  }
  ReportAnalytics.init({
    reportId: DataTypes.UUID,
    userId: DataTypes.UUID,
    viewCount: DataTypes.INTEGER,
    downloadCount: DataTypes.INTEGER,
    lastViewed: DataTypes.DATE,
    deviceType: DataTypes.STRING,
    ipAddress: DataTypes.STRING,
    userAgent: DataTypes.STRING
  }, {
    sequelize,
    modelName: 'ReportAnalytics',
  });
  return ReportAnalytics;
};