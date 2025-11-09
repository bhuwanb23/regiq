module.exports = (sequelize, DataTypes) => {
  const ReportVersion = sequelize.define('ReportVersion', {
    id: {
      type: DataTypes.UUID,
      defaultValue: DataTypes.UUIDV4,
      primaryKey: true
    },
    reportId: {
      type: DataTypes.UUID,
      allowNull: false
    },
    versionNumber: {
      type: DataTypes.INTEGER,
      allowNull: false
    },
    title: {
      type: DataTypes.STRING,
      allowNull: false
    },
    content: {
      type: DataTypes.TEXT
    },
    createdBy: {
      type: DataTypes.UUID,
      allowNull: false
    },
    changeLog: {
      type: DataTypes.TEXT
    }
  }, {
    tableName: 'report_versions',
    timestamps: true,
    underscored: true
  });

  ReportVersion.associate = function(models) {
    // Associations can be defined here if needed
  };

  return ReportVersion;
};