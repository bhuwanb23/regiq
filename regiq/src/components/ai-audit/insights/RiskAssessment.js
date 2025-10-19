import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { COLORS, TYPOGRAPHY, SPACING, BORDER_RADIUS, SHADOWS } from '../../../constants/theme';

const RiskAssessment = ({ modelData }) => {
  const riskFactors = [
    {
      category: 'Bias Risk',
      level: 'Medium',
      score: 6.8,
      factors: [
        { name: 'Gender Bias', severity: 'Low', value: 0.12 },
        { name: 'Age Discrimination', severity: 'Medium', value: 0.28 },
        { name: 'Regional Bias', severity: 'Low', value: 0.15 },
      ],
      recommendation: 'Monitor age-related decisions more closely',
      icon: 'people',
      color: COLORS.warning,
    },
    {
      category: 'Performance Risk',
      level: 'Low',
      score: 3.2,
      factors: [
        { name: 'Accuracy Degradation', severity: 'Low', value: 0.08 },
        { name: 'False Positive Rate', severity: 'Low', value: 0.05 },
        { name: 'Model Drift', severity: 'Low', value: 0.04 },
      ],
      recommendation: 'Continue current monitoring schedule',
      icon: 'trending-down',
      color: COLORS.success,
    },
    {
      category: 'Compliance Risk',
      level: 'High',
      score: 8.1,
      factors: [
        { name: 'Regulatory Alignment', severity: 'High', value: 0.45 },
        { name: 'Documentation Gap', severity: 'Medium', value: 0.32 },
        { name: 'Audit Trail', severity: 'Low', value: 0.18 },
      ],
      recommendation: 'Immediate compliance review required',
      icon: 'shield-checkmark',
      color: COLORS.error,
    },
    {
      category: 'Operational Risk',
      level: 'Medium',
      score: 5.9,
      factors: [
        { name: 'Data Quality', severity: 'Medium', value: 0.25 },
        { name: 'System Reliability', severity: 'Low', value: 0.12 },
        { name: 'Scalability Issues', severity: 'Medium', value: 0.31 },
      ],
      recommendation: 'Enhance data validation processes',
      icon: 'settings',
      color: COLORS.info,
    },
  ];

  const getRiskLevelColor = (level) => {
    switch (level) {
      case 'Low': return COLORS.success;
      case 'Medium': return COLORS.warning;
      case 'High': return COLORS.error;
      default: return COLORS.gray400;
    }
  };

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'Low': return COLORS.success;
      case 'Medium': return COLORS.warning;
      case 'High': return COLORS.error;
      default: return COLORS.gray400;
    }
  };

  const getOverallRiskLevel = () => {
    const avgScore = riskFactors.reduce((sum, factor) => sum + factor.score, 0) / riskFactors.length;
    if (avgScore <= 4) return { level: 'Low', color: COLORS.success };
    if (avgScore <= 7) return { level: 'Medium', color: COLORS.warning };
    return { level: 'High', color: COLORS.error };
  };

  const overallRisk = getOverallRiskLevel();

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Risk Assessment</Text>
      <Text style={styles.subtitle}>Comprehensive model risk analysis and mitigation</Text>

      {/* Overall Risk Score */}
      <View style={styles.overallRiskContainer}>
        <View style={styles.riskScoreSection}>
          <Text style={styles.overallRiskTitle}>Overall Risk Level</Text>
          <View style={styles.riskScoreDisplay}>
            <Text style={[styles.riskScore, { color: overallRisk.color }]}>
              {(riskFactors.reduce((sum, factor) => sum + factor.score, 0) / riskFactors.length).toFixed(1)}
            </Text>
            <View style={[styles.riskLevelBadge, { backgroundColor: `${overallRisk.color}20` }]}>
              <Text style={[styles.riskLevelText, { color: overallRisk.color }]}>
                {overallRisk.level} Risk
              </Text>
            </View>
          </View>
        </View>

        <View style={styles.riskMeter}>
          <View style={styles.riskMeterBackground}>
            <View
              style={[
                styles.riskMeterFill,
                {
                  width: `${(riskFactors.reduce((sum, factor) => sum + factor.score, 0) / riskFactors.length) * 10}%`,
                  backgroundColor: overallRisk.color,
                }
              ]}
            />
          </View>
          <View style={styles.riskMeterLabels}>
            <Text style={styles.riskMeterLabel}>Low</Text>
            <Text style={styles.riskMeterLabel}>Medium</Text>
            <Text style={styles.riskMeterLabel}>High</Text>
          </View>
        </View>
      </View>

      {/* Risk Categories */}
      <View style={styles.categoriesContainer}>
        {riskFactors.map((category, index) => (
          <View key={index} style={styles.categoryCard}>
            <View style={styles.categoryHeader}>
              <View style={[styles.categoryIcon, { backgroundColor: `${category.color}20` }]}>
                <Ionicons name={category.icon} size={18} color={category.color} />
              </View>
              
              <View style={styles.categoryInfo}>
                <Text style={styles.categoryName}>{category.category}</Text>
                <View style={styles.categoryMeta}>
                  <Text style={[
                    styles.categoryLevel,
                    { color: getRiskLevelColor(category.level) }
                  ]}>
                    {category.level} Risk
                  </Text>
                  <Text style={styles.categoryScore}>Score: {category.score}/10</Text>
                </View>
              </View>

              <View style={styles.scoreContainer}>
                <Text style={[styles.scoreValue, { color: category.color }]}>
                  {category.score}
                </Text>
              </View>
            </View>

            {/* Risk Factors */}
            <View style={styles.factorsContainer}>
              {category.factors.map((factor, factorIndex) => (
                <View key={factorIndex} style={styles.factorRow}>
                  <View style={styles.factorInfo}>
                    <Text style={styles.factorName}>{factor.name}</Text>
                    <View style={styles.factorMeta}>
                      <View style={[
                        styles.severityBadge,
                        { backgroundColor: `${getSeverityColor(factor.severity)}20` }
                      ]}>
                        <Text style={[
                          styles.severityText,
                          { color: getSeverityColor(factor.severity) }
                        ]}>
                          {factor.severity}
                        </Text>
                      </View>
                      <Text style={styles.factorValue}>{factor.value.toFixed(2)}</Text>
                    </View>
                  </View>
                  
                  <View style={styles.factorProgress}>
                    <View style={styles.factorProgressBackground}>
                      <View
                        style={[
                          styles.factorProgressBar,
                          {
                            width: `${factor.value * 100}%`,
                            backgroundColor: getSeverityColor(factor.severity),
                          }
                        ]}
                      />
                    </View>
                  </View>
                </View>
              ))}
            </View>

            {/* Recommendation */}
            <View style={styles.recommendationContainer}>
              <Ionicons name="bulb" size={14} color={COLORS.accent} />
              <Text style={styles.recommendationText}>{category.recommendation}</Text>
            </View>
          </View>
        ))}
      </View>

      {/* Action Items */}
      <View style={styles.actionItemsContainer}>
        <Text style={styles.actionItemsTitle}>Immediate Action Items</Text>
        
        <View style={styles.actionItem}>
          <View style={[styles.priorityIndicator, { backgroundColor: COLORS.error }]} />
          <View style={styles.actionContent}>
            <Text style={styles.actionTitle}>Compliance Review</Text>
            <Text style={styles.actionDescription}>
              Schedule immediate regulatory compliance assessment
            </Text>
          </View>
          <TouchableOpacity style={styles.actionButton}>
            <Text style={styles.actionButtonText}>Schedule</Text>
          </TouchableOpacity>
        </View>

        <View style={styles.actionItem}>
          <View style={[styles.priorityIndicator, { backgroundColor: COLORS.warning }]} />
          <View style={styles.actionContent}>
            <Text style={styles.actionTitle}>Bias Monitoring</Text>
            <Text style={styles.actionDescription}>
              Implement enhanced age bias detection mechanisms
            </Text>
          </View>
          <TouchableOpacity style={styles.actionButton}>
            <Text style={styles.actionButtonText}>Implement</Text>
          </TouchableOpacity>
        </View>

        <View style={styles.actionItem}>
          <View style={[styles.priorityIndicator, { backgroundColor: COLORS.info }]} />
          <View style={styles.actionContent}>
            <Text style={styles.actionTitle}>Data Quality</Text>
            <Text style={styles.actionDescription}>
              Enhance data validation and quality assurance processes
            </Text>
          </View>
          <TouchableOpacity style={styles.actionButton}>
            <Text style={styles.actionButtonText}>Plan</Text>
          </TouchableOpacity>
        </View>
      </View>
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
  overallRiskContainer: {
    backgroundColor: COLORS.surfaceSecondary,
    borderRadius: BORDER_RADIUS.md,
    padding: SPACING.md,
    marginBottom: SPACING.md,
  },
  riskScoreSection: {
    marginBottom: SPACING.sm,
  },
  overallRiskTitle: {
    fontSize: TYPOGRAPHY.fontSize.base,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.textPrimary,
    marginBottom: SPACING.xs,
    textAlign: 'center',
  },
  riskScoreDisplay: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
  },
  riskScore: {
    fontSize: TYPOGRAPHY.fontSize['2xl'],
    fontWeight: TYPOGRAPHY.fontWeight.bold,
    marginRight: SPACING.sm,
  },
  riskLevelBadge: {
    paddingHorizontal: SPACING.sm,
    paddingVertical: SPACING.xs,
    borderRadius: BORDER_RADIUS.md,
  },
  riskLevelText: {
    fontSize: TYPOGRAPHY.fontSize.base,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
  },
  riskMeter: {
    marginTop: SPACING.sm,
  },
  riskMeterBackground: {
    height: 8,
    backgroundColor: COLORS.gray300,
    borderRadius: 4,
    overflow: 'hidden',
  },
  riskMeterFill: {
    height: 8,
    borderRadius: 4,
  },
  riskMeterLabels: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginTop: 4,
  },
  riskMeterLabel: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.textSecondary,
  },
  categoriesContainer: {
    marginBottom: SPACING.md,
  },
  categoryCard: {
    backgroundColor: COLORS.surfaceSecondary,
    borderRadius: BORDER_RADIUS.md,
    padding: SPACING.md,
    marginBottom: SPACING.md,
  },
  categoryHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: SPACING.sm,
  },
  categoryIcon: {
    width: 36,
    height: 36,
    borderRadius: 18,
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: SPACING.sm,
  },
  categoryInfo: {
    flex: 1,
  },
  categoryName: {
    fontSize: TYPOGRAPHY.fontSize.base,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.textPrimary,
    marginBottom: 4,
  },
  categoryMeta: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  categoryLevel: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
    marginRight: SPACING.md,
  },
  categoryScore: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    color: COLORS.textSecondary,
  },
  scoreContainer: {
    alignItems: 'center',
  },
  scoreValue: {
    fontSize: TYPOGRAPHY.fontSize.lg,
    fontWeight: TYPOGRAPHY.fontWeight.bold,
  },
  factorsContainer: {
    marginBottom: SPACING.sm,
  },
  factorRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: SPACING.sm,
    paddingVertical: SPACING.xs,
  },
  factorInfo: {
    flex: 1,
    marginRight: SPACING.sm,
  },
  factorName: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
    color: COLORS.textPrimary,
    marginBottom: 4,
  },
  factorMeta: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  severityBadge: {
    paddingHorizontal: 6,
    paddingVertical: 2,
    borderRadius: 8,
    marginRight: SPACING.xs,
  },
  severityText: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
  },
  factorValue: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.textSecondary,
  },
  factorProgress: {
    width: 60,
  },
  factorProgressBackground: {
    height: 4,
    backgroundColor: COLORS.gray300,
    borderRadius: 2,
    overflow: 'hidden',
  },
  factorProgressBar: {
    height: 4,
    borderRadius: 2,
  },
  recommendationContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: `${COLORS.accent}15`,
    padding: SPACING.sm,
    borderRadius: BORDER_RADIUS.md,
    marginTop: SPACING.xs,
  },
  recommendationText: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    color: COLORS.textPrimary,
    marginLeft: SPACING.sm,
    flex: 1,
    lineHeight: 18,
  },
  actionItemsContainer: {
    backgroundColor: COLORS.surfaceSecondary,
    borderRadius: BORDER_RADIUS.md,
    padding: SPACING.md,
  },
  actionItemsTitle: {
    fontSize: TYPOGRAPHY.fontSize.base,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.textPrimary,
    marginBottom: SPACING.sm,
  },
  actionItem: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: COLORS.white,
    borderRadius: BORDER_RADIUS.sm,
    padding: SPACING.sm,
    marginBottom: SPACING.xs,
  },
  priorityIndicator: {
    width: 4,
    height: 40,
    borderRadius: 2,
    marginRight: SPACING.sm,
  },
  actionContent: {
    flex: 1,
  },
  actionTitle: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
    color: COLORS.textPrimary,
    marginBottom: SPACING.xs,
  },
  actionDescription: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.textSecondary,
  },
  actionButton: {
    backgroundColor: COLORS.primary,
    paddingHorizontal: SPACING.sm,
    paddingVertical: SPACING.xs,
    borderRadius: BORDER_RADIUS.sm,
  },
  actionButtonText: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.white,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
  },
});

export default RiskAssessment;
