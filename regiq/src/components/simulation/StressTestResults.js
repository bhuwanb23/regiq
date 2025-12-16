import React from 'react';
import { View, Text, StyleSheet, FlatList } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { COLORS, TYPOGRAPHY, SPACING, BORDER_RADIUS, SHADOWS } from '../../constants/theme';

const StressTestResults = ({ stressTestData = [], loading = false }) => {
  if (loading) {
    return (
      <View style={styles.container}>
        <Text style={styles.title}>Stress Test Results</Text>
        <View style={styles.loadingContainer}>
          <Text style={styles.loadingText}>Running stress tests...</Text>
        </View>
      </View>
    );
  }

  const getSeverityColor = (severity) => {
    switch (severity?.toLowerCase()) {
      case 'low': return COLORS.success;
      case 'medium': return COLORS.warning;
      case 'high': return COLORS.error;
      default: return COLORS.info;
    }
  };

  const getSeverityBackground = (severity) => {
    switch (severity?.toLowerCase()) {
      case 'low': return `${COLORS.success}15`;
      case 'medium': return `${COLORS.warning}15`;
      case 'high': return `${COLORS.error}15`;
      default: return `${COLORS.info}15`;
    }
  };

  const getStatusIcon = (status) => {
    switch (status?.toLowerCase()) {
      case 'passed': return 'checkmark-circle';
      case 'failed': return 'close-circle';
      case 'warning': return 'warning';
      default: return 'help-circle';
    }
  };

  const getStatusColor = (status) => {
    switch (status?.toLowerCase()) {
      case 'passed': return COLORS.success;
      case 'failed': return COLORS.error;
      case 'warning': return COLORS.warning;
      default: return COLORS.info;
    }
  };

  const renderTestResult = ({ item }) => (
    <View style={styles.resultCard}>
      <View style={styles.resultHeader}>
        <View style={styles.resultInfo}>
          <Text style={styles.resultTitle}>{item.testName || 'Unnamed Test'}</Text>
          <Text style={styles.resultDescription} numberOfLines={2}>
            {item.description || 'No description available'}
          </Text>
        </View>
        <View style={[
          styles.severityBadge,
          { backgroundColor: getSeverityBackground(item.severity) }
        ]}>
          <Text style={[
            styles.severityText,
            { color: getSeverityColor(item.severity) }
          ]}>
            {item.severity || 'Medium'}
          </Text>
        </View>
      </View>

      <View style={styles.resultDetails}>
        <View style={styles.detailRow}>
          <Ionicons 
            name={getStatusIcon(item.status)} 
            size={16} 
            color={getStatusColor(item.status)} 
          />
          <Text style={[
            styles.statusText,
            { color: getStatusColor(item.status) }
          ]}>
            {item.status || 'Unknown'}
          </Text>
        </View>

        <View style={styles.metrics}>
          <View style={styles.metricItem}>
            <Text style={styles.metricLabel}>Impact</Text>
            <Text style={styles.metricValue}>{item.impact || 'N/A'}</Text>
          </View>
          <View style={styles.metricItem}>
            <Text style={styles.metricLabel}>Duration</Text>
            <Text style={styles.metricValue}>{item.duration || 'N/A'}</Text>
          </View>
          <View style={styles.metricItem}>
            <Text style={styles.metricLabel}>Recovery</Text>
            <Text style={styles.metricValue}>{item.recoveryTime || 'N/A'}</Text>
          </View>
        </View>
      </View>

      {item.recommendations && item.recommendations.length > 0 && (
        <View style={styles.recommendations}>
          <Text style={styles.recommendationsTitle}>Recommendations</Text>
          {item.recommendations.map((rec, index) => (
            <View key={index} style={styles.recommendationItem}>
              <View style={styles.bulletPoint} />
              <Text style={styles.recommendationText}>{rec}</Text>
            </View>
          ))}
        </View>
      )}
    </View>
  );

  // Default data if none provided
  const defaultData = [
    {
      id: '1',
      testName: 'Market Crash Simulation',
      description: 'Simulating 25% market drop to test portfolio resilience',
      severity: 'high',
      status: 'warning',
      impact: '15.2%',
      duration: '2h',
      recoveryTime: '4d',
      recommendations: [
        'Increase cash reserves by 10%',
        'Diversify portfolio holdings',
        'Implement dynamic hedging strategy'
      ]
    },
    {
      id: '2',
      testName: 'Liquidity Stress Test',
      description: 'Testing withdrawal capacity during high-demand periods',
      severity: 'medium',
      status: 'passed',
      impact: '3.7%',
      duration: '1h',
      recoveryTime: '1d',
      recommendations: [
        'Maintain 15% liquid assets',
        'Establish credit facilities'
      ]
    },
    {
      id: '3',
      testName: 'Regulatory Capital Test',
      description: 'Validating capital adequacy under stressed conditions',
      severity: 'high',
      status: 'failed',
      impact: '22.8%',
      duration: '3h',
      recoveryTime: '7d',
      recommendations: [
        'Raise additional capital',
        'Reduce risk-weighted assets',
        'Optimize capital allocation'
      ]
    }
  ];

  const dataToShow = stressTestData.length > 0 ? stressTestData : defaultData;

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Stress Test Results</Text>
      
      <FlatList
        data={dataToShow}
        renderItem={renderTestResult}
        keyExtractor={(item) => item.id}
        style={styles.resultsList}
        showsVerticalScrollIndicator={false}
        contentContainerStyle={styles.listContent}
      />
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
    alignItems: 'center',
    justifyContent: 'center',
    padding: SPACING.xl,
  },
  loadingText: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    color: COLORS.textSecondary,
  },
  resultsList: {
    flex: 1,
  },
  listContent: {
    paddingBottom: SPACING.sm,
  },
  resultCard: {
    backgroundColor: COLORS.surfaceSecondary,
    borderRadius: BORDER_RADIUS.md,
    padding: SPACING.md,
    marginBottom: SPACING.md,
  },
  resultHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: SPACING.sm,
  },
  resultInfo: {
    flex: 1,
    marginRight: SPACING.sm,
  },
  resultTitle: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.textPrimary,
    marginBottom: SPACING.xs,
  },
  resultDescription: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.textSecondary,
  },
  severityBadge: {
    paddingHorizontal: SPACING.xs,
    paddingVertical: 2,
    borderRadius: BORDER_RADIUS.full,
  },
  severityText: {
    fontSize: 10,
    fontWeight: TYPOGRAPHY.fontWeight.bold,
    textTransform: 'uppercase',
  },
  resultDetails: {
    marginBottom: SPACING.sm,
  },
  detailRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: SPACING.sm,
  },
  statusText: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
    marginLeft: SPACING.xs,
  },
  metrics: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  metricItem: {
    alignItems: 'center',
  },
  metricLabel: {
    fontSize: 9,
    color: COLORS.textSecondary,
    marginBottom: 2,
  },
  metricValue: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    fontWeight: TYPOGRAPHY.fontWeight.bold,
    color: COLORS.textPrimary,
  },
  recommendations: {
    borderTopWidth: 1,
    borderTopColor: COLORS.gray300,
    paddingTop: SPACING.sm,
  },
  recommendationsTitle: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.textPrimary,
    marginBottom: SPACING.xs,
  },
  recommendationItem: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    marginBottom: SPACING.xs,
  },
  bulletPoint: {
    width: 4,
    height: 4,
    borderRadius: 2,
    backgroundColor: COLORS.primary,
    marginRight: SPACING.sm,
    marginTop: 6,
  },
  recommendationText: {
    fontSize: 9,
    color: COLORS.textSecondary,
    flex: 1,
    lineHeight: 14,
  },
});

export default StressTestResults;