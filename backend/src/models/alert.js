module.exports = (sequelize, DataTypes) => {
  const Alert = sequelize.define('Alert', {
    id: {
      type: DataTypes.UUID,
      defaultValue: DataTypes.UUIDV4,
      primaryKey: true
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
    title: {
      type: DataTypes.STRING,
      allowNull: false
    },
    description: {
      type: DataTypes.TEXT
    },
    relatedEntityId: {
      type: DataTypes.UUID,
      field: 'related_entity_id'
    },
    relatedEntityType: {
      type: DataTypes.STRING,
      field: 'related_entity_type'
    },
    isRead: {
      type: DataTypes.BOOLEAN,
      defaultValue: false,
      field: 'is_read'
    },
    triggeredBy: {
      type: DataTypes.UUID,
      field: 'triggered_by'
    }
  }, {
    tableName: 'alerts',
    timestamps: true,
    underscored: true
  });

  return Alert;
};