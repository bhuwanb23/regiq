module.exports = (sequelize, DataTypes) => {
  const NotificationPreference = sequelize.define('NotificationPreference', {
    id: {
      type: DataTypes.UUID,
      defaultValue: DataTypes.UUIDV4,
      primaryKey: true
    },
    userId: {
      type: DataTypes.UUID,
      allowNull: false,
      field: 'user_id'
    },
    notificationType: {
      type: DataTypes.STRING,
      allowNull: false,
      field: 'notification_type'
    },
    channel: {
      type: DataTypes.STRING,
      allowNull: false,
      field: 'channel'
    },
    isEnabled: {
      type: DataTypes.BOOLEAN,
      defaultValue: true,
      field: 'is_enabled'
    },
    schedule: {
      type: DataTypes.JSON,
      allowNull: true,
      field: 'schedule'
    }
  }, {
    tableName: 'notification_preferences',
    timestamps: true,
    underscored: true
  });

  return NotificationPreference;
};