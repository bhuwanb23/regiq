const dotenv = require('dotenv');
const Joi = require('joi');

// Load environment variables
dotenv.config();

// Define validation schema
const envSchema = Joi.object({
  NODE_ENV: Joi.string()
    .valid('development', 'production', 'test')
    .default('development'),
  PORT: Joi.number().default(3000),
  DB_HOST: Joi.string().default('localhost'),
  DB_PORT: Joi.number().default(27017),
  DB_NAME: Joi.string().default('regiq_backend'),
  DB_USER: Joi.string().allow('').optional(),
  DB_PASSWORD: Joi.string().allow('').optional(),
  JWT_SECRET: Joi.string().required(),
  JWT_EXPIRES_IN: Joi.string().default('24h'),
  LOG_LEVEL: Joi.string().default('info')
}).unknown();

// Validate environment variables
const { error, value: envVars } = envSchema.validate(process.env);

if (error) {
  throw new Error(`Config validation error: ${error.message}`);
}

module.exports = {
  env: envVars.NODE_ENV,
  port: envVars.PORT,
  mongoose: {
    url: envVars.DB_USER && envVars.DB_PASSWORD
      ? `mongodb://${envVars.DB_USER}:${envVars.DB_PASSWORD}@${envVars.DB_HOST}:${envVars.DB_PORT}/${envVars.DB_NAME}`
      : `mongodb://${envVars.DB_HOST}:${envVars.DB_PORT}/${envVars.DB_NAME}`,
    options: {
      useNewUrlParser: true,
      useUnifiedTopology: true,
    },
  },
  jwt: {
    secret: envVars.JWT_SECRET,
    expiresIn: envVars.JWT_EXPIRES_IN,
  },
  log: {
    level: envVars.LOG_LEVEL,
  },
};