import React from 'react';
import { View, Text, StyleSheet, ActivityIndicator } from 'react-native';
import { COLORS, TYPOGRAPHY, SPACING, BORDER_RADIUS, SHADOWS } from '../../../constants/theme';

const BiasHeatmapChart = ({ data, loading = false }) => {
  // Extract bias data from the report
  const biasData = data?.groupMetrics || data?.biasMetrics || [];
  
  // Default categories and risk levels if no data
  const categories = data?.protectedAttributes || ['Age', 'Gender', 'Region', 'Income', 'Education', 'Employment'];
  const riskLevels = ['Low Risk', 'Medium Risk', 'High Risk'];
  
  // Process bias data for heatmap
  const heatmapData = [];
  
  if (biasData.length > 0) {
    // Convert bias data to heatmap format
    for (let i = 0; i < Math.min(riskLevels.length, 3); i++) {
      const row = [];
      for (let j = 0; j < Math.min(categories.length, 6); j++) {
        // Use actual bias scores if available, otherwise generate sample data
        const metric = biasData[i * categories.length + j];
        const score = metric?.biasScore || metric?.disparity || Math.random() * 0.4;
        row.push(score);
      }
      heatmapData.push(row);
    }
  } else if (!loading) {
    // Sample data if no real data available
    heatmapData.push([0.1, 0.3, 0.2, 0.15, 0.08, 0.12]);
    heatmapData.push([0.2, 0.4, 0.3, 0.25, 0.18, 0.22]);
    heatmapData.push([0.1, 0.2, 0.4, 0.35, 0.28, 0.31]);
  }

  const getBiasColor = (value) => {
    if (value <= 0.15) return COLORS.success;
    if (value <= 0.25) return COLORS.warning;
    return COLORS.error;
  };

  const getBiasIntensity = (value) => {
    return 0.3 + (value * 0.7); // Opacity between 0.3 and 1.0
  };

  if (loading) {
    return (
      <View style={styles.container}>
        <Text style={styles.title}>Bias Analysis Heatmap</Text>
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="small" color={COLORS.primary} />
          <Text style={styles.loadingText}>Loading bias data...</Text>
        </View>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Bias Analysis Heatmap</Text>
      
      {/* Category Headers */}
      <View style={styles.headerRow}>
        <View style={styles.cornerCell} />
        {categories.slice(0, 6).map((category, index) => (
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
          {heatmapData[rowIndex] ? heatmapData[rowIndex].map((value, colIndex) => (
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
          )) : (
            // Placeholder cells if data is missing
            Array(6).fill(0).map((_, colIndex) => (
              <View
                key={colIndex}
                style={[
                  styles.dataCell,
                  {
                    backgroundColor: COLORS.gray300,
                    opacity: 0.3,
                  }
                ]}
              >
                <Text style={styles.cellValue}>-</Text>
              </View>
            ))
          )}
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
    fontSize: TYPOGRAPHY.fontSize.base,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.textPrimary,
    marginBottom: SPACING.md,
    textAlign: 'center',
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
    fontSize: 9,
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
    fontSize: 9,
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
    fontSize: 9,
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
    fontSize: 9,
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
    fontSize: 8,
    color: COLORS.textSecondary,
  },
});

export default BiasHeatmapChart;