module.exports = (sequelize, DataTypes) => {
  const MitigationRecommendation = sequelize.define('MitigationRecommendation', {
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
    biasType: {
      type: DataTypes.STRING,
      allowNull: false,
      field: 'bias_type'
    },
    severity: {
      type: DataTypes.ENUM('low', 'medium', 'high', 'critical'),
      defaultValue: 'medium'
    },
    recommendationType: {
      type: DataTypes.STRING,
      allowNull: false,
      field: 'recommendation_type'
    },
    title: {
      type: DataTypes.STRING,
      allowNull: false
    },
    description: {
      type: DataTypes.TEXT
    },
    implementationSteps: {
      type: DataTypes.JSON,
      field: 'implementation_steps'
    },
    expectedImpact: {
      type: DataTypes.FLOAT,
      field: 'expected_impact'
    },
    confidenceScore: {
      type: DataTypes.FLOAT,
      field: 'confidence_score'
    },
    priority: {
      type: DataTypes.ENUM('low', 'normal', 'high', 'urgent'),
      defaultValue: 'normal'
    },
    applicability: {
      type: DataTypes.JSON
    },
    resources: {
      type: DataTypes.JSON
    },
    estimatedEffort: {
      type: DataTypes.STRING,
      field: 'estimated_effort'
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
    tableName: 'mitigation_recommendations',
    timestamps: true,
    underscored: true
  });

  return MitigationRecommendation;
};