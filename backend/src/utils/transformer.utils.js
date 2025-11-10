/**
 * Transformer Utilities for AI/ML Service
 * Handles transformation of requests and responses between internal format and AI/ML service format
 */

class TransformerUtils {
  /**
   * Transform regulatory data for compliance analysis
   * @param {Object} internalData - Internal regulatory data format
   * @returns {Object} Transformed data for AI/ML service
   */
  static transformComplianceData(internalData) {
    return {
      document_id: internalData.id,
      document_title: internalData.title,
      document_content: internalData.content,
      document_type: internalData.type,
      jurisdiction: internalData.jurisdiction,
      effective_date: internalData.effectiveDate,
      created_at: internalData.createdAt,
      metadata: internalData.metadata || {},
      related_documents: internalData.relatedDocuments || [],
    };
  }

  /**
   * Transform compliance analysis results to internal format
   * @param {Object} aiMlResponse - AI/ML service response
   * @returns {Object} Transformed results in internal format
   */
  static transformComplianceResults(aiMlResponse) {
    return {
      analysisId: aiMlResponse.analysis_id,
      documentId: aiMlResponse.document_id,
      complianceScore: aiMlResponse.compliance_score,
      violations: aiMlResponse.violations || [],
      recommendations: aiMlResponse.recommendations || [],
      riskLevel: aiMlResponse.risk_level,
      confidence: aiMlResponse.confidence,
      analyzedAt: aiMlResponse.analyzed_at,
      processingTime: aiMlResponse.processing_time,
    };
  }

  /**
   * Transform financial data for risk assessment
   * @param {Object} internalData - Internal financial data format
   * @returns {Object} Transformed data for AI/ML service
   */
  static transformRiskData(internalData) {
    return {
      company_id: internalData.companyId,
      financial_data: {
        revenue: internalData.revenue,
        expenses: internalData.expenses,
        assets: internalData.assets,
        liabilities: internalData.liabilities,
        cash_flow: internalData.cashFlow,
        debt_ratio: internalData.debtRatio,
        current_ratio: internalData.currentRatio,
        roe: internalData.roe,
        roa: internalData.roa,
      },
      market_data: {
        stock_price: internalData.stockPrice,
        market_cap: internalData.marketCap,
        pe_ratio: internalData.peRatio,
        beta: internalData.beta,
      },
      time_period: internalData.timePeriod,
      industry: internalData.industry,
      created_at: internalData.createdAt,
    };
  }

  /**
   * Transform risk assessment results to internal format
   * @param {Object} aiMlResponse - AI/ML service response
   * @returns {Object} Transformed results in internal format
   */
  static transformRiskResults(aiMlResponse) {
    return {
      assessmentId: aiMlResponse.assessment_id,
      companyId: aiMlResponse.company_id,
      overallRiskScore: aiMlResponse.overall_risk_score,
      financialRisk: aiMlResponse.financial_risk,
      marketRisk: aiMlResponse.market_risk,
      operationalRisk: aiMlResponse.operational_risk,
      creditRisk: aiMlResponse.credit_risk,
      liquidityRisk: aiMlResponse.liquidity_risk,
      recommendations: aiMlResponse.recommendations || [],
      confidence: aiMlResponse.confidence,
      assessedAt: aiMlResponse.assessed_at,
      processingTime: aiMlResponse.processing_time,
    };
  }

  /**
   * Transform market data for sentiment analysis
   * @param {Object} internalData - Internal market data format
   * @returns {Object} Transformed data for AI/ML service
   */
  static transformSentimentData(internalData) {
    return {
      source_id: internalData.sourceId,
      content: internalData.content,
      source_type: internalData.sourceType,
      timestamp: internalData.timestamp,
      language: internalData.language || 'en',
      metadata: internalData.metadata || {},
    };
  }

  /**
   * Transform sentiment analysis results to internal format
   * @param {Object} aiMlResponse - AI/ML service response
   * @returns {Object} Transformed results in internal format
   */
  static transformSentimentResults(aiMlResponse) {
    return {
      analysisId: aiMlResponse.analysis_id,
      sourceId: aiMlResponse.source_id,
      sentiment: aiMlResponse.sentiment,
      sentimentScore: aiMlResponse.sentiment_score,
      positiveScore: aiMlResponse.positive_score,
      negativeScore: aiMlResponse.negative_score,
      neutralScore: aiMlResponse.neutral_score,
      keyTopics: aiMlResponse.key_topics || [],
      entities: aiMlResponse.entities || [],
      confidence: aiMlResponse.confidence,
      analyzedAt: aiMlResponse.analyzed_at,
      processingTime: aiMlResponse.processing_time,
    };
  }

  /**
   * Transform data for anomaly detection
   * @param {Object} internalData - Internal data format
   * @returns {Object} Transformed data for AI/ML service
   */
  static transformAnomalyData(internalData) {
    return {
      dataset_id: internalData.datasetId,
      data_points: internalData.dataPoints.map(point => ({
        id: point.id,
        timestamp: point.timestamp,
        values: point.values,
        metadata: point.metadata || {},
      })),
      detection_parameters: internalData.detectionParameters || {},
      created_at: internalData.createdAt,
    };
  }

  /**
   * Transform anomaly detection results to internal format
   * @param {Object} aiMlResponse - AI/ML service response
   * @returns {Object} Transformed results in internal format
   */
  static transformAnomalyResults(aiMlResponse) {
    return {
      detectionId: aiMlResponse.detection_id,
      datasetId: aiMlResponse.dataset_id,
      anomalies: aiMlResponse.anomalies.map(anomaly => ({
        dataPointId: anomaly.data_point_id,
        timestamp: anomaly.timestamp,
        anomalyScore: anomaly.anomaly_score,
        isAnomaly: anomaly.is_anomaly,
        features: anomaly.features || {},
        explanation: anomaly.explanation || '',
      })),
      totalAnomalies: aiMlResponse.total_anomalies,
      confidence: aiMlResponse.confidence,
      detectedAt: aiMlResponse.detected_at,
      processingTime: aiMlResponse.processing_time,
    };
  }

  /**
   * Validate input data before transformation
   * @param {Object} data - Data to validate
   * @param {string} type - Type of data (compliance, risk, sentiment, anomaly)
   * @returns {Object} Validation result
   */
  static validateInputData(data, type) {
    const errors = [];
    
    switch (type) {
      case 'compliance':
        if (!data.id) errors.push('Document ID is required');
        if (!data.content) errors.push('Document content is required');
        break;
      case 'risk':
        if (!data.companyId) errors.push('Company ID is required');
        if (!data.revenue) errors.push('Revenue data is required');
        break;
      case 'sentiment':
        if (!data.content) errors.push('Content is required');
        if (!data.sourceId) errors.push('Source ID is required');
        break;
      case 'anomaly':
        if (!data.datasetId) errors.push('Dataset ID is required');
        if (!data.dataPoints || !Array.isArray(data.dataPoints)) {
          errors.push('Data points array is required');
        }
        break;
      default:
        errors.push('Invalid data type specified');
    }
    
    return {
      isValid: errors.length === 0,
      errors,
    };
  }
}

module.exports = TransformerUtils;