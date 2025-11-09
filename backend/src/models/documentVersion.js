module.exports = (sequelize, DataTypes) => {
  const DocumentVersion = sequelize.define('DocumentVersion', {
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
    versionNumber: {
      type: DataTypes.INTEGER,
      allowNull: false,
      field: 'version_number'
    },
    title: {
      type: DataTypes.STRING,
      allowNull: false
    },
    content: {
      type: DataTypes.TEXT,
      allowNull: false
    },
    changes: {
      type: DataTypes.JSON
    },
    createdBy: {
      type: DataTypes.UUID,
      field: 'created_by'
    },
    createdAt: {
      type: DataTypes.DATE,
      field: 'created_at'
    }
  }, {
    tableName: 'document_versions',
    timestamps: false,
    underscored: true
  });

  return DocumentVersion;
};