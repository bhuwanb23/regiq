import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { COLORS, TYPOGRAPHY, SPACING, BORDER_RADIUS, SHADOWS } from '../../../constants/theme';

const PerformanceMetrics = ({ modelData }) => {
  const metrics = [
    {
      name: 'Accuracy',
      value: 94.2,
      unit: '%',
      trend: 'up',
      change: '+2.1%',
      icon: 'checkmark-circle',
      color: COLORS.success,
      description: 'Overall prediction accuracy',
    },
    {
      name: 'Precision',
      value: 91.8,
      unit: '%',
      trend: 'up',
      change: '+1.5%',
      icon: 'target',
      color: COLORS.info,
      description: 'True positive rate',
    },
    {
      name: 'Recall',
      value: 89.3,
      unit: '%',
      trend: 'down',
      change: '-0.8%',
      icon: 'search',
      color: COLORS.warning,
      description: 'Sensitivity measure',
    },
    {
      name: 'F1 Score',
      value: 90.5,
      unit: '%',
      trend: 'up',
      change: '+0.3%',
      icon: 'analytics',
      color: COLORS.primary,
      description: 'Harmonic mean of precision and recall',
    },
    {
      name: 'AUC-ROC',
      value: 0.923,
      unit: '',
      trend: 'stable',
      change: '0.0%',
      icon: 'trending-up',
      color: COLORS.secondary,
      description: 'Area under ROC curve',
    },
    {
      name: 'Log Loss',
      value: 0.187,
      unit: '',
      trend: 'down',
      change: '-0.02',
      icon: 'trending-down',
      color: COLORS.success,
      description: 'Logarithmic loss (lower is better)',
    },
  ];

  const getTrendIcon = (trend) => {
    switch (trend) {
      case 'up': return 'arrow-up';
      case 'down': return 'arrow-down';
      default: return 'remove';
    }
  };

  const getTrendColor = (trend) => {
    switch (trend) {
      case 'up': return COLORS.success;
      case 'down': return COLORS.error;
      default: return COLORS.gray400;
    }
  };

  const getPerformanceLevel = (value, metricName) => {
    if (metricName === 'Log Loss') {
      if (value <= 0.2) return 'Excellent';
      if (value <= 0.4) return 'Good';
      if (value <= 0.6) return 'Fair';
      return 'Poor';
    } else {
      if (value >= 90) return 'Excellent';
      if (value >= 80) return 'Good';
      if (value >= 70) return 'Fair';
      return 'Poor';
    }
  };

  const getPerformanceLevelColor = (level) => {
    switch (level) {
      case 'Excellent': return COLORS.success;
      case 'Good': return COLORS.info;
      case 'Fair': return COLORS.warning;
      default: return COLORS.error;
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Performance Metrics</Text>
      <Text style={styles.subtitle}>Model evaluation and performance indicators</Text>

      <View style={styles.metricsGrid}>
        {metrics.reduce((rows, metric, index) => {
          if (index % 2 === 0) rows.push([]);
          rows[rows.length - 1].push(metric);
          return rows;
        }, []).map((row, rowIndex) => (
          <View key={rowIndex} style={styles.metricRow}>
            {row.map((metric, index) => (
              <View key={index} style={styles.metricCard}>
            <View style={styles.metricHeader}>
              <View style={[styles.iconContainer, { backgroundColor: `${metric.color}20` }]}>
                <Ionicons name={metric.icon} size={16} color={metric.color} />
              </View>
              
              <View style={styles.trendContainer}>
                <Ionicons 
                  name={getTrendIcon(metric.trend)} 
                  size={12} 
                  color={getTrendColor(metric.trend)} 
                />
                <Text style={[
                  styles.changeText,
                  { color: getTrendColor(metric.trend) }
                ]}>
                  {metric.change}
                </Text>
              </View>
            </View>

            <Text style={styles.metricName}>{metric.name}</Text>
            
            <View style={styles.valueContainer}>
              <Text style={styles.metricValue}>
                {metric.value}{metric.unit}
              </Text>
              
              <View style={[
                styles.levelBadge,
                { backgroundColor: `${getPerformanceLevelColor(getPerformanceLevel(metric.value, metric.name))}20` }
              ]}>
                <Text style={[
                  styles.levelText,
                  { color: getPerformanceLevelColor(getPerformanceLevel(metric.value, metric.name)) }
                ]}>
                  {getPerformanceLevel(metric.value, metric.name)}
                </Text>
              </View>
            </View>

            <Text style={styles.description}>{metric.description}</Text>

            {/* Progress Bar */}
            <View style={styles.progressContainer}>
              <View style={styles.progressBackground}>
                <View
                  style={[
                    styles.progressBar,
                    {
                      width: metric.name === 'Log Loss' ? `${(1 - metric.value) * 100}%` : `${metric.value}%`,
                      backgroundColor: metric.color,
                    }
                  ]}
                />
              </View>
            </View>
              </View>
            ))}
          </View>
        ))}
      </View>

      {/* Overall Performance Summary */}
      <View style={styles.summaryContainer}>
        <Text style={styles.summaryTitle}>Overall Performance</Text>
        <View style={styles.summaryContent}>
          <View style={styles.summaryItem}>
            <Text style={styles.summaryValue}>A+</Text>
            <Text style={styles.summaryLabel}>Grade</Text>
          </View>
          <View style={styles.summaryDivider} />
          <View style={styles.summaryItem}>
            <Text style={styles.summaryValue}>91.2%</Text>
            <Text style={styles.summaryLabel}>Avg Score</Text>
          </View>
          <View style={styles.summaryDivider} />
          <View style={styles.summaryItem}>
            <Text style={[styles.summaryValue, { color: COLORS.success }]}>+1.2%</Text>
            <Text style={styles.summaryLabel}>vs Last Month</Text>
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
  metricsGrid: {
    marginBottom: SPACING.md,
  },
  metricRow: {
    flexDirection: 'row',
    marginBottom: SPACING.sm,
  },
  metricCard: {
    flex: 1,
    backgroundColor: COLORS.white,
    borderRadius: BORDER_RADIUS.lg,
    padding: SPACING.md,
    marginHorizontal: SPACING.xs,
    ...SHADOWS.sm,
  },
  metricHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: SPACING.xs,
  },
  iconContainer: {
    width: 28,
    height: 28,
    borderRadius: 14,
    alignItems: 'center',
    justifyContent: 'center',
  },
  trendContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  changeText: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
    marginLeft: SPACING.xs,
  },
  metricName: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
    color: COLORS.textPrimary,
    marginBottom: SPACING.xs,
  },
  valueContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: SPACING.xs,
  },
  metricValue: {
    fontSize: TYPOGRAPHY.fontSize.lg,
    fontWeight: TYPOGRAPHY.fontWeight.bold,
    color: COLORS.textPrimary,
  },
  levelBadge: {
    paddingHorizontal: SPACING.xs,
    paddingVertical: 2,
    borderRadius: BORDER_RADIUS.sm,
  },
  levelText: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
  },
  description: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.textSecondary,
    marginBottom: SPACING.sm,
    lineHeight: 16,
  },
  progressContainer: {
    marginTop: SPACING.xs,
  },
  progressBackground: {
    height: 4,
    backgroundColor: COLORS.surfaceSecondary,
    borderRadius: 2,
    overflow: 'hidden',
  },
  progressBar: {
    height: 4,
    borderRadius: 2,
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
  summaryContent: {
    flexDirection: 'row',
    justifyContent: 'space-around',
  },
  summaryItem: {
    alignItems: 'center',
  },
  summaryValue: {
    fontSize: TYPOGRAPHY.fontSize.lg,
    fontWeight: TYPOGRAPHY.fontWeight.bold,
    color: COLORS.primary,
    marginBottom: 2,
  },
  summaryLabel: {
    fontSize: 9,
    color: COLORS.textSecondary,
  },
  summaryDivider: {
    width: 1,
    backgroundColor: COLORS.gray300,
    marginHorizontal: SPACING.sm,
  },
});

export default PerformanceMetrics;
