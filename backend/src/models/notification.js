module.exports = (sequelize, DataTypes) => {
  const Notification = sequelize.define('Notification', {
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
    type: {
      type: DataTypes.ENUM('EMAIL', 'PUSH', 'SMS', 'IN_APP'),
      allowNull: false,
      field: 'type'
    },
    title: {
      type: DataTypes.STRING,
      allowNull: false,
      field: 'title'
    },
    message: {
      type: DataTypes.TEXT,
      allowNull: false,
      field: 'message'
    },
    templateId: {
      type: DataTypes.UUID,
      allowNull: true,
      field: 'template_id'
    },
    status: {
      type: DataTypes.ENUM('PENDING', 'SENT', 'FAILED', 'READ'),
      defaultValue: 'PENDING',
      field: 'status'
    },
    priority: {
      type: DataTypes.ENUM('LOW', 'NORMAL', 'HIGH', 'URGENT'),
      defaultValue: 'NORMAL',
      field: 'priority'
    },
    scheduledAt: {
      type: DataTypes.DATE,
      allowNull: true,
      field: 'scheduled_at'
    },
    sentAt: {
      type: DataTypes.DATE,
      allowNull: true,
      field: 'sent_at'
    },
    readAt: {
      type: DataTypes.DATE,
      allowNull: true,
      field: 'read_at'
    },
    metadata: {
      type: DataTypes.JSON,
      allowNull: true,
      field: 'metadata'
    },
    channel: {
      type: DataTypes.STRING,
      allowNull: true,
      field: 'channel'
    }
  }, {
    tableName: 'notifications',
    timestamps: true,
    underscored: true
  });

  return Notification;
};