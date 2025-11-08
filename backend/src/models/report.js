module.exports = (sequelize, DataTypes) => {
  const Report = sequelize.define('Report', {
    id: {
      type: DataTypes.UUID,
      defaultValue: DataTypes.UUIDV4,
      primaryKey: true
    },
    reportType: {
      type: DataTypes.STRING,
      allowNull: false,
      field: 'report_type'
    },
    title: {
      type: DataTypes.STRING,
      allowNull: false
    },
    content: {
      type: DataTypes.JSON
    },
    templateId: {
      type: DataTypes.UUID,
      field: 'template_id'
    },
    parameters: {
      type: DataTypes.JSON
    },
    status: {
      type: DataTypes.ENUM('pending', 'in_progress', 'completed', 'failed'),
      defaultValue: 'pending'
    },
    format: {
      type: DataTypes.STRING,
      defaultValue: 'pdf'
    },
    downloadUrl: {
      type: DataTypes.STRING,
      field: 'download_url'
    }
  }, {
    tableName: 'reports',
    timestamps: true,
    underscored: true
  });

  return Report;
};