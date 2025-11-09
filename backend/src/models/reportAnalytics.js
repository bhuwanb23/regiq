module.exports = (sequelize, DataTypes) => {
  const ReportAnalytics = sequelize.define('ReportAnalytics', {
    id: {
      type: DataTypes.UUID,
      defaultValue: DataTypes.UUIDV4,
      primaryKey: true
    },
    reportId: {
      type: DataTypes.UUID,
      allowNull: false
    },
    userId: {
      type: DataTypes.UUID
    },
    viewCount: {
      type: DataTypes.INTEGER,
      defaultValue: 0
    },
    downloadCount: {
      type: DataTypes.INTEGER,
      defaultValue: 0
    },
    lastViewed: {
      type: DataTypes.DATE
    },
    deviceType: {
      type: DataTypes.STRING
    },
    ipAddress: {
      type: DataTypes.STRING
    },
    userAgent: {
      type: DataTypes.STRING
    }
  }, {
    tableName: 'report_analytics',
    timestamps: true,
    underscored: true
  });

  ReportAnalytics.associate = function(models) {
    // Associations can be defined here if needed
  };

  return ReportAnalytics;
};