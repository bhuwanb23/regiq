const { 
  RegulatoryDocument, 
  ComplianceResult, 
  RegulatoryAlert, 
  DocumentVersion, 
  DocumentMetadata, 
  DocumentShare, 
  AnalysisResult 
} = require('../models');

const { Sequelize } = require('sequelize');
const sequelize = require('../config/database');

class RegulatoryService {
  /**
   * New regulatory intelligence endpoints
   */
  async getRegulations(filters = {}) {
    try {
      const whereClause = {};
      const orderClause = [['createdAt', 'DESC']];
      
      // Apply filters
      if (filters.jurisdiction) {
        whereClause.jurisdiction = filters.jurisdiction;
      }
      
      if (filters.documentType) {
        whereClause.documentType = filters.documentType;
      }
      
      if (filters.status) {
        whereClause.status = filters.status;
      }
      
      if (filters.category) {
        whereClause.tags = {
          [Sequelize.Op.contains]: [filters.category]
        };
      }
      
      // Pagination
      const page = parseInt(filters.page) || 1;
      const limit = parseInt(filters.limit) || 20;
      const offset = (page - 1) * limit;
      
      const { count, rows } = await RegulatoryDocument.findAndCountAll({
        where: whereClause,
        order: orderClause,
        limit,
        offset
      });
      
      return {
        regulations: rows,
        pagination: {
          page,
          limit,
          totalCount: count,
          totalPages: Math.ceil(count / limit)
        }
      };
    } catch (error) {
      throw new Error(`Failed to get regulations: ${error.message}`);
    }
  }

  async getRegulationById(id) {
    try {
      const regulation = await RegulatoryDocument.findByPk(id);
      if (!regulation) {
        throw new Error('Regulation not found');
      }
      return regulation;
    } catch (error) {
      throw new Error(`Failed to get regulation: ${error.message}`);
    }
  }

  async searchRegulations(filters = {}) {
    try {
      const whereClause = {};
      
      // Text search - use case-insensitive LIKE for SQLite
      if (filters.q) {
        whereClause[Sequelize.Op.or] = [
          { title: { [Sequelize.Op.like]: `%${filters.q}%` } },
          { content: { [Sequelize.Op.like]: `%${filters.q}%` } }
        ];
      }
      
      // Apply other filters
      if (filters.jurisdiction) {
        whereClause.jurisdiction = filters.jurisdiction;
      }
      
      if (filters.documentType) {
        whereClause.documentType = filters.documentType;
      }
      
      if (filters.category) {
        whereClause.tags = {
          [Sequelize.Op.contains]: [filters.category]
        };
      }
      
      // Date range filtering
      if (filters.dateFrom || filters.dateTo) {
        whereClause.effectiveDate = {};
        if (filters.dateFrom) {
          whereClause.effectiveDate[Sequelize.Op.gte] = new Date(filters.dateFrom);
        }
        if (filters.dateTo) {
          whereClause.effectiveDate[Sequelize.Op.lte] = new Date(filters.dateTo);
        }
      }
      
      // Pagination
      const page = parseInt(filters.page) || 1;
      const limit = parseInt(filters.limit) || 20;
      const offset = (page - 1) * limit;
      
      const { count, rows } = await RegulatoryDocument.findAndCountAll({
        where: whereClause,
        order: [['effectiveDate', 'DESC']],
        limit,
        offset
      });
      
      return {
        results: rows,
        pagination: {
          page,
          limit,
          totalCount: count,
          totalPages: Math.ceil(count / limit)
        }
      };
    } catch (error) {
      throw new Error(`Failed to search regulations: ${error.message}`);
    }
  }

  async getRegulationCategories() {
    try {
      // Get all unique tags from regulatory documents
      const categories = await RegulatoryDocument.aggregate('tags', 'DISTINCT', {
        plain: false
      });
      
      // Flatten the array of arrays
      const flatCategories = categories.reduce((acc, curr) => {
        if (Array.isArray(curr.DISTINCT)) {
          return acc.concat(curr.DISTINCT);
        }
        return acc;
      }, []);
      
      // Get unique categories
      const uniqueCategories = [...new Set(flatCategories)];
      
      return uniqueCategories;
    } catch (error) {
      throw new Error(`Failed to get regulation categories: ${error.message}`);
    }
  }

