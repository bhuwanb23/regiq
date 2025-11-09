module.exports = (sequelize, DataTypes) => {
  const ComplianceResult = sequelize.define('ComplianceResult', {
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
    complianceScore: {
      type: DataTypes.FLOAT,
      allowNull: false,
      field: 'compliance_score'
    },
    findings: {
      type: DataTypes.JSON
    },
    recommendations: {
      type: DataTypes.JSON
    },
    riskLevel: {
      type: DataTypes.ENUM('low', 'medium', 'high', 'critical'),
      field: 'risk_level'
    },
    checkedBy: {
      type: DataTypes.UUID,
      field: 'checked_by'
    },
    checkedAt: {
      type: DataTypes.DATE,
      field: 'checked_at'
    },
    status: {
      type: DataTypes.ENUM('pending', 'completed', 'failed'),
      defaultValue: 'pending'
    }
  }, {
    tableName: 'compliance_results',
    timestamps: true,
    underscored: true
  });

  return ComplianceResult;
};