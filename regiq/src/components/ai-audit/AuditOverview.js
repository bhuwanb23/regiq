import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { COLORS, TYPOGRAPHY, SPACING, BORDER_RADIUS, SHADOWS } from '../../constants/theme';

const AuditOverview = ({ overviewData }) => {
  const {
    activeModels = 12,
    riskScore = 7.2,
    modelsThisMonth = 2,
    riskLevel = 'Medium Risk',
    totalAudits = 45,
    criticalIssues = 3,
  } = overviewData || {};

  const getRiskColor = (score) => {
    if (score <= 3) return COLORS.success;
    if (score <= 7) return COLORS.warning;
    return COLORS.error;
  };

  const getRiskBackground = (score) => {
    if (score <= 3) return `${COLORS.success}20`;
    if (score <= 7) return `${COLORS.warning}20`;
    return `${COLORS.error}20`;
  };

  const StatCard = ({ title, value, subtitle, icon, iconColor, iconBg, trend }) => (
    <View style={styles.statCard}>
      <View style={styles.statHeader}>
        <Text style={styles.statTitle}>{title}</Text>
        <View style={[styles.statIcon, { backgroundColor: iconBg }]}>
          <Ionicons name={icon} size={14} color={iconColor} />
        </View>
      </View>
      
      <Text style={styles.statValue}>{value}</Text>
      
      <View style={styles.statFooter}>
        <Text style={[
          styles.statSubtitle,
          trend && trend > 0 ? { color: COLORS.success } : 
          trend && trend < 0 ? { color: COLORS.error } : 
          { color: COLORS.textSecondary }
        ]}>
          {subtitle}
        </Text>
      </View>
    </View>
  );

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.title}>Model Overview</Text>
        <Text style={styles.subtitle}>Monitor AI model performance and bias</Text>
      </View>

      {/* Stats Grid */}
      <View style={styles.statsGrid}>
        <StatCard
          title="Active Models"
          value={activeModels}
          subtitle={`+${modelsThisMonth} this month`}
          icon="hardware-chip"
          iconColor={COLORS.secondary}
          iconBg={`${COLORS.secondary}20`}
          trend={modelsThisMonth}
        />
        
        <StatCard
          title="Risk Score"
          value={riskScore}
          subtitle={riskLevel}
          icon="shield-half"
          iconColor={getRiskColor(riskScore)}
          iconBg={getRiskBackground(riskScore)}
        />
      </View>

      {/* Additional Metrics */}
      <View style={styles.metricsRow}>
        <View style={styles.metricItem}>
          <View style={styles.metricHeader}>
            <View style={[styles.metricIcon, { backgroundColor: `${COLORS.info}20` }]}>
              <Ionicons name="analytics" size={12} color={COLORS.info} />
            </View>
            <Text style={styles.metricValue}>{totalAudits}</Text>
          </View>
          <Text style={styles.metricLabel}>Total Audits</Text>
        </View>

        <View style={styles.metricDivider} />

        <View style={styles.metricItem}>
          <View style={styles.metricHeader}>
            <View style={[styles.metricIcon, { backgroundColor: `${COLORS.error}20` }]}>
              <Ionicons name="warning" size={12} color={COLORS.error} />
            </View>
            <Text style={styles.metricValue}>{criticalIssues}</Text>
          </View>
          <Text style={styles.metricLabel}>Critical Issues</Text>
        </View>

        <View style={styles.metricDivider} />

        <View style={styles.metricItem}>
          <View style={styles.metricHeader}>
            <View style={[styles.metricIcon, { backgroundColor: `${COLORS.success}20` }]}>
              <Ionicons name="checkmark-circle" size={12} color={COLORS.success} />
            </View>
            <Text style={styles.metricValue}>{Math.round(((totalAudits - criticalIssues) / totalAudits) * 100)}%</Text>
          </View>
          <Text style={styles.metricLabel}>Passed</Text>
        </View>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    marginBottom: SPACING.md,
  },
  header: {
    marginBottom: SPACING.md,
    paddingHorizontal: SPACING.xs,
  },
  title: {
    fontSize: TYPOGRAPHY.fontSize.lg,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.textPrimary,
    marginBottom: 4,
  },
  subtitle: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    color: COLORS.textSecondary,
  },
  statsGrid: {
    flexDirection: 'row',
    marginBottom: SPACING.md,
    marginHorizontal: -SPACING.xs,
  },
  statCard: {
    flex: 1,
    backgroundColor: COLORS.white,
    borderRadius: BORDER_RADIUS.lg,
    padding: SPACING.sm,
    marginHorizontal: SPACING.xs,
    borderWidth: 1,
    borderColor: COLORS.gray200,
    ...SHADOWS.sm,
  },
  statHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: SPACING.xs,
  },
  statTitle: {
    fontSize: 10,
    color: COLORS.textTertiary,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
    textTransform: 'uppercase',
    letterSpacing: 0.5,
    flex: 1,
  },
  statIcon: {
    width: 24,
    height: 24,
    borderRadius: 12,
    alignItems: 'center',
    justifyContent: 'center',
  },
  statValue: {
    fontSize: TYPOGRAPHY.fontSize.lg,
    fontWeight: TYPOGRAPHY.fontWeight.bold,
    color: COLORS.textPrimary,
    marginBottom: SPACING.xs,
  },
  statFooter: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  statSubtitle: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
  },
  metricsRow: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: COLORS.white,
    borderRadius: BORDER_RADIUS.lg,
    paddingVertical: SPACING.sm,
    paddingHorizontal: SPACING.md,
    ...SHADOWS.sm,
  },
  metricItem: {
    flex: 1,
    alignItems: 'center',
  },
  metricHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 4,
  },
  metricIcon: {
    width: 20,
    height: 20,
    borderRadius: 10,
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: 4,
  },
  metricValue: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    fontWeight: TYPOGRAPHY.fontWeight.bold,
    color: COLORS.textPrimary,
  },
  metricLabel: {
    fontSize: 10,
    color: COLORS.textSecondary,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
    textAlign: 'center',
  },
  metricDivider: {
    width: 1,
    height: 30,
    backgroundColor: COLORS.gray300,
    marginHorizontal: SPACING.sm,
  },
});

export default AuditOverview;
