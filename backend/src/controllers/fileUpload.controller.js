const fileUploadService = require('../services/fileUpload.service');
const multer = require('multer');
const path = require('path');

// Configure multer for file uploads
const storage = multer.memoryStorage();
const upload = multer({ 
  storage: storage,
  limits: {
    fileSize: 50 * 1024 * 1024 // 50MB limit
  },
  fileFilter: (req, file, cb) => {
    // Accept all file types for now
    cb(null, true);
  }
});

class FileUploadController {
  async uploadFile(req, res) {
    try {
      // Check if file was uploaded
      if (!req.file) {
        return res.status(400).json({
          success: false,
          message: 'No file uploaded'
        });
      }

      // For now, we'll use a test user ID
      // In a real implementation, this would come from authentication middleware
      const userId = 'test-user-id';

      // Save file information to database
      const uploadData = {
        userId: userId,
        fileName: req.file.originalname,
        originalName: req.file.originalname,
        fileExtension: path.extname(req.file.originalname),
        mimeType: req.file.mimetype,
        fileSize: req.file.size,
        uploadStatus: 'uploaded',
        processingStatus: 'pending'
      };

      const uploadRecord = await fileUploadService.createFileUpload(uploadData);

      res.status(201).json({
        success: true,
        message: 'File uploaded successfully',
        data: uploadRecord
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }

  async getFileUpload(req, res) {
    try {
      const { id } = req.params;
      const upload = await fileUploadService.getFileUploadById(id);
      res.status(200).json({
        success: true,
        message: 'File upload retrieved successfully',
        data: upload
      });
    } catch (error) {
      res.status(404).json({
        success: false,
        message: error.message
      });
    }
  }

  async listFileUploads(req, res) {
    try {
      const { limit = 10, offset = 0 } = req.query;
      const result = await fileUploadService.getAllFileUploads(
        parseInt(limit),
        parseInt(offset)
      );
      res.status(200).json({
        success: true,
        message: 'File uploads retrieved successfully',
        data: result
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }

  async updateFileUpload(req, res) {
    try {
      const { id } = req.params;
      const upload = await fileUploadService.updateFileUpload(id, req.body);
      res.status(200).json({
        success: true,
        message: 'File upload updated successfully',
        data: upload
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  async deleteFileUpload(req, res) {
    try {
      const { id } = req.params;
      const result = await fileUploadService.deleteFileUpload(id);
      res.status(200).json({
        success: true,
        message: result.message
      });
    } catch (error) {
      res.status(404).json({
        success: false,
        message: error.message
      });
    }
  }

  async getUserFileUploads(req, res) {
    try {
      // For now, we'll use a test user ID
      // In a real implementation, this would come from authentication middleware
      const userId = 'test-user-id';
      const { limit = 10, offset = 0 } = req.query;
      const result = await fileUploadService.getUserFileUploads(
        userId,
        parseInt(limit),
        parseInt(offset)
      );
      res.status(200).json({
        success: true,
        message: 'User file uploads retrieved successfully',
        data: result
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }

  async updateUploadStatus(req, res) {
    try {
      const { id } = req.params;
      const { status } = req.body;
      const upload = await fileUploadService.updateUploadStatus(id, status);
      res.status(200).json({
        success: true,
        message: 'Upload status updated successfully',
        data: upload
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  getUploadMiddleware() {
    return upload.single('file');
  }
}

module.exports = new FileUploadController();