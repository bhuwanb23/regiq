'use strict';
/** @type {import('sequelize-cli').Migration} */
module.exports = {
  async up(queryInterface, Sequelize) {
    // Add accessed_at column to search_cache table
    await queryInterface.addColumn('search_cache', 'accessed_at', {
      type: Sequelize.DATE,
      allowNull: true,
      defaultValue: Sequelize.literal('CURRENT_TIMESTAMP')
    });
    
    // Add index on accessed_at for LRU queries
    await queryInterface.addIndex('search_cache', ['accessed_at'], {
      name: 'idx_search_cache_accessed_at'
    });
  },

  async down(queryInterface, Sequelize) {
    // Remove index first
    await queryInterface.removeIndex('search_cache', 'idx_search_cache_accessed_at');
    
    // Remove accessed_at column
    await queryInterface.removeColumn('search_cache', 'accessed_at');
  }
};