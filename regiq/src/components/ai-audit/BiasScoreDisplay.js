import React from 'react';
import { View, Text, StyleSheet, ActivityIndicator } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { COLORS, TYPOGRAPHY, SPACING, BORDER_RADIUS, SHADOWS } from '../../constants/theme';

const BiasScoreDisplay = ({ data, loading = false, historicalData = [] }) => {
  // Extract bias scores from the report
  const overallBiasScore = data?.overallBiasScore || data?.biasScore || 0;
  const demographicParity = data?.demographicParityDifference || data?.demographicParity || 0;
  const equalOpportunity = data?.equalOpportunityDifference || data?.equalOpportunity || 0;
  const disparateImpact = data?.disparateImpact || 1.0;

  if (loading) {
    return (
      <View style={styles.container}>
        <Text style={styles.title}>Bias Scores</Text>
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="small" color={COLORS.primary} />
          <Text style={styles.loadingText}>Loading bias scores...</Text>
        </View>
      </View>
    );
  }

  const getScoreColor = (score) => {
    if (score <= 0.1) return COLORS.success;
    if (score <= 0.25) return COLORS.warning;
    return COLORS.error;
  };

  const getScoreLabel = (score) => {
    if (score <= 0.1) return 'Low';
    if (score <= 0.25) return 'Medium';
    return 'High';
  };

  const getScoreRating = (score) => {
    if (score <= 0.1) return 'Excellent';
    if (score <= 0.15) return 'Good';
    if (score <= 0.25) return 'Fair';
    return 'Poor';
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Bias Scores</Text>
      
      {/* Overall Bias Score */}
      <View style={styles.scoreCard}>
        <Text style={styles.scoreLabel}>Overall Bias Score</Text>
        <Text style={[styles.scoreValue, { color: getScoreColor(overallBiasScore) }]}>
          {overallBiasScore.toFixed(3)}
        </Text>
        <Text style={[styles.scoreRating, { color: getScoreColor(overallBiasScore) }]}>
          {getScoreRating(overallBiasScore)}
        </Text>
        
        <View style={styles.progressBar}>
          <View 
            style={[
              styles.progressFill,
              {
                width: `${overallBiasScore * 100}%`,
                backgroundColor: getScoreColor(overallBiasScore)
              }
            ]}
          />
        </View>
      </View>

      {/* Detailed Metrics */}
      <View style={styles.metricsContainer}>
        <View style={styles.metricCard}>
          <View style={styles.metricHeader}>
            <Ionicons name="people" size={16} color={COLORS.textSecondary} />
            <Text style={styles.metricTitle}>Demographic Parity</Text>
          </View>
          <Text style={[styles.metricValue, { color: getScoreColor(demographicParity) }]}>
            {demographicParity.toFixed(3)}
          </Text>
          <Text style={styles.metricLabel}>{getScoreLabel(demographicParity)}</Text>
        </View>

        <View style={styles.metricCard}>
          <View style={styles.metricHeader}>
            <Ionicons name="accessibility" size={16} color={COLORS.textSecondary} />
            <Text style={styles.metricTitle}>Equal Opportunity</Text>
          </View>
          <Text style={[styles.metricValue, { color: getScoreColor(equalOpportunity) }]}>
            {equalOpportunity.toFixed(3)}
          </Text>
          <Text style={styles.metricLabel}>{getScoreLabel(equalOpportunity)}</Text>
        </View>

        <View style={styles.metricCard}>
          <View style={styles.metricHeader}>
            <Ionicons name="stats-chart" size={16} color={COLORS.textSecondary} />
            <Text style={styles.metricTitle}>Disparate Impact</Text>
          </View>
          <Text style={[styles.metricValue, { 
            color: disparateImpact >= 0.8 && disparateImpact <= 1.2 ? COLORS.success : COLORS.error 
          }]}>
            {disparateImpact.toFixed(3)}
          </Text>
          <Text style={styles.metricLabel}>
            {disparateImpact >= 0.8 && disparateImpact <= 1.2 ? 'Fair' : 'Unfair'}
          </Text>
        </View>
      </View>

      {/* Historical Trend */}
      {historicalData.length > 0 && (
        <View style={styles.historicalContainer}>
          <Text style={styles.sectionTitle}>Historical Trend</Text>
          <View style={styles.trendContainer}>
            {historicalData.slice(0, 5).map((entry, index) => (
              <View key={index} style={styles.trendItem}>
                <Text style={styles.trendDate}>
                  {new Date(entry.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                </Text>
                <View style={styles.trendDotContainer}>
                  <View 
                    style={[
                      styles.trendDot,
                      { backgroundColor: getScoreColor(entry.biasScore) }
                    ]}
                  />
                  <View style={styles.trendLine} />
                </View>
                <Text style={[styles.trendScore, { color: getScoreColor(entry.biasScore) }]}>
                  {entry.biasScore.toFixed(2)}
                </Text>
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
  historicalContainer: {
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
  trendContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  trendItem: {
    alignItems: 'center',
    flex: 1,
  },
  trendDate: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.textSecondary,
    marginBottom: SPACING.sm,
  },
  trendDotContainer: {
    alignItems: 'center',
    marginBottom: SPACING.sm,
  },
  trendDot: {
    width: 12,
    height: 12,
    borderRadius: 6,
    zIndex: 1,
  },
  trendLine: {
    width: 2,
    height: 40,
    backgroundColor: COLORS.gray300,
    position: 'absolute',
    top: 6,
  },
  trendScore: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
  },
});

export default BiasScoreDisplay;