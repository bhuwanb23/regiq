module.exports = (sequelize, DataTypes) => {
  const DataBiasDetection = sequelize.define('DataBiasDetection', {
    id: {
      type: DataTypes.UUID,
      defaultValue: DataTypes.UUIDV4,
      primaryKey: true
    },
    datasetId: {
      type: DataTypes.UUID,
      allowNull: false,
      field: 'dataset_id'
    },
    datasetName: {
      type: DataTypes.STRING,
      allowNull: false,
      field: 'dataset_name'
    },
    fileType: {
      type: DataTypes.STRING,
      field: 'file_type'
    },
    fileSize: {
      type: DataTypes.INTEGER,
      field: 'file_size'
    },
    rowCount: {
      type: DataTypes.INTEGER,
      field: 'row_count'
    },
    columnCount: {
      type: DataTypes.INTEGER,
      field: 'column_count'
    },
    protectedAttributes: {
      type: DataTypes.JSON,
      field: 'protected_attributes'
    },
    biasMetrics: {
      type: DataTypes.JSON,
      field: 'bias_metrics'
    },
    representationBias: {
      type: DataTypes.JSON,
      field: 'representation_bias'
    },
    measurementBias: {
      type: DataTypes.JSON,
      field: 'measurement_bias'
    },
    evaluationBias: {
      type: DataTypes.JSON,
      field: 'evaluation_bias'
    },
    historicalBias: {
      type: DataTypes.JSON,
      field: 'historical_bias'
    },
    aggregationBias: {
      type: DataTypes.JSON,
      field: 'aggregation_bias'
    },
    selectionBias: {
      type: DataTypes.JSON,
      field: 'selection_bias'
    },
    survivorshipBias: {
      type: DataTypes.JSON,
      field: 'survivorship_bias'
    },
    severityScore: {
      type: DataTypes.FLOAT,
      field: 'severity_score'
    },
    recommendations: {
      type: DataTypes.JSON
    },
    status: {
      type: DataTypes.ENUM('pending', 'in_progress', 'completed', 'failed'),
      defaultValue: 'pending'
    },
    analysisParameters: {
      type: DataTypes.JSON,
      field: 'analysis_parameters'
    },
    createdAt: {
      type: DataTypes.DATE,
      field: 'created_at'
    },
    updatedAt: {
      type: DataTypes.DATE,
      field: 'updated_at'
    }
  }, {
    tableName: 'data_bias_detections',
    timestamps: true,
    underscored: true
  });

  return DataBiasDetection;
};