import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { COLORS, TYPOGRAPHY, SPACING, BORDER_RADIUS, SHADOWS } from '../../../constants/theme';

const ModelDriftChart = ({ data }) => {
  const driftData = [
    { period: 'Week 1', value: 0.02, status: 'stable' },
    { period: 'Week 2', value: 0.04, status: 'stable' },
    { period: 'Week 3', value: 0.03, status: 'stable' },
    { period: 'Week 4', value: 0.05, status: 'warning' },
    { period: 'Week 5', value: 0.07, status: 'warning' },
    { period: 'Week 6', value: 0.06, status: 'warning' },
    { period: 'Week 7', value: 0.04, status: 'stable' },
    { period: 'Week 8', value: 0.03, status: 'stable' },
  ];

  const maxValue = Math.max(...driftData.map(d => d.value));
  const warningThreshold = 0.05;
  const criticalThreshold = 0.08;

  const getDriftColor = (value) => {
    if (value >= criticalThreshold) return COLORS.error;
    if (value >= warningThreshold) return COLORS.warning;
    return COLORS.success;
  };

  const getDriftStatus = (value) => {
    if (value >= criticalThreshold) return 'Critical';
    if (value >= warningThreshold) return 'Warning';
    return 'Stable';
  };

  const getStatusIcon = (value) => {
    if (value >= criticalThreshold) return 'alert-circle';
    if (value >= warningThreshold) return 'warning';
    return 'checkmark-circle';
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Model Drift Detection</Text>
      <Text style={styles.subtitle}>Performance degradation over time</Text>

      {/* Chart Area */}
      <View style={styles.chartContainer}>
        {/* Threshold Lines */}
        <View style={styles.thresholdContainer}>
          <View style={[styles.thresholdLine, { 
            bottom: `${(criticalThreshold / maxValue) * 80}%`,
            backgroundColor: COLORS.error 
          }]} />
          <View style={[styles.thresholdLine, { 
            bottom: `${(warningThreshold / maxValue) * 80}%`,
            backgroundColor: COLORS.warning 
          }]} />
        </View>

        {/* Data Points */}
        <View style={styles.dataContainer}>
          {driftData.map((point, index) => (
            <View key={index} style={styles.dataPoint}>
              <View
                style={[
                  styles.bar,
                  {
                    height: `${(point.value / maxValue) * 80}%`,
                    backgroundColor: getDriftColor(point.value),
                  }
                ]}
              />
              <View style={[
                styles.dot,
                { backgroundColor: getDriftColor(point.value) }
              ]}>
                <Text style={styles.dotValue}>{point.value.toFixed(2)}</Text>
              </View>
            </View>
          ))}
        </View>

        {/* X-axis Labels */}
        <View style={styles.xAxisContainer}>
          {driftData.map((point, index) => (
            <Text key={index} style={styles.xAxisLabel}>
              {point.period.replace('Week ', 'W')}
            </Text>
          ))}
        </View>
      </View>

      {/* Current Status */}
      <View style={styles.statusContainer}>
        <View style={styles.currentStatus}>
          <Ionicons 
            name={getStatusIcon(driftData[driftData.length - 1].value)} 
            size={16} 
            color={getDriftColor(driftData[driftData.length - 1].value)} 
          />
          <Text style={styles.statusText}>
            Current Status: {getDriftStatus(driftData[driftData.length - 1].value)}
          </Text>
        </View>
        
        <Text style={styles.currentValue}>
          {driftData[driftData.length - 1].value.toFixed(3)}
        </Text>
      </View>

      {/* Metrics */}
      <View style={styles.metricsContainer}>
        <View style={styles.metricItem}>
          <Text style={styles.metricValue}>
            {Math.max(...driftData.map(d => d.value)).toFixed(3)}
          </Text>
          <Text style={styles.metricLabel}>Peak Drift</Text>
        </View>
        
        <View style={styles.metricDivider} />
        
        <View style={styles.metricItem}>
          <Text style={styles.metricValue}>
            {(driftData.reduce((sum, d) => sum + d.value, 0) / driftData.length).toFixed(3)}
          </Text>
          <Text style={styles.metricLabel}>Average</Text>
        </View>
        
        <View style={styles.metricDivider} />
        
        <View style={styles.metricItem}>
          <Text style={[
            styles.metricValue,
            { color: driftData[driftData.length - 1].value > driftData[driftData.length - 2].value ? COLORS.error : COLORS.success }
          ]}>
            {driftData[driftData.length - 1].value > driftData[driftData.length - 2].value ? '+' : ''}
            {((driftData[driftData.length - 1].value - driftData[driftData.length - 2].value) * 100).toFixed(1)}%
          </Text>
          <Text style={styles.metricLabel}>Week Change</Text>
        </View>
      </View>

      {/* Legend */}
      <View style={styles.legend}>
        <View style={styles.legendItem}>
          <View style={[styles.legendColor, { backgroundColor: COLORS.success }]} />
          <Text style={styles.legendText}>Stable (&lt;0.05)</Text>
        </View>
        <View style={styles.legendItem}>
          <View style={[styles.legendColor, { backgroundColor: COLORS.warning }]} />
          <Text style={styles.legendText}>Warning (0.05-0.08)</Text>
        </View>
        <View style={styles.legendItem}>
          <View style={[styles.legendColor, { backgroundColor: COLORS.error }]} />
          <Text style={styles.legendText}>Critical (&gt;0.08)</Text>
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
    height: 140,
    marginBottom: SPACING.md,
    position: 'relative',
  },
  thresholdContainer: {
    position: 'absolute',
    left: 0,
    right: 0,
    top: 0,
    bottom: 20,
  },
  thresholdLine: {
    position: 'absolute',
    left: 0,
    right: 0,
    height: 1,
    opacity: 0.5,
  },
  dataContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-end',
    height: 110,
    paddingHorizontal: SPACING.sm,
  },
  dataPoint: {
    alignItems: 'center',
    flex: 1,
    marginHorizontal: 1,
  },
  bar: {
    width: 12,
    borderRadius: 6,
    minHeight: 8,
  },
  dot: {
    width: 20,
    height: 20,
    borderRadius: 10,
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: 6,
    borderWidth: 2,
    borderColor: COLORS.white,
  },
  dotValue: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.white,
    fontWeight: TYPOGRAPHY.fontWeight.bold,
    textShadowColor: 'rgba(0,0,0,0.5)',
    textShadowOffset: { width: 0, height: 1 },
    textShadowRadius: 1,
  },
  xAxisContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingHorizontal: SPACING.sm,
    marginTop: SPACING.sm,
    backgroundColor: COLORS.surfaceSecondary,
    borderRadius: BORDER_RADIUS.sm,
    paddingVertical: SPACING.xs,
  },
  xAxisLabel: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.textSecondary,
    textAlign: 'center',
    flex: 1,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
  },
  statusContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    backgroundColor: COLORS.surfaceSecondary,
    borderRadius: BORDER_RADIUS.md,
    padding: SPACING.sm,
    marginBottom: SPACING.md,
  },
  currentStatus: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  statusText: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
    color: COLORS.textPrimary,
    marginLeft: SPACING.xs,
  },
  currentValue: {
    fontSize: TYPOGRAPHY.fontSize.lg,
    fontWeight: TYPOGRAPHY.fontWeight.bold,
    color: COLORS.primary,
  },
  metricsContainer: {
    flexDirection: 'row',
    backgroundColor: COLORS.surfaceSecondary,
    borderRadius: BORDER_RADIUS.md,
    paddingVertical: SPACING.sm,
    paddingHorizontal: SPACING.md,
    marginBottom: SPACING.md,
  },
  metricItem: {
    flex: 1,
    alignItems: 'center',
  },
  metricValue: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    fontWeight: TYPOGRAPHY.fontWeight.bold,
    color: COLORS.textPrimary,
    marginBottom: 2,
  },
  metricLabel: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.textSecondary,
    textAlign: 'center',
  },
  metricDivider: {
    width: 1,
    backgroundColor: COLORS.gray300,
    marginHorizontal: SPACING.sm,
  },
  legend: {
    flexDirection: 'row',
    justifyContent: 'space-around',
  },
  legendItem: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  legendColor: {
    width: 10,
    height: 10,
    borderRadius: 5,
    marginRight: 4,
  },
  legendText: {
    fontSize: 9,
    color: COLORS.textSecondary,
  },
});

export default ModelDriftChart;
