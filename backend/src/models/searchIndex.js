module.exports = (sequelize, DataTypes) => {
  const SearchIndex = sequelize.define('SearchIndex', {
    id: {
      type: DataTypes.UUID,
      defaultValue: DataTypes.UUIDV4,
      primaryKey: true
    },
    document_id: {
      type: DataTypes.INTEGER,
      allowNull: false
    },
    title: {
      type: DataTypes.STRING,
      allowNull: false
    },
    content: {
      type: DataTypes.TEXT,
      allowNull: false
    },
    document_type: {
      type: DataTypes.STRING,
      allowNull: true
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