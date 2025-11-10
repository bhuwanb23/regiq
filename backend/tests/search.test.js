const request = require('supertest');
const { app } = require('../src/server');
const { SearchIndex, SearchAnalytics, SearchCache } = require('../src/models');
const { sequelize } = require('../src/models');

describe('Search API', () => {
  beforeAll(async () => {
    // Sync database before running tests
    await sequelize.sync({ force: true });
  });

  afterAll(async () => {
    // Close database connection after tests
    await sequelize.close();
  });

  describe('GET /search', () => {
    it('should return empty results for empty query', async () => {
      const response = await request(app)
        .get('/search')
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.data).toEqual([]);
      expect(response.body.pagination).toHaveProperty('total', 0);
    });

    it('should return 400 for invalid filters format', async () => {
      const response = await request(app)
        .get('/search?q=test&filters=invalid-json')
        .expect(400);

      expect(response.body.success).toBe(false);
      expect(response.body.message).toContain('Invalid filters format');
    });
  });

  describe('GET /search/suggestions', () => {
    it('should return 400 when query parameter is missing', async () => {
      const response = await request(app)
        .get('/search/suggestions')
        .expect(400);

      expect(response.body.success).toBe(false);
      expect(response.body.message).toContain('Query parameter "q" is required');
    });

    it('should return empty suggestions for query with no matches', async () => {
      const response = await request(app)
        .get('/search/suggestions?q=nonexistent')
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.data).toEqual([]);
    });
  });

  describe('POST /search/index', () => {
    it('should return 400 when document data is missing', async () => {
      const response = await request(app)
        .post('/search/index')
        .expect(400);

      expect(response.body.success).toBe(false);
      expect(response.body.message).toContain('Document data is required');
    });

    it('should successfully index a document', async () => {
      const documentData = {
        document: {
          id: 1,
          title: 'Test Document',
          content: 'This is a test document for search functionality',
          jurisdiction: 'US',
          documentType: 'regulation',
          source: 'test-source'
        }
      };

      const response = await request(app)
        .post('/search/index')
        .send(documentData)
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.message).toContain('Document indexed successfully');
    });
  });

  describe('DELETE /search/index/:documentId', () => {
    it('should return 400 when document ID is missing', async () => {
      const response = await request(app)
        .delete('/search/index/')
        .expect(400);

      expect(response.body.success).toBe(false);
      expect(response.body.message).toContain('Document ID is required');
    });

    it('should successfully remove document from index', async () => {
      const response = await request(app)
        .delete('/search/index/1')
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.message).toContain('Document removed from index successfully');
    });
  });
});