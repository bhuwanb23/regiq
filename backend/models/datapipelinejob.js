'use strict';
const {
  Model
} = require('sequelize');
module.exports = (sequelize, DataTypes) => {
  class DataPipelineJob extends Model {
    /**
     * Helper method for defining associations.
     * This method is not a part of Sequelize lifecycle.
     * The `models/index` file will call this method automatically.
     */
    static associate(models) {
      // define association here
    }
  }
  DataPipelineJob.init({
    uploadId: DataTypes.UUID,
    fileName: DataTypes.STRING,
    fileFormat: DataTypes.STRING,
    fileSize: DataTypes.INTEGER,
    pipelineType: DataTypes.STRING,
    priority: DataTypes.STRING,
    configuration: DataTypes.JSON,
    status: DataTypes.STRING,
    progress: DataTypes.FLOAT,
    stage: DataTypes.STRING,
    estimatedCompletionTime: DataTypes.DATE,
    recordsProcessed: DataTypes.INTEGER,
    totalRecords: DataTypes.INTEGER,
    throughput: DataTypes.FLOAT
  }, {
    sequelize,
    modelName: 'DataPipelineJob',
  });
  return DataPipelineJob;
};