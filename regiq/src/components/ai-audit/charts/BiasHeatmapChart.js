import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { COLORS, TYPOGRAPHY, SPACING, BORDER_RADIUS, SHADOWS } from '../../../constants/theme';

const BiasHeatmapChart = ({ data }) => {
  const categories = ['Age', 'Gender', 'Region', 'Income', 'Education', 'Employment'];
  const riskLevels = ['Low Risk', 'Medium Risk', 'High Risk'];
  
  const heatmapData = [
    [0.1, 0.3, 0.2, 0.15, 0.08, 0.12],
    [0.2, 0.4, 0.3, 0.25, 0.18, 0.22],
    [0.1, 0.2, 0.4, 0.35, 0.28, 0.31],
  ];

  const getBiasColor = (value) => {
    if (value <= 0.15) return COLORS.success;
    if (value <= 0.25) return COLORS.warning;
    return COLORS.error;
  };

  const getBiasIntensity = (value) => {
    return 0.3 + (value * 0.7); // Opacity between 0.3 and 1.0
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Bias Analysis Heatmap</Text>
      
      {/* Category Headers */}
      <View style={styles.headerRow}>
        <View style={styles.cornerCell} />
        {categories.map((category, index) => (
          <View key={index} style={styles.headerCell}>
            <Text style={styles.headerText}>{category}</Text>
          </View>
        ))}
      </View>

      {/* Heatmap Grid */}
      {riskLevels.map((riskLevel, rowIndex) => (
        <View key={rowIndex} style={styles.dataRow}>
          <View style={styles.rowHeaderCell}>
            <Text style={styles.rowHeaderText}>{riskLevel}</Text>
          </View>
          {heatmapData[rowIndex].map((value, colIndex) => (
            <View
              key={colIndex}
              style={[
                styles.dataCell,
                {
                  backgroundColor: getBiasColor(value),
                  opacity: getBiasIntensity(value),
                }
              ]}
            >
              <Text style={styles.cellValue}>{value.toFixed(2)}</Text>
            </View>
          ))}
        </View>
      ))}

      {/* Legend */}
      <View style={styles.legend}>
        <Text style={styles.legendTitle}>Bias Score</Text>
        <View style={styles.legendItems}>
          <View style={styles.legendItem}>
            <View style={[styles.legendColor, { backgroundColor: COLORS.success }]} />
            <Text style={styles.legendText}>Low (≤0.15)</Text>
          </View>
          <View style={styles.legendItem}>
            <View style={[styles.legendColor, { backgroundColor: COLORS.warning }]} />
            <Text style={styles.legendText}>Medium (0.15-0.25)</Text>
          </View>
          <View style={styles.legendItem}>
            <View style={[styles.legendColor, { backgroundColor: COLORS.error }]} />
            <Text style={styles.legendText}>High ({'>'}0.25)</Text>
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
    padding: SPACING.lg,
    marginBottom: SPACING.md,
    ...SHADOWS.sm,
  },
  title: {
    fontSize: TYPOGRAPHY.fontSize.lg,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.textPrimary,
    marginBottom: SPACING.md,
    textAlign: 'center',
  },
  headerRow: {
    flexDirection: 'row',
    marginBottom: SPACING.xs,
  },
  cornerCell: {
    width: 80,
    height: 30,
  },
  headerCell: {
    flex: 1,
    height: 32,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: COLORS.surfaceSecondary,
    marginHorizontal: 2,
    borderRadius: 6,
  },
  headerText: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
    color: COLORS.textSecondary,
    textAlign: 'center',
  },
  dataRow: {
    flexDirection: 'row',
    marginBottom: SPACING.xs,
  },
  rowHeaderCell: {
    width: 90,
    height: 40,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: COLORS.surfaceSecondary,
    borderRadius: 6,
    marginRight: SPACING.sm,
  },
  rowHeaderText: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
    color: COLORS.textSecondary,
    textAlign: 'center',
  },
  dataCell: {
    flex: 1,
    height: 40,
    justifyContent: 'center',
    alignItems: 'center',
    marginHorizontal: 2,
    borderRadius: 6,
  },
  cellValue: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    fontWeight: TYPOGRAPHY.fontWeight.bold,
    color: COLORS.white,
    textShadowColor: 'rgba(0,0,0,0.3)',
    textShadowOffset: { width: 0, height: 1 },
    textShadowRadius: 1,
  },
  legend: {
    marginTop: SPACING.md,
    paddingTop: SPACING.sm,
    borderTopWidth: 1,
    borderTopColor: COLORS.gray200,
  },
  legendTitle: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.textPrimary,
    marginBottom: SPACING.xs,
  },
  legendItems: {
    flexDirection: 'row',
    justifyContent: 'space-around',
  },
  legendItem: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  legendColor: {
    width: 12,
    height: 12,
    borderRadius: 6,
    marginRight: 4,
  },
  legendText: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.textSecondary,
  },
});

export default BiasHeatmapChart;
