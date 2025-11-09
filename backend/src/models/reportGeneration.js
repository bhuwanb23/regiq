module.exports = (sequelize, DataTypes) => {
  const ReportGeneration = sequelize.define('ReportGeneration', {
    id: {
      type: DataTypes.UUID,
      defaultValue: DataTypes.UUIDV4,
      primaryKey: true
    },
    title: {
      type: DataTypes.STRING,
      allowNull: false
    },
    description: {
      type: DataTypes.TEXT
    },
    reportType: {
      type: DataTypes.STRING,
      allowNull: false
    },
    generatedBy: {
      type: DataTypes.UUID,
      allowNull: false
    },
    templateId: {
      type: DataTypes.UUID
    },
    content: {
      type: DataTypes.TEXT
    },
    format: {
      type: DataTypes.STRING,
      allowNull: false
    },
    fileSize: {
      type: DataTypes.INTEGER
    },
    filePath: {
      type: DataTypes.STRING
    },
    status: {
      type: DataTypes.STRING,
      defaultValue: 'pending'
    },
    metadata: {
      type: DataTypes.JSON
    }
  }, {
    tableName: 'report_generations',
    timestamps: true,
    underscored: true
  });

  ReportGeneration.associate = function(models) {
    // Associations can be defined here if needed
  };

  return ReportGeneration;
};