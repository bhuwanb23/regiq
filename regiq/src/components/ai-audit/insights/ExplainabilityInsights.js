import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { COLORS, TYPOGRAPHY, SPACING, BORDER_RADIUS, SHADOWS } from '../../../constants/theme';

const ExplainabilityInsights = ({ modelData }) => {
  const shapInsights = [
    {
      feature: 'Income Level',
      impact: 'High Positive',
      value: '+0.34',
      description: 'Higher income strongly correlates with loan approval',
      confidence: 92,
    },
    {
      feature: 'Credit History',
      impact: 'High Positive',
      value: '+0.31',
      description: 'Good credit history significantly improves approval odds',
      confidence: 89,
    },
    {
      feature: 'Age',
      impact: 'Medium Negative',
      value: '-0.12',
      description: 'Younger applicants face slightly higher rejection rates',
      confidence: 76,
    },
    {
      feature: 'Employment Status',
      impact: 'Medium Positive',
      value: '+0.18',
      description: 'Stable employment positively influences decisions',
      confidence: 84,
    },
  ];

  const limeInsights = [
    {
      title: 'Local Consistency',
      status: 'Good',
      score: 87,
      description: 'Feature attributions are consistent across similar cases',
      icon: 'checkmark-circle',
      color: COLORS.success,
    },
    {
      title: 'Demographic Fairness',
      status: 'Excellent',
      score: 94,
      description: 'No significant bias detected across demographic groups',
      icon: 'people',
      color: COLORS.success,
    },
    {
      title: 'Decision Boundary',
      status: 'Fair',
      score: 73,
      description: 'Some complexity in decision boundaries detected',
      icon: 'analytics',
      color: COLORS.warning,
    },
    {
      title: 'Feature Stability',
      status: 'Good',
      score: 81,
      description: 'Feature importance remains stable over time',
      icon: 'trending-up',
      color: COLORS.info,
    },
  ];

  const getImpactColor = (impact) => {
    if (impact.includes('High Positive')) return COLORS.success;
    if (impact.includes('Medium Positive')) return COLORS.info;
    if (impact.includes('High Negative')) return COLORS.error;
    if (impact.includes('Medium Negative')) return COLORS.warning;
    return COLORS.gray400;
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'Excellent': return COLORS.success;
      case 'Good': return COLORS.info;
      case 'Fair': return COLORS.warning;
      case 'Poor': return COLORS.error;
      default: return COLORS.gray400;
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Explainability Analysis</Text>
      <Text style={styles.subtitle}>Understanding model decisions and behavior</Text>

      {/* SHAP Analysis Section */}
      <View style={styles.section}>
        <View style={styles.sectionHeader}>
          <Ionicons name="bulb" size={18} color={COLORS.info} />
          <Text style={styles.sectionTitle}>SHAP Feature Attribution</Text>
        </View>
        
        <Text style={styles.sectionDescription}>
          Shows how each feature contributes to individual predictions
        </Text>

        <View style={styles.shapContainer}>
          {shapInsights.map((insight, index) => (
            <View key={index} style={styles.shapItem}>
              <View style={styles.shapHeader}>
                <Text style={styles.featureName}>{insight.feature}</Text>
                <View style={[
                  styles.impactBadge,
                  { backgroundColor: `${getImpactColor(insight.impact)}20` }
                ]}>
                  <Text style={[
                    styles.impactText,
                    { color: getImpactColor(insight.impact) }
                  ]}>
                    {insight.impact}
                  </Text>
                </View>
              </View>

              <View style={styles.shapContent}>
                <View style={styles.valueContainer}>
                  <Text style={[
                    styles.shapValue,
                    { color: getImpactColor(insight.impact) }
                  ]}>
                    {insight.value}
                  </Text>
                  <View style={styles.confidenceContainer}>
                    <Text style={styles.confidenceText}>{insight.confidence}% confidence</Text>
                    <View style={styles.confidenceBar}>
                      <View
                        style={[
                          styles.confidenceFill,
                          { 
                            width: `${insight.confidence}%`,
                            backgroundColor: getImpactColor(insight.impact)
                          }
                        ]}
                      />
                    </View>
                  </View>
                </View>
              </View>

              <Text style={styles.shapDescription}>{insight.description}</Text>
            </View>
          ))}
        </View>
      </View>

      {/* LIME Analysis Section */}
      <View style={styles.section}>
        <View style={styles.sectionHeader}>
          <Ionicons name="search" size={18} color={COLORS.secondary} />
          <Text style={styles.sectionTitle}>LIME Local Explanations</Text>
        </View>
        
        <Text style={styles.sectionDescription}>
          Local interpretable model-agnostic explanations for individual predictions
        </Text>

        <View style={styles.limeContainer}>
          {limeInsights.map((insight, index) => (
            <View key={index} style={styles.limeItem}>
              <View style={styles.limeHeader}>
                <View style={[styles.limeIcon, { backgroundColor: `${insight.color}20` }]}>
                  <Ionicons name={insight.icon} size={16} color={insight.color} />
                </View>
                
                <View style={styles.limeInfo}>
                  <Text style={styles.limeTitle}>{insight.title}</Text>
                  <Text style={styles.limeDescription}>{insight.description}</Text>
                </View>

                <View style={styles.limeScore}>
                  <Text style={[
                    styles.scoreValue,
                    { color: getStatusColor(insight.status) }
                  ]}>
                    {insight.score}
                  </Text>
                  <Text style={[
                    styles.statusText,
                    { color: getStatusColor(insight.status) }
                  ]}>
                    {insight.status}
                  </Text>
                </View>
              </View>

              <View style={styles.progressContainer}>
                <View style={styles.progressBackground}>
                  <View
                    style={[
                      styles.progressBar,
                      {
                        width: `${insight.score}%`,
                        backgroundColor: insight.color,
                      }
                    ]}
                  />
                </View>
              </View>
            </View>
          ))}
        </View>
      </View>

      {/* Action Buttons */}
      <View style={styles.actionContainer}>
        <TouchableOpacity style={styles.actionButton}>
          <Ionicons name="download" size={16} color={COLORS.primary} />
          <Text style={styles.actionText}>Export SHAP Report</Text>
        </TouchableOpacity>
        
        <TouchableOpacity style={[styles.actionButton, styles.secondaryButton]}>
          <Ionicons name="eye" size={16} color={COLORS.secondary} />
          <Text style={[styles.actionText, styles.secondaryText]}>View LIME Details</Text>
        </TouchableOpacity>
      </View>

      {/* Summary */}
      <View style={styles.summaryContainer}>
        <Text style={styles.summaryTitle}>Explainability Summary</Text>
        <View style={styles.summaryGrid}>
          <View style={styles.summaryItem}>
            <Text style={styles.summaryValue}>4</Text>
            <Text style={styles.summaryLabel}>Key Features</Text>
          </View>
          <View style={styles.summaryItem}>
            <Text style={styles.summaryValue}>87%</Text>
            <Text style={styles.summaryLabel}>Avg Confidence</Text>
          </View>
          <View style={styles.summaryItem}>
            <Text style={styles.summaryValue}>Good</Text>
            <Text style={styles.summaryLabel}>Interpretability</Text>
          </View>
        </View>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: COLORS.white,
    borderRadius: BORDER_RADIUS.lg,
    padding: SPACING.md,
    marginBottom: SPACING.md,
  },
  title: {
    fontSize: TYPOGRAPHY.fontSize.lg,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.textPrimary,
    marginBottom: SPACING.xs,
  },
  subtitle: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.textSecondary,
    marginBottom: SPACING.md,
  },
  section: {
    marginBottom: SPACING.lg,
  },
  sectionHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: SPACING.xs,
  },
  sectionTitle: {
    fontSize: TYPOGRAPHY.fontSize.base,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.textPrimary,
    marginLeft: SPACING.xs,
  },
  sectionDescription: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.textSecondary,
    marginBottom: SPACING.sm,
  },
  shapContainer: {
    backgroundColor: COLORS.surfaceSecondary,
    borderRadius: BORDER_RADIUS.md,
    padding: SPACING.sm,
  },
  shapItem: {
    marginBottom: SPACING.sm,
    paddingBottom: SPACING.sm,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.gray200,
  },
  shapHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: SPACING.xs,
  },
  featureName: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
    color: COLORS.textPrimary,
  },
  impactBadge: {
    paddingHorizontal: SPACING.xs,
    paddingVertical: 2,
    borderRadius: BORDER_RADIUS.sm,
  },
  impactText: {
    fontSize: 9,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
  },
  shapContent: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: SPACING.xs,
  },
  valueContainer: {
    flex: 1,
  },
  shapValue: {
    fontSize: TYPOGRAPHY.fontSize.lg,
    fontWeight: TYPOGRAPHY.fontWeight.bold,
    marginBottom: SPACING.xs,
  },
  confidenceContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  confidenceText: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.textSecondary,
    marginRight: SPACING.xs,
    minWidth: 80,
  },
  confidenceBar: {
    flex: 1,
    height: 4,
    backgroundColor: COLORS.gray300,
    borderRadius: 2,
    overflow: 'hidden',
  },
  confidenceFill: {
    height: 4,
    borderRadius: 2,
  },
  shapDescription: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.textSecondary,
    fontStyle: 'italic',
  },
  limeContainer: {
    backgroundColor: COLORS.surfaceSecondary,
    borderRadius: BORDER_RADIUS.md,
    padding: SPACING.sm,
  },
  limeItem: {
    marginBottom: SPACING.sm,
  },
  limeHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: SPACING.xs,
  },
  limeIcon: {
    width: 32,
    height: 32,
    borderRadius: 16,
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: SPACING.sm,
  },
  limeInfo: {
    flex: 1,
  },
  limeTitle: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
    color: COLORS.textPrimary,
    marginBottom: SPACING.xs,
  },
  limeDescription: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.textSecondary,
  },
  limeScore: {
    alignItems: 'flex-end',
  },
  scoreValue: {
    fontSize: TYPOGRAPHY.fontSize.lg,
    fontWeight: TYPOGRAPHY.fontWeight.bold,
  },
  statusText: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
  },
  progressContainer: {
    marginTop: SPACING.xs,
  },
  progressBackground: {
    height: 4,
    backgroundColor: COLORS.gray300,
    borderRadius: 2,
    overflow: 'hidden',
  },
  progressBar: {
    height: 4,
    borderRadius: 2,
  },
  actionContainer: {
    flexDirection: 'row',
    marginBottom: SPACING.md,
    marginHorizontal: -SPACING.xs,
  },
  actionButton: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: `${COLORS.primary}15`,
    paddingVertical: SPACING.sm,
    borderRadius: BORDER_RADIUS.md,
    marginHorizontal: SPACING.xs,
  },
  secondaryButton: {
    backgroundColor: `${COLORS.secondary}15`,
  },
  actionText: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
    color: COLORS.primary,
    marginLeft: SPACING.xs,
  },
  secondaryText: {
    color: COLORS.secondary,
  },
  summaryContainer: {
    backgroundColor: COLORS.surfaceSecondary,
    borderRadius: BORDER_RADIUS.md,
    padding: SPACING.md,
  },
  summaryTitle: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.textPrimary,
    marginBottom: SPACING.sm,
    textAlign: 'center',
  },
  summaryGrid: {
    flexDirection: 'row',
    justifyContent: 'space-around',
  },
  summaryItem: {
    alignItems: 'center',
  },
  summaryValue: {
    fontSize: TYPOGRAPHY.fontSize.base,
    fontWeight: TYPOGRAPHY.fontWeight.bold,
    color: COLORS.primary,
    marginBottom: 2,
  },
  summaryLabel: {
    fontSize: 9,
    color: COLORS.textSecondary,
  },
});

export default ExplainabilityInsights;
