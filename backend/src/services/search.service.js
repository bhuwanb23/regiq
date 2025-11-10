const { SearchIndex, SearchAnalytics, SearchCache, RegulatoryDocument } = require('../models');
const { Op, sequelize } = require('sequelize');

class SearchService {
  /**
   * Perform a full-text search on regulatory documents
   * @param {Object} query - Search parameters
   * @param {string} query.q - Search query text
   * @param {Object} query.filters - Additional filters
   * @param {number} query.page - Page number for pagination
   * @param {number} query.limit - Number of results per page
   * @param {string} query.sortBy - Field to sort by
   * @param {string} query.sortOrder - Sort order (asc/desc)
   * @returns {Object} Search results with pagination info
   */
  async searchDocuments(query) {
    const {
      q = '',
      filters = {},
      page = 1,
      limit = 10
    } = query;

    const offset = (page - 1) * limit;

    // Check cache first
    const cacheKey = this.generateCacheKey(query);
    const cachedResult = await this.getCachedResult(cacheKey);
    if (cachedResult) {
      return cachedResult;
    }

    try {
      let count, rows;

      // If we have a search query, use FTS
      if (q) {
        // Use raw query for FTS search
        const ftsQuery = `
          SELECT si.*, sf.rank
          FROM search_indices si
          JOIN search_fts sf ON si.id = sf.rowid
          WHERE search_fts MATCH ?
          ORDER BY sf.rank
          LIMIT ? OFFSET ?
        `;
        
        const ftsResults = await sequelize.query(ftsQuery, {
          replacements: [q, limit, offset],
          type: sequelize.QueryTypes.SELECT
        });
        
        // Get count for pagination
        const countQuery = `
          SELECT COUNT(*) as count
          FROM search_indices si
          JOIN search_fts sf ON si.id = sf.rowid
          WHERE search_fts MATCH ?
        `;
        
        const countResult = await sequelize.query(countQuery, {
          replacements: [q],
          type: sequelize.QueryTypes.SELECT
        });
        
        count = countResult[0].count;
        rows = ftsResults;
      } else {
        // Regular search without FTS
        const whereConditions = this.buildFilterWhereConditions(filters);
        
        const result = await SearchIndex.findAndCountAll({
          where: whereConditions,
          include: [{
            model: RegulatoryDocument,
            as: 'document',
            attributes: ['id', 'title', 'content', 'jurisdiction', 'documentType', 'effectiveDate', 'createdAt']
          }],
          limit,
          offset
        });
        
        count = result.count;
        rows = result.rows;
      }

      // Track search analytics
      await this.trackSearch(q, count, filters);

      // Prepare results
      const results = {
        data: await Promise.all(rows.map(async (item) => {
          // Get the associated document
          const document = await RegulatoryDocument.findByPk(item.document_id || item.documentId, {
            attributes: ['id', 'title', 'content', 'jurisdiction', 'documentType', 'effectiveDate', 'createdAt']
          });
          
          return {
            id: document ? document.id : item.document_id || item.documentId,
            title: document ? document.title : item.title,
            content: document ? document.content : item.content,
            jurisdiction: document ? document.jurisdiction : item.jurisdiction,
            documentType: document ? document.documentType : null,
            effectiveDate: document ? document.effectiveDate : null,
            createdAt: document ? document.createdAt : item.createdAt,
            relevanceScore: item.rank || 0
          };
        })),
        pagination: {
          page,
          limit,
          total: count,
          totalPages: Math.ceil(count / limit)
        },
        query: q
      };

      // Cache results
      await this.cacheResult(cacheKey, results);

      return results;
    } catch (error) {
      console.error('Search failed:', error);
      throw new Error(`Search failed: ${error.message}`);
    }
  }

  /**
   * Generate cache key for search query
   * @param {Object} query - Search query parameters
   * @returns {string} Cache key
   */
  generateCacheKey(query) {
    return JSON.stringify(query);
  }

