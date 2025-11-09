'use strict';
/** @type {import('sequelize-cli').Migration} */
module.exports = {
  async up(queryInterface, Sequelize) {
    await queryInterface.createTable('risk_scenarios', {
      id: {
        type: Sequelize.UUID,
        defaultValue: Sequelize.UUIDV4,
        primaryKey: true,
        allowNull: false
      },
      name: {
        type: Sequelize.STRING,
        allowNull: false
      },
      description: {
        type: Sequelize.TEXT
      },
      scenario_type: {
        type: Sequelize.STRING,
        allowNull: false
      },
      parameters: {
        type: Sequelize.JSON
      },
      probability: {
        type: Sequelize.FLOAT,
        validate: {
          min: 0,
          max: 1
        }
      },
      impact: {
        type: Sequelize.FLOAT,
        validate: {
          min: 0,
          max: 100
        }
      },
      severity: {
        type: Sequelize.ENUM('low', 'medium', 'high', 'critical'),
        defaultValue: 'medium'
      },
      time_horizon: {
        type: Sequelize.INTEGER
      },
      jurisdiction: {
        type: Sequelize.STRING
      },
      is_active: {
        type: Sequelize.BOOLEAN,
        defaultValue: true
      },
      created_by: {
        type: Sequelize.UUID
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
    await queryInterface.dropTable('risk_scenarios');
  }
};