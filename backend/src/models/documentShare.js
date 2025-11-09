module.exports = (sequelize, DataTypes) => {
  const DocumentShare = sequelize.define('DocumentShare', {
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
    sharedBy: {
      type: DataTypes.UUID,
      allowNull: false,
      field: 'shared_by'
    },
    sharedWith: {
      type: DataTypes.UUID,
      allowNull: false,
      field: 'shared_with'
    },
    permissionLevel: {
      type: DataTypes.ENUM('read', 'write', 'admin'),
      defaultValue: 'read',
      field: 'permission_level'
    },
    expiresAt: {
      type: DataTypes.DATE,
      field: 'expires_at'
    },
    isActive: {
      type: DataTypes.BOOLEAN,
      defaultValue: true,
      field: 'is_active'
    }
  }, {
    tableName: 'document_shares',
    timestamps: true,
    underscored: true
  });

  return DocumentShare;
};