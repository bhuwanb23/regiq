module.exports = (sequelize, DataTypes) => {
  const SearchCache = sequelize.define('SearchCache', {
    id: {
      type: DataTypes.UUID,
      defaultValue: DataTypes.UUIDV4,
      primaryKey: true
    },
    queryHash: {
      type: DataTypes.STRING,
      allowNull: false,
      unique: true,
      field: 'query_hash'
    },
    query: {
      type: DataTypes.JSON,
      allowNull: false
    },
    results: {
      type: DataTypes.JSON,
      allowNull: false
    },
    resultCount: {
      type: DataTypes.INTEGER,
      allowNull: false,
      field: 'result_count'
    },
    createdAt: {
      type: DataTypes.DATE,
      allowNull: false,
      field: 'created_at'
    },
    expiresAt: {
      type: DataTypes.DATE,
      allowNull: false,
      field: 'expires_at'
    }
  }, {
    tableName: 'search_cache',
    timestamps: false,
    underscored: true
  });

  return SearchCache;
};