module.exports = (sequelize, DataTypes) => {
  const SearchAnalytics = sequelize.define('SearchAnalytics', {
    id: {
      type: DataTypes.UUID,
      defaultValue: DataTypes.UUIDV4,
      primaryKey: true
    },
    userId: {
      type: DataTypes.INTEGER,
      allowNull: true,
      field: 'user_id'
    },
    query: {
      type: DataTypes.TEXT,
      allowNull: false
    },
    filters: {
      type: DataTypes.JSON,
      defaultValue: {}
    },
    resultsCount: {
      type: DataTypes.INTEGER,
      allowNull: false,
      defaultValue: 0,
      field: 'results_count'
    },
    responseTime: {
      type: DataTypes.FLOAT,
      allowNull: false,
      defaultValue: 0,
      field: 'response_time'
    },
    timestamp: {
      type: DataTypes.DATE,
      allowNull: false,
      defaultValue: DataTypes.NOW
    },
    clickedResultId: {
      type: DataTypes.UUID,
      allowNull: true,
      field: 'clicked_result_id'
    },
    sessionId: {
      type: DataTypes.STRING,
      allowNull: true,
      field: 'session_id'
    },
    userAgent: {
      type: DataTypes.STRING,
      allowNull: true,
      field: 'user_agent'
    },
    ipAddress: {
      type: DataTypes.STRING,
      allowNull: true,
      field: 'ip_address'
    }
  }, {
    tableName: 'search_analytics',
    timestamps: false,
    underscored: true
  });

  SearchAnalytics.associate = (models) => {
    SearchAnalytics.belongsTo(models.User, {
      foreignKey: 'userId',
      as: 'user'
    });
  };

  return SearchAnalytics;
};