  async getUpcomingDeadlines(filters = {}) {
    try {
      const whereClause = {
        effectiveDate: {
          [Sequelize.Op.gte]: new Date(),
          [Sequelize.Op.lte]: new Date(Date.now() + 90 * 24 * 60 * 60 * 1000) // Next 90 days
        }
      };
      
      // Apply filters
      if (filters.jurisdiction) {
        whereClause.jurisdiction = filters.jurisdiction;
      }
      
      if (filters.documentType) {
        whereClause.documentType = filters.documentType;
      }
      
      // Pagination
      const page = parseInt(filters.page) || 1;
      const limit = parseInt(filters.limit) || 20;
      const offset = (page - 1) * limit;
      
      const { count, rows } = await RegulatoryDocument.findAndCountAll({
        where: whereClause,
        order: [['effectiveDate', 'ASC']],
        limit,
        offset
      });
      
      return {
        deadlines: rows,
        pagination: {
          page,
          limit,
          totalCount: count,
          totalPages: Math.ceil(count / limit)
        }
      };
    } catch (error) {
      throw new Error(`Failed to get upcoming deadlines: ${error.message}`);
    }
  }

  /**
   * Document upload and processing
   */
  async uploadDocument(documentData, userId) {
    try {
      const document = await RegulatoryDocument.create({
        ...documentData,
        uploadedBy: userId
      });
      return document;
    } catch (error) {
      throw new Error(`Failed to upload document: ${error.message}`);
    }
  }

  async processDocument(documentId) {
    try {
      const document = await RegulatoryDocument.findByPk(documentId);
      if (!document) {
        throw new Error('Document not found');
      }

      // Simulate document processing
      await document.update({
        status: 'processed',
        processedAt: new Date()
      });

      return document;
    } catch (error) {
      throw new Error(`Failed to process document: ${error.message}`);
    }
  }

  async getDocumentProcessingStatus(documentId) {
    try {
      const document = await RegulatoryDocument.findByPk(documentId, {
        attributes: ['id', 'status', 'processedAt']
      });
      if (!document) {
        throw new Error('Document not found');
      }
      return document;
    } catch (error) {
      throw new Error(`Failed to get document status: ${error.message}`);
    }
  }

  /**
   * Regulatory document search and filtering
   */
  async searchDocuments(filters = {}) {
    try {
      const whereClause = {};
      
      if (filters.title) {
        whereClause.title = {
          [Sequelize.Op.like]: `%${filters.title}%`
        };
      }
      
      if (filters.documentType) {
        whereClause.documentType = filters.documentType;
      }
      
      if (filters.jurisdiction) {
        whereClause.jurisdiction = filters.jurisdiction;
      }
      
      if (filters.tags && filters.tags.length > 0) {
        whereClause.tags = {
          [Sequelize.Op.contains]: filters.tags
        };
      }
      
      const documents = await RegulatoryDocument.findAll({
        where: whereClause,
        order: [['createdAt', 'DESC']],
        limit: filters.limit || 50
      });
      
      return documents;
    } catch (error) {
      throw new Error(`Failed to search documents: ${error.message}`);
    }
  }

  async getDocumentById(documentId) {
    try {
      const document = await RegulatoryDocument.findByPk(documentId);
      if (!document) {
        throw new Error('Document not found');
      }
      return document;
    } catch (error) {
      throw new Error(`Failed to get document: ${error.message}`);
    }
  }

  /**
   * Compliance checking
   */
  async checkCompliance(documentId, userId) {
    try {
      const document = await RegulatoryDocument.findByPk(documentId);
      if (!document) {
        throw new Error('Document not found');
      }

      // Simulate compliance checking
      const complianceScore = Math.random() * 100;
      const riskLevel = complianceScore > 80 ? 'low' : complianceScore > 60 ? 'medium' : complianceScore > 40 ? 'high' : 'critical';

      const result = await ComplianceResult.create({
        documentId,
        complianceScore,
        riskLevel,
        checkedBy: userId,
        checkedAt: new Date(),
        status: 'completed'
      });

      return result;
    } catch (error) {
      throw new Error(`Failed to check compliance: ${error.message}`);
    }
  }

  async getComplianceResult(resultId) {
    try {
      const result = await ComplianceResult.findByPk(resultId);
      if (!result) {
        throw new Error('Compliance result not found');
      }
      return result;
    } catch (error) {
      throw new Error(`Failed to get compliance result: ${error.message}`);
    }
  }

