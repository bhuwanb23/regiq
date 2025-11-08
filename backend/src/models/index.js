const fs = require('fs');
const path = require('path');
const sequelize = require('../config/database');

// Initialize models
const modelDefiners = [
  require('./user'),
  require('./regulatoryDocument'),
  require('./modelAnalysis'),
  require('./riskSimulation'),
  require('./report'),
  require('./dataPipelineJob'),
  require('./alert'),
  require('./auditLog')
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