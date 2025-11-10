'use strict';
/** @type {import('sequelize-cli').Migration} */
module.exports = {
  async up(queryInterface, Sequelize) {
    await queryInterface.createTable('search_analytics', {
      id: {
        allowNull: false,
        primaryKey: true,
        type: Sequelize.UUID,
        defaultValue: Sequelize.UUIDV4
      },
      userId: {
        type: Sequelize.INTEGER,
        allowNull: true,
        field: 'user_id'
      },
      query: {
        type: Sequelize.TEXT,
        allowNull: false
      },
      filters: {
        type: Sequelize.JSON,
        defaultValue: {}
      },
      resultsCount: {
        type: Sequelize.INTEGER,
        allowNull: false,
        defaultValue: 0,
        field: 'results_count'
      },
      responseTime: {
        type: Sequelize.FLOAT,
        allowNull: false,
        defaultValue: 0,
        field: 'response_time'
      },
      timestamp: {
        allowNull: false,
        type: Sequelize.DATE,
        defaultValue: Sequelize.NOW
      },
      clickedResultId: {
        type: Sequelize.UUID,
        allowNull: true,
        field: 'clicked_result_id'
      },
      sessionId: {
        type: Sequelize.STRING,
        allowNull: true,
        field: 'session_id'
      },
      userAgent: {
        type: Sequelize.STRING,
        allowNull: true,
        field: 'user_agent'
      },
      ipAddress: {
        type: Sequelize.STRING,
        allowNull: true,
        field: 'ip_address'
      }
    });

    // Create indexes for better query performance
    // Note: Adding indexes after table creation to avoid issues
    // await queryInterface.addIndex('search_analytics', ['userId']);
    // await queryInterface.addIndex('search_analytics', ['timestamp']);
    // await queryInterface.addIndex('search_analytics', ['query']);
    // await queryInterface.addIndex('search_analytics', ['sessionId']);
  },

  async down(queryInterface, Sequelize) {
    await queryInterface.dropTable('search_analytics');
  }
};