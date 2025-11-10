module.exports = (sequelize, DataTypes) => {
  const SearchIndex = sequelize.define('SearchIndex', {
    id: {
      type: DataTypes.UUID,
      defaultValue: DataTypes.UUIDV4,
      primaryKey: true
    },
    documentId: {
      type: DataTypes.INTEGER,
      allowNull: false,
      field: 'document_id'
    },
    title: {
      type: DataTypes.STRING,
      allowNull: false
    },
    content: {
      type: DataTypes.TEXT,
      allowNull: false
    },
    documentType: {
      type: DataTypes.STRING,
      allowNull: true,
      field: 'document_type'
    },
    jurisdiction: {
      type: DataTypes.STRING,
      allowNull: true
    },
    source: {
      type: DataTypes.STRING,
      allowNull: true
    },
    tags: {
      type: DataTypes.JSON,
      defaultValue: []
    }
  }, {
    tableName: 'search_indices',
    timestamps: true,
    underscored: true
  });

  SearchIndex.associate = (models) => {
    SearchIndex.belongsTo(models.RegulatoryDocument, {
      foreignKey: 'document_id',
      as: 'document'
    });
  };

  return SearchIndex;
};