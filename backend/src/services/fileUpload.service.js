const { FileUpload } = require('../models');
const fs = require('fs').promises;
const path = require('path');

class FileUploadService {
  async createFileUpload(uploadData) {
    try {
      const upload = await FileUpload.create(uploadData);
      return upload;
    } catch (error) {
      throw new Error(`Failed to create file upload record: ${error.message}`);
    }
  }

  async getFileUploadById(id) {
    try {
      const upload = await FileUpload.findByPk(id);
      if (!upload) {
        throw new Error('File upload not found');
      }
      return upload;
    } catch (error) {
      throw new Error(`Failed to get file upload: ${error.message}`);
    }
  }

  async getAllFileUploads(limit = 10, offset = 0) {
    try {
      const { rows, count } = await FileUpload.findAndCountAll({
        limit,
        offset,
        order: [['created_at', 'DESC']]
      });
      return { uploads: rows, count, limit, offset };
    } catch (error) {
      throw new Error(`Failed to list file uploads: ${error.message}`);
    }
  }

  async updateFileUpload(id, updateData) {
    try {
      const upload = await this.getFileUploadById(id);
      const updatedUpload = await upload.update(updateData);
      return updatedUpload;
    } catch (error) {
      throw new Error(`Failed to update file upload: ${error.message}`);
    }
  }

  async deleteFileUpload(id) {
    try {
      const upload = await this.getFileUploadById(id);
      await upload.destroy();
      return { success: true, message: 'File upload deleted successfully' };
    } catch (error) {
      throw new Error(`Failed to delete file upload: ${error.message}`);
    }
  }

  async getUserFileUploads(userId, limit = 10, offset = 0) {
    try {
      const { rows, count } = await FileUpload.findAndCountAll({
        where: { userId },
        limit,
        offset,
        order: [['created_at', 'DESC']]
      });
      return { uploads: rows, count, limit, offset };
    } catch (error) {
      throw new Error(`Failed to get user file uploads: ${error.message}`);
    }
  }

  async updateUploadStatus(id, status, additionalData = {}) {
    try {
      const upload = await this.getFileUploadById(id);
      const updateData = { uploadStatus: status, ...additionalData };
      const updatedUpload = await upload.update(updateData);
      return updatedUpload;
    } catch (error) {
      throw new Error(`Failed to update upload status: ${error.message}`);
    }
  }

  async updateProcessingStatus(id, status, additionalData = {}) {
    try {
      const upload = await this.getFileUploadById(id);
      const updateData = { processingStatus: status, ...additionalData };
      const updatedUpload = await upload.update(updateData);
      return updatedUpload;
    } catch (error) {
      throw new Error(`Failed to update processing status: ${error.message}`);
    }
  }

  async saveFileToDisk(file, uploadDir = 'uploads') {
    try {
      // Ensure upload directory exists
      await fs.mkdir(uploadDir, { recursive: true });
      
      // Generate unique filename
      const timestamp = Date.now();
      const uniqueFileName = `${timestamp}-${file.originalname}`;
      const filePath = path.join(uploadDir, uniqueFileName);
      
      // Save file to disk
      await fs.writeFile(filePath, file.buffer);
      
      return {
        fileName: uniqueFileName,
        originalName: file.originalname,
        filePath: filePath,
        fileSize: file.size,
        mimeType: file.mimetype
      };
    } catch (error) {
      throw new Error(`Failed to save file to disk: ${error.message}`);
    }
  }
}

module.exports = new FileUploadService();