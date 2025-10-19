import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { COLORS, TYPOGRAPHY, SPACING, BORDER_RADIUS, SHADOWS } from '../../constants/theme';

const ResultsOverview = ({ 
  complianceScore = 87,
  flaggedItems = 23,
  riskLevel = 'low',
  additionalMetrics = []
}) => {
  const getRiskColor = (level) => {
    switch (level) {
      case 'low': return COLORS.success;
      case 'medium': return COLORS.warning;
      case 'high': return COLORS.error;
      default: return COLORS.success;
    }
  };

  const getRiskBackground = (level) => {
    switch (level) {
      case 'low': return `${COLORS.success}15`;
      case 'medium': return `${COLORS.warning}15`;
      case 'high': return `${COLORS.error}15`;
      default: return `${COLORS.success}15`;
    }
  };

  const getRiskText = (level) => {
    switch (level) {
      case 'low': return 'Low Risk';
      case 'medium': return 'Medium Risk';
      case 'high': return 'High Risk';
      default: return 'Low Risk';
    }
  };

  const getFlaggedRiskLevel = () => {
    if (flaggedItems <= 10) return 'low';
    if (flaggedItems <= 30) return 'medium';
    return 'high';
  };

  const flaggedRiskLevel = getFlaggedRiskLevel();

  return (
    <View style={styles.container}>
      <Text style={styles.sectionTitle}>Simulation Results</Text>
      
      <View style={styles.cardsContainer}>
        {/* Compliance Score Card */}
        <View style={styles.card}>
          <View style={styles.cardHeader}>
            <View style={[styles.iconContainer, { backgroundColor: `${COLORS.secondary}20` }]}>
              <Ionicons name="shield-checkmark" size={18} color={COLORS.secondary} />
            </View>
            <View style={[
              styles.riskBadge,
              { backgroundColor: getRiskBackground(riskLevel) }
            ]}>
              <Text style={[styles.riskBadgeText, { color: getRiskColor(riskLevel) }]}>
                {getRiskText(riskLevel)}
              </Text>
            </View>
          </View>
          
          <Text style={styles.cardValue}>{complianceScore}%</Text>
          <Text style={styles.cardLabel}>Compliance Score</Text>
          
          <View style={styles.progressContainer}>
            <View style={styles.progressBackground}>
              <View 
                style={[
                  styles.progressBar,
                  { 
                    width: `${complianceScore}%`,
                    backgroundColor: getRiskColor(riskLevel)
                  }
                ]}
              />
            </View>
          </View>
        </View>

        {/* Flagged Items Card */}
        <View style={styles.card}>
          <View style={styles.cardHeader}>
            <View style={[styles.iconContainer, { backgroundColor: `${COLORS.warning}20` }]}>
              <Ionicons name="flag" size={18} color={COLORS.warning} />
            </View>
            <View style={[
              styles.riskBadge,
              { backgroundColor: getRiskBackground(flaggedRiskLevel) }
            ]}>
              <Text style={[styles.riskBadgeText, { color: getRiskColor(flaggedRiskLevel) }]}>
                {getRiskText(flaggedRiskLevel)}
              </Text>
            </View>
          </View>
          
          <Text style={styles.cardValue}>{flaggedItems}</Text>
          <Text style={styles.cardLabel}>Flagged Items</Text>
          
          <View style={styles.flaggedDetails}>
            <View style={styles.flaggedItem}>
              <View style={[styles.flaggedDot, { backgroundColor: COLORS.error }]} />
              <Text style={styles.flaggedText}>High: 3</Text>
            </View>
            <View style={styles.flaggedItem}>
              <View style={[styles.flaggedDot, { backgroundColor: COLORS.warning }]} />
              <Text style={styles.flaggedText}>Medium: 8</Text>
            </View>
            <View style={styles.flaggedItem}>
              <View style={[styles.flaggedDot, { backgroundColor: COLORS.info }]} />
              <Text style={styles.flaggedText}>Low: 12</Text>
            </View>
          </View>
        </View>
      </View>

      {/* Additional Metrics */}
      {additionalMetrics.length > 0 && (
        <View style={styles.additionalMetrics}>
          {additionalMetrics.map((metric, index) => (
            <View key={index} style={styles.metricItem}>
              <View style={styles.metricHeader}>
                <Ionicons 
                  name={metric.icon} 
                  size={14} 
                  color={metric.color || COLORS.primary} 
                />
                <Text style={styles.metricValue}>{metric.value}</Text>
              </View>
              <Text style={styles.metricLabel}>{metric.label}</Text>
            </View>
          ))}
        </View>
      )}

      {/* Summary Stats */}
      <View style={styles.summaryContainer}>
        <View style={styles.summaryItem}>
          <Text style={styles.summaryValue}>
            {Math.round((complianceScore / 100) * 10) / 10}
          </Text>
          <Text style={styles.summaryLabel}>Risk Rating</Text>
        </View>
        
        <View style={styles.summaryDivider} />
        
        <View style={styles.summaryItem}>
          <Text style={styles.summaryValue}>
            {complianceScore >= 85 ? 'Pass' : 'Fail'}
          </Text>
          <Text style={styles.summaryLabel}>Regulatory Status</Text>
        </View>
        
        <View style={styles.summaryDivider} />
        
        <View style={styles.summaryItem}>
          <Text style={[
            styles.summaryValue,
            { color: flaggedItems <= 10 ? COLORS.success : COLORS.warning }
          ]}>
            {flaggedItems <= 10 ? 'Good' : 'Review'}
          </Text>
          <Text style={styles.summaryLabel}>Action Required</Text>
        </View>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    marginBottom: SPACING.md,
  },
  sectionTitle: {
    fontSize: TYPOGRAPHY.fontSize.lg,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.textPrimary,
    marginBottom: SPACING.md,
    paddingHorizontal: SPACING.xs,
  },
  cardsContainer: {
    flexDirection: 'row',
    marginHorizontal: -SPACING.xs,
    marginBottom: SPACING.md,
  },
  card: {
    flex: 1,
    backgroundColor: COLORS.white,
    borderRadius: BORDER_RADIUS.lg,
    padding: SPACING.md,
    marginHorizontal: SPACING.xs,
    borderWidth: 1,
    borderColor: COLORS.gray200,
    ...SHADOWS.sm,
  },
  cardHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: SPACING.sm,
  },
  iconContainer: {
    width: 32,
    height: 32,
    borderRadius: 16,
    alignItems: 'center',
    justifyContent: 'center',
  },
  riskBadge: {
    paddingHorizontal: SPACING.xs,
    paddingVertical: 2,
    borderRadius: BORDER_RADIUS.full,
  },
  riskBadgeText: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
  },
  cardValue: {
    fontSize: TYPOGRAPHY.fontSize['2xl'],
    fontWeight: TYPOGRAPHY.fontWeight.bold,
    color: COLORS.primary,
    marginBottom: SPACING.xs,
  },
  cardLabel: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    color: COLORS.textSecondary,
    marginBottom: SPACING.sm,
  },
  progressContainer: {
    marginTop: SPACING.xs,
  },
  progressBackground: {
    height: 4,
    backgroundColor: COLORS.gray200,
    borderRadius: 2,
    overflow: 'hidden',
  },
  progressBar: {
    height: 4,
    borderRadius: 2,
  },
  flaggedDetails: {
    marginTop: SPACING.xs,
  },
  flaggedItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 2,
  },
  flaggedDot: {
    width: 6,
    height: 6,
    borderRadius: 3,
    marginRight: SPACING.xs,
  },
  flaggedText: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.textSecondary,
  },
  additionalMetrics: {
    flexDirection: 'row',
    backgroundColor: COLORS.white,
    borderRadius: BORDER_RADIUS.lg,
    padding: SPACING.sm,
    marginBottom: SPACING.md,
    ...SHADOWS.sm,
  },
  metricItem: {
    flex: 1,
    alignItems: 'center',
  },
  metricHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: SPACING.xs,
  },
  metricValue: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    fontWeight: TYPOGRAPHY.fontWeight.bold,
    color: COLORS.textPrimary,
    marginLeft: SPACING.xs,
  },
  metricLabel: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.textSecondary,
    textAlign: 'center',
  },
  summaryContainer: {
    flexDirection: 'row',
    backgroundColor: COLORS.white,
    borderRadius: BORDER_RADIUS.lg,
    paddingVertical: SPACING.sm,
    paddingHorizontal: SPACING.md,
    ...SHADOWS.sm,
  },
  summaryItem: {
    flex: 1,
    alignItems: 'center',
  },
  summaryValue: {
    fontSize: TYPOGRAPHY.fontSize.base,
    fontWeight: TYPOGRAPHY.fontWeight.bold,
    color: COLORS.primary,
    marginBottom: 2,
  },
  summaryLabel: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.textSecondary,
    textAlign: 'center',
  },
  summaryDivider: {
    width: 1,
    backgroundColor: COLORS.gray300,
    marginHorizontal: SPACING.sm,
  },
});

export default ResultsOverview;
