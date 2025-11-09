const { 
  RegulatoryDocument, 
  ComplianceResult, 
  RegulatoryAlert, 
  DocumentVersion, 
  DocumentMetadata, 
  DocumentShare, 
  AnalysisResult 
} = require('../models');

class RegulatoryService {
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
          [sequelize.Op.iLike]: `%${filters.title}%`
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
          [sequelize.Op.contains]: filters.tags
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

      const updateData = { status };
      if (status === 'resolved') {
        updateData.resolvedAt = new Date();
        updateData.assignedTo = userId;
      }

      await alert.update(updateData);
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
      const document = await RegulatoryDocument.findByPk(documentId);
      if (!document) {
        throw new Error('Document not found');
      }

      // Get the latest version number
      const latestVersion = await DocumentVersion.findOne({
        where: { documentId },
        order: [['versionNumber', 'DESC']]
      });

      const versionNumber = latestVersion ? latestVersion.versionNumber + 1 : 1;

      const version = await DocumentVersion.create({
        documentId,
        versionNumber,
        title: versionData.title,
        content: versionData.content,
        changes: versionData.changes,
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
        order: [['versionNumber', 'ASC']]
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
      const [docMetadata, created] = await DocumentMetadata.findOrCreate({
        where: { documentId },
        defaults: { documentId, ...metadata }
      });

      if (!created) {
        await docMetadata.update(metadata);
      }

      return docMetadata;
    } catch (error) {
      throw new Error(`Failed to update document metadata: ${error.message}`);
    }
  }

  async getDocumentMetadata(documentId) {
    try {
      const metadata = await DocumentMetadata.findOne({
        where: { documentId }
      });
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
        sharedBy: userId,
        sharedWith,
        permissionLevel
      });
      return share;
    } catch (error) {
      throw new Error(`Failed to share document: ${error.message}`);
    }
  }

  async getSharedDocuments(userId) {
    try {
      const shares = await DocumentShare.findAll({
        where: { 
          sharedWith: userId,
          isActive: true
        },
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
  async storeAnalysisResult(analysisData, userId) {
    try {
      const result = await AnalysisResult.create({
        ...analysisData,
        performedBy: userId,
        performedAt: new Date(),
        status: 'completed'
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
        order: [['performedAt', 'DESC']]
      });
      return results;
    } catch (error) {
      throw new Error(`Failed to get document analysis results: ${error.message}`);
    }
  }
}

module.exports = new RegulatoryService();