  /**
   * Regulatory alert generation
   */
  async createAlert(alertData, userId) {
    try {
      const alert = await RegulatoryAlert.create({
        ...alertData,
        assignedTo: userId,
        triggeredAt: new Date()
      });
      return alert;
    } catch (error) {
      throw new Error(`Failed to create alert: ${error.message}`);
    }
  }

  async getAlerts(filters = {}) {
    try {
      const whereClause = {};
      
      if (filters.status) {
        whereClause.status = filters.status;
      }
      
      if (filters.severity) {
        whereClause.severity = filters.severity;
      }
      
      if (filters.assignedTo) {
        whereClause.assignedTo = filters.assignedTo;
      }
      
      const alerts = await RegulatoryAlert.findAll({
        where: whereClause,
        order: [['triggeredAt', 'DESC']],
        limit: filters.limit || 50
      });
      
      return alerts;
    } catch (error) {
      throw new Error(`Failed to get alerts: ${error.message}`);
    }
  }

  async updateAlertStatus(alertId, status, userId) {
    try {
      const alert = await RegulatoryAlert.findByPk(alertId);
      if (!alert) {
        throw new Error('Alert not found');
      }
      
      await alert.update({
        status,
        updatedAt: new Date()
      });
      
      return alert;
    } catch (error) {
      throw new Error(`Failed to update alert status: ${error.message}`);
    }
  }

  /**
   * Document versioning
   */
  async createDocumentVersion(documentId, versionData, userId) {
    try {
      const version = await DocumentVersion.create({
        documentId,
        ...versionData,
        createdBy: userId,
        createdAt: new Date()
      });
      return version;
    } catch (error) {
      throw new Error(`Failed to create document version: ${error.message}`);
    }
  }

  async getDocumentVersions(documentId) {
    try {
      const versions = await DocumentVersion.findAll({
        where: { documentId },
        order: [['createdAt', 'DESC']]
      });
      return versions;
    } catch (error) {
      throw new Error(`Failed to get document versions: ${error.message}`);
    }
  }

  /**
   * Document metadata management
   */
  async updateDocumentMetadata(documentId, metadata) {
    try {
      const docMetadata = await DocumentMetadata.findOne({
        where: { documentId }
      });
      
      if (docMetadata) {
        await docMetadata.update(metadata);
        return docMetadata;
      } else {
        const newMetadata = await DocumentMetadata.create({
          documentId,
          ...metadata
        });
        return newMetadata;
      }
    } catch (error) {
      throw new Error(`Failed to update document metadata: ${error.message}`);
    }
  }

  async getDocumentMetadata(documentId) {
    try {
      const metadata = await DocumentMetadata.findOne({
        where: { documentId }
      });
      if (!metadata) {
        throw new Error('Document metadata not found');
      }
      return metadata;
    } catch (error) {
      throw new Error(`Failed to get document metadata: ${error.message}`);
    }
  }

  /**
   * Document sharing
   */
  async shareDocument(documentId, sharedWith, permissionLevel, userId) {
    try {
      const share = await DocumentShare.create({
        documentId,
        sharedWith,
        permissionLevel,
        sharedBy: userId,
        sharedAt: new Date()
      });
      return share;
    } catch (error) {
      throw new Error(`Failed to share document: ${error.message}`);
    }
  }

  async getSharedDocuments(userId) {
    try {
      const shares = await DocumentShare.findAll({
        where: { sharedWith: userId },
        include: [{
          model: RegulatoryDocument,
          as: 'document'
        }]
      });
      return shares;
    } catch (error) {
      throw new Error(`Failed to get shared documents: ${error.message}`);
    }
  }

  /**
   * Analysis result storage
   */
  async storeAnalysisResult(resultData, userId) {
    try {
      const result = await AnalysisResult.create({
        ...resultData,
        analyzedBy: userId,
        analyzedAt: new Date()
      });
      return result;
    } catch (error) {
      throw new Error(`Failed to store analysis result: ${error.message}`);
    }
  }

  async getAnalysisResult(resultId) {
    try {
      const result = await AnalysisResult.findByPk(resultId);
      if (!result) {
        throw new Error('Analysis result not found');
      }
      return result;
    } catch (error) {
      throw new Error(`Failed to get analysis result: ${error.message}`);
    }
  }

  async getDocumentAnalysisResults(documentId) {
    try {
      const results = await AnalysisResult.findAll({
        where: { documentId },
        order: [['analyzedAt', 'DESC']]
      });
      return results;
    } catch (error) {
      throw new Error(`Failed to get document analysis results: ${error.message}`);
    }
  }
}

module.exports = new RegulatoryService();