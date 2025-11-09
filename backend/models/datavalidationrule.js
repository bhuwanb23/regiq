module.exports = (sequelize, DataTypes) => {
  const DataValidationRule = sequelize.define('DataValidationRule', {
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
    ruleType: {
      type: DataTypes.ENUM('format', 'range', 'presence', 'custom'),
      allowNull: false,
      field: 'rule_type'
    },
    fieldName: {
      type: DataTypes.STRING,
      allowNull: false,
      field: 'field_name'
    },
    dataType: {
      type: DataTypes.STRING,
      allowNull: false,
      field: 'data_type'
    },
    validationPattern: {
      type: DataTypes.STRING,
      field: 'validation_pattern'
    },
    minValue: {
      type: DataTypes.DECIMAL,
      field: 'min_value'
    },
    maxValue: {
      type: DataTypes.DECIMAL,
      field: 'max_value'
    },
    allowedValues: {
      type: DataTypes.JSON,
      field: 'allowed_values'
    },
    isActive: {
      type: DataTypes.BOOLEAN,
      defaultValue: true,
      field: 'is_active'
    },
    priority: {
      type: DataTypes.INTEGER,
      defaultValue: 0
    },
    errorMessage: {
      type: DataTypes.TEXT,
      field: 'error_message'
    },
    createdBy: {
      type: DataTypes.UUID,
      field: 'created_by'
    }
  }, {
    tableName: 'data_validation_rules',
    timestamps: true,
    underscored: true
  });

  return DataValidationRule;
};