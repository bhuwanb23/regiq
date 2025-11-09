module.exports = (sequelize, DataTypes) => {
  const DocumentMetadata = sequelize.define('DocumentMetadata', {
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
    category: {
      type: DataTypes.STRING
    },
    industry: {
      type: DataTypes.STRING
    },
    region: {
      type: DataTypes.STRING
    },
    regulatoryBody: {
      type: DataTypes.STRING,
      field: 'regulatory_body'
    },
    effectiveDate: {
      type: DataTypes.DATE,
      field: 'effective_date'
    },
    expirationDate: {
      type: DataTypes.DATE,
      field: 'expiration_date'
    },
    language: {
      type: DataTypes.STRING
    },
    keywords: {
      type: DataTypes.JSON
    },
    customFields: {
      type: DataTypes.JSON,
      field: 'custom_fields'
    }
  }, {
    tableName: 'document_metadata',
    timestamps: true,
    underscored: true
  });

  return DocumentMetadata;
};