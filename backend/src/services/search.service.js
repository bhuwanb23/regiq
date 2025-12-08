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
    console.log('searchDocuments called with query:', query);
    
    // Ensure query is an object to prevent "Cannot read properties of undefined" errors
    const safeQuery = query || {};
    
    const {
      q = '',
      filters = {},
      page = 1,
      limit = 10,
      sortBy = 'relevance',
      sortOrder = 'desc'
    } = safeQuery;

    console.log('Parsed parameters:', { q, filters, page, limit, sortBy, sortOrder });

    const offset = (page - 1) * limit;

    // Check cache first
    const cacheKey = this.generateCacheKey(safeQuery);
    const cachedResult = await this.getCachedResult(cacheKey);
    if (cachedResult) {
      return cachedResult;
    }

    // Track response time
    const startTime = Date.now();
    
    try {
      let count, rows;

      // If we have a search query, use FTS
      if (q) {
        // Use raw query for FTS search with timeout
        const ftsQuery = `
          SELECT si.*, sf.rank
          FROM search_indices si
          JOIN search_fts sf ON si.id = sf.rowid
          WHERE search_fts MATCH ?
          ORDER BY sf.rank
          LIMIT ? OFFSET ?
        `;
        
        // Add query timeout (5 seconds)
        const ftsResults = await sequelize.query(ftsQuery, {
          replacements: [q, limit, offset],
          type: sequelize.QueryTypes.SELECT,
          timeout: 5000
        });
        
        // Get count for pagination with timeout
        const countQuery = `
          SELECT COUNT(*) as count
          FROM search_indices si
          JOIN search_fts sf ON si.id = sf.rowid
          WHERE search_fts MATCH ?
        `;
        
        const countResult = await sequelize.query(countQuery, {
          replacements: [q],
          type: sequelize.QueryTypes.SELECT,
          timeout: 5000
        });
        
        count = countResult[0].count;
        rows = ftsResults;
      } else {
        // Regular search without FTS with timeout
        const whereConditions = this.buildFilterWhereConditions(filters);
        
        const result = await SearchIndex.findAndCountAll({
          where: whereConditions,
          include: [{
            model: RegulatoryDocument,
            as: 'document',
            attributes: ['id', 'title', 'content', 'jurisdiction', 'documentType', 'effectiveDate', 'createdAt']
          }],
          limit,
          offset,
          timeout: 5000
        });
        
        count = result.count;
        rows = result.rows;
      }

      // Calculate response time
      const responseTime = Date.now() - startTime;
      
      // Track search analytics with response time
      await this.trackSearch(q, count, filters, responseTime);

      // Prepare results with enhanced ranking
      let searchData = await Promise.all(rows.map(async (item) => {
        // Get the associated document
        const document = await RegulatoryDocument.findByPk(item.document_id, {
          attributes: ['id', 'title', 'content', 'jurisdiction', 'documentType', 'effectiveDate', 'createdAt']
        });
        
        // Calculate enhanced relevance score
        const relevanceScore = this.calculateRelevanceScore(item, document, q);
        
        return {
          id: document ? document.id : item.document_id,
          title: document ? document.title : item.title,
          content: document ? document.content : item.content,
          jurisdiction: document ? document.jurisdiction : item.jurisdiction,
          documentType: document ? document.documentType : null,
          effectiveDate: document ? document.effectiveDate : null,
          createdAt: document ? document.createdAt : item.createdAt,
          relevanceScore: relevanceScore
        };
      }));
      
      // Sort results based on sortBy parameter
      if (sortBy === 'relevance') {
        searchData.sort((a, b) => {
          if (sortOrder === 'asc') {
            return a.relevanceScore - b.relevanceScore;
          } else {
            return b.relevanceScore - a.relevanceScore;
          }
        });
      } else if (sortBy === 'date' && sortOrder === 'desc') {
        searchData.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
      } else if (sortBy === 'date' && sortOrder === 'asc') {
        searchData.sort((a, b) => new Date(a.createdAt) - new Date(b.createdAt));
      }
      
      // Apply pagination to sorted data
      const startIndex = offset;
      const endIndex = startIndex + limit;
      const paginatedData = searchData.slice(startIndex, endIndex);

      const results = {
        data: paginatedData,
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
      // Track failed searches
      const responseTime = Date.now() - startTime;
      await this.trackSearch(q, 0, filters, responseTime);
      
      console.error('Search failed:', error);
      throw new Error(`Search failed: ${error.message}`);
    }
  }

  /**
   * Calculate enhanced relevance score for search results
   * @param {Object} item - Search index item
   * @param {Object} document - Associated regulatory document
   * @param {string} query - Search query
   * @returns {number} Relevance score between 0 and 1
   */
  calculateRelevanceScore(item, document, query) {
    // Start with FTS rank if available
    let score = item.rank || 0;
    
    // If we don't have a query, return a basic score based on document properties
    if (!query) {
      // Boost newer documents
      if (document && document.createdAt) {
        const now = new Date();
        const created = new Date(document.createdAt);
        const daysOld = (now - created) / (1000 * 60 * 60 * 24);
        // Newer documents get higher scores (max boost for documents less than 30 days old)
        const freshnessBoost = Math.max(0, 1 - (daysOld / 30));
        score += freshnessBoost * 0.3;
      }
      
      // Boost documents with compliance scores
      if (document && document.complianceScore) {
        score += (document.complianceScore / 100) * 0.2;
      }
      
      return Math.min(1, score);
    }
    
    // Enhanced scoring for queries
    
    // 1. Term frequency in title (weighted heavily)
    const titleMatches = (item.title || '').toLowerCase().split(' ').filter(word => 
      word.includes(query.toLowerCase())
    ).length;
    score += titleMatches * 0.4;
    
    // 2. Term frequency in content
    const contentMatches = (item.content || '').toLowerCase().split(' ').filter(word => 
      word.includes(query.toLowerCase())
    ).length;
    score += contentMatches * 0.1;
    
    // 3. Exact phrase match bonus
    if ((item.title || '').toLowerCase().includes(query.toLowerCase())) {
      score += 0.3;
    }
    
    if ((item.content || '').toLowerCase().includes(query.toLowerCase())) {
      score += 0.1;
    }
    
    // 4. Document type boosting
    const importantDocTypes = ['regulation', 'directive', 'act'];
    if (document && document.documentType && 
        importantDocTypes.includes(document.documentType.toLowerCase())) {
      score += 0.2;
    }
    
    // 5. Freshness boost
    if (document && document.createdAt) {
      const now = new Date();
      const created = new Date(document.createdAt);
      const daysOld = (now - created) / (1000 * 60 * 60 * 24);
      // Newer documents get higher scores (max boost for documents less than 30 days old)
      const freshnessBoost = Math.max(0, 1 - (daysOld / 30));
      score += freshnessBoost * 0.15;
    }
    
    // 6. Compliance score boost
    if (document && document.complianceScore) {
      score += (document.complianceScore / 100) * 0.1;
    }
    
    // Normalize score to 0-1 range
    return Math.min(1, score);
  }

  /**
   * Generate cache key for search query
   * @param {Object} query - Search query parameters
   * @returns {string} Cache key
   */
  generateCacheKey(query) {
    // Create a more stable cache key by sorting keys
    const sortedQuery = {};
    Object.keys(query).sort().forEach(key => {
      sortedQuery[key] = query[key];
    });
    return JSON.stringify(sortedQuery);
  }

  /**
   * Get cached search results with LRU eviction
   * @param {string} key - Cache key
   * @returns {Object|null} Cached results or null
   */
  async getCachedResult(key) {
    try {
      const cacheEntry = await SearchCache.findOne({
        where: {
          query_hash: key,
          expires_at: {
            [Op.gt]: new Date()
          }
        },
        order: [['accessed_at', 'DESC']] // Get most recently accessed
      });

      if (cacheEntry) {
        // Update last accessed time for LRU eviction
        await cacheEntry.update({
          accessed_at: new Date()
        });
        
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
      const now = new Date();

      await SearchCache.upsert({
        query_hash: key,
        query: results.query,
        results: results,
        result_count: results.pagination.total,
        created_at: now,
        accessed_at: now,
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
   * @param {number} responseTime - Response time in milliseconds
   * @param {string} userId - User ID (if available)
   * @param {string} sessionId - Session ID (if available)
   */
  async trackSearch(query, resultCount, filters, responseTime = 0, userId = null, sessionId = null) {
    try {
      // Ensure query is a string to prevent "Cannot read properties of undefined" errors
      const safeQuery = query || '';
      const safeFilters = filters || {};
      const safeResultCount = resultCount || 0;
      const safeResponseTime = responseTime || 0;
      
      await SearchAnalytics.create({
        query: safeQuery,
        result_count: safeResultCount,
        filters: JSON.stringify(safeFilters),
        response_time: safeResponseTime,
        user_id: userId,
        session_id: sessionId,
        timestamp: new Date()
      });
    } catch (error) {
      console.warn('Failed to track search:', error.message);
    }
  }

  /**
   * Get popular search queries
   * @param {number} limit - Number of queries to return
   * @returns {Array} Popular search queries
   */
  async getPopularQueries(limit = 10) {
    try {
      const popularQueries = await SearchAnalytics.findAll({
        attributes: [
          'query',
          [sequelize.fn('COUNT', sequelize.col('query')), 'count'],
          [sequelize.fn('AVG', sequelize.col('results_count')), 'avg_results'],
          [sequelize.fn('AVG', sequelize.col('response_time')), 'avg_response_time']
        ],
        group: ['query'],
        order: [[sequelize.fn('COUNT', sequelize.col('query')), 'DESC']],
        limit: limit
      });
      
      return popularQueries.map(item => ({
        query: item.query,
        count: item.getDataValue('count'),
        avgResults: parseFloat(item.getDataValue('avg_results')).toFixed(2),
        avgResponseTime: parseFloat(item.getDataValue('avg_response_time')).toFixed(2)
      }));
    } catch (error) {
      console.warn('Failed to get popular queries:', error.message);
      return [];
    }
  }

  /**
   * Get search trends over time
   * @param {number} days - Number of days to analyze
   * @returns {Array} Search trends data
   */
  async getSearchTrends(days = 30) {
    try {
      const startDate = new Date();
      startDate.setDate(startDate.getDate() - days);
      
      const trends = await SearchAnalytics.findAll({
        attributes: [
          [sequelize.fn('DATE', sequelize.col('timestamp')), 'date'],
          [sequelize.fn('COUNT', sequelize.col('id')), 'count'],
          [sequelize.fn('AVG', sequelize.col('results_count')), 'avg_results']
        ],
        where: {
          timestamp: {
            [Op.gte]: startDate
          }
        },
        group: [sequelize.fn('DATE', sequelize.col('timestamp'))],
        order: [[sequelize.fn('DATE', sequelize.col('timestamp')), 'ASC']]
      });
      
      return trends.map(item => ({
        date: item.getDataValue('date'),
        count: item.getDataValue('count'),
        avgResults: parseFloat(item.getDataValue('avg_results')).toFixed(2)
      }));
    } catch (error) {
      console.warn('Failed to get search trends:', error.message);
      return [];
    }
  }

  /**
   * Get zero result searches
   * @param {number} limit - Number of queries to return
   * @returns {Array} Zero result searches
   */
  async getZeroResultSearches(limit = 10) {
    try {
      const zeroResults = await SearchAnalytics.findAll({
        attributes: ['query', 'filters', 'timestamp'],
        where: {
          results_count: 0
        },
        order: [['timestamp', 'DESC']],
        limit: limit
      });
      
      return zeroResults;
    } catch (error) {
      console.warn('Failed to get zero result searches:', error.message);
      return [];
    }
  }

  /**
   * Warm the cache with popular queries
   * @param {number} limit - Number of popular queries to warm
   */
  async warmCacheWithPopularQueries(limit = 50) {
    try {
      // Get popular queries
      const popularQueries = await this.getPopularQueries(limit);
      
      // Warm cache for each popular query
      for (const item of popularQueries) {
        const query = item.query;
        
        // Skip if already cached
        const cacheKey = this.generateCacheKey({ q: query });
        const cachedResult = await this.getCachedResult(cacheKey);
        if (cachedResult) {
          continue;
        }
        
        // Execute search to populate cache
        try {
          await this.searchDocuments({ q: query });
          console.log(`Warmed cache for query: ${query}`);
        } catch (error) {
          console.warn(`Failed to warm cache for query: ${query}`, error.message);
        }
      }
    } catch (error) {
      console.warn('Failed to warm cache with popular queries:', error.message);
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
      // Validate document object
      if (!document || typeof document !== 'object') {
        throw new Error('Document data is required and must be an object');
      }
      
      if (!document.id) {
        throw new Error('Document ID is required');
      }
      
      console.log('Indexing document with data:', document);
      
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