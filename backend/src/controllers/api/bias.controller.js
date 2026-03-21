const biasService = require('../../services/api/bias.service');

class BiasController {
  /**
   * Bias Analysis Endpoints
   */
  async analyzeBias(req, res) {
    try {
      const analysis = await biasService.analyzeBias(req.body);
      res.status(201).json({
        success: true,
        message: 'Bias analysis completed successfully',
        data: analysis
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  async listBiasAnalyses(req, res) {
    try {
      const analyses = await biasService.listBiasAnalyses(req.query);
      res.status(200).json({
        success: true,
        data: analyses
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }

  async getBiasAnalysis(req, res) {
    try {
      const { id } = req.params;
      const analysis = await biasService.getBiasAnalysis(id);
      res.status(200).json({
        success: true,
        data: analysis
      });
    } catch (error) {
      res.status(404).json({
        success: false,
        message: error.message
      });
    }
  }

  /**
   * Bias Reports Endpoints
   */
  async listBiasReports(req, res) {
    try {
      const reports = await biasService.listBiasReports(req.query);
      res.status(200).json({
        success: true,
        data: reports
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }

  async getBiasReport(req, res) {
    try {
      const { id } = req.params;
      const report = await biasService.getBiasReport(id);
      res.status(200).json({
        success: true,
        data: report
      });
    } catch (error) {
      res.status(404).json({
        success: false,
        message: error.message
      });
    }
  }

  /**
   * Bias Mitigation Endpoints
   */
  async listMitigationStrategies(req, res) {
    try {
      const strategies = await biasService.listMitigationStrategies(req.query);
      res.status(200).json({
        success: true,
        data: strategies
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }

  async applyMitigation(req, res) {
    try {
      const result = await biasService.applyMitigation(req.body);
      res.status(200).json({
        success: true,
        message: 'Mitigation applied successfully',
        data: result
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  async getMitiagationStrategy(req, res) {
    try {
      const { id } = req.params;
      const strategy = await biasService.getMitiagationStrategy(id);
      res.status(200).json({
        success: true,
        data: strategy
      });
    } catch (error) {
      res.status(404).json({
        success: false,
        message: error.message
      });
    }
  }

  /**
   * Model Upload Endpoint
   */
  async uploadModel(req, res) {
    try {
      // Check if file was uploaded
      if (!req.file) {
        return res.status(400).json({
          success: false,
          message: 'No file uploaded'
        });
      }
      
      // Handle file upload
      const model = await biasService.uploadModel(req.file, req.body);
      res.status(201).json({
        success: true,
        message: 'Model uploaded successfully',
        data: model
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  /**
   * Bias Scoring Endpoint
   */
  async getBiasScores(req, res) {
    try {
      const scores = await biasService.getBiasScores(req.query);
      res.status(200).json({
        success: true,
        data: scores
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }

  /**
   * Visualization Data Endpoint
   */
  async getVisualizationData(req, res) {
    try {
      const data = await biasService.getVisualizationData(req.query);
      res.status(200).json({
        success: true,
        data: data
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }

  /**
   * Fairness Metrics Endpoint
   */
  async getFairnessMetrics(req, res) {
    try {
      const { id } = req.params;
      const metrics = await biasService.getFairnessMetrics(id);
      res.status(200).json({
        success: true,
        data: metrics
      });
    } catch (error) {
      res.status(404).json({
        success: false,
        message: error.message
      });
    }
  }

  /**
   * Explainability Endpoint (SHAP/LIME)
   */
  async getExplanation(req, res) {
    try {
      const { analysis_id, explainer_type } = req.body;
      const explanation = await biasService.getExplanation(analysis_id, explainer_type);
      res.status(200).json({
        success: true,
        data: explanation
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }
}

module.exports = new BiasController();