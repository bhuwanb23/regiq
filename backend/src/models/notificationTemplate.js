module.exports = (sequelize, DataTypes) => {
  const NotificationTemplate = sequelize.define('NotificationTemplate', {
    id: {
      type: DataTypes.UUID,
      defaultValue: DataTypes.UUIDV4,
      primaryKey: true
    },
    name: {
      type: DataTypes.STRING,
      allowNull: false,
      field: 'name'
    },
    type: {
      type: DataTypes.ENUM('EMAIL', 'PUSH', 'SMS', 'IN_APP'),
      allowNull: false,
      field: 'type'
    },
    subject: {
      type: DataTypes.STRING,
      allowNull: true,
      field: 'subject'
    },
    content: {
      type: DataTypes.TEXT,
      allowNull: false,
      field: 'content'
    },
    variables: {
      type: DataTypes.JSON,
      allowNull: true,
      field: 'variables'
    },
    isActive: {
      type: DataTypes.BOOLEAN,
      defaultValue: true,
      field: 'is_active'
    }
  }, {
    tableName: 'notification_templates',
    timestamps: true,
    underscored: true
  });

  return NotificationTemplate;
};