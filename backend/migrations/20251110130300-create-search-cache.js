'use strict';
/** @type {import('sequelize-cli').Migration} */
module.exports = {
  async up(queryInterface, Sequelize) {
    await queryInterface.createTable('search_cache', {
      id: {
        allowNull: false,
        primaryKey: true,
        type: Sequelize.UUID,
        defaultValue: Sequelize.UUIDV4
      },
      query_hash: {
        type: Sequelize.STRING,
        allowNull: false,
        unique: true
      },
      query: {
        type: Sequelize.JSON,
        allowNull: false
      },
      results: {
        type: Sequelize.JSON,
        allowNull: false
      },
      result_count: {
        type: Sequelize.INTEGER,
        allowNull: false
      },
      created_at: {
        allowNull: false,
        type: Sequelize.DATE
      },
      expires_at: {
        allowNull: false,
        type: Sequelize.DATE
      }
    });

    // Create indexes for better query performance
    // Note: Adding indexes after table creation to avoid issues
    // await queryInterface.addIndex('search_cache', ['query_hash']);
    // await queryInterface.addIndex('search_cache', ['expires_at']);
  },

  async down(queryInterface, Sequelize) {
    await queryInterface.dropTable('search_cache');
  }
};