module.exports = (sequelize, DataTypes) => {
  const ReportDistribution = sequelize.define('ReportDistribution', {
    id: {
      type: DataTypes.UUID,
      defaultValue: DataTypes.UUIDV4,
      primaryKey: true
    },
    reportId: {
      type: DataTypes.UUID,
      allowNull: false
    },
    distributionType: {
      type: DataTypes.STRING,
      allowNull: false
    },
    recipient: {
      type: DataTypes.STRING,
      allowNull: false
    },
    deliveryMethod: {
      type: DataTypes.STRING,
      allowNull: false
    },
    status: {
      type: DataTypes.STRING,
      defaultValue: 'pending'
    },
    sentAt: {
      type: DataTypes.DATE
    },
    deliveredAt: {
      type: DataTypes.DATE
    },
    metadata: {
      type: DataTypes.JSON
    }
  }, {
    tableName: 'report_distributions',
    timestamps: true,
    underscored: true
  });

  ReportDistribution.associate = function(models) {
    // Associations can be defined here if needed
  };

  return ReportDistribution;
};