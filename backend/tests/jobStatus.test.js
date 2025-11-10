const request = require('supertest');
const app = require('../src/server').app;
const { JobStatus, JobHistory, User } = require('../src/models');
const jobStatusService = require('../src/services/jobStatus.service');
const passwordUtils = require('../src/utils/password.utils');

describe('Job Status API', () => {
  let testJobId;
  let authToken;
  let testUser;

  beforeAll(async () => {
    // Create a test user
    const hashedPassword = await passwordUtils.hashPassword('TestPass123!');
    testUser = await User.create({
      firstName: 'Test',
      lastName: 'User',
      email: 'test.jobstatus@example.com',
      passwordHash: hashedPassword,
      role: 'analyst'
    });

    // Login to get auth token
    const loginRes = await request(app)
      .post('/auth/login')
      .send({
        email: 'test.jobstatus@example.com',
        password: 'TestPass123!'
      });

    authToken = loginRes.body.data.accessToken;

    // Create a test job for testing
    const testJob = await jobStatusService.createJobStatus({
      jobId: 'test-job-' + Date.now(),
      jobType: 'TEST',
      status: 'pending',
      priority: 'normal'
    });
    testJobId = testJob.jobId;
  });

  afterAll(async () => {
    // Clean up test data
    await JobStatus.destroy({ where: { jobId: testJobId } });
    await JobHistory.destroy({ where: { jobId: testJobId } });
    if (testUser) {
      await User.destroy({ where: { id: testUser.id } });
    }
  });

  describe('GET /status/jobs/:jobId', () => {
    it('should get job status by ID', async () => {
      const response = await request(app)
        .get(`/status/jobs/${testJobId}`)
        .set('Authorization', `Bearer ${authToken}`)
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.data.jobId).toBe(testJobId);
      expect(response.body.data.jobType).toBe('TEST');
    });

    it('should return 404 for non-existent job', async () => {
      const response = await request(app)
        .get('/status/jobs/non-existent-job')
        .set('Authorization', `Bearer ${authToken}`)
        .expect(404);

      expect(response.body.success).toBe(false);
    });
  });

  describe('GET /status/jobs', () => {
    it('should get all job statuses with pagination', async () => {
      const response = await request(app)
        .get('/status/jobs')
        .set('Authorization', `Bearer ${authToken}`)
        .query({ page: 1, limit: 10 })
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(Array.isArray(response.body.data)).toBe(true);
    });
  });

  describe('PUT /status/jobs/:jobId/progress', () => {
    it('should update job progress', async () => {
      const response = await request(app)
        .put(`/status/jobs/${testJobId}/progress`)
        .set('Authorization', `Bearer ${authToken}`)
        .send({
          progress: 50,
          stage: 'processing'
        })
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.data.progress).toBe(50);
      expect(response.body.data.stage).toBe('processing');
    });
  });

  describe('PUT /status/jobs/:jobId/cancel', () => {
    it('should cancel a job', async () => {
      const response = await request(app)
        .put(`/status/jobs/${testJobId}/cancel`)
        .set('Authorization', `Bearer ${authToken}`)
        .send({
          reason: 'Test cancellation'
        })
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.data.status).toBe('cancelled');
    });
  });

  describe('GET /status/metrics/performance', () => {
    it('should get performance metrics', async () => {
      const response = await request(app)
        .get('/status/metrics/performance')
        .set('Authorization', `Bearer ${authToken}`)
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.data).toHaveProperty('statusCounts');
    });
  });
});

describe('Job Status Service', () => {
  describe('createJobStatus', () => {
    it('should create a new job status record', async () => {
      const jobData = {
        jobId: 'service-test-job-' + Date.now(),
        jobType: 'SERVICE_TEST',
        status: 'pending'
      };

      const jobStatus = await jobStatusService.createJobStatus(jobData);
      
      expect(jobStatus.jobId).toBe(jobData.jobId);
      expect(jobStatus.jobType).toBe(jobData.jobType);
      expect(jobStatus.status).toBe('pending');
      
      // Clean up
      await JobStatus.destroy({ where: { jobId: jobData.jobId } });
    });
  });

  describe('updateJobStatus', () => {
    let testJob;

    beforeAll(async () => {
      testJob = await jobStatusService.createJobStatus({
        jobId: 'update-test-job-' + Date.now(),
        jobType: 'UPDATE_TEST',
        status: 'pending'
      });
    });

    afterAll(async () => {
      await JobStatus.destroy({ where: { jobId: testJob.jobId } });
    });

    it('should update job status', async () => {
      const updatedJob = await jobStatusService.updateJobStatus(testJob.jobId, {
        status: 'processing',
        progress: 25
      });

      expect(updatedJob.status).toBe('processing');
      expect(updatedJob.progress).toBe(25);
    });
  });

  describe('cancelJob', () => {
    let testJob;

    beforeAll(async () => {
      testJob = await jobStatusService.createJobStatus({
        jobId: 'cancel-test-job-' + Date.now(),
        jobType: 'CANCEL_TEST',
        status: 'processing'
      });
    });

    afterAll(async () => {
      await JobStatus.destroy({ where: { jobId: testJob.jobId } });
    });

    it('should cancel a job', async () => {
      const cancelledJob = await jobStatusService.cancelJob(testJob.jobId, 'Test reason');
      
      expect(cancelledJob.status).toBe('cancelled');
      expect(cancelledJob.errorMessage).toBe('Test reason');
    });
  });
});