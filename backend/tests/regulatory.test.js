const request = require('supertest');
const app = require('../src/server');

describe('Regulatory Intelligence API', () => {
  const authToken = 'test_jwt_token';
  const userId = 'test-user-id';

  describe('Document Upload and Processing', () => {
    it('should upload a regulatory document', async () => {
      const documentData = {
        title: 'Test Regulatory Document',
        content: 'This is a test regulatory document content',
        documentType: 'regulation',
        jurisdiction: 'US'
      };

      const res = await request(app)
        .post('/regulatory/documents/upload')
        .set('Authorization', `Bearer ${authToken}`)
        .send(documentData)
        .expect(201);

      expect(res.body.success).toBe(true);
      expect(res.body.data.title).toBe(documentData.title);
    });

    it('should process a document', async () => {
      const res = await request(app)
        .post('/regulatory/documents/test-document-id/process')
        .set('Authorization', `Bearer ${authToken}`)
        .expect(200);

      expect(res.body.success).toBe(true);
    });

    it('should get document processing status', async () => {
      const res = await request(app)
        .get('/regulatory/documents/test-document-id/status')
        .set('Authorization', `Bearer ${authToken}`)
        .expect(200);

      expect(res.body.success).toBe(true);
    });
  });

  describe('Document Search and Filtering', () => {
    it('should search documents', async () => {
      const res = await request(app)
        .get('/regulatory/documents?title=test')
        .set('Authorization', `Bearer ${authToken}`)
        .expect(200);

      expect(res.body.success).toBe(true);
      expect(Array.isArray(res.body.data)).toBe(true);
    });

    it('should get a specific document', async () => {
      const res = await request(app)
        .get('/regulatory/documents/test-document-id')
        .set('Authorization', `Bearer ${authToken}`)
        .expect(200);

      expect(res.body.success).toBe(true);
    });
  });

  describe('Compliance Checking', () => {
    it('should check document compliance', async () => {
      const res = await request(app)
        .post('/regulatory/compliance/check')
        .set('Authorization', `Bearer ${authToken}`)
        .send({ documentId: 'test-document-id' })
        .expect(200);

      expect(res.body.success).toBe(true);
    });

    it('should get compliance result', async () => {
      const res = await request(app)
        .get('/regulatory/compliance/results/test-result-id')
        .set('Authorization', `Bearer ${authToken}`)
        .expect(200);

      expect(res.body.success).toBe(true);
    });
  });

  describe('Regulatory Alerts', () => {
    it('should create a regulatory alert', async () => {
      const alertData = {
        title: 'Test Alert',
        description: 'This is a test alert',
        alertType: 'compliance',
        severity: 'high'
      };

      const res = await request(app)
        .post('/regulatory/alerts')
        .set('Authorization', `Bearer ${authToken}`)
        .send(alertData)
        .expect(201);

      expect(res.body.success).toBe(true);
      expect(res.body.data.title).toBe(alertData.title);
    });

    it('should get alerts', async () => {
      const res = await request(app)
        .get('/regulatory/alerts?severity=high')
        .set('Authorization', `Bearer ${authToken}`)
        .expect(200);

      expect(res.body.success).toBe(true);
      expect(Array.isArray(res.body.data)).toBe(true);
    });

    it('should update alert status', async () => {
      const res = await request(app)
        .put('/regulatory/alerts/test-alert-id')
        .set('Authorization', `Bearer ${authToken}`)
        .send({ status: 'resolved' })
        .expect(200);

      expect(res.body.success).toBe(true);
    });
  });

  describe('Document Versioning', () => {
    it('should create a document version', async () => {
      const versionData = {
        title: 'Version 2',
        content: 'Updated content',
        changes: ['Updated section 1', 'Added section 2']
      };

      const res = await request(app)
        .post('/regulatory/documents/test-document-id/versions')
        .set('Authorization', `Bearer ${authToken}`)
        .send(versionData)
        .expect(201);

      expect(res.body.success).toBe(true);
    });

    it('should get document versions', async () => {
      const res = await request(app)
        .get('/regulatory/documents/test-document-id/versions')
        .set('Authorization', `Bearer ${authToken}`)
        .expect(200);

      expect(res.body.success).toBe(true);
      expect(Array.isArray(res.body.data)).toBe(true);
    });
  });

  describe('Document Metadata', () => {
    it('should update document metadata', async () => {
      const metadata = {
        category: 'Banking',
        industry: 'Financial Services',
        region: 'North America'
      };

      const res = await request(app)
        .put('/regulatory/documents/test-document-id/metadata')
        .set('Authorization', `Bearer ${authToken}`)
        .send(metadata)
        .expect(200);

      expect(res.body.success).toBe(true);
    });

    it('should get document metadata', async () => {
      const res = await request(app)
        .get('/regulatory/documents/test-document-id/metadata')
        .set('Authorization', `Bearer ${authToken}`)
        .expect(200);

      expect(res.body.success).toBe(true);
    });
  });

  describe('Document Sharing', () => {
    it('should share a document', async () => {
      const shareData = {
        sharedWith: 'other-user-id',
        permissionLevel: 'read'
      };

      const res = await request(app)
        .post('/regulatory/documents/test-document-id/share')
        .set('Authorization', `Bearer ${authToken}`)
        .send(shareData)
        .expect(201);

      expect(res.body.success).toBe(true);
    });

    it('should get shared documents', async () => {
      const res = await request(app)
        .get('/regulatory/documents/shared')
        .set('Authorization', `Bearer ${authToken}`)
        .expect(200);

      expect(res.body.success).toBe(true);
      expect(Array.isArray(res.body.data)).toBe(true);
    });
  });

  describe('Analysis Results', () => {
    it('should store analysis result', async () => {
      const analysisData = {
        documentId: 'test-document-id',
        analysisType: 'bias_analysis',
        results: { score: 0.85, findings: ['bias detected'] },
        summary: 'Analysis summary'
      };

      const res = await request(app)
        .post('/regulatory/analysis')
        .set('Authorization', `Bearer ${authToken}`)
        .send(analysisData)
        .expect(201);

      expect(res.body.success).toBe(true);
    });

    it('should get analysis result', async () => {
      const res = await request(app)
        .get('/regulatory/analysis/test-analysis-id')
        .set('Authorization', `Bearer ${authToken}`)
        .expect(200);

      expect(res.body.success).toBe(true);
    });

    it('should get document analysis results', async () => {
      const res = await request(app)
        .get('/regulatory/analysis/document/test-document-id')
        .set('Authorization', `Bearer ${authToken}`)
        .expect(200);

      expect(res.body.success).toBe(true);
      expect(Array.isArray(res.body.data)).toBe(true);
    });
  });
});