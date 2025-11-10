module.exports = (sequelize, DataTypes) => {
  const SearchFacets = sequelize.define('SearchFacets', {
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
    facetType: {
      type: DataTypes.STRING,
      allowNull: false,
      field: 'facet_type'
    },
    facetValue: {
      type: DataTypes.STRING,
      allowNull: false,
      field: 'facet_value'
    }
  }, {
    tableName: 'search_facets',
    timestamps: true,
    underscored: true
  });

  SearchFacets.associate = (models) => {
    SearchFacets.belongsTo(models.RegulatoryDocument, {
      foreignKey: 'document_id',
      as: 'document'
    });
  };

  return SearchFacets;
};