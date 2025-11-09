module.exports = (sequelize, DataTypes) => {
  const BiasResult = sequelize.define('BiasResult', {
    id: {
      type: DataTypes.UUID,
      defaultValue: DataTypes.UUIDV4,
      primaryKey: true
    },
    analysisId: {
      type: DataTypes.UUID,
      allowNull: false,
      field: 'analysis_id'
    },
    analysisType: {
      type: DataTypes.STRING,
      allowNull: false,
      field: 'analysis_type'
    },
    entityId: {
      type: DataTypes.UUID,
      allowNull: false,
      field: 'entity_id'
    },
    entityType: {
      type: DataTypes.STRING,
      allowNull: false,
      field: 'entity_type'
    },
    biasMetrics: {
      type: DataTypes.JSON,
      field: 'bias_metrics'
    },
    overallScore: {
      type: DataTypes.FLOAT,
      field: 'overall_score'
    },
    demographicParity: {
      type: DataTypes.FLOAT,
      field: 'demographic_parity'
    },
    equalOpportunity: {
      type: DataTypes.FLOAT,
      field: 'equal_opportunity'
    },
    disparateImpact: {
      type: DataTypes.FLOAT,
      field: 'disparate_impact'
    },
    statisticalParity: {
      type: DataTypes.FLOAT,
      field: 'statistical_parity'
    },
    consistency: {
      type: DataTypes.FLOAT
    },
    groupFairness: {
      type: DataTypes.JSON,
      field: 'group_fairness'
    },
    individualFairness: {
      type: DataTypes.JSON,
      field: 'individual_fairness'
    },
    biasCategories: {
      type: DataTypes.JSON,
      field: 'bias_categories'
    },
    confidenceInterval: {
      type: DataTypes.JSON,
      field: 'confidence_interval'
    },
    statisticalSignificance: {
      type: DataTypes.FLOAT,
      field: 'statistical_significance'
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
    tableName: 'bias_results',
    timestamps: true,
    underscored: true
  });

  return BiasResult;
};