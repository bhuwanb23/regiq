const fs = require('fs');
const path = require('path');
const sequelize = require('../config/database');

// Initialize models
const modelDefiners = [
  require('./user'),
  require('./regulatoryDocument'),
  require('./complianceResult'),
  require('./regulatoryAlert'),
  require('./documentVersion'),
  require('./documentMetadata'),
  require('./documentShare'),
  require('./analysisResult'),
  require('./modelAnalysis'),
  require('./dataBiasDetection'),
  require('./mitigationRecommendation'),
  require('./biasResult'),
  require('./biasTrend'),
  require('./comparisonReport'),
  require('./biasSchedule'),
  require('./biasNotification'),
  require('./riskSimulation'),
  require('./riskScenario'),
  require('./riskAlert'),
  require('./riskVisualization'),
  require('./riskSchedule'),
  require('./riskComparison'),
  require('./report'),
  require('./dataPipelineJob'),
  require('./alert'),
  require('./auditLog'),
  require('./reportTemplate'),
  require('./reportGeneration'),
  require('./reportSchedule'),
  require('./reportDistribution'),
  require('./reportVersion'),
  require('./reportAnalytics'),
  require('./dataValidationRule'),
  require('./dataQualityMetric'),
  require('./dataLineage'),
  require('./fileUpload')
];

// We define all models according to their files.
const models = {};
for (const modelDefiner of modelDefiners) {
  const model = modelDefiner(sequelize, sequelize.constructor);
  models[model.name] = model;
}

// Apply associations if any
Object.keys(models).forEach(modelName => {
  if (models[modelName].associate) {
    models[modelName].associate(models);
  }
});

// Export models and sequelize instance
module.exports = {
  ...models,
  sequelize,
  Sequelize: sequelize.constructor
};