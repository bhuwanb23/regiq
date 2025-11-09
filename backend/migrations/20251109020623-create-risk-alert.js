'use strict';
/** @type {import('sequelize-cli').Migration} */
module.exports = {
  async up(queryInterface, Sequelize) {
    await queryInterface.createTable('risk_alerts', {
      id: {
        type: Sequelize.UUID,
        defaultValue: Sequelize.UUIDV4,
        primaryKey: true,
        allowNull: false
      },
      alert_name: {
        type: Sequelize.STRING,
        allowNull: false
      },
      description: {
        type: Sequelize.TEXT
      },
      alert_type: {
        type: Sequelize.STRING,
        allowNull: false
      },
      severity: {
        type: Sequelize.ENUM('low', 'medium', 'high', 'critical'),
        defaultValue: 'medium'
      },
      threshold: {
        type: Sequelize.FLOAT
      },
      current_value: {
        type: Sequelize.FLOAT
      },
      triggered_at: {
        type: Sequelize.DATE
      },
      resolved_at: {
        type: Sequelize.DATE
      },
      is_active: {
        type: Sequelize.BOOLEAN,
        defaultValue: true
      },
      simulation_id: {
        type: Sequelize.UUID
      },
      scenario_id: {
        type: Sequelize.UUID
      },
      recipients: {
        type: Sequelize.JSON
      },
      metadata: {
        type: Sequelize.JSON
      },
      created_at: {
        allowNull: false,
        type: Sequelize.DATE
      },
      updated_at: {
        allowNull: false,
        type: Sequelize.DATE
      }
    });
  },
  async down(queryInterface, Sequelize) {
    await queryInterface.dropTable('risk_alerts');
  }
};