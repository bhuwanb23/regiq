'use strict';
/** @type {import('sequelize-cli').Migration} */
module.exports = {
  async up(queryInterface, Sequelize) {
    await queryInterface.createTable('data_validation_rules', {
      id: {
        allowNull: false,
        primaryKey: true,
        type: Sequelize.UUID,
        defaultValue: Sequelize.UUIDV4
      },
      name: {
        type: Sequelize.STRING,
        allowNull: false
      },
      description: {
        type: Sequelize.TEXT
      },
      ruleType: {
        type: Sequelize.ENUM('format', 'range', 'presence', 'custom'),
        allowNull: false,
        field: 'rule_type'
      },
      fieldName: {
        type: Sequelize.STRING,
        allowNull: false,
        field: 'field_name'
      },
      dataType: {
        type: Sequelize.STRING,
        allowNull: false,
        field: 'data_type'
      },
      validationPattern: {
        type: Sequelize.STRING,
        field: 'validation_pattern'
      },
      minValue: {
        type: Sequelize.DECIMAL,
        field: 'min_value'
      },
      maxValue: {
        type: Sequelize.DECIMAL,
        field: 'max_value'
      },
      allowedValues: {
        type: Sequelize.JSON,
        field: 'allowed_values'
      },
      isActive: {
        type: Sequelize.BOOLEAN,
        defaultValue: true,
        field: 'is_active'
      },
      priority: {
        type: Sequelize.INTEGER
      },
      errorMessage: {
        type: Sequelize.TEXT,
        field: 'error_message'
      },
      createdBy: {
        type: Sequelize.UUID,
        allowNull: false,
        field: 'created_by'
      },
      createdAt: {
        allowNull: false,
        type: Sequelize.DATE,
        field: 'created_at'
      },
      updatedAt: {
        allowNull: false,
        type: Sequelize.DATE,
        field: 'updated_at'
      }
    });
  },
  async down(queryInterface, Sequelize) {
    await queryInterface.dropTable('data_validation_rules');
  }
};