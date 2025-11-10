'use strict';
/** @type {import('sequelize-cli').Migration} */
module.exports = {
  async up(queryInterface, Sequelize) {
    // Create the search index table for full-text search capabilities
    await queryInterface.createTable('search_indices', {
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
        references: {
          model: 'RegulatoryDocuments',
          key: 'id'
        },
        onDelete: 'CASCADE'
      },
      title: {
        type: Sequelize.STRING,
        allowNull: false
      },
      content: {
        type: Sequelize.TEXT,
        allowNull: false
      },
      documentType: {
        type: Sequelize.STRING,
        allowNull: true,
        field: 'document_type'
      },
      jurisdiction: {
        type: Sequelize.STRING,
        allowNull: true
      },
      source: {
        type: Sequelize.STRING,
        allowNull: true
      },
      tags: {
        type: Sequelize.JSON,
        defaultValue: []
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

    // Create FTS (Full-Text Search) virtual table
    // Note: SQLite FTS5 syntax - this will be handled differently in production with PostgreSQL
    await queryInterface.sequelize.query(`
      CREATE VIRTUAL TABLE IF NOT EXISTS search_fts USING fts5(
        title, 
        content, 
        documentType, 
        jurisdiction, 
        source, 
        tags,
        content='search_indices',
        content_rowid='id'
      );
    `);

    // Create triggers to keep FTS table in sync with search_indices
    await queryInterface.sequelize.query(`
      CREATE TRIGGER IF NOT EXISTS search_indices_ai AFTER INSERT ON search_indices 
      BEGIN
        INSERT INTO search_fts(rowid, title, content, documentType, jurisdiction, source, tags) 
        VALUES (new.id, new.title, new.content, new.documentType, new.jurisdiction, new.source, new.tags);
      END;
    `);

    await queryInterface.sequelize.query(`
      CREATE TRIGGER IF NOT EXISTS search_indices_ad AFTER DELETE ON search_indices 
      BEGIN
        INSERT INTO search_fts(search_fts, rowid, title, content, documentType, jurisdiction, source, tags) 
        VALUES ('delete', old.id, old.title, old.content, old.documentType, old.jurisdiction, old.source, old.tags);
      END;
    `);

    await queryInterface.sequelize.query(`
      CREATE TRIGGER IF NOT EXISTS search_indices_au AFTER UPDATE ON search_indices 
      BEGIN
        INSERT INTO search_fts(search_fts, rowid, title, content, documentType, jurisdiction, source, tags) 
        VALUES ('delete', old.id, old.title, old.content, old.documentType, old.jurisdiction, old.source, old.tags);
        INSERT INTO search_fts(rowid, title, content, documentType, jurisdiction, source, tags) 
        VALUES (new.id, new.title, new.content, new.documentType, new.jurisdiction, new.source, new.tags);
      END;
    `);
  },

  async down(queryInterface, Sequelize) {
    // Drop triggers first
    await queryInterface.sequelize.query('DROP TRIGGER IF EXISTS search_indices_ai;');
    await queryInterface.sequelize.query('DROP TRIGGER IF EXISTS search_indices_ad;');
    await queryInterface.sequelize.query('DROP TRIGGER IF EXISTS search_indices_au;');
    
    // Drop FTS table
    await queryInterface.sequelize.query('DROP TABLE IF EXISTS search_fts;');
    
    // Drop main table
    await queryInterface.dropTable('search_indices');
  }
};