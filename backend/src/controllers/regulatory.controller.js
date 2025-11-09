const regulatoryService = require('../services/regulatory.service');

class RegulatoryController {
  /**
   * Document upload and processing endpoints
   */
  async uploadDocument(req, res) {
    try {
      // For testing without authentication, use a dummy user ID
      const document = await regulatoryService.uploadDocument(req.body, 'test-user-id');
      res.status(201).json({
        success: true,
        message: 'Document uploaded successfully',
        data: document
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  async processDocument(req, res) {
    try {
      const { id } = req.params;
      const document = await regulatoryService.processDocument(id);
      res.status(200).json({
        success: true,
        message: 'Document processing started',
        data: document
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  async getDocumentProcessingStatus(req, res) {
    try {
      const { id } = req.params;
      const status = await regulatoryService.getDocumentProcessingStatus(id);
      res.status(200).json({
        success: true,
        data: status
      });
    } catch (error) {
      res.status(404).json({
        success: false,
        message: error.message
      });
    }
  }

  /**
   * Regulatory document search and filtering
   */
  async searchDocuments(req, res) {
    try {
      const documents = await regulatoryService.searchDocuments(req.query);
      res.status(200).json({
        success: true,
        data: documents
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }

  async getDocumentById(req, res) {
    try {
      const { id } = req.params;
      const document = await regulatoryService.getDocumentById(id);
      res.status(200).json({
        success: true,
        data: document
      });
    } catch (error) {
      res.status(404).json({
        success: false,
        message: error.message
      });
    }
  }

  /**
   * Compliance checking endpoints
   */
  async checkCompliance(req, res) {
    try {
      const { documentId } = req.body;
      // For testing without authentication, use a dummy user ID
      const result = await regulatoryService.checkCompliance(documentId, 'test-user-id');
      res.status(200).json({
        success: true,
        message: 'Compliance check completed',
        data: result
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  async getComplianceResult(req, res) {
    try {
      const { id } = req.params;
      const result = await regulatoryService.getComplianceResult(id);
      res.status(200).json({
        success: true,
        data: result
      });
    } catch (error) {
      res.status(404).json({
        success: false,
        message: error.message
      });
    }
  }

  /**
   * Regulatory alert generation
   */
  async createAlert(req, res) {
    try {
      // For testing without authentication, use a dummy user ID
      const alert = await regulatoryService.createAlert(req.body, 'test-user-id');
      res.status(201).json({
        success: true,
        message: 'Alert created successfully',
        data: alert
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  async getAlerts(req, res) {
    try {
      const alerts = await regulatoryService.getAlerts(req.query);
      res.status(200).json({
        success: true,
        data: alerts
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }

  async updateAlertStatus(req, res) {
    try {
      const { id } = req.params;
      const { status } = req.body;
      // For testing without authentication, use a dummy user ID
      const alert = await regulatoryService.updateAlertStatus(id, status, 'test-user-id');
      res.status(200).json({
        success: true,
        message: 'Alert status updated',
        data: alert
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  /**
   * Document versioning
   */
  async createDocumentVersion(req, res) {
    try {
      const { id } = req.params;
      // For testing without authentication, use a dummy user ID
      const version = await regulatoryService.createDocumentVersion(id, req.body, 'test-user-id');
      res.status(201).json({
        success: true,
        message: 'Document version created',
        data: version
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  async getDocumentVersions(req, res) {
    try {
      const { id } = req.params;
      const versions = await regulatoryService.getDocumentVersions(id);
      res.status(200).json({
        success: true,
        data: versions
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }

  /**
   * Document metadata management
   */
  async updateDocumentMetadata(req, res) {
    try {
      const { id } = req.params;
      const metadata = await regulatoryService.updateDocumentMetadata(id, req.body);
      res.status(200).json({
        success: true,
        message: 'Document metadata updated',
        data: metadata
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  async getDocumentMetadata(req, res) {
    try {
      const { id } = req.params;
      const metadata = await regulatoryService.getDocumentMetadata(id);
      res.status(200).json({
        success: true,
        data: metadata
      });
    } catch (error) {
      res.status(404).json({
        success: false,
        message: error.message
      });
    }
  }

  /**
   * Document sharing
   */
  async shareDocument(req, res) {
    try {
      const { id } = req.params;
      const share = await regulatoryService.shareDocument(id, req.body.sharedWith, req.body.permissionLevel, req.user.id);
      res.status(201).json({
        success: true,
        message: 'Document shared successfully',
        data: share
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  async getSharedDocuments(req, res) {
    try {
      const documents = await regulatoryService.getSharedDocuments(req.user.id);
      res.status(200).json({
        success: true,
        data: documents
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }

  /**
   * Analysis result storage
   */
  async storeAnalysisResult(req, res) {
    try {
      const result = await regulatoryService.storeAnalysisResult(req.body, req.user.id);
      res.status(201).json({
        success: true,
        message: 'Analysis result stored',
        data: result
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  async getAnalysisResult(req, res) {
    try {
      const { id } = req.params;
      const result = await regulatoryService.getAnalysisResult(id);
      res.status(200).json({
        success: true,
        data: result
      });
    } catch (error) {
      res.status(404).json({
        success: false,
        message: error.message
      });
    }
  }

  async getDocumentAnalysisResults(req, res) {
    try {
      const { documentId } = req.params;
      const results = await regulatoryService.getDocumentAnalysisResults(documentId);
      res.status(200).json({
        success: true,
        data: results
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }
}

module.exports = new RegulatoryController();