  /**
   * Get cached search results
   * @param {string} key - Cache key
   * @returns {Object|null} Cached results or null
   */
  async getCachedResult(key) {
    try {
      const cacheEntry = await SearchCache.findOne({
        where: {
          query_hash: key,  // Using the actual column name
          expires_at: {
            [Op.gt]: new Date()
          }
        }
      });

      if (cacheEntry) {
        return cacheEntry.results;
      }
      return null;
    } catch (error) {
      // If cache fails, continue with search
      return null;
    }
  }

  /**
   * Cache search results
   * @param {string} key - Cache key
   * @param {Object} results - Search results
   */
  async cacheResult(key, results) {
    try {
      const expiresAt = new Date();
      expiresAt.setHours(expiresAt.getHours() + 1); // Cache for 1 hour

      await SearchCache.upsert({
        query_hash: key,
        query: results.query,
        results: results,
        result_count: results.pagination.total,
        created_at: new Date(),
        expires_at: expiresAt
      });
    } catch (error) {
      // If caching fails, continue without caching
      console.warn('Failed to cache search results:', error.message);
    }
  }

  /**
   * Build WHERE conditions for filters
   * @param {Object} filters - Filter parameters
   * @returns {Object} WHERE conditions
   */
  buildFilterWhereConditions(filters) {
    const conditions = {};

    if (filters.jurisdiction) {
      conditions.jurisdiction = filters.jurisdiction;
    }

    if (filters.documentType) {
      conditions.document_type = filters.documentType;
    }

    if (filters.source) {
      conditions.source = filters.source;
    }

    return conditions;
  }

  /**
   * Track search analytics
   * @param {string} query - Search query
   * @param {number} resultCount - Number of results
   * @param {Object} filters - Applied filters
   */
  async trackSearch(query, resultCount, filters) {
    try {
      await SearchAnalytics.create({
        query,
        result_count: resultCount,
        filters: JSON.stringify(filters),
        timestamp: new Date()
      });
    } catch (error) {
      console.warn('Failed to track search:', error.message);
    }
  }

  /**
   * Get search suggestions
   * @param {string} query - Partial query
   * @returns {Array} Search suggestions
   */
  async getSuggestions(query) {
    try {
      if (!query) {
        return [];
      }
      
      // For SQLite FTS, we can use the FTS table to get suggestions
      const suggestionQuery = `
        SELECT DISTINCT si.title
        FROM search_indices si
        JOIN search_fts sf ON si.id = sf.rowid
        WHERE search_fts MATCH ?
        LIMIT 10
      `;
      
      const suggestions = await sequelize.query(suggestionQuery, {
        replacements: [`${query}*`], // Prefix search for suggestions
        type: sequelize.QueryTypes.SELECT
      });

      return suggestions.map(s => s.title);
    } catch (error) {
      console.warn('Failed to get suggestions:', error.message);
      return [];
    }
  }

  /**
   * Index a document for search
   * @param {Object} document - Document to index
   */
  async indexDocument(document) {
    try {
      if (!document || !document.id) {
        throw new Error('Document ID is required');
      }
      
      // This will be handled by the database triggers
      // The triggers automatically sync the FTS table with the search_indices table
      await SearchIndex.create({
        document_id: document.id,
        title: document.title || '',
        content: document.content || '',
        jurisdiction: document.jurisdiction || null,
        document_type: document.documentType || null,
        source: document.source || null,
        tags: document.tags || []
      });
    } catch (error) {
      console.warn('Failed to index document:', error.message);
      throw error;
    }
  }

  /**
   * Remove document from search index
   * @param {number} documentId - Document ID
   */
  async removeDocumentFromIndex(documentId) {
    try {
      if (!documentId) {
        throw new Error('Document ID is required');
      }
      
      // This will be handled by the database triggers
      // The triggers automatically sync the FTS table with the search_indices table
      await SearchIndex.destroy({
        where: { document_id: documentId }
      });
    } catch (error) {
      console.warn('Failed to remove document from index:', error.message);
      throw error;
    }
  }
}

module.exports = new SearchService();