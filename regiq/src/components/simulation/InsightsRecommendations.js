import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { COLORS, TYPOGRAPHY, SPACING, BORDER_RADIUS, SHADOWS } from '../../constants/theme';

const InsightsRecommendations = ({ 
  insights = [],
  onInsightPress 
}) => {
  const defaultInsights = [
    {
      id: 1,
      type: 'warning',
      title: 'High-Risk Transactions',
      description: 'Review 23 flagged transactions in credit assessment module',
      priority: 'high',
      actionRequired: true,
    },
    {
      id: 2,
      type: 'success',
      title: 'Model Performance',
      description: '87% compliance rate exceeds regulatory threshold',
      priority: 'medium',
      actionRequired: false,
    },
    {
      id: 3,
      type: 'alert',
      title: 'Action Required',
      description: 'Update bias detection algorithms before Q2 deadline',
      priority: 'high',
      actionRequired: true,
    },
    {
      id: 4,
      type: 'info',
      title: 'Optimization Opportunity',
      description: 'Consider implementing enhanced feature selection for better accuracy',
      priority: 'low',
      actionRequired: false,
    },
  ];

  const insightData = insights.length > 0 ? insights : defaultInsights;

  const getInsightConfig = (type) => {
    switch (type) {
      case 'success':
        return {
          icon: 'checkmark-circle',
          color: COLORS.success,
          backgroundColor: `${COLORS.success}15`,
        };
      case 'warning':
        return {
          icon: 'bulb',
          color: COLORS.info,
          backgroundColor: `${COLORS.info}15`,
        };
      case 'alert':
        return {
          icon: 'warning',
          color: COLORS.warning,
          backgroundColor: `${COLORS.warning}15`,
        };
      case 'error':
        return {
          icon: 'alert-circle',
          color: COLORS.error,
          backgroundColor: `${COLORS.error}15`,
        };
      default:
        return {
          icon: 'information-circle',
          color: COLORS.info,
          backgroundColor: `${COLORS.info}15`,
        };
    }
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high': return COLORS.error;
      case 'medium': return COLORS.warning;
      case 'low': return COLORS.success;
      default: return COLORS.info;
    }
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Key Insights & Recommendations</Text>
        <View style={styles.summaryBadge}>
          <Text style={styles.summaryText}>
            {insightData.filter(i => i.actionRequired).length} Action Items
          </Text>
        </View>
      </View>

      <View style={styles.insightsContainer}>
        {insightData.map((insight, index) => {
          const config = getInsightConfig(insight.type);
          
          return (
            <TouchableOpacity
              key={insight.id || index}
              style={[
                styles.insightCard,
                { backgroundColor: config.backgroundColor }
              ]}
              onPress={() => onInsightPress?.(insight)}
              activeOpacity={0.7}
            >
              <View style={styles.insightContent}>
                <View style={styles.insightHeader}>
                  <View style={styles.insightIconContainer}>
                    <Ionicons 
                      name={config.icon} 
                      size={18} 
                      color={config.color} 
                    />
                  </View>
                  
                  <View style={styles.insightInfo}>
                    <View style={styles.insightTitleRow}>
                      <Text style={[styles.insightTitle, { color: config.color }]}>
                        {insight.title}
                      </Text>
                      {insight.priority && (
                        <View style={[
                          styles.priorityBadge,
                          { backgroundColor: getPriorityColor(insight.priority) }
                        ]}>
                          <Text style={styles.priorityText}>
                            {insight.priority.toUpperCase()}
                          </Text>
                        </View>
                      )}
                    </View>
                    
                    <Text style={[styles.insightDescription, { color: config.color }]}>
                      {insight.description}
                    </Text>
                  </View>
                </View>

                {insight.actionRequired && (
                  <View style={styles.actionContainer}>
                    <View style={styles.actionIndicator}>
                      <Ionicons name="arrow-forward" size={12} color={config.color} />
                    </View>
                    <Text style={[styles.actionText, { color: config.color }]}>
                      Action Required
                    </Text>
                  </View>
                )}
              </View>

              {/* Progress indicator for actionable items */}
              {insight.actionRequired && (
                <View style={styles.progressIndicator}>
                  <View style={[styles.progressDot, { backgroundColor: config.color }]} />
                </View>
              )}
            </TouchableOpacity>
          );
        })}
      </View>

      {/* Quick Actions */}
      <View style={styles.quickActions}>
        <Text style={styles.quickActionsTitle}>Quick Actions</Text>
        
        <View style={styles.actionButtons}>
          <TouchableOpacity style={styles.actionButton}>
            <Ionicons name="eye" size={16} color={COLORS.primary} />
            <Text style={styles.actionButtonText}>Review All</Text>
          </TouchableOpacity>
          
          <TouchableOpacity style={styles.actionButton}>
            <Ionicons name="checkmark-done" size={16} color={COLORS.success} />
            <Text style={styles.actionButtonText}>Mark Resolved</Text>
          </TouchableOpacity>
          
          <TouchableOpacity style={styles.actionButton}>
            <Ionicons name="share" size={16} color={COLORS.secondary} />
            <Text style={styles.actionButtonText}>Share Report</Text>
          </TouchableOpacity>
        </View>
      </View>

      {/* Summary Stats */}
      <View style={styles.summaryStats}>
        <View style={styles.statItem}>
          <Text style={styles.statValue}>
            {insightData.filter(i => i.type === 'success').length}
          </Text>
          <Text style={styles.statLabel}>Positive</Text>
        </View>
        
        <View style={styles.statDivider} />
        
        <View style={styles.statItem}>
          <Text style={[styles.statValue, { color: COLORS.warning }]}>
            {insightData.filter(i => i.actionRequired).length}
          </Text>
          <Text style={styles.statLabel}>Need Action</Text>
        </View>
        
        <View style={styles.statDivider} />
        
        <View style={styles.statItem}>
          <Text style={[styles.statValue, { color: COLORS.error }]}>
            {insightData.filter(i => i.priority === 'high').length}
          </Text>
          <Text style={styles.statLabel}>High Priority</Text>
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
  summaryBadge: {
    backgroundColor: `${COLORS.accent}20`,
    paddingHorizontal: SPACING.sm,
    paddingVertical: SPACING.xs,
    borderRadius: BORDER_RADIUS.full,
  },
  summaryText: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.accent,
  },
  insightsContainer: {
    marginBottom: SPACING.md,
  },
  insightCard: {
    borderRadius: BORDER_RADIUS.lg,
    padding: SPACING.md,
    marginBottom: SPACING.sm,
    borderWidth: 1,
    borderColor: 'transparent',
    position: 'relative',
  },
  insightContent: {
    flex: 1,
  },
  insightHeader: {
    flexDirection: 'row',
    alignItems: 'flex-start',
  },
  insightIconContainer: {
    marginRight: SPACING.sm,
    marginTop: 2,
  },
  insightInfo: {
    flex: 1,
  },
  insightTitleRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: SPACING.xs,
  },
  insightTitle: {
    fontSize: TYPOGRAPHY.fontSize.base,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    flex: 1,
  },
  priorityBadge: {
    paddingHorizontal: SPACING.xs,
    paddingVertical: 2,
    borderRadius: BORDER_RADIUS.sm,
    marginLeft: SPACING.sm,
  },
  priorityText: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    fontWeight: TYPOGRAPHY.fontWeight.bold,
    color: COLORS.white,
  },
  insightDescription: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    lineHeight: 18,
  },
  actionContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: SPACING.sm,
  },
  actionIndicator: {
    marginRight: SPACING.xs,
  },
  actionText: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
  },
  progressIndicator: {
    position: 'absolute',
    right: SPACING.md,
    top: SPACING.md,
  },
  progressDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
  },
  quickActions: {
    marginBottom: SPACING.md,
  },
  quickActionsTitle: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.textPrimary,
    marginBottom: SPACING.sm,
  },
  actionButtons: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  actionButton: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: COLORS.surfaceSecondary,
    paddingVertical: SPACING.sm,
    borderRadius: BORDER_RADIUS.md,
    marginHorizontal: SPACING.xs,
  },
  actionButtonText: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
    color: COLORS.textPrimary,
    marginLeft: SPACING.xs,
  },
  summaryStats: {
    flexDirection: 'row',
    backgroundColor: COLORS.surfaceSecondary,
    borderRadius: BORDER_RADIUS.md,
    paddingVertical: SPACING.sm,
    paddingHorizontal: SPACING.md,
  },
  statItem: {
    flex: 1,
    alignItems: 'center',
  },
  statValue: {
    fontSize: TYPOGRAPHY.fontSize.lg,
    fontWeight: TYPOGRAPHY.fontWeight.bold,
    color: COLORS.success,
    marginBottom: 2,
  },
  statLabel: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.textSecondary,
    textAlign: 'center',
  },
  statDivider: {
    width: 1,
    backgroundColor: COLORS.gray300,
    marginHorizontal: SPACING.sm,
  },
});

export default InsightsRecommendations;
