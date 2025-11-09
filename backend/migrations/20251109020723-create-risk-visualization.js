'use strict';
/** @type {import('sequelize-cli').Migration} */
module.exports = {
  async up(queryInterface, Sequelize) {
    await queryInterface.createTable('risk_visualizations', {
      id: {
        type: Sequelize.UUID,
        defaultValue: Sequelize.UUIDV4,
        primaryKey: true,
        allowNull: false
      },
      visualization_name: {
        type: Sequelize.STRING,
        allowNull: false
      },
      description: {
        type: Sequelize.TEXT
      },
      visualization_type: {
        type: Sequelize.STRING,
        allowNull: false
      },
      data_type: {
        type: Sequelize.STRING,
        allowNull: false
      },
      data: {
        type: Sequelize.JSON,
        allowNull: false
      },
      x_axis_label: {
        type: Sequelize.STRING
      },
      y_axis_label: {
        type: Sequelize.STRING
      },
      chart_title: {
        type: Sequelize.STRING
      },
      simulation_id: {
        type: Sequelize.UUID,
        allowNull: false
      },
      scenario_id: {
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
    await queryInterface.dropTable('risk_visualizations');
  }
};