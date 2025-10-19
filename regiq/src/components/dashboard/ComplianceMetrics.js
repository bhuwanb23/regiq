import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';
import ComplianceGauge from '../common/ComplianceGauge';
import { COLORS, TYPOGRAPHY, SPACING, BORDER_RADIUS, SHADOWS } from '../../constants/theme';

const ComplianceMetrics = ({ 
  complianceScore = 78, 
  regulations = 12, 
  alerts = 2, 
  onViewDetails,
  onGenerateReport 
}) => {
  const getComplianceStatus = (score) => {
    if (score >= 90) return { text: 'Excellent', color: COLORS.success };
    if (score >= 80) return { text: 'Good', color: COLORS.info };
    if (score >= 70) return { text: 'Fair', color: COLORS.warning };
    return { text: 'Needs Attention', color: COLORS.error };
  };

  const status = getComplianceStatus(complianceScore);

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.title}>Compliance Health</Text>
        <TouchableOpacity onPress={onViewDetails}>
          <Text style={styles.viewDetailsText}>Details</Text>
        </TouchableOpacity>
      </View>

      {/* Main Score Display */}
      <View style={styles.scoreContainer}>
        <View style={styles.scoreCircle}>
          <Text style={styles.scoreNumber}>{complianceScore}</Text>
          <Text style={styles.scorePercent}>%</Text>
        </View>
        <View style={styles.scoreInfo}>
          <Text style={[styles.scoreStatus, { color: status.color }]}>
            {status.text}
          </Text>
          <Text style={styles.scoreSubtext}>Overall Score</Text>
        </View>
      </View>

      {/* Compact Metrics */}
      <View style={styles.metricsRow}>
        <View style={styles.metricItem}>
          <View style={styles.metricIconSmall}>
            <Ionicons name="shield-checkmark" size={12} color={COLORS.primary} />
          </View>
          <Text style={styles.metricNumber}>{regulations}</Text>
          <Text style={styles.metricText}>Regulations</Text>
        </View>
        
        <View style={styles.metricDivider} />
        
        <View style={styles.metricItem}>
          <View style={styles.metricIconSmall}>
            <Ionicons name="warning" size={12} color={COLORS.warning} />
          </View>
          <Text style={styles.metricNumber}>{alerts}</Text>
          <Text style={styles.metricText}>Alerts</Text>
        </View>
        
        <View style={styles.metricDivider} />
        
        <View style={styles.metricItem}>
          <View style={styles.metricIconSmall}>
            <Ionicons name="checkmark-circle" size={12} color={COLORS.success} />
          </View>
          <Text style={styles.metricNumber}>98%</Text>
          <Text style={styles.metricText}>Passed</Text>
        </View>
      </View>

      {/* Compact Actions */}
      <View style={styles.actionsRow}>
        <TouchableOpacity 
          style={styles.actionButton}
          onPress={onGenerateReport}
        >
          <Ionicons name="document-text" size={12} color={COLORS.primary} />
          <Text style={styles.actionText}>Report</Text>
        </TouchableOpacity>
        
        <TouchableOpacity style={styles.actionButton}>
          <Ionicons name="analytics" size={12} color={COLORS.primary} />
          <Text style={styles.actionText}>Trends</Text>
        </TouchableOpacity>
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
    ...SHADOWS.sm,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: SPACING.sm,
  },
  title: {
    fontSize: TYPOGRAPHY.fontSize.base,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.textPrimary,
  },
  viewDetailsText: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.primary,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
  },
  scoreContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: SPACING.md,
    paddingVertical: SPACING.sm,
    paddingHorizontal: SPACING.sm,
  },
  scoreCircle: {
    width: 60,
    height: 60,
    borderRadius: 30,
    backgroundColor: `${COLORS.primary}15`,
    borderWidth: 3,
    borderColor: COLORS.primary,
    alignItems: 'center',
    justifyContent: 'center',
    flexDirection: 'row',
    marginRight: SPACING.md,
  },
  scoreNumber: {
    fontSize: TYPOGRAPHY.fontSize.lg,
    fontWeight: TYPOGRAPHY.fontWeight.bold,
    color: COLORS.primary,
  },
  scorePercent: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
    color: COLORS.primary,
    marginTop: -2,
  },
  scoreInfo: {
    flex: 1,
  },
  scoreStatus: {
    fontSize: TYPOGRAPHY.fontSize.base,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
  },
  scoreSubtext: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.textSecondary,
    marginTop: 2,
  },
  metricsRow: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: COLORS.surfaceSecondary,
    borderRadius: BORDER_RADIUS.sm,
    paddingVertical: SPACING.sm,
    paddingHorizontal: SPACING.sm,
    marginBottom: SPACING.sm,
  },
  metricItem: {
    flex: 1,
    alignItems: 'center',
  },
  metricIconSmall: {
    width: 20,
    height: 20,
    borderRadius: 10,
    backgroundColor: COLORS.white,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 4,
    ...SHADOWS.sm,
  },
  metricNumber: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    fontWeight: TYPOGRAPHY.fontWeight.bold,
    color: COLORS.textPrimary,
    marginBottom: 2,
  },
  metricText: {
    fontSize: 10,
    color: COLORS.textSecondary,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
  },
  metricDivider: {
    width: 1,
    height: 30,
    backgroundColor: COLORS.gray300,
    marginHorizontal: SPACING.xs,
  },
  actionsRow: {
    flexDirection: 'row',
    justifyContent: 'space-around',
  },
  actionButton: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: SPACING.xs,
    paddingHorizontal: SPACING.sm,
    borderRadius: BORDER_RADIUS.sm,
    backgroundColor: `${COLORS.primary}10`,
  },
  actionText: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.primary,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
    marginLeft: 4,
  },
  breakdownSection: {
    marginTop: SPACING.md,
  },
  breakdownTitle: {
    fontSize: TYPOGRAPHY.fontSize.base,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.textPrimary,
    marginBottom: SPACING.md,
  },
  breakdownItem: {
    marginBottom: SPACING.md,
  },
  breakdownHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: SPACING.xs,
  },
  breakdownLabel: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    color: COLORS.textSecondary,
  },
  breakdownScore: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
    color: COLORS.textPrimary,
  },
  progressBar: {
    height: 6,
    backgroundColor: COLORS.gray200,
    borderRadius: BORDER_RADIUS.sm,
    overflow: 'hidden',
  },
  progressFill: {
    height: '100%',
    borderRadius: BORDER_RADIUS.sm,
  },
});

export default ComplianceMetrics;
