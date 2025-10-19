import React, { useState } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, ScrollView } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { COLORS, TYPOGRAPHY, SPACING, BORDER_RADIUS, SHADOWS } from '../../constants/theme';

const RiskImpactChart = ({ 
  chartData = [],
  timeframe = '7D',
  onTimeframeChange 
}) => {
  const [activeTimeframe, setActiveTimeframe] = useState(timeframe);

  // Mock data for the chart
  const mockData = [
    { day: 'Mon', value: 65, risk: 'medium' },
    { day: 'Tue', value: 72, risk: 'medium' },
    { day: 'Wed', value: 68, risk: 'medium' },
    { day: 'Thu', value: 85, risk: 'high' },
    { day: 'Fri', value: 78, risk: 'high' },
    { day: 'Sat', value: 92, risk: 'high' },
    { day: 'Sun', value: 87, risk: 'high' },
  ];

  // Heatmap data for risk categories
  const heatmapData = [
    { category: 'Credit', low: 10, medium: 19, high: 8 },
    { category: 'Fraud', low: 24, medium: 67, high: 92 },
    { category: 'AML', low: 35, medium: 52, high: 78 },
    { category: 'KYC', low: 15, medium: 44, high: 65 },
    { category: 'Risk', low: 28, medium: 38, high: 85 },
  ];

  const data = chartData.length > 0 ? chartData : mockData;
  const maxValue = Math.max(...data.map(d => d.value));

  const getRiskColor = (risk) => {
    switch (risk) {
      case 'low': return COLORS.success;
      case 'medium': return COLORS.warning;
      case 'high': return COLORS.error;
      default: return COLORS.info;
    }
  };

  const getHeatmapColor = (value) => {
    const intensity = value / 100;
    const baseColor = COLORS.secondary;
    return `${baseColor}${Math.round(intensity * 255).toString(16).padStart(2, '0')}`;
  };

  const handleTimeframePress = (newTimeframe) => {
    setActiveTimeframe(newTimeframe);
    onTimeframeChange?.(newTimeframe);
  };

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.title}>Risk Impact Analysis</Text>
        <View style={styles.timeframeButtons}>
          {['7D', '30D'].map((tf) => (
            <TouchableOpacity
              key={tf}
              style={[
                styles.timeframeButton,
                activeTimeframe === tf && styles.timeframeButtonActive
              ]}
              onPress={() => handleTimeframePress(tf)}
            >
              <Text style={[
                styles.timeframeButtonText,
                activeTimeframe === tf && styles.timeframeButtonTextActive
              ]}>
                {tf}
              </Text>
            </TouchableOpacity>
          ))}
        </View>
      </View>

      {/* Line Chart */}
      <View style={styles.chartContainer}>
        <Text style={styles.chartTitle}>Risk Score Trend</Text>
        
        <View style={styles.lineChart}>
          {/* Y-axis labels */}
          <View style={styles.yAxisLabels}>
            <Text style={styles.axisLabel}>100</Text>
            <Text style={styles.axisLabel}>75</Text>
            <Text style={styles.axisLabel}>50</Text>
            <Text style={styles.axisLabel}>25</Text>
            <Text style={styles.axisLabel}>0</Text>
          </View>

          {/* Chart area */}
          <View style={styles.chartArea}>
            {/* Grid lines */}
            <View style={styles.gridLines}>
              {[0, 1, 2, 3, 4].map((i) => (
                <View key={i} style={styles.gridLine} />
              ))}
            </View>

            {/* Data points */}
            <View style={styles.dataPoints}>
              {data.map((point, index) => (
                <View key={index} style={styles.dataColumn}>
                  <View
                    style={[
                      styles.dataBar,
                      {
                        height: `${(point.value / maxValue) * 80}%`,
                        backgroundColor: getRiskColor(point.risk),
                      }
                    ]}
                  />
                  <View style={[
                    styles.dataPoint,
                    { backgroundColor: getRiskColor(point.risk) }
                  ]}>
                    <Text style={styles.dataPointValue}>{point.value}</Text>
                  </View>
                </View>
              ))}
            </View>

            {/* X-axis labels */}
            <View style={styles.xAxisLabels}>
              {data.map((point, index) => (
                <Text key={index} style={styles.axisLabel}>
                  {point.day}
                </Text>
              ))}
            </View>
          </View>
        </View>
      </View>

      {/* Heatmap */}
      <View style={styles.heatmapContainer}>
        <Text style={styles.chartTitle}>Risk Category Heatmap</Text>
        
        <View style={styles.heatmap}>
          {/* Headers */}
          <View style={styles.heatmapHeader}>
            <View style={styles.heatmapCorner} />
            <Text style={styles.heatmapHeaderText}>Low</Text>
            <Text style={styles.heatmapHeaderText}>Med</Text>
            <Text style={styles.heatmapHeaderText}>High</Text>
          </View>

          {/* Data rows */}
          {heatmapData.map((row, index) => (
            <View key={index} style={styles.heatmapRow}>
              <Text style={styles.heatmapRowLabel}>{row.category}</Text>
              <View style={[
                styles.heatmapCell,
                { backgroundColor: getHeatmapColor(row.low) }
              ]}>
                <Text style={styles.heatmapCellText}>{row.low}</Text>
              </View>
              <View style={[
                styles.heatmapCell,
                { backgroundColor: getHeatmapColor(row.medium) }
              ]}>
                <Text style={styles.heatmapCellText}>{row.medium}</Text>
              </View>
              <View style={[
                styles.heatmapCell,
                { backgroundColor: getHeatmapColor(row.high) }
              ]}>
                <Text style={styles.heatmapCellText}>{row.high}</Text>
              </View>
            </View>
          ))}
        </View>
      </View>

      {/* Legend */}
      <View style={styles.legend}>
        <View style={styles.legendItem}>
          <View style={[styles.legendColor, { backgroundColor: COLORS.success }]} />
          <Text style={styles.legendText}>Low Risk (0-40)</Text>
        </View>
        <View style={styles.legendItem}>
          <View style={[styles.legendColor, { backgroundColor: COLORS.warning }]} />
          <Text style={styles.legendText}>Medium (41-70)</Text>
        </View>
        <View style={styles.legendItem}>
          <View style={[styles.legendColor, { backgroundColor: COLORS.error }]} />
          <Text style={styles.legendText}>High (71-100)</Text>
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
    borderWidth: 1,
    borderColor: COLORS.gray200,
    marginBottom: SPACING.md,
    ...SHADOWS.sm,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: SPACING.md,
  },
  title: {
    fontSize: TYPOGRAPHY.fontSize.base,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.primary,
  },
  timeframeButtons: {
    flexDirection: 'row',
    gap: SPACING.xs,
  },
  timeframeButton: {
    paddingHorizontal: SPACING.sm,
    paddingVertical: SPACING.xs,
    borderRadius: BORDER_RADIUS.full,
    backgroundColor: COLORS.surfaceSecondary,
  },
  timeframeButtonActive: {
    backgroundColor: COLORS.secondary,
  },
  timeframeButtonText: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.textSecondary,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
  },
  timeframeButtonTextActive: {
    color: COLORS.white,
  },
  chartContainer: {
    marginBottom: SPACING.lg,
  },
  chartTitle: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.textPrimary,
    marginBottom: SPACING.sm,
  },
  lineChart: {
    flexDirection: 'row',
    height: 120,
  },
  yAxisLabels: {
    justifyContent: 'space-between',
    paddingVertical: SPACING.xs,
    marginRight: SPACING.sm,
  },
  axisLabel: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.textSecondary,
  },
  chartArea: {
    flex: 1,
    position: 'relative',
  },
  gridLines: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 20,
    justifyContent: 'space-between',
  },
  gridLine: {
    height: 1,
    backgroundColor: COLORS.gray200,
  },
  dataPoints: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-end',
    height: 100,
    paddingHorizontal: SPACING.xs,
  },
  dataColumn: {
    alignItems: 'center',
    flex: 1,
  },
  dataBar: {
    width: 8,
    borderRadius: 4,
    marginBottom: SPACING.xs,
  },
  dataPoint: {
    width: 20,
    height: 20,
    borderRadius: 10,
    alignItems: 'center',
    justifyContent: 'center',
  },
  dataPointValue: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.white,
    fontWeight: TYPOGRAPHY.fontWeight.bold,
  },
  xAxisLabels: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingHorizontal: SPACING.xs,
    marginTop: SPACING.xs,
  },
  heatmapContainer: {
    marginBottom: SPACING.md,
  },
  heatmap: {
    backgroundColor: COLORS.surfaceSecondary,
    borderRadius: BORDER_RADIUS.md,
    padding: SPACING.sm,
  },
  heatmapHeader: {
    flexDirection: 'row',
    marginBottom: SPACING.xs,
  },
  heatmapCorner: {
    width: 50,
  },
  heatmapHeaderText: {
    flex: 1,
    fontSize: TYPOGRAPHY.fontSize.xs,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.textSecondary,
    textAlign: 'center',
  },
  heatmapRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: SPACING.xs,
  },
  heatmapRowLabel: {
    width: 50,
    fontSize: TYPOGRAPHY.fontSize.xs,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
    color: COLORS.textSecondary,
  },
  heatmapCell: {
    flex: 1,
    height: 30,
    alignItems: 'center',
    justifyContent: 'center',
    marginHorizontal: 1,
    borderRadius: 4,
  },
  heatmapCellText: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    fontWeight: TYPOGRAPHY.fontWeight.bold,
    color: COLORS.white,
  },
  legend: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    paddingTop: SPACING.sm,
    borderTopWidth: 1,
    borderTopColor: COLORS.gray200,
  },
  legendItem: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  legendColor: {
    width: 10,
    height: 10,
    borderRadius: 5,
    marginRight: SPACING.xs,
  },
  legendText: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.textSecondary,
  },
});

export default RiskImpactChart;
