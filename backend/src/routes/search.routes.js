const express = require('express');
const router = express.Router();
const searchController = require('../controllers/search.controller');

// Search documents
router.get('/', searchController.searchDocuments);

// Get search suggestions
router.get('/suggestions', searchController.getSuggestions);

// Index a document for search (admin only)
router.post('/index', searchController.indexDocument);

// Remove document from search index (admin only)
router.delete('/index/:documentId', (req, res, next) => {
  // Check if documentId is a valid integer
  if (!req.params.documentId || isNaN(parseInt(req.params.documentId))) {
    return res.status(400).json({
      success: false,
      message: 'Document ID is required and must be a valid integer'
    });
  }
  next();
}, searchController.removeDocumentFromIndex);

module.exports = router;