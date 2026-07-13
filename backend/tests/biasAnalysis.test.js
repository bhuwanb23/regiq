const request = require('supertest');
const app = require('../src/server');

describe('Bias Analysis API', () => {
  const testModelId = 'test-model-id';
  const testDatasetId = 'test-dataset-id';

  describe('Model Bias Analysis Endpoints', () => {
    it('should analyze a model for bias', async () => {
      const modelData = {
        modelId: testModelId,
        modelName: 'Test Model',
        modelType: 'classification',
        framework: 'tensorflow',
        version: '1.0.0',
        targetVariable: 'income',
        protectedAttributes: ['gender', 'race'],
        trainingDataSize: 10000,
        demographicParityDifference: 0.15,
        equalOpportunityDifference: 0.12
      };

      const res = await request(app)
        .post('/bias/analysis/model')
        .send(modelData)
        .expect(201);

      expect(res.body.success).toBe(true);
      expect(res.body.data.modelId).toBe(testModelId);
    });

    it('should get a specific model analysis', async () => {
      // First create a model analysis
      const modelData = {
        modelId: testModelId,
        modelName: 'Test Model',
        modelType: 'classification',
        framework: 'tensorflow',
        version: '1.0.0',
        targetVariable: 'income',
        protectedAttributes: ['gender', 'race'],
        trainingDataSize: 10000
      };

      const createRes = await request(app)
        .post('/bias/analysis/model')
        .send(modelData);

      const analysisId = createRes.body.data.id;

      // Then get it
      const res = await request(app)
        .get(`/bias/analysis/model/${analysisId}`)
        .expect(200);

      expect(res.body.success).toBe(true);
      expect(res.body.data.id).toBe(analysisId);
    });

    it('should list model analyses', async () => {
      const res = await request(app)
        .get('/bias/analysis/model')
        .expect(200);

      expect(res.body.success).toBe(true);
      expect(Array.isArray(res.body.data)).toBe(true);
    });

    it('should delete a model analysis', async () => {
      // First create a model analysis
      const modelData = {
        modelId: testModelId,
        modelName: 'Test Model',
        modelType: 'classification',
        framework: 'tensorflow',
        version: '1.0.0',
        targetVariable: 'income',
        protectedAttributes: ['gender', 'race']
      };

      const createRes = await request(app)
        .post('/bias/analysis/model')
        .send(modelData);

      const analysisId = createRes.body.data.id;

      // Then delete it
      const res = await request(app)
        .delete(`/bias/analysis/model/${analysisId}`)
        .expect(200);

      expect(res.body.success).toBe(true);
    });
  });

  describe('Data Bias Detection Services', () => {
    it('should detect bias in datasets', async () => {
      const datasetData = {
        datasetId: testDatasetId,
        datasetName: 'Test Dataset',
        fileType: 'csv',
        fileSize: 1024,
        rowCount: 1000,
        columnCount: 10,
        protectedAttributes: ['gender', 'age'],
        severityScore: 0.75
      };

      const res = await request(app)
        .post('/bias/detection/data')
        .send(datasetData)
        .expect(201);

      expect(res.body.success).toBe(true);
      expect(res.body.data.datasetId).toBe(testDatasetId);
    });

    it('should get a specific data bias detection result', async () => {
      // First create a data bias detection
      const datasetData = {
        datasetId: testDatasetId,
        datasetName: 'Test Dataset',
        fileType: 'csv',
        fileSize: 1024,
        rowCount: 1000,
        columnCount: 10,
        protectedAttributes: ['gender', 'age']
      };

      const createRes = await request(app)
        .post('/bias/detection/data')
        .send(datasetData);

      const detectionId = createRes.body.data.id;

      // Then get it
      const res = await request(app)
        .get(`/bias/detection/data/${detectionId}`)
        .expect(200);

      expect(res.body.success).toBe(true);
      expect(res.body.data.id).toBe(detectionId);
    });

    it('should list data bias detections', async () => {
      const res = await request(app)
        .get('/bias/detection/data')
        .expect(200);

      expect(res.body.success).toBe(true);
      expect(Array.isArray(res.body.data)).toBe(true);
    });

    it('should perform batch data bias detection', async () => {
      const batchData = {
        datasets: [
          {
            datasetId: 'dataset-1',
            datasetName: 'Dataset 1',
            fileType: 'csv',
            protectedAttributes: ['gender']
          },
          {
            datasetId: 'dataset-2',
            datasetName: 'Dataset 2',
            fileType: 'json',
            protectedAttributes: ['race']
          }
        ]
      };

      const res = await request(app)
        .post('/bias/detection/data/batch')
        .send(batchData)
        .expect(201);

      expect(res.body.success).toBe(true);
      expect(Array.isArray(res.body.data)).toBe(true);
      expect(res.body.data.length).toBe(2);
    });
  });

  describe('Bias Mitigation Recommendations', () => {
    it('should get mitigation recommendations', async () => {
      // First create a model analysis to get recommendations for
      const modelData = {
        modelId: testModelId,
        modelName: 'Test Model',
        modelType: 'classification',
        framework: 'tensorflow',
        version: '1.0.0',
        targetVariable: 'income',
        protectedAttributes: ['gender', 'race']
      };

      const createRes = await request(app)
        .post('/bias/analysis/model')
        .send(modelData);

      const analysisId = createRes.body.data.id;

      // Then get recommendations
      const res = await request(app)
        .get(`/bias/mitigation/${analysisId}`)
        .expect(200);

      expect(res.body.success).toBe(true);
      expect(Array.isArray(res.body.data)).toBe(true);
    });

    it('should apply mitigation techniques', async () => {
      const mitigationData = {
        technique: 'reweighing',
        parameters: {
          sensitive_attribute: 'gender'
        }
      };

      const res = await request(app)
        .post('/bias/mitigation/apply/test-analysis-id')
        .send(mitigationData)
        .expect(200);

      expect(res.body.success).toBe(true);
    });

    it('should get mitigation templates', async () => {
      const res = await request(app)
        .get('/bias/mitigation/templates')
        .expect(200);

      expect(res.body.success).toBe(true);
      expect(Array.isArray(res.body.data)).toBe(true);
    });
  });

  describe('Bias Analysis Result Storage', () => {
    it('should store bias analysis results', async () => {
      const resultData = {
        analysisId: 'test-analysis-id',
        analysisType: 'model',
        entityId: testModelId,
        entityType: 'model',
        overallScore: 0.75,
        demographicParity: 0.15
      };

      const res = await request(app)
        .post('/bias/results')
        .send(resultData)
        .expect(201);

      expect(res.body.success).toBe(true);
      expect(res.body.data.analysisId).toBe('test-analysis-id');
    });

    it('should retrieve bias analysis results', async () => {
      // First store results
      const resultData = {
        analysisId: 'test-analysis-id',
        analysisType: 'model',
        entityId: testModelId,
        entityType: 'model',
        overallScore: 0.75
      };

      const createRes = await request(app)
        .post('/bias/results')
        .send(resultData);

      const resultId = createRes.body.data.id;

      // Then retrieve them
      const res = await request(app)
        .get(`/bias/results/${resultId}`)
        .expect(200);

      expect(res.body.success).toBe(true);
      expect(res.body.data.id).toBe(resultId);
    });

    it('should list bias analysis results', async () => {
      const res = await request(app)
        .get('/bias/results')
        .expect(200);

      expect(res.body.success).toBe(true);
      expect(Array.isArray(res.body.data)).toBe(true);
    });
  });

  describe('Bias Trend Monitoring', () => {
    it('should get bias trends', async () => {
      const res = await request(app)
        .get('/bias/trends')
        .expect(200);

      expect(res.body.success).toBe(true);
      expect(Array.isArray(res.body.data)).toBe(true);
    });

    it('should get trends for specific model', async () => {
      const res = await request(app)
        .get(`/bias/trends/model/${testModelId}`)
        .expect(200);

      expect(res.body.success).toBe(true);
      expect(Array.isArray(res.body.data)).toBe(true);
    });

    it('should create trend monitoring alerts', async () => {
      const alertData = {
        modelId: testModelId,
        modelName: 'Test Model',
        metricType: 'demographic_parity',
        metricValue: 0.15,
        threshold: 0.10,
        alertSeverity: 'high'
      };

      const res = await request(app)
        .post('/bias/trends/alerts')
        .send(alertData)
        .expect(201);

      expect(res.body.success).toBe(true);
      expect(res.body.data.modelId).toBe(testModelId);
    });
  });

  describe('Bias Comparison Reports', () => {
    it('should generate comparison reports', async () => {
      const reportData = {
        reportName: 'Model Comparison Report',
        comparisonType: 'model',
        modelsCompared: ['model-1', 'model-2'],
        metricsCompared: ['demographic_parity', 'equal_opportunity']
      };

      const res = await request(app)
        .post('/bias/reports/compare')
        .send(reportData)
        .expect(201);

      expect(res.body.success).toBe(true);
      expect(res.body.data.reportName).toBe('Model Comparison Report');
    });

    it('should get specific comparison report', async () => {
      // First generate a report
      const reportData = {
        reportName: 'Model Comparison Report',
        comparisonType: 'model',
        modelsCompared: ['model-1', 'model-2']
      };

      const createRes = await request(app)
        .post('/bias/reports/compare')
        .send(reportData);

      const reportId = createRes.body.data.id;

      // Then get it
      const res = await request(app)
        .get(`/bias/reports/compare/${reportId}`)
        .expect(200);

      expect(res.body.success).toBe(true);
      expect(res.body.data.id).toBe(reportId);
    });

    it('should list comparison reports', async () => {
      const res = await request(app)
        .get('/bias/reports/compare')
        .expect(200);

      expect(res.body.success).toBe(true);
      expect(Array.isArray(res.body.data)).toBe(true);
    });
  });

  describe('Bias Analysis Scheduling', () => {
    it('should schedule bias analysis', async () => {
      const scheduleData = {
        scheduleName: 'Weekly Model Analysis',
        analysisType: 'model',
        entityId: testModelId,
        entityType: 'model',
        scheduleType: 'recurring',
        frequency: 'weekly',
        cronExpression: '0 0 * * 0'
      };

      const res = await request(app)
        .post('/bias/schedule')
        .send(scheduleData)
        .expect(201);

      expect(res.body.success).toBe(true);
      expect(res.body.data.scheduleName).toBe('Weekly Model Analysis');
    });

    it('should get scheduled analysis', async () => {
      // First schedule analysis
      const scheduleData = {
        scheduleName: 'Daily Dataset Analysis',
        analysisType: 'data',
        entityId: testDatasetId,
        entityType: 'dataset',
        scheduleType: 'recurring',
        frequency: 'daily'
      };

      const createRes = await request(app)
        .post('/bias/schedule')
        .send(scheduleData);

      const scheduleId = createRes.body.data.id;

      // Then get it
      const res = await request(app)
        .get(`/bias/schedule/${scheduleId}`)
        .expect(200);

      expect(res.body.success).toBe(true);
      expect(res.body.data.id).toBe(scheduleId);
    });

    it('should list scheduled analyses', async () => {
      const res = await request(app)
        .get('/bias/schedule')
        .expect(200);

      expect(res.body.success).toBe(true);
      expect(Array.isArray(res.body.data)).toBe(true);
    });

    it('should update scheduled analysis', async () => {
      // First schedule analysis
      const scheduleData = {
        scheduleName: 'Monthly Analysis',
        analysisType: 'model',
        entityId: testModelId,
        entityType: 'model',
        scheduleType: 'recurring',
        frequency: 'monthly'
      };

      const createRes = await request(app)
        .post('/bias/schedule')
        .send(scheduleData);

      const scheduleId = createRes.body.data.id;

      // Then update it
      const updateData = {
        frequency: 'weekly'
      };

      const res = await request(app)
        .put(`/bias/schedule/${scheduleId}`)
        .send(updateData)
        .expect(200);

      expect(res.body.success).toBe(true);
    });

    it('should cancel scheduled analysis', async () => {
      // First schedule analysis
      const scheduleData = {
        scheduleName: 'Test Schedule',
        analysisType: 'model',
        entityId: testModelId,
        entityType: 'model',
        scheduleType: 'recurring'
      };

      const createRes = await request(app)
        .post('/bias/schedule')
        .send(scheduleData);

      const scheduleId = createRes.body.data.id;

      // Then cancel it
      const res = await request(app)
        .delete(`/bias/schedule/${scheduleId}`)
        .expect(200);

      expect(res.body.success).toBe(true);
    });
  });

  describe('Bias Analysis Notifications', () => {
    it('should create notification rules', async () => {
      const notificationData = {
        notificationName: 'High Bias Alert',
        triggerType: 'metric_threshold',
        triggerCondition: {
          metric: 'demographic_parity',
          operator: '>',
          threshold: 0.1
        },
        recipients: ['admin@example.com'],
        notificationType: 'email'
      };

      const res = await request(app)
        .post('/bias/notifications')
        .send(notificationData)
        .expect(201);

      expect(res.body.success).toBe(true);
      expect(res.body.data.notificationName).toBe('High Bias Alert');
    });

    it('should get notification rule', async () => {
      // First create notification rule
      const notificationData = {
        notificationName: 'Test Notification',
        triggerType: 'metric_threshold',
        triggerCondition: {
          metric: 'equal_opportunity',
          operator: '>',
          threshold: 0.05
        },
        recipients: ['user@example.com']
      };

      const createRes = await request(app)
        .post('/bias/notifications')
        .send(notificationData);

      const notificationId = createRes.body.data.id;

      // Then get it
      const res = await request(app)
        .get(`/bias/notifications/${notificationId}`)
        .expect(200);

      expect(res.body.success).toBe(true);
      expect(res.body.data.id).toBe(notificationId);
    });

    it('should list notification rules', async () => {
      const res = await request(app)
        .get('/bias/notifications')
        .expect(200);

      expect(res.body.success).toBe(true);
      expect(Array.isArray(res.body.data)).toBe(true);
    });

    it('should update notification rule', async () => {
      // First create notification rule
      const notificationData = {
        notificationName: 'Update Test',
        triggerType: 'metric_threshold',
        triggerCondition: {
          metric: 'disparate_impact',
          operator: '<',
          threshold: 0.8
        },
        recipients: ['test@example.com']
      };

      const createRes = await request(app)
        .post('/bias/notifications')
        .send(notificationData);

      const notificationId = createRes.body.data.id;

      // Then update it
      const updateData = {
        recipients: ['updated@example.com']
      };

      const res = await request(app)
        .put(`/bias/notifications/${notificationId}`)
        .send(updateData)
        .expect(200);

      expect(res.body.success).toBe(true);
    });

    it('should delete notification rule', async () => {
      // First create notification rule
      const notificationData = {
        notificationName: 'Delete Test',
        triggerType: 'metric_threshold',
        triggerCondition: {
          metric: 'statistical_parity',
          operator: '>',
          threshold: 0.1
        },
        recipients: ['delete@example.com']
      };

      const createRes = await request(app)
        .post('/bias/notifications')
        .send(notificationData);

      const notificationId = createRes.body.data.id;

      // Then delete it
      const res = await request(app)
        .delete(`/bias/notifications/${notificationId}`)
        .expect(200);

      expect(res.body.success).toBe(true);
    });
  });
});