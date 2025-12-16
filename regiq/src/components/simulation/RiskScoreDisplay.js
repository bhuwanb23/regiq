import React from 'react';
import { View, Text, StyleSheet, ActivityIndicator } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { COLORS, TYPOGRAPHY, SPACING, BORDER_RADIUS, SHADOWS } from '../../constants/theme';

const RiskScoreDisplay = ({ data, loading = false, predictiveData = [] }) => {
  // Extract risk scores from the data
  const overallRiskScore = data?.overallRiskScore || data?.riskScore || 0;
  const complianceRisk = data?.complianceRisk || data?.regulatoryRisk || 0;
  const operationalRisk = data?.operationalRisk || 0;
  const financialRisk = data?.financialRisk || 0;

  if (loading) {
    return (
      <View style={styles.container}>
        <Text style={styles.title}>Risk Scores</Text>
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="small" color={COLORS.primary} />
          <Text style={styles.loadingText}>Loading risk scores...</Text>
        </View>
      </View>
    );
  }

  const getScoreColor = (score) => {
    if (score <= 30) return COLORS.success;
    if (score <= 60) return COLORS.warning;
    return COLORS.error;
  };

  const getScoreLabel = (score) => {
    if (score <= 30) return 'Low';
    if (score <= 60) return 'Medium';
    return 'High';
  };

  const getScoreRating = (score) => {
    if (score <= 20) return 'Excellent';
    if (score <= 40) return 'Good';
    if (score <= 60) return 'Fair';
    return 'Poor';
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Risk Scores</Text>
      
      {/* Overall Risk Score */}
      <View style={styles.scoreCard}>
        <Text style={styles.scoreLabel}>Overall Risk Score</Text>
        <Text style={[styles.scoreValue, { color: getScoreColor(overallRiskScore) }]}>
          {overallRiskScore.toFixed(1)}
        </Text>
        <Text style={[styles.scoreRating, { color: getScoreColor(overallRiskScore) }]}>
          {getScoreRating(overallRiskScore)}
        </Text>
        
        <View style={styles.progressBar}>
          <View 
            style={[
              styles.progressFill,
              {
                width: `${overallRiskScore}%`,
                backgroundColor: getScoreColor(overallRiskScore)
              }
            ]}
          />
        </View>
      </View>

      {/* Detailed Metrics */}
      <View style={styles.metricsContainer}>
        <View style={styles.metricCard}>
          <View style={styles.metricHeader}>
            <Ionicons name="document-text" size={16} color={COLORS.textSecondary} />
            <Text style={styles.metricTitle}>Compliance</Text>
          </View>
          <Text style={[styles.metricValue, { color: getScoreColor(complianceRisk) }]}>
            {complianceRisk.toFixed(1)}
          </Text>
          <Text style={styles.metricLabel}>{getScoreLabel(complianceRisk)}</Text>
        </View>

        <View style={styles.metricCard}>
          <View style={styles.metricHeader}>
            <Ionicons name="construct" size={16} color={COLORS.textSecondary} />
            <Text style={styles.metricTitle}>Operational</Text>
          </View>
          <Text style={[styles.metricValue, { color: getScoreColor(operationalRisk) }]}>
            {operationalRisk.toFixed(1)}
          </Text>
          <Text style={styles.metricLabel}>{getScoreLabel(operationalRisk)}</Text>
        </View>

        <View style={styles.metricCard}>
          <View style={styles.metricHeader}>
            <Ionicons name="cash" size={16} color={COLORS.textSecondary} />
            <Text style={styles.metricTitle}>Financial</Text>
          </View>
          <Text style={[styles.metricValue, { color: getScoreColor(financialRisk) }]}>
            {financialRisk.toFixed(1)}
          </Text>
          <Text style={styles.metricLabel}>{getScoreLabel(financialRisk)}</Text>
        </View>
      </View>

      {/* Predictive Analytics */}
      {predictiveData.length > 0 && (
        <View style={styles.predictiveContainer}>
          <Text style={styles.sectionTitle}>Predictive Analytics</Text>
          <View style={styles.predictionList}>
            {predictiveData.slice(0, 3).map((prediction, index) => (
              <View key={index} style={styles.predictionItem}>
                <View style={styles.predictionHeader}>
                  <Text style={styles.predictionTitle}>{prediction.title}</Text>
                  <View style={[
                    styles.predictionBadge,
                    { backgroundColor: getScoreColor(prediction.riskScore) }
                  ]}>
                    <Text style={styles.predictionBadgeText}>
                      {getScoreLabel(prediction.riskScore)}
                    </Text>
                  </View>
                </View>
                <Text style={styles.predictionDescription}>
                  {prediction.description}
                </Text>
                <View style={styles.predictionTrend}>
                  <Text style={styles.predictionConfidence}>
                    Confidence: {prediction.confidence}%
                  </Text>
                  <Text style={styles.predictionTimeline}>
                    Timeline: {prediction.timeline}
                  </Text>
                </View>
              </View>
            ))}
          </View>
        </View>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: COLORS.white,
    borderRadius: BORDER_RADIUS.lg,
    padding: SPACING.lg,
    marginBottom: SPACING.md,
    ...SHADOWS.sm,
  },
  title: {
    fontSize: TYPOGRAPHY.fontSize.base,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.textPrimary,
    marginBottom: SPACING.md,
  },
  loadingContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    padding: SPACING.xl,
  },
  loadingText: {
    marginLeft: SPACING.sm,
    fontSize: TYPOGRAPHY.fontSize.sm,
    color: COLORS.textSecondary,
  },
  scoreCard: {
    backgroundColor: COLORS.surfaceSecondary,
    borderRadius: BORDER_RADIUS.md,
    padding: SPACING.lg,
    alignItems: 'center',
    marginBottom: SPACING.md,
  },
  scoreLabel: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    color: COLORS.textSecondary,
    marginBottom: SPACING.xs,
  },
  scoreValue: {
    fontSize: TYPOGRAPHY.fontSize['3xl'],
    fontWeight: TYPOGRAPHY.fontWeight.bold,
    marginBottom: SPACING.xs,
  },
  scoreRating: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
    marginBottom: SPACING.md,
  },
  progressBar: {
    height: 8,
    backgroundColor: COLORS.gray300,
    borderRadius: 4,
    width: '100%',
    overflow: 'hidden',
  },
  progressFill: {
    height: '100%',
    borderRadius: 4,
  },
  metricsContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: SPACING.md,
  },
  metricCard: {
    flex: 1,
    backgroundColor: COLORS.surfaceSecondary,
    borderRadius: BORDER_RADIUS.md,
    padding: SPACING.md,
    marginHorizontal: SPACING.xs,
    alignItems: 'center',
  },
  metricHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: SPACING.xs,
  },
  metricTitle: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.textSecondary,
    marginLeft: SPACING.xs,
  },
  metricValue: {
    fontSize: TYPOGRAPHY.fontSize.lg,
    fontWeight: TYPOGRAPHY.fontWeight.bold,
    marginBottom: SPACING.xs,
  },
  metricLabel: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.textSecondary,
  },
  predictiveContainer: {
    borderTopWidth: 1,
    borderTopColor: COLORS.gray200,
    paddingTop: SPACING.md,
  },
  sectionTitle: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.textPrimary,
    marginBottom: SPACING.md,
  },
  predictionList: {
    gap: SPACING.md,
  },
  predictionItem: {
    backgroundColor: COLORS.surfaceSecondary,
    borderRadius: BORDER_RADIUS.md,
    padding: SPACING.md,
  },
  predictionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: SPACING.sm,
  },
  predictionTitle: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.textPrimary,
    flex: 1,
    marginRight: SPACING.sm,
  },
  predictionBadge: {
    paddingHorizontal: SPACING.xs,
    paddingVertical: 2,
    borderRadius: BORDER_RADIUS.full,
  },
  predictionBadgeText: {
    fontSize: 10,
    fontWeight: TYPOGRAPHY.fontWeight.bold,
    color: COLORS.white,
    textTransform: 'uppercase',
  },
  predictionDescription: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.textSecondary,
    lineHeight: 16,
    marginBottom: SPACING.sm,
  },
  predictionTrend: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  predictionConfidence: {
    fontSize: 9,
    color: COLORS.textSecondary,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
  },
  predictionTimeline: {
    fontSize: 9,
    color: COLORS.textSecondary,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
  },
});

export default RiskScoreDisplay;