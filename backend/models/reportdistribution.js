'use strict';
const {
  Model
} = require('sequelize');
module.exports = (sequelize, DataTypes) => {
  class ReportDistribution extends Model {
    /**
     * Helper method for defining associations.
     * This method is not a part of Sequelize lifecycle.
     * The `models/index` file will call this method automatically.
     */
    static associate(models) {
      // define association here
    }
  }
  ReportDistribution.init({
    reportId: DataTypes.UUID,
    distributionType: DataTypes.STRING,
    recipient: DataTypes.STRING,
    deliveryMethod: DataTypes.STRING,
    status: DataTypes.STRING,
    sentAt: DataTypes.DATE,
    deliveredAt: DataTypes.DATE,
    metadata: DataTypes.JSON
  }, {
    sequelize,
    modelName: 'ReportDistribution',
  });
  return ReportDistribution;
};