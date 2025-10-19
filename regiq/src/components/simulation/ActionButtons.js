import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { COLORS, TYPOGRAPHY, SPACING, BORDER_RADIUS, SHADOWS } from '../../constants/theme';

const ActionButtons = ({ 
  onDownloadReport,
  onShareResults,
  onViewInAudit,
  onRunAgain,
  onNewSimulation 
}) => {
  return (
    <View style={styles.container}>
      {/* Primary Actions */}
      <View style={styles.primaryActions}>
        <TouchableOpacity 
          style={[styles.actionButton, styles.primaryButton]}
          onPress={onDownloadReport}
          activeOpacity={0.8}
        >
          <View style={styles.buttonContent}>
            <Ionicons name="download" size={18} color={COLORS.white} />
            <Text style={[styles.buttonText, styles.primaryButtonText]}>
              Download Full Report
            </Text>
          </View>
          <View style={styles.buttonBadge}>
            <Text style={styles.badgeText}>PDF</Text>
          </View>
        </TouchableOpacity>

        <TouchableOpacity 
          style={[styles.actionButton, styles.secondaryButton]}
          onPress={onShareResults}
          activeOpacity={0.8}
        >
          <View style={styles.buttonContent}>
            <Ionicons name="share" size={18} color={COLORS.white} />
            <Text style={[styles.buttonText, styles.secondaryButtonText]}>
              Share Results
            </Text>
          </View>
          <View style={styles.shareOptions}>
            <Ionicons name="mail" size={12} color={COLORS.secondary} />
            <Ionicons name="link" size={12} color={COLORS.secondary} />
          </View>
        </TouchableOpacity>
      </View>

      {/* Secondary Actions */}
      <View style={styles.secondaryActions}>
        <TouchableOpacity 
          style={[styles.actionButton, styles.outlineButton]}
          onPress={onViewInAudit}
          activeOpacity={0.7}
        >
          <View style={styles.buttonContent}>
            <Ionicons name="open" size={16} color={COLORS.primary} />
            <Text style={[styles.buttonText, styles.outlineButtonText]}>
              View in AI Model Audit
            </Text>
          </View>
          <Ionicons name="arrow-forward" size={14} color={COLORS.primary} />
        </TouchableOpacity>
      </View>

      {/* Quick Actions Grid */}
      <View style={styles.quickActionsGrid}>
        <TouchableOpacity style={styles.quickActionButton}>
          <View style={[styles.quickActionIcon, { backgroundColor: `${COLORS.info}20` }]}>
            <Ionicons name="document-text" size={16} color={COLORS.info} />
          </View>
          <Text style={styles.quickActionText}>Export Data</Text>
        </TouchableOpacity>

        <TouchableOpacity style={styles.quickActionButton}>
          <View style={[styles.quickActionIcon, { backgroundColor: `${COLORS.success}20` }]}>
            <Ionicons name="checkmark-circle" size={16} color={COLORS.success} />
          </View>
          <Text style={styles.quickActionText}>Mark Complete</Text>
        </TouchableOpacity>

        <TouchableOpacity style={styles.quickActionButton}>
          <View style={[styles.quickActionIcon, { backgroundColor: `${COLORS.warning}20` }]}>
            <Ionicons name="bookmark" size={16} color={COLORS.warning} />
          </View>
          <Text style={styles.quickActionText}>Save Template</Text>
        </TouchableOpacity>

        <TouchableOpacity style={styles.quickActionButton}>
          <View style={[styles.quickActionIcon, { backgroundColor: `${COLORS.accent}20` }]}>
            <Ionicons name="calendar" size={16} color={COLORS.accent} />
          </View>
          <Text style={styles.quickActionText}>Schedule</Text>
        </TouchableOpacity>
      </View>

      {/* Footer Actions */}
      <View style={styles.footerActions}>
        <TouchableOpacity 
          style={styles.footerButton}
          onPress={onRunAgain}
        >
          <Ionicons name="refresh" size={16} color={COLORS.textSecondary} />
          <Text style={styles.footerButtonText}>Run Again</Text>
        </TouchableOpacity>

        <TouchableOpacity 
          style={[styles.footerButton, styles.newSimulationButton]}
          onPress={onNewSimulation}
        >
          <Ionicons name="add-circle" size={16} color={COLORS.white} />
          <Text style={[styles.footerButtonText, styles.newSimulationText]}>
            New Simulation
          </Text>
        </TouchableOpacity>
      </View>

      {/* Status Indicator */}
      <View style={styles.statusContainer}>
        <View style={styles.statusIndicator}>
          <View style={[styles.statusDot, { backgroundColor: COLORS.success }]} />
          <Text style={styles.statusText}>Simulation Complete</Text>
        </View>
        <Text style={styles.timestampText}>
          Generated {new Date().toLocaleTimeString()}
        </Text>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    paddingHorizontal: SPACING.md,
    paddingVertical: SPACING.md,
  },
  primaryActions: {
    marginBottom: SPACING.md,
  },
  actionButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingVertical: SPACING.md,
    paddingHorizontal: SPACING.md,
    borderRadius: BORDER_RADIUS.lg,
    marginBottom: SPACING.sm,
    ...SHADOWS.sm,
  },
  primaryButton: {
    backgroundColor: COLORS.primary,
  },
  secondaryButton: {
    backgroundColor: COLORS.secondary,
  },
  outlineButton: {
    backgroundColor: COLORS.white,
    borderWidth: 1,
    borderColor: COLORS.primary,
  },
  buttonContent: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  buttonText: {
    fontSize: TYPOGRAPHY.fontSize.base,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    marginLeft: SPACING.sm,
  },
  primaryButtonText: {
    color: COLORS.white,
  },
  secondaryButtonText: {
    color: COLORS.white,
  },
  outlineButtonText: {
    color: COLORS.primary,
  },
  buttonBadge: {
    backgroundColor: `${COLORS.white}30`,
    paddingHorizontal: SPACING.xs,
    paddingVertical: 2,
    borderRadius: BORDER_RADIUS.sm,
  },
  badgeText: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    fontWeight: TYPOGRAPHY.fontWeight.bold,
    color: COLORS.white,
  },
  shareOptions: {
    flexDirection: 'row',
    gap: SPACING.xs,
  },
  secondaryActions: {
    marginBottom: SPACING.md,
  },
  quickActionsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginHorizontal: -SPACING.xs,
    marginBottom: SPACING.md,
  },
  quickActionButton: {
    backgroundColor: COLORS.white,
    borderRadius: BORDER_RADIUS.md,
    padding: SPACING.sm,
    alignItems: 'center',
    marginHorizontal: SPACING.xs,
    marginBottom: SPACING.sm,
    borderWidth: 1,
    borderColor: COLORS.gray200,
    flex: 1,
    ...SHADOWS.sm,
  },
  quickActionIcon: {
    width: 32,
    height: 32,
    borderRadius: 16,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: SPACING.xs,
  },
  quickActionText: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
    color: COLORS.textPrimary,
    textAlign: 'center',
  },
  footerActions: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    backgroundColor: COLORS.white,
    borderTopWidth: 1,
    borderTopColor: COLORS.gray200,
    paddingTop: SPACING.md,
    marginBottom: SPACING.md,
  },
  footerButton: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: SPACING.sm,
    paddingHorizontal: SPACING.md,
    borderRadius: BORDER_RADIUS.lg,
  },
  newSimulationButton: {
    backgroundColor: COLORS.accent,
  },
  footerButtonText: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
    color: COLORS.textSecondary,
    marginLeft: SPACING.xs,
  },
  newSimulationText: {
    color: COLORS.white,
  },
  statusContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    backgroundColor: COLORS.surfaceSecondary,
    borderRadius: BORDER_RADIUS.md,
    paddingVertical: SPACING.sm,
    paddingHorizontal: SPACING.md,
  },
  statusIndicator: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  statusDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    marginRight: SPACING.xs,
  },
  statusText: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
    color: COLORS.textPrimary,
  },
  timestampText: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.textSecondary,
  },
});

export default ActionButtons;
