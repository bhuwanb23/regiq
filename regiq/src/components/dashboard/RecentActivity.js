import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, FlatList } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { COLORS, TYPOGRAPHY, SPACING, BORDER_RADIUS, SHADOWS } from '../../constants/theme';

const RecentActivity = ({ activities = [], onViewAll, onActivityPress }) => {
  const defaultActivities = [
    {
      id: 1,
      type: 'compliance_check',
      title: 'Compliance Check Completed',
      description: 'GDPR compliance audit finished with 95% score',
      timestamp: '2 hours ago',
      status: 'success',
      icon: 'shield-checkmark',
    },
    {
      id: 2,
      type: 'ai_audit',
      title: 'AI Model Bias Detected',
      description: 'Credit scoring model shows 6.7% gender bias',
      timestamp: '4 hours ago',
      status: 'warning',
      icon: 'analytics',
    },
    {
      id: 3,
      type: 'regulation_update',
      title: 'New Regulation Update',
      description: 'EU AI Act transparency requirements updated',
      timestamp: '1 day ago',
      status: 'info',
      icon: 'document-text',
    },
    {
      id: 4,
      type: 'report_generated',
      title: 'Risk Report Generated',
      description: 'Monthly risk assessment report is ready',
      timestamp: '2 days ago',
      status: 'success',
      icon: 'bar-chart',
    },
    {
      id: 5,
      type: 'alert',
      title: 'Compliance Alert',
      description: 'KYC API requires immediate attention',
      timestamp: '3 days ago',
      status: 'error',
      icon: 'warning',
    },
  ];

  const activityData = activities.length > 0 ? activities : defaultActivities;

  const getActivityColor = (status) => {
    switch (status) {
      case 'success':
        return COLORS.success;
      case 'warning':
        return COLORS.warning;
      case 'error':
        return COLORS.error;
      case 'info':
        return COLORS.info;
      default:
        return COLORS.gray400;
    }
  };

  const getActivityBackground = (status) => {
    switch (status) {
      case 'success':
        return `${COLORS.success}15`;
      case 'warning':
        return `${COLORS.warning}15`;
      case 'error':
        return `${COLORS.error}15`;
      case 'info':
        return `${COLORS.info}15`;
      default:
        return `${COLORS.gray400}15`;
    }
  };

  const renderActivityItem = ({ item, index }) => (
    <TouchableOpacity
      style={[
        styles.activityItem,
        index === activityData.length - 1 && styles.lastActivityItem,
      ]}
      onPress={() => onActivityPress?.(item)}
    >
      <View style={styles.activityContent}>
        <View style={[
          styles.activityIcon,
          { backgroundColor: getActivityBackground(item.status) }
        ]}>
          <Ionicons
            name={item.icon}
            size={16}
            color={getActivityColor(item.status)}
          />
        </View>
        
        <View style={styles.activityDetails}>
          <Text style={styles.activityTitle}>{item.title}</Text>
          <Text style={styles.activityDescription}>{item.description}</Text>
          <Text style={styles.activityTimestamp}>{item.timestamp}</Text>
        </View>
        
        <View style={styles.activityStatus}>
          <View style={[
            styles.statusDot,
            { backgroundColor: getActivityColor(item.status) }
          ]} />
        </View>
      </View>
    </TouchableOpacity>
  );

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.title}>Recent Activity</Text>
        <TouchableOpacity onPress={onViewAll}>
          <Text style={styles.viewAllText}>View All</Text>
        </TouchableOpacity>
      </View>

      {/* Activity List */}
      <View style={styles.activityList}>
        <FlatList
          data={activityData.slice(0, 5)}
          renderItem={renderActivityItem}
          keyExtractor={(item) => item.id.toString()}
          showsVerticalScrollIndicator={false}
          scrollEnabled={false}
        />
      </View>

      {/* Activity Summary */}
      <View style={styles.summaryContainer}>
        <View style={styles.summaryItem}>
          <View style={[styles.summaryIcon, { backgroundColor: `${COLORS.success}20` }]}>
            <Ionicons name="checkmark-circle" size={16} color={COLORS.success} />
          </View>
          <Text style={styles.summaryText}>12 completed today</Text>
        </View>
        
        <View style={styles.summaryItem}>
          <View style={[styles.summaryIcon, { backgroundColor: `${COLORS.warning}20` }]}>
            <Ionicons name="time" size={16} color={COLORS.warning} />
          </View>
          <Text style={styles.summaryText}>3 pending review</Text>
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
    color: COLORS.textPrimary,
  },
  viewAllText: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.primary,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
  },
  activityList: {
    marginBottom: SPACING.md,
  },
  activityItem: {
    paddingVertical: SPACING.sm,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.gray200,
  },
  lastActivityItem: {
    borderBottomWidth: 0,
  },
  activityContent: {
    flexDirection: 'row',
    alignItems: 'flex-start',
  },
  activityIcon: {
    width: 32,
    height: 32,
    borderRadius: 16,
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: SPACING.sm,
  },
  activityDetails: {
    flex: 1,
    marginRight: SPACING.sm,
  },
  activityTitle: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
    color: COLORS.textPrimary,
    marginBottom: 2,
  },
  activityDescription: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.textSecondary,
    lineHeight: 16,
    marginBottom: 4,
  },
  activityTimestamp: {
    fontSize: 10,
    color: COLORS.textTertiary,
  },
  activityStatus: {
    alignItems: 'center',
    justifyContent: 'flex-start',
    paddingTop: 4,
  },
  statusDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
  },
  summaryContainer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    paddingTop: SPACING.md,
    borderTopWidth: 1,
    borderTopColor: COLORS.gray200,
  },
  summaryItem: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  summaryIcon: {
    width: 20,
    height: 20,
    borderRadius: 10,
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: SPACING.xs,
  },
  summaryText: {
    fontSize: 10,
    color: COLORS.textSecondary,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
  },
});

export default RecentActivity;
