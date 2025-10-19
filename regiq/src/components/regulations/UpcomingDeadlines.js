import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { COLORS, TYPOGRAPHY, SPACING, BORDER_RADIUS, SHADOWS } from '../../constants/theme';

const UpcomingDeadlines = ({ deadlines = [], onDeadlinePress, onViewAll }) => {
  const defaultDeadlines = [
    {
      id: 1,
      title: 'AI Act Compliance',
      daysRemaining: 15,
      date: 'Dec 15',
      priority: 'critical',
      description: 'EU AI Act implementation deadline',
    },
    {
      id: 2,
      title: 'CFPB Data Standards',
      daysRemaining: 45,
      date: 'Jan 30',
      priority: 'medium',
      description: 'Open banking data sharing compliance',
    },
    {
      id: 3,
      title: 'MAS Token Standards',
      daysRemaining: 67,
      date: 'Feb 15',
      priority: 'high',
      description: 'Digital payment token regulations',
    },
  ];

  const deadlineData = deadlines.length > 0 ? deadlines : defaultDeadlines;

  const getPriorityColor = (priority) => {
    switch (priority?.toLowerCase()) {
      case 'critical':
        return COLORS.error;
      case 'high':
        return COLORS.warning;
      case 'medium':
        return COLORS.info;
      case 'low':
        return COLORS.success;
      default:
        return COLORS.gray400;
    }
  };

  const getPriorityBackground = (priority) => {
    switch (priority?.toLowerCase()) {
      case 'critical':
        return `${COLORS.error}15`;
      case 'high':
        return `${COLORS.warning}15`;
      case 'medium':
        return `${COLORS.info}15`;
      case 'low':
        return `${COLORS.success}15`;
      default:
        return `${COLORS.gray400}15`;
    }
  };

  const formatDaysRemaining = (days) => {
    if (days <= 0) return 'Overdue';
    if (days === 1) return '1 day left';
    if (days <= 7) return `${days} days left`;
    if (days <= 30) return `${Math.ceil(days / 7)} weeks left`;
    return `${Math.ceil(days / 30)} months left`;
  };

  const getUrgencyLevel = (days) => {
    if (days <= 0) return 'overdue';
    if (days <= 7) return 'urgent';
    if (days <= 30) return 'warning';
    return 'normal';
  };

  const getUrgencyColor = (days) => {
    const urgency = getUrgencyLevel(days);
    switch (urgency) {
      case 'overdue':
        return COLORS.error;
      case 'urgent':
        return COLORS.error;
      case 'warning':
        return COLORS.warning;
      default:
        return COLORS.success;
    }
  };

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <View style={styles.titleContainer}>
          <Ionicons name="time" size={16} color={COLORS.accent} />
          <Text style={styles.title}>Upcoming Deadlines</Text>
        </View>
        <TouchableOpacity onPress={onViewAll}>
          <Text style={styles.viewAllText}>View All ({deadlineData.length})</Text>
        </TouchableOpacity>
      </View>

      {/* Deadlines List */}
      <View style={styles.deadlinesList}>
        {deadlineData.slice(0, 3).map((deadline, index) => {
          const urgencyColor = getUrgencyColor(deadline.daysRemaining);
          const isUrgent = deadline.daysRemaining <= 7;
          
          return (
            <TouchableOpacity
              key={deadline.id}
              style={[
                styles.deadlineItem,
                { backgroundColor: `${urgencyColor}15` },
                isUrgent && styles.urgentDeadline
              ]}
              onPress={() => onDeadlinePress?.(deadline)}
              activeOpacity={0.7}
            >
              <View style={[
                styles.priorityBorder,
                { backgroundColor: urgencyColor }
              ]} />
              
              <View style={styles.deadlineContent}>
                <View style={styles.deadlineInfo}>
                  <View style={styles.deadlineTitleRow}>
                    <Text style={styles.deadlineTitle}>{deadline.title}</Text>
                    {isUrgent && (
                      <View style={styles.urgentBadge}>
                        <Ionicons name="warning" size={10} color={COLORS.white} />
                      </View>
                    )}
                  </View>
                  <Text style={styles.deadlineDescription}>{deadline.description}</Text>
                  <Text style={[
                    styles.daysRemaining,
                    { color: urgencyColor },
                    isUrgent && styles.urgentText
                  ]}>
                    {formatDaysRemaining(deadline.daysRemaining)}
                  </Text>
                </View>
                
                <View style={styles.dateContainer}>
                  <Text style={[
                    styles.dateText,
                    { 
                      backgroundColor: urgencyColor,
                      color: COLORS.white 
                    }
                  ]}>
                    {deadline.date}
                  </Text>
                  <TouchableOpacity 
                    style={styles.actionButton}
                    onPress={(e) => {
                      e.stopPropagation();
                      console.log('Quick action for deadline:', deadline.id);
                    }}
                  >
                    <Ionicons name="chevron-forward" size={12} color={COLORS.gray400} />
                  </TouchableOpacity>
                </View>
              </View>
            </TouchableOpacity>
          );
        })}
      </View>

      {/* Summary Stats */}
      <View style={styles.summaryContainer}>
        <View style={styles.summaryItem}>
          <View style={[styles.summaryIcon, { backgroundColor: `${COLORS.error}20` }]}>
            <Ionicons name="warning" size={12} color={COLORS.error} />
          </View>
          <Text style={styles.summaryText}>
            {deadlineData.filter(d => d.priority === 'critical').length} Critical
          </Text>
        </View>
        
        <View style={styles.summaryItem}>
          <View style={[styles.summaryIcon, { backgroundColor: `${COLORS.warning}20` }]}>
            <Ionicons name="time" size={12} color={COLORS.warning} />
          </View>
          <Text style={styles.summaryText}>
            {deadlineData.filter(d => d.daysRemaining <= 30).length} This Month
          </Text>
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
    marginBottom: SPACING.sm,
  },
  titleContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  title: {
    fontSize: TYPOGRAPHY.fontSize.base,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.textPrimary,
    marginLeft: SPACING.xs,
  },
  viewAllText: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.primary,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
  },
  deadlinesList: {
    marginBottom: SPACING.sm,
  },
  deadlineItem: {
    flexDirection: 'row',
    borderRadius: BORDER_RADIUS.md,
    marginBottom: SPACING.xs,
    overflow: 'hidden',
    borderWidth: 1,
    borderColor: 'transparent',
  },
  urgentDeadline: {
    borderColor: `${COLORS.error}30`,
    ...SHADOWS.sm,
  },
  priorityBorder: {
    width: 4,
  },
  deadlineContent: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    padding: SPACING.sm,
  },
  deadlineInfo: {
    flex: 1,
  },
  deadlineTitleRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 2,
  },
  deadlineTitle: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.textPrimary,
    flex: 1,
  },
  urgentBadge: {
    backgroundColor: COLORS.error,
    borderRadius: BORDER_RADIUS.full,
    width: 16,
    height: 16,
    alignItems: 'center',
    justifyContent: 'center',
    marginLeft: SPACING.xs,
  },
  deadlineDescription: {
    fontSize: 10,
    color: COLORS.textSecondary,
    marginBottom: 4,
  },
  daysRemaining: {
    fontSize: 10,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
  },
  urgentText: {
    fontWeight: TYPOGRAPHY.fontWeight.bold,
  },
  dateContainer: {
    alignItems: 'center',
    justifyContent: 'center',
  },
  dateText: {
    fontSize: 10,
    fontWeight: TYPOGRAPHY.fontWeight.bold,
    paddingHorizontal: SPACING.xs,
    paddingVertical: 4,
    borderRadius: BORDER_RADIUS.sm,
    overflow: 'hidden',
    marginBottom: 4,
  },
  actionButton: {
    padding: 4,
    borderRadius: BORDER_RADIUS.sm,
    backgroundColor: `${COLORS.gray400}20`,
  },
  summaryContainer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    paddingTop: SPACING.sm,
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

export default UpcomingDeadlines;
