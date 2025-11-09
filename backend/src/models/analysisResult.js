module.exports = (sequelize, DataTypes) => {
  const AnalysisResult = sequelize.define('AnalysisResult', {
    id: {
      type: DataTypes.UUID,
      defaultValue: DataTypes.UUIDV4,
      primaryKey: true
    },
    documentId: {
      type: DataTypes.UUID,
      allowNull: false,
      field: 'document_id'
    },
    analysisType: {
      type: DataTypes.STRING,
      allowNull: false,
      field: 'analysis_type'
    },
    results: {
      type: DataTypes.JSON
    },
    summary: {
      type: DataTypes.TEXT
    },
    confidenceScore: {
      type: DataTypes.FLOAT,
      field: 'confidence_score'
    },
    performedBy: {
      type: DataTypes.UUID,
      field: 'performed_by'
    },
    performedAt: {
      type: DataTypes.DATE,
      field: 'performed_at'
    },
    status: {
      type: DataTypes.ENUM('pending', 'completed', 'failed'),
      defaultValue: 'pending'
    }
  }, {
    tableName: 'analysis_results',
    timestamps: true,
    underscored: true
  });

  return AnalysisResult;
};