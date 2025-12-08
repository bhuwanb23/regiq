'use strict';
/** @type {import('sequelize-cli').Migration} */
module.exports = {
    async up(queryInterface, Sequelize) {
        // Add indexes to improve search performance
        await queryInterface.addIndex('search_indices', ['jurisdiction'], {
            name: 'idx_search_jurisdiction'
        });

        await queryInterface.addIndex('search_indices', ['document_type'], {
            name: 'idx_search_document_type'
        });

        await queryInterface.addIndex('search_indices', ['created_at'], {
            name: 'idx_search_created_at'
        });

        await queryInterface.addIndex('search_indices', ['document_id'], {
            name: 'idx_search_document_id'
        });

        // Add composite indexes for common filter combinations
        await queryInterface.addIndex('search_indices', ['jurisdiction', 'document_type'], {
            name: 'idx_search_jurisdiction_doc_type'
        });

        await queryInterface.addIndex('search_indices', ['jurisdiction', 'created_at'], {
            name: 'idx_search_jurisdiction_created_at'
        });

        await queryInterface.addIndex('search_indices', ['document_type', 'created_at'], {
            name: 'idx_search_doc_type_created_at'
        });
    },

    async down(queryInterface, Sequelize) {
        // Remove indexes
        await queryInterface.removeIndex('search_indices', 'idx_search_jurisdiction');
        await queryInterface.removeIndex('search_indices', 'idx_search_document_type');
        await queryInterface.removeIndex('search_indices', 'idx_search_created_at');
        await queryInterface.removeIndex('search_indices', 'idx_search_document_id');
        await queryInterface.removeIndex('search_indices', 'idx_search_jurisdiction_doc_type');
        await queryInterface.removeIndex('search_indices', 'idx_search_jurisdiction_created_at');
        await queryInterface.removeIndex('search_indices', 'idx_search_doc_type_created_at');
    }
};