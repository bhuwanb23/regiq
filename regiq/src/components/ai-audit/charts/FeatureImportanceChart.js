import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { COLORS, TYPOGRAPHY, SPACING, BORDER_RADIUS, SHADOWS } from '../../../constants/theme';

const FeatureImportanceChart = ({ data }) => {
  const features = [
    { name: 'Income Level', value: 0.35, icon: 'cash', trend: 'up' },
    { name: 'Credit History', value: 0.32, icon: 'card', trend: 'up' },
    { name: 'Age', value: 0.15, icon: 'person', trend: 'down' },
    { name: 'Employment Status', value: 0.12, icon: 'briefcase', trend: 'up' },
    { name: 'Debt-to-Income Ratio', value: 0.06, icon: 'trending-down', trend: 'down' },
    { name: 'Geographic Location', value: 0.04, icon: 'location', trend: 'stable' },
    { name: 'Education Level', value: 0.03, icon: 'school', trend: 'up' },
    { name: 'Account History', value: 0.02, icon: 'time', trend: 'stable' },
  ];

  const getBarColor = (value) => {
    if (value >= 0.3) return COLORS.primary;
    if (value >= 0.15) return COLORS.secondary;
    if (value >= 0.05) return COLORS.accent;
    return COLORS.gray400;
  };

  const getTrendIcon = (trend) => {
    switch (trend) {
      case 'up': return 'trending-up';
      case 'down': return 'trending-down';
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

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Feature Importance Analysis</Text>
      <Text style={styles.subtitle}>Impact of each feature on model decisions</Text>
      
      <View style={styles.chartContainer}>
        {features.map((feature, index) => (
          <View key={index} style={styles.featureRow}>
            <View style={styles.featureInfo}>
              <View style={styles.featureHeader}>
                <Ionicons name={feature.icon} size={14} color={COLORS.textSecondary} />
                <Text style={styles.featureName}>{feature.name}</Text>
                <Ionicons 
                  name={getTrendIcon(feature.trend)} 
                  size={10} 
                  color={getTrendColor(feature.trend)} 
                />
              </View>
              
              <View style={styles.barContainer}>
                <View
                  style={[
                    styles.bar,
                    {
                      width: `${feature.value * 100}%`,
                      backgroundColor: getBarColor(feature.value),
                    }
                  ]}
                />
                <View style={styles.barBackground} />
              </View>
            </View>
            
            <View style={styles.valueContainer}>
              <Text style={styles.percentage}>{(feature.value * 100).toFixed(1)}%</Text>
              <Text style={styles.importance}>
                {feature.value >= 0.3 ? 'Critical' : 
                 feature.value >= 0.15 ? 'High' : 
                 feature.value >= 0.05 ? 'Medium' : 'Low'}
              </Text>
            </View>
          </View>
        ))}
      </View>

      {/* Summary Stats */}
      <View style={styles.summaryContainer}>
        <View style={styles.summaryItem}>
          <Text style={styles.summaryValue}>
            {features.filter(f => f.value >= 0.15).length}
          </Text>
          <Text style={styles.summaryLabel}>High Impact</Text>
        </View>
        <View style={styles.summaryDivider} />
        <View style={styles.summaryItem}>
          <Text style={styles.summaryValue}>
            {(features.slice(0, 3).reduce((sum, f) => sum + f.value, 0) * 100).toFixed(0)}%
          </Text>
          <Text style={styles.summaryLabel}>Top 3 Features</Text>
        </View>
        <View style={styles.summaryDivider} />
        <View style={styles.summaryItem}>
          <Text style={styles.summaryValue}>
            {features.filter(f => f.trend === 'up').length}
          </Text>
          <Text style={styles.summaryLabel}>Trending Up</Text>
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
  chartContainer: {
    marginBottom: SPACING.md,
  },
  featureRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: SPACING.md,
    paddingVertical: SPACING.sm,
    backgroundColor: COLORS.surfaceSecondary,
    borderRadius: BORDER_RADIUS.md,
    paddingHorizontal: SPACING.sm,
  },
  featureInfo: {
    flex: 1,
    marginRight: SPACING.sm,
  },
  featureHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: SPACING.xs,
  },
  featureName: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
    color: COLORS.textPrimary,
    flex: 1,
    marginLeft: SPACING.xs,
  },
  barContainer: {
    position: 'relative',
    height: 10,
    marginTop: SPACING.xs,
  },
  bar: {
    height: 10,
    borderRadius: 5,
    position: 'absolute',
    left: 0,
    top: 0,
    zIndex: 1,
  },
  barBackground: {
    height: 10,
    backgroundColor: COLORS.gray300,
    borderRadius: 5,
    position: 'absolute',
    left: 0,
    right: 0,
    top: 0,
  },
  valueContainer: {
    alignItems: 'flex-end',
    minWidth: 60,
  },
  percentage: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    fontWeight: TYPOGRAPHY.fontWeight.bold,
    color: COLORS.textPrimary,
  },
  importance: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.textSecondary,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
  },
  summaryContainer: {
    flexDirection: 'row',
    backgroundColor: COLORS.surfaceSecondary,
    borderRadius: BORDER_RADIUS.md,
    paddingVertical: SPACING.sm,
    paddingHorizontal: SPACING.md,
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
    fontSize: 9,
    color: COLORS.textSecondary,
    textAlign: 'center',
  },
  summaryDivider: {
    width: 1,
    backgroundColor: COLORS.gray300,
    marginHorizontal: SPACING.sm,
  },
});

export default FeatureImportanceChart;
