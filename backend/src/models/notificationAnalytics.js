module.exports = (sequelize, DataTypes) => {
  const NotificationAnalytics = sequelize.define('NotificationAnalytics', {
    id: {
      type: DataTypes.UUID,
      defaultValue: DataTypes.UUIDV4,
      primaryKey: true
    },
    notificationId: {
      type: DataTypes.UUID,
      allowNull: false,
      field: 'notification_id'
    },
    userId: {
      type: DataTypes.UUID,
      allowNull: false,
      field: 'user_id'
    },
    deliveredAt: {
      type: DataTypes.DATE,
      allowNull: true,
      field: 'delivered_at'
    },
    openedAt: {
      type: DataTypes.DATE,
      allowNull: true,
      field: 'opened_at'
    },
    clickedAt: {
      type: DataTypes.DATE,
      allowNull: true,
      field: 'clicked_at'
    },
    deviceInfo: {
      type: DataTypes.JSON,
      allowNull: true,
      field: 'device_info'
    },
    ipAddress: {
      type: DataTypes.STRING,
      allowNull: true,
      field: 'ip_address'
    },
    userAgent: {
      type: DataTypes.STRING,
      allowNull: true,
      field: 'user_agent'
    }
  }, {
    tableName: 'notification_analytics',
    timestamps: true,
    underscored: true
  });

  return NotificationAnalytics;
};