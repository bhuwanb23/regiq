module.exports = (sequelize, DataTypes) => {
  const ReportTemplate = sequelize.define('ReportTemplate', {
    id: {
      type: DataTypes.UUID,
      defaultValue: DataTypes.UUIDV4,
      primaryKey: true
    },
    name: {
      type: DataTypes.STRING,
      allowNull: false
    },
    description: {
      type: DataTypes.TEXT
    },
    templateType: {
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
    isActive: {
      type: DataTypes.BOOLEAN,
      defaultValue: true
    },
    metadata: {
      type: DataTypes.JSON
    }
  }, {
    tableName: 'report_templates',
    timestamps: true,
    underscored: true
  });

  ReportTemplate.associate = function(models) {
    // Associations can be defined here if needed
  };

  return ReportTemplate;
};