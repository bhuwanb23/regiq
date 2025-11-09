module.exports = (sequelize, DataTypes) => {
  const RegulatoryDocument = sequelize.define('RegulatoryDocument', {
    id: {
      type: DataTypes.UUID,
      defaultValue: DataTypes.UUIDV4,
      primaryKey: true
    },
    title: {
      type: DataTypes.STRING,
      allowNull: false
    },
    content: {
      type: DataTypes.TEXT,
      allowNull: false
    },
    documentType: {
      type: DataTypes.STRING,
      allowNull: false,
      field: 'document_type'
    },
    source: {
      type: DataTypes.STRING,
      allowNull: true
    },
    jurisdiction: {
      type: DataTypes.STRING,
      allowNull: true
    },
    effectiveDate: {
      type: DataTypes.DATE,
      field: 'effective_date'
    },
    complianceScore: {
      type: DataTypes.FLOAT,
      field: 'compliance_score'
    },
    keyFindings: {
      type: DataTypes.JSON,
      field: 'key_findings'
    },
    riskFactors: {
      type: DataTypes.JSON,
      field: 'risk_factors'
    },
    recommendedActions: {
      type: DataTypes.JSON,
      field: 'recommended_actions'
    },
    tags: {
      type: DataTypes.JSON,
      defaultValue: []
    },
    status: {
      type: DataTypes.ENUM('pending', 'processed', 'archived'),
      defaultValue: 'pending'
    },
    fileSize: {
      type: DataTypes.INTEGER,
      field: 'file_size'
    },
    mimeType: {
      type: DataTypes.STRING,
      field: 'mime_type'
    },
    uploadedBy: {
      type: DataTypes.UUID,
      field: 'uploaded_by'
    },
    processedAt: {
      type: DataTypes.DATE,
      field: 'processed_at'
    }
  }, {
    tableName: 'regulatory_documents',
    timestamps: true,
    underscored: true
  });

  return RegulatoryDocument;
};