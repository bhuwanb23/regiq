const { DataQualityMetric } = require('../models');

class PreprocessingService {
  async cleanData(data, cleaningRules = {}) {
    try {
      const cleanedData = [];
      const qualityMetrics = {
        totalRecords: data.length,
        cleanedRecords: 0,
        errorRecords: 0,
        transformations: []
      };

      for (const record of data) {
        try {
          const cleanedRecord = this.applyCleaningRules(record, cleaningRules);
          cleanedData.push(cleanedRecord);
          qualityMetrics.cleanedRecords++;
          qualityMetrics.transformations.push({
            recordId: record.id || null,
            transformationsApplied: Object.keys(cleaningRules).length
          });
        } catch (error) {
          qualityMetrics.errorRecords++;
          console.error(`Error cleaning record: ${error.message}`);
        }
      }

      return {
        cleanedData,
        qualityMetrics
      };
    } catch (error) {
      throw new Error(`Failed to clean data: ${error.message}`);
    }
  }

  applyCleaningRules(record, cleaningRules) {
    const cleanedRecord = { ...record };

    for (const [fieldName, rules] of Object.entries(cleaningRules)) {
      if (cleanedRecord[fieldName] !== undefined) {
        for (const rule of rules) {
          switch (rule.type) {
            case 'trim':
              if (typeof cleanedRecord[fieldName] === 'string') {
                cleanedRecord[fieldName] = cleanedRecord[fieldName].trim();
              }
              break;
              
            case 'toLowerCase':
              if (typeof cleanedRecord[fieldName] === 'string') {
                cleanedRecord[fieldName] = cleanedRecord[fieldName].toLowerCase();
              }
              break;
              
            case 'toUpperCase':
              if (typeof cleanedRecord[fieldName] === 'string') {
                cleanedRecord[fieldName] = cleanedRecord[fieldName].toUpperCase();
              }
              break;
              
            case 'removeSpecialChars':
              if (typeof cleanedRecord[fieldName] === 'string') {
                cleanedRecord[fieldName] = cleanedRecord[fieldName].replace(/[^a-zA-Z0-9\s]/g, '');
              }
              break;
              
            case 'defaultValue':
              if (cleanedRecord[fieldName] === null || cleanedRecord[fieldName] === undefined || cleanedRecord[fieldName] === '') {
                cleanedRecord[fieldName] = rule.value;
              }
              break;
              
            case 'dateFormat':
              // This would require a more complex implementation with date parsing
              break;
              
            default:
              // Custom rule handling
              break;
          }
        }
      }
    }

    return cleanedRecord;
  }

  async transformData(data, transformations = {}) {
    try {
      const transformedData = [];
      
      for (const record of data) {
        const transformedRecord = this.applyTransformations(record, transformations);
        transformedData.push(transformedRecord);
      }

      return transformedData;
    } catch (error) {
      throw new Error(`Failed to transform data: ${error.message}`);
    }
  }

  applyTransformations(record, transformations) {
    const transformedRecord = { ...record };

    for (const [targetField, transformation] of Object.entries(transformations)) {
      switch (transformation.type) {
        case 'combine':
          // Combine multiple fields
          const combinedValue = transformation.fields
            .map(field => record[field] || '')
            .join(transformation.separator || ' ');
          transformedRecord[targetField] = combinedValue;
          break;
          
        case 'extract':
          // Extract part of a field (e.g., domain from email)
          if (transformation.field && record[transformation.field]) {
            if (transformation.pattern) {
              const regex = new RegExp(transformation.pattern);
              const match = record[transformation.field].match(regex);
              transformedRecord[targetField] = match ? match[1] : null;
            }
          }
          break;
          
        case 'calculate':
          // Perform calculations
          if (transformation.operation && transformation.fields) {
            const values = transformation.fields.map(field => parseFloat(record[field]) || 0);
            switch (transformation.operation) {
              case 'sum':
                transformedRecord[targetField] = values.reduce((a, b) => a + b, 0);
                break;
              case 'average':
                transformedRecord[targetField] = values.reduce((a, b) => a + b, 0) / values.length;
                break;
              case 'multiply':
                transformedRecord[targetField] = values.reduce((a, b) => a * b, 1);
                break;
            }
          }
          break;
          
        default:
          // Custom transformation
          break;
      }
    }

    return transformedRecord;
  }

  async standardizeData(data, standardizationRules = {}) {
    try {
      const standardizedData = [];
      
      for (const record of data) {
        const standardizedRecord = this.applyStandardization(record, standardizationRules);
        standardizedData.push(standardizedRecord);
      }

      return standardizedData;
    } catch (error) {
      throw new Error(`Failed to standardize data: ${error.message}`);
    }
  }

  applyStandardization(record, standardizationRules) {
    const standardizedRecord = { ...record };

    for (const [fieldName, rules] of Object.entries(standardizationRules)) {
      if (standardizedRecord[fieldName] !== undefined) {
        for (const rule of rules) {
          switch (rule.type) {
            case 'normalize':
              // Normalize values to a standard format
              if (rule.mapping && rule.mapping[standardizedRecord[fieldName]] !== undefined) {
                standardizedRecord[fieldName] = rule.mapping[standardizedRecord[fieldName]];
              }
              break;
              
            case 'categorize':
              // Categorize values based on rules
              if (rule.categories) {
                for (const [category, values] of Object.entries(rule.categories)) {
                  if (values.includes(standardizedRecord[fieldName])) {
                    standardizedRecord[fieldName] = category;
                    break;
                  }
                }
              }
              break;
              
            default:
              // Custom standardization
              break;
          }
        }
      }
    }

    return standardizedRecord;
  }
}

module.exports = new PreprocessingService();