import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { COLORS, TYPOGRAPHY, SPACING, BORDER_RADIUS, SHADOWS } from '../../constants/theme';

const ReportsStatsCard = () => {
  const stats = [
    {
      icon: 'document-text',
      value: '24',
      label: 'Total Reports',
      color: COLORS.primary,
      backgroundColor: `${COLORS.primary}15`,
    },
    {
      icon: 'checkmark-circle',
      value: '18',
      label: 'Completed',
      color: COLORS.success,
      backgroundColor: `${COLORS.success}15`,
    },
    {
      icon: 'time',
      value: '4',
      label: 'In Progress',
      color: COLORS.warning,
      backgroundColor: `${COLORS.warning}15`,
    },
    {
      icon: 'close-circle',
      value: '2',
      label: 'Failed',
      color: COLORS.error,
      backgroundColor: `${COLORS.error}15`,
    },
  ];

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Reports Overview</Text>
      
      <View style={styles.statsGrid}>
        {stats.map((stat, index) => (
          <View key={index} style={styles.statCard}>
            <View style={[styles.iconContainer, { backgroundColor: stat.backgroundColor }]}>
              <Ionicons name={stat.icon} size={20} color={stat.color} />
            </View>
            
            <Text style={[styles.statValue, { color: stat.color }]}>
              {stat.value}
            </Text>
            <Text style={styles.statLabel}>{stat.label}</Text>
          </View>
        ))}
      </View>
      
      {/* Additional Info */}
      <View style={styles.additionalInfo}>
        <View style={styles.infoItem}>
          <Ionicons name="calendar" size={14} color={COLORS.textSecondary} />
          <Text style={styles.infoText}>Last generated: Oct 19, 2024</Text>
        </View>
        
        <View style={styles.infoItem}>
          <Ionicons name="trending-up" size={14} color={COLORS.success} />
          <Text style={styles.infoText}>75% completion rate</Text>
        </View>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: COLORS.white,
    borderRadius: BORDER_RADIUS.xl,
    padding: SPACING.lg,
    marginHorizontal: SPACING.md,
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
  statsGrid: {
    flexDirection: 'row',
    marginBottom: SPACING.md,
  },
  statCard: {
    flex: 1,
    alignItems: 'center',
    paddingVertical: SPACING.sm,
  },
  iconContainer: {
    width: 40,
    height: 40,
    borderRadius: 20,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: SPACING.xs,
  },
  statValue: {
    fontSize: TYPOGRAPHY.fontSize.xl,
    fontWeight: TYPOGRAPHY.fontWeight.bold,
    marginBottom: 2,
  },
  statLabel: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.textSecondary,
    textAlign: 'center',
  },
  additionalInfo: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingTop: SPACING.sm,
    borderTopWidth: 1,
    borderTopColor: COLORS.gray200,
  },
  infoItem: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  infoText: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.textSecondary,
    marginLeft: SPACING.xs,
  },
});

export default ReportsStatsCard;
