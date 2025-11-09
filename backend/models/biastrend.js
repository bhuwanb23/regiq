'use strict';
const {
  Model
} = require('sequelize');
module.exports = (sequelize, DataTypes) => {
  class BiasTrend extends Model {
    /**
     * Helper method for defining associations.
     * This method is not a part of Sequelize lifecycle.
     * The `models/index` file will call this method automatically.
     */
    static associate(models) {
      // define association here
    }
  }
  BiasTrend.init({
    modelId: DataTypes.UUID,
    modelName: DataTypes.STRING,
    metricType: DataTypes.STRING,
    metricValue: DataTypes.FLOAT,
    threshold: DataTypes.FLOAT,
    trendDirection: DataTypes.STRING,
    significance: DataTypes.FLOAT,
    timePeriod: DataTypes.STRING,
    periodStart: DataTypes.DATE,
    periodEnd: DataTypes.DATE,
    comparisonBaseline: DataTypes.FLOAT,
    variance: DataTypes.FLOAT,
    alertTriggered: DataTypes.BOOLEAN,
    alertSeverity: DataTypes.STRING
  }, {
    sequelize,
    modelName: 'BiasTrend',
  });
  return BiasTrend;
};