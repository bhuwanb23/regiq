const biasAnalysisController = require('../src/controllers/biasAnalysis.controller');

// Mock request and response objects
const mockReq = {
  query: {},
  params: {}
};

const mockRes = {
  status: function(code) {
    this.statusCode = code;
    return this;
  },
  json: function(data) {
    this.body = data;
    console.log('Response status:', this.statusCode);
    console.log('Response body:', JSON.stringify(data, null, 2));
  }
};

async function testController() {
  try {
    console.log('Testing listModelAnalyses controller...');
    await biasAnalysisController.listModelAnalyses(mockReq, mockRes);
  } catch (error) {
    console.log('Controller test failed:', error.message);
    console.log('Error stack:', error.stack);
  }
}

testController();