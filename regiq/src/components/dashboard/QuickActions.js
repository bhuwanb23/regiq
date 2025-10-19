import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';
import { COLORS, TYPOGRAPHY, SPACING, BORDER_RADIUS, SHADOWS } from '../../constants/theme';

const QuickActions = ({ onActionPress }) => {
  const actions = [
    {
      id: 'scan_model',
      title: 'AI Audit',
      subtitle: 'Bias check',
      icon: 'analytics',
      gradient: [COLORS.primary, COLORS.primaryDark],
      route: 'AI Audit',
    },
    {
      id: 'run_simulation',
      title: 'Risk Test',
      subtitle: 'Simulation',
      icon: 'flask',
      gradient: [COLORS.secondary, COLORS.secondaryDark],
      route: 'Simulation',
    },
    {
      id: 'generate_report',
      title: 'Reports',
      subtitle: 'Generate',
      icon: 'document-text',
      gradient: [COLORS.accent, COLORS.accentDark],
      route: 'Reports',
    },
    {
      id: 'check_regulations',
      title: 'Updates',
      subtitle: 'Regulations',
      icon: 'shield-checkmark',
      gradient: [COLORS.info, '#2563EB'],
      route: 'Regulations',
    },
  ];

  const handleActionPress = (action) => {
    onActionPress?.(action);
  };

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.title}>Quick Actions</Text>
      </View>

      {/* Actions Grid */}
      <View style={styles.actionsGrid}>
        {actions.map((action, index) => (
          <TouchableOpacity
            key={action.id}
            style={[
              styles.actionCard,
              index % 2 === 0 ? styles.leftCard : styles.rightCard,
            ]}
            onPress={() => handleActionPress(action)}
            activeOpacity={0.8}
          >
            <LinearGradient
              colors={action.gradient}
              style={styles.gradientBackground}
              start={{ x: 0, y: 0 }}
              end={{ x: 1, y: 1 }}
            >
              <View style={styles.actionContent}>
                <View style={styles.actionIcon}>
                  <Ionicons name={action.icon} size={18} color={COLORS.white} />
                </View>
                
                <View style={styles.actionText}>
                  <Text style={styles.actionTitle}>{action.title}</Text>
                  <Text style={styles.actionSubtitle}>{action.subtitle}</Text>
                </View>
                
                <View style={styles.actionArrow}>
                  <Ionicons name="chevron-forward" size={12} color={COLORS.white} />
                </View>
              </View>
            </LinearGradient>
          </TouchableOpacity>
        ))}
      </View>

      {/* Additional Actions */}
      <View style={styles.additionalActions}>
        <TouchableOpacity style={styles.additionalAction}>
          <View style={[styles.additionalIcon, { backgroundColor: `${COLORS.primary}20` }]}>
            <Ionicons name="settings" size={16} color={COLORS.primary} />
          </View>
          <Text style={styles.additionalText}>Settings</Text>
        </TouchableOpacity>

        <TouchableOpacity style={styles.additionalAction}>
          <View style={[styles.additionalIcon, { backgroundColor: `${COLORS.secondary}20` }]}>
            <Ionicons name="help-circle" size={16} color={COLORS.secondary} />
          </View>
          <Text style={styles.additionalText}>Help</Text>
        </TouchableOpacity>

        <TouchableOpacity style={styles.additionalAction}>
          <View style={[styles.additionalIcon, { backgroundColor: `${COLORS.accent}20` }]}>
            <Ionicons name="notifications" size={16} color={COLORS.accent} />
          </View>
          <Text style={styles.additionalText}>Alerts</Text>
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
    marginBottom: SPACING.lg,
  },
  title: {
    fontSize: TYPOGRAPHY.fontSize.base,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.textPrimary,
  },
  actionsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginBottom: SPACING.lg,
  },
  actionCard: {
    width: '48%',
    height: 80,
    marginBottom: SPACING.sm,
    borderRadius: BORDER_RADIUS.md,
    overflow: 'hidden',
    ...SHADOWS.sm,
  },
  leftCard: {
    marginRight: '4%',
  },
  rightCard: {
    marginLeft: 0,
  },
  gradientBackground: {
    flex: 1,
    borderRadius: BORDER_RADIUS.lg,
  },
  actionContent: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    padding: SPACING.xs,
  },
  actionIcon: {
    width: 32,
    height: 32,
    borderRadius: 16,
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: SPACING.xs,
  },
  actionText: {
    flex: 1,
  },
  actionTitle: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.white,
    marginBottom: 1,
  },
  actionSubtitle: {
    fontSize: 10,
    color: 'rgba(255, 255, 255, 0.8)',
    lineHeight: 12,
  },
  actionArrow: {
    width: 20,
    height: 20,
    borderRadius: 10,
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
    alignItems: 'center',
    justifyContent: 'center',
  },
  additionalActions: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    paddingTop: SPACING.md,
    borderTopWidth: 1,
    borderTopColor: COLORS.gray200,
  },
  additionalAction: {
    alignItems: 'center',
    flex: 1,
  },
  additionalIcon: {
    width: 28,
    height: 28,
    borderRadius: 14,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: SPACING.xs,
  },
  additionalText: {
    fontSize: 10,
    color: COLORS.textSecondary,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
    textAlign: 'center',
  },
});

export default QuickActions;
