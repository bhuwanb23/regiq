module.exports = (sequelize, DataTypes) => {
  const DataLineage = sequelize.define('DataLineage', {
    id: {
      type: DataTypes.UUID,
      defaultValue: DataTypes.UUIDV4,
      primaryKey: true
    },
    jobId: {
      type: DataTypes.UUID,
      allowNull: false,
      field: 'job_id'
    },
    sourceSystem: {
      type: DataTypes.STRING,
      allowNull: false,
      field: 'source_system'
    },
    targetSystem: {
      type: DataTypes.STRING,
      allowNull: false,
      field: 'target_system'
    },
    sourceTable: {
      type: DataTypes.STRING,
      field: 'source_table'
    },
    targetTable: {
      type: DataTypes.STRING,
      field: 'target_table'
    },
    sourceColumn: {
      type: DataTypes.STRING,
      field: 'source_column'
    },
    targetColumn: {
      type: DataTypes.STRING,
      field: 'target_column'
    },
    transformationType: {
      type: DataTypes.STRING,
      field: 'transformation_type'
    },
    transformationLogic: {
      type: DataTypes.TEXT,
      field: 'transformation_logic'
    },
    lineageType: {
      type: DataTypes.ENUM('etl', 'elt', 'streaming', 'batch'),
      allowNull: false,
      field: 'lineage_type'
    },
    status: {
      type: DataTypes.ENUM('active', 'inactive', 'deprecated'),
      defaultValue: 'active'
    },
    startTime: {
      type: DataTypes.DATE,
      field: 'start_time'
    },
    endTime: {
      type: DataTypes.DATE,
      field: 'end_time'
    },
    duration: {
      type: DataTypes.INTEGER
    },
    recordCount: {
      type: DataTypes.INTEGER,
      field: 'record_count'
    },
    errorCount: {
      type: DataTypes.INTEGER,
      field: 'error_count'
    }
  }, {
    tableName: 'data_lineage',
    timestamps: true,
    underscored: true
  });

  return DataLineage;
};