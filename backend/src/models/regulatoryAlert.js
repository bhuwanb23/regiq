module.exports = (sequelize, DataTypes) => {
  const RegulatoryAlert = sequelize.define('RegulatoryAlert', {
    id: {
      type: DataTypes.UUID,
      defaultValue: DataTypes.UUIDV4,
      primaryKey: true
    },
    title: {
      type: DataTypes.STRING,
      allowNull: false
    },
    description: {
      type: DataTypes.TEXT
    },
    alertType: {
      type: DataTypes.STRING,
      allowNull: false,
      field: 'alert_type'
    },
    severity: {
      type: DataTypes.ENUM('low', 'medium', 'high', 'critical'),
      defaultValue: 'medium'
    },
    documentId: {
      type: DataTypes.UUID,
      field: 'document_id'
    },
    complianceResultId: {
      type: DataTypes.UUID,
      field: 'compliance_result_id'
    },
    assignedTo: {
      type: DataTypes.UUID,
      field: 'assigned_to'
    },
    status: {
      type: DataTypes.ENUM('new', 'acknowledged', 'resolved', 'dismissed'),
      defaultValue: 'new'
    },
    triggeredAt: {
      type: DataTypes.DATE,
      field: 'triggered_at'
    },
    resolvedAt: {
      type: DataTypes.DATE,
      field: 'resolved_at'
    }
  }, {
    tableName: 'regulatory_alerts',
    timestamps: true,
    underscored: true
  });

  return RegulatoryAlert;
};