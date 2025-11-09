module.exports = (sequelize, DataTypes) => {
  const ModelAnalysis = sequelize.define('ModelAnalysis', {
    id: {
      type: DataTypes.UUID,
      defaultValue: DataTypes.UUIDV4,
      primaryKey: true
    },
    modelId: {
      type: DataTypes.UUID,
      allowNull: false,
      field: 'model_id'
    },
    modelName: {
      type: DataTypes.STRING,
      allowNull: false,
      field: 'model_name'
    },
    modelType: {
      type: DataTypes.STRING,
      allowNull: false,
      field: 'model_type'
    },
    framework: {
      type: DataTypes.STRING,
      allowNull: false
    },
    version: {
      type: DataTypes.STRING,
      allowNull: false
    },
    targetVariable: {
      type: DataTypes.STRING,
      allowNull: false,
      field: 'target_variable'
    },
    protectedAttributes: {
      type: DataTypes.JSON,
      allowNull: false,
      field: 'protected_attributes'
    },
    trainingDataSize: {
      type: DataTypes.INTEGER,
      field: 'training_data_size'
    },
    performanceMetrics: {
      type: DataTypes.JSON,
      field: 'performance_metrics'
    },
    demographicParityDifference: {
      type: DataTypes.FLOAT,
      field: 'demographic_parity_difference'
    },
    equalOpportunityDifference: {
      type: DataTypes.FLOAT,
      field: 'equal_opportunity_difference'
    },
    disparateImpact: {
      type: DataTypes.FLOAT,
      field: 'disparate_impact'
    },
    statisticalParityDifference: {
      type: DataTypes.FLOAT,
      field: 'statistical_parity_difference'
    },
    consistencyScore: {
      type: DataTypes.FLOAT,
      field: 'consistency_score'
    },
    featureImportanceBias: {
      type: DataTypes.JSON,
      field: 'feature_importance_bias'
    },
    groupMetrics: {
      type: DataTypes.JSON,
      field: 'group_metrics'
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
    tableName: 'model_analyses',
    timestamps: true,
    underscored: true
  });

  return ModelAnalysis;
};