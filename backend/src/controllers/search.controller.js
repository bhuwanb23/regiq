const SearchService = require('../services/search.service');

class SearchController {
  /**
   * Search documents endpoint
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   */
  async searchDocuments(req, res) {
    console.log('Search controller called with query:', req.query);
    try {
      const {
        q,
        filters,
        page,
        limit,
        sortBy,
        sortOrder
      } = req.query;

      // Parse filters if provided as JSON string
      let parsedFilters = {};
      if (filters) {
        try {
          parsedFilters = JSON.parse(filters);
        } catch (error) {
          return res.status(400).json({
            success: false,
            message: 'Invalid filters format. Must be valid JSON.'
          });
        }
      }

      const searchQuery = {
        q: q || '',
        filters: parsedFilters,
        page: parseInt(page) || 1,
        limit: parseInt(limit) || 10,
        sortBy: sortBy || 'relevance',
        sortOrder: sortOrder || 'desc'
      };
      
      console.log('Calling SearchService with searchQuery:', searchQuery);

      const results = await SearchService.searchDocuments(searchQuery);

      res.json({
        success: true,
        data: results.data,
        pagination: results.pagination,
        query: results.query
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: 'Search failed',
        error: error.message
      });
    }
  }

  /**
   * Get search suggestions endpoint
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   */
  async getSuggestions(req, res) {
    try {
      const { q } = req.query;

      if (!q) {
        return res.status(400).json({
          success: false,
          message: 'Query parameter "q" is required'
        });
      }

      const suggestions = await SearchService.getSuggestions(q);

      res.json({
        success: true,
        data: suggestions
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: 'Failed to get suggestions',
        error: error.message
      });
    }
  }

  /**
   * Get popular search queries
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   */
  async getPopularQueries(req, res) {
    try {
      const { limit = 10 } = req.query;
      const popularQueries = await SearchService.getPopularQueries(parseInt(limit));

      res.json({
        success: true,
        data: popularQueries
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: 'Failed to get popular queries',
        error: error.message
      });
    }
  }

  /**
   * Get search trends over time
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   */
  async getSearchTrends(req, res) {
    try {
      const { days = 30 } = req.query;
      const trends = await SearchService.getSearchTrends(parseInt(days));

      res.json({
        success: true,
        data: trends
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: 'Failed to get search trends',
        error: error.message
      });
    }
  }

  /**
   * Get zero result searches
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   */
  async getZeroResultSearches(req, res) {
    try {
      const { limit = 10 } = req.query;
      const zeroResults = await SearchService.getZeroResultSearches(parseInt(limit));

      res.json({
        success: true,
        data: zeroResults
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: 'Failed to get zero result searches',
        error: error.message
      });
    }
  }

  /**
   * Get cache statistics
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   */
  async getCacheStats(req, res) {
    try {
      const stats = await SearchService.getCacheStats();

      res.json({
        success: true,
        data: stats
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: 'Failed to get cache statistics',
        error: error.message
      });
    }
  }

  /**
   * Index a document for search
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   */
  async indexDocument(req, res) {
    try {
      // Check if body exists and has document property
      if (!req.body || Object.keys(req.body).length === 0) {
        return res.status(400).json({
          success: false,
          message: 'Document data is required'
        });
      }

      const { document } = req.body;

      if (!document) {
        return res.status(400).json({
          success: false,
          message: 'Document data is required'
        });
      }

      await SearchService.indexDocument(document);

      res.json({
        success: true,
        message: 'Document indexed successfully'
      });
    } catch (error) {
      if (error.message.includes('Document ID is required')) {
        return res.status(400).json({
          success: false,
          message: error.message
        });
      }
      
      res.status(500).json({
        success: false,
        message: 'Failed to index document',
        error: error.message
      });
    }
  }

  /**
   * Remove document from search index
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   */
  async removeDocumentFromIndex(req, res) {
    try {
      const { documentId } = req.params;

      if (!documentId) {
        return res.status(400).json({
          success: false,
          message: 'Document ID is required'
        });
      }

      await SearchService.removeDocumentFromIndex(parseInt(documentId));

      res.json({
        success: true,
        message: 'Document removed from index successfully'
      });
    } catch (error) {
      if (error.message.includes('Document ID is required')) {
        return res.status(400).json({
          success: false,
          message: error.message
        });
      }
      
      res.status(500).json({
        success: false,
        message: 'Failed to remove document from index',
        error: error.message
      });
    }
  }
}

module.exports = new SearchController();