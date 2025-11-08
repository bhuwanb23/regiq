const { RegulatoryDocument } = require('../models');

class RegulatoryDocumentService {
  // Create a new regulatory document
  async createDocument(documentData) {
    try {
      const document = await RegulatoryDocument.create(documentData);
      return document;
    } catch (error) {
      throw new Error(`Error creating document: ${error.message}`);
    }
  }

  // Get all regulatory documents
  async getAllDocuments() {
    try {
      const documents = await RegulatoryDocument.findAll();
      return documents;
    } catch (error) {
      throw new Error(`Error fetching documents: ${error.message}`);
    }
  }

  // Get document by ID
  async getDocumentById(id) {
    try {
      const document = await RegulatoryDocument.findByPk(id);
      return document;
    } catch (error) {
      throw new Error(`Error fetching document: ${error.message}`);
    }
  }

  // Update document
  async updateDocument(id, documentData) {
    try {
      const document = await RegulatoryDocument.findByPk(id);
      if (!document) {
        throw new Error('Document not found');
      }

      await document.update(documentData);
      return document;
    } catch (error) {
      throw new Error(`Error updating document: ${error.message}`);
    }
  }

  // Delete document
  async deleteDocument(id) {
    try {
      const document = await RegulatoryDocument.findByPk(id);
      if (!document) {
        throw new Error('Document not found');
      }

      await document.destroy();
      return { message: 'Document deleted successfully' };
    } catch (error) {
      throw new Error(`Error deleting document: ${error.message}`);
    }
  }

  // Search documents by title or content
  async searchDocuments(query) {
    try {
      const documents = await RegulatoryDocument.findAll({
        where: {
          [sequelize.Op.or]: [
            { title: { [sequelize.Op.iLike]: `%${query}%` } },
            { content: { [sequelize.Op.iLike]: `%${query}%` } }
          ]
        }
      });
      return documents;
    } catch (error) {
      throw new Error(`Error searching documents: ${error.message}`);
    }
  }
}

module.exports = new RegulatoryDocumentService();