const fs = require('fs');
const path = require('path');

const migrationsDir = path.join(__dirname, '..', 'migrations');

// Define the column mappings for each table
const columnMappings = {
  'data_bias_detections': {
    'datasetId': 'dataset_id',
    'datasetName': 'dataset_name',
    'fileType': 'file_type',
    'fileSize': 'file_size',
    'rowCount': 'row_count',
    'columnCount': 'column_count',
    'protectedAttributes': 'protected_attributes',
    'biasMetrics': 'bias_metrics',
    'representationBias': 'representation_bias',
    'measurementBias': 'measurement_bias',
    'evaluationBias': 'evaluation_bias',
    'historicalBias': 'historical_bias',
    'aggregationBias': 'aggregation_bias',
    'selectionBias': 'selection_bias',
    'survivorshipBias': 'survivorship_bias',
    'severityScore': 'severity_score',
    'analysisParameters': 'analysis_parameters',
    'createdAt': 'created_at',
    'updatedAt': 'updated_at'
  },
  'mitigation_recommendations': {
    'analysisId': 'analysis_id',
    'analysisType': 'analysis_type',
    'biasType': 'bias_type',
    'recommendationType': 'recommendation_type',
    'implementationSteps': 'implementation_steps',
    'expectedImpact': 'expected_impact',
    'confidenceScore': 'confidence_score',
    'estimatedEffort': 'estimated_effort',
    'createdAt': 'created_at',
    'updatedAt': 'updated_at'
  },
  'bias_results': {
    'analysisId': 'analysis_id',
    'entityId': 'entity_id',
    'entityType': 'entity_type',
    'biasMetrics': 'bias_metrics',
    'demographicParity': 'demographic_parity',
    'equalOpportunity': 'equal_opportunity',
    'disparateImpact': 'disparate_impact',
    'statisticalParity': 'statistical_parity',
    'groupFairness': 'group_fairness',
    'individualFairness': 'individual_fairness',
    'biasCategories': 'bias_categories',
    'confidenceInterval': 'confidence_interval',
    'statisticalSignificance': 'statistical_significance',
    'createdAt': 'created_at',
    'updatedAt': 'updated_at'
  },
  'bias_trends': {
    'modelId': 'model_id',
    'modelName': 'model_name',
    'metricType': 'metric_type',
    'metricValue': 'metric_value',
    'threshold': 'threshold',
    'trendDirection': 'trend_direction',
    'significance': 'significance',
    'timePeriod': 'time_period',
    'periodStart': 'period_start',
    'periodEnd': 'period_end',
    'comparisonBaseline': 'comparison_baseline',
    'variance': 'variance',
    'alertTriggered': 'alert_triggered',
    'alertSeverity': 'alert_severity',
    'createdAt': 'created_at',
    'updatedAt': 'updated_at'
  },
  'comparison_reports': {
    'modelsCompared': 'models_compared',
    'datasetsCompared': 'datasets_compared',
    'metricsCompared': 'metrics_compared',
    'comparisonType': 'comparison_type',
    'timeRange': 'time_range',
    'baselineModelId': 'baseline_model_id',
    'comparisonResults': 'comparison_results',
    'visualizationData': 'visualization_data',
    'reportFormat': 'report_format',
    'generatedBy': 'generated_by',
    'createdAt': 'created_at',
    'updatedAt': 'updated_at'
  },
  'bias_schedules': {
    'scheduleName': 'schedule_name',
    'analysisType': 'analysis_type',
    'entityId': 'entity_id',
    'entityType': 'entity_type',
    'scheduleType': 'schedule_type',
    'cronExpression': 'cron_expression',
    'nextRunTime': 'next_run_time',
    'lastRunTime': 'last_run_time',
    'lastRunStatus': 'last_run_status',
    'notificationEmails': 'notification_emails',
    'createdAt': 'created_at',
    'updatedAt': 'updated_at'
  },
  'bias_notifications': {
    'notificationName': 'notification_name',
    'triggerType': 'trigger_type',
    'triggerCondition': 'trigger_condition',
    'severityThreshold': 'severity_threshold',
    'metricType': 'metric_type',
    'comparisonOperator': 'comparison_operator',
    'notificationType': 'notification_type',
    'notificationTemplate': 'notification_template',
    'lastTriggered': 'last_triggered',
    'cooldownPeriod': 'cooldown_period',
    'createdAt': 'created_at',
    'updatedAt': 'updated_at'
  },
  'model_analyses': {
    'modelId': 'model_id',
    'modelName': 'model_name',
    'modelType': 'model_type',
    'targetVariable': 'target_variable',
    'protectedAttributes': 'protected_attributes',
    'trainingDataSize': 'training_data_size',
    'performanceMetrics': 'performance_metrics',
    'demographicParityDifference': 'demographic_parity_difference',
    'equalOpportunityDifference': 'equal_opportunity_difference',
    'disparateImpact': 'disparate_impact',
    'statisticalParityDifference': 'statistical_parity_difference',
    'consistencyScore': 'consistency_score',
    'featureImportanceBias': 'feature_importance_bias',
    'groupMetrics': 'group_metrics',
    'analysisParameters': 'analysis_parameters',
    'createdAt': 'created_at',
    'updatedAt': 'updated_at'
  }
};

// Read all migration files
const migrationFiles = fs.readdirSync(migrationsDir);

// For each migration file, fix the column names
migrationFiles.forEach(file => {
  if (file.endsWith('.js')) {
    const filePath = path.join(migrationsDir, file);
    let content = fs.readFileSync(filePath, 'utf8');
    
    // Extract table name from file name
    const tableName = file
      .replace(/\d+-create-/, '')
      .replace(/\.js$/, '')
      .replace(/-/g, '_')
      .replace(/s$/, 's'); // Keep pluralization
    
    // Get the column mappings for this table
    const mappings = columnMappings[tableName];
    
    if (mappings) {
      // Replace each column name
      for (const [oldName, newName] of Object.entries(mappings)) {
        const regex = new RegExp(`\\b${oldName}:`, 'g');
        content = content.replace(regex, `${newName}:`);
      }
    }
    
    // Write the fixed content back to the file
    fs.writeFileSync(filePath, content);
    console.log(`Fixed column names in ${file}`);
  }
});

console.log('All migration files fixed!');