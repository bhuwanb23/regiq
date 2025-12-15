const multer = require('multer');
const path = require('path');

// Configure storage
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, 'uploads/');
  },
  filename: (req, file, cb) => {
    const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
    cb(null, file.fieldname + '-' + uniqueSuffix + path.extname(file.originalname));
  }
});

// File filter to allow only model files
const fileFilter = (req, file, cb) => {
  // Allow model files
  if (file.mimetype === 'application/octet-stream' || 
      file.mimetype === 'application/json' ||
      file.mimetype === 'text/plain' ||
      file.originalname.endsWith('.h5') ||
      file.originalname.endsWith('.pkl') ||
      file.originalname.endsWith('.joblib') ||
      file.originalname.endsWith('.pt') ||
      file.originalname.endsWith('.pth') ||
      file.originalname.endsWith('.onnx')) {
    cb(null, true);
  } else {
    cb(new Error('Invalid file type. Only model files are allowed.'), false);
  }
};

// Create upload middleware
const upload = multer({ 
  storage: storage,
  fileFilter: fileFilter,
  limits: {
    fileSize: 100 * 1024 * 1024 // 100MB limit
  }
});

module.exports = upload;