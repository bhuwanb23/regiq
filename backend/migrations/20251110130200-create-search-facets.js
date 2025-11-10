'use strict';
/** @type {import('sequelize-cli').Migration} */
module.exports = {
  async up(queryInterface, Sequelize) {
    await queryInterface.createTable('search_facets', {
      id: {
        allowNull: false,
        primaryKey: true,
        type: Sequelize.UUID,
        defaultValue: Sequelize.UUIDV4
      },
      documentId: {
        type: Sequelize.INTEGER,
        allowNull: false,
        field: 'document_id',
        // references: {
        //   model: 'RegulatoryDocuments',
        //   key: 'id'
        // },
        onDelete: 'CASCADE'
      },
      facetType: {
        type: Sequelize.STRING,
        allowNull: false,
        field: 'facet_type'
      },
      facetValue: {
        type: Sequelize.STRING,
        allowNull: false,
        field: 'facet_value'
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

    // Create indexes for better query performance
    // Note: Adding indexes after table creation to avoid issues
    // await queryInterface.addIndex('search_facets', ['documentId']);
    // await queryInterface.addIndex('search_facets', ['facetType']);
    // await queryInterface.addIndex('search_facets', ['facetValue']);
    // await queryInterface.addIndex('search_facets', ['facetType', 'facetValue']);
  },

  async down(queryInterface, Sequelize) {
    await queryInterface.dropTable('search_facets');
  }
};