import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';
import { COLORS, TYPOGRAPHY, SPACING, BORDER_RADIUS, SHADOWS } from '../../constants/theme';

const StatCard = ({ 
  title, 
  value, 
  subtitle, 
  icon, 
  trend, 
  trendValue, 
  color = COLORS.primary,
  variant = 'default' // 'default', 'gradient', 'minimal'
}) => {
  const getTrendIcon = () => {
    if (trend === 'up') return 'trending-up';
    if (trend === 'down') return 'trending-down';
    return 'remove';
  };

  const getTrendColor = () => {
    if (trend === 'up') return COLORS.success;
    if (trend === 'down') return COLORS.error;
    return COLORS.gray400;
  };

  if (variant === 'gradient') {
    return (
      <View style={[styles.container, styles.gradientContainer]}>
        <LinearGradient
          colors={[color, `${color}CC`]}
          style={styles.gradientBackground}
          start={{ x: 0, y: 0 }}
          end={{ x: 1, y: 1 }}
        >
          <View style={styles.content}>
            <View style={styles.header}>
              <View style={[styles.iconContainer, styles.whiteIconContainer]}>
                <Ionicons name={icon} size={24} color={COLORS.white} />
              </View>
              {trend && (
                <View style={styles.trendContainer}>
                  <Ionicons name={getTrendIcon()} size={16} color={COLORS.white} />
                  <Text style={styles.trendTextWhite}>{trendValue}</Text>
                </View>
              )}
            </View>
            <Text style={styles.valueWhite}>{value}</Text>
            <Text style={styles.titleWhite}>{title}</Text>
            {subtitle && <Text style={styles.subtitleWhite}>{subtitle}</Text>}
          </View>
        </LinearGradient>
      </View>
    );
  }

  if (variant === 'minimal') {
    return (
      <View style={[styles.container, styles.minimalContainer]}>
        <View style={styles.content}>
          <View style={styles.header}>
            <Text style={styles.titleMinimal}>{title}</Text>
            {trend && (
              <View style={styles.trendContainer}>
                <Ionicons name={getTrendIcon()} size={14} color={getTrendColor()} />
                <Text style={[styles.trendText, { color: getTrendColor() }]}>{trendValue}</Text>
              </View>
            )}
          </View>
          <View style={styles.valueRow}>
            <Text style={styles.valueMinimal}>{value}</Text>
            <View style={[styles.iconContainer, { backgroundColor: `${color}20` }]}>
              <Ionicons name={icon} size={20} color={color} />
            </View>
          </View>
          {subtitle && <Text style={styles.subtitle}>{subtitle}</Text>}
        </View>
      </View>
    );
  }

  // Default variant
  return (
    <View style={[styles.container, styles.defaultContainer]}>
      <View style={styles.content}>
        <View style={styles.header}>
          <View style={[styles.iconContainer, { backgroundColor: `${color}20` }]}>
            <Ionicons name={icon} size={24} color={color} />
          </View>
          {trend && (
            <View style={styles.trendContainer}>
              <Ionicons name={getTrendIcon()} size={16} color={getTrendColor()} />
              <Text style={[styles.trendText, { color: getTrendColor() }]}>{trendValue}</Text>
            </View>
          )}
        </View>
        <Text style={styles.value}>{value}</Text>
        <Text style={styles.title}>{title}</Text>
        {subtitle && <Text style={styles.subtitle}>{subtitle}</Text>}
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    width: '48%',
    marginHorizontal: '1%',
    marginBottom: SPACING.sm,
    minHeight: 100,
  },
  defaultContainer: {
    backgroundColor: COLORS.white,
    borderRadius: BORDER_RADIUS.lg,
    ...SHADOWS.sm,
  },
  gradientContainer: {
    borderRadius: BORDER_RADIUS.lg,
    overflow: 'hidden',
    ...SHADOWS.md,
  },
  minimalContainer: {
    backgroundColor: COLORS.surfaceSecondary,
    borderRadius: BORDER_RADIUS.md,
    borderWidth: 1,
    borderColor: COLORS.gray200,
  },
  gradientBackground: {
    flex: 1,
    borderRadius: BORDER_RADIUS.lg,
  },
  content: {
    flex: 1,
    padding: SPACING.sm,
    justifyContent: 'space-between',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: SPACING.sm,
  },
  valueRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: SPACING.xs,
  },
  iconContainer: {
    width: 36,
    height: 36,
    borderRadius: 18,
    alignItems: 'center',
    justifyContent: 'center',
  },
  whiteIconContainer: {
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
  },
  trendContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(255, 255, 255, 0.1)',
    paddingHorizontal: SPACING.xs,
    paddingVertical: 2,
    borderRadius: BORDER_RADIUS.sm,
  },
  value: {
    fontSize: TYPOGRAPHY.fontSize.lg,
    fontWeight: TYPOGRAPHY.fontWeight.bold,
    color: COLORS.textPrimary,
    marginBottom: 2,
  },
  valueWhite: {
    fontSize: TYPOGRAPHY.fontSize.lg,
    fontWeight: TYPOGRAPHY.fontWeight.bold,
    color: COLORS.white,
    marginBottom: 2,
  },
  valueMinimal: {
    fontSize: TYPOGRAPHY.fontSize.base,
    fontWeight: TYPOGRAPHY.fontWeight.bold,
    color: COLORS.textPrimary,
  },
  title: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
    color: COLORS.textSecondary,
    lineHeight: 14,
    textAlign: 'center',
  },
  titleWhite: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
    color: COLORS.white,
    lineHeight: 14,
    textAlign: 'center',
  },
  titleMinimal: {
    fontSize: 10,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
    color: COLORS.textSecondary,
    textTransform: 'uppercase',
    letterSpacing: 0.5,
  },
  subtitle: {
    fontSize: 10,
    color: COLORS.textTertiary,
    marginTop: 2,
    textAlign: 'center',
  },
  subtitleWhite: {
    fontSize: 10,
    color: 'rgba(255, 255, 255, 0.8)',
    marginTop: 2,
    textAlign: 'center',
  },
  trendText: {
    fontSize: 10,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
    marginLeft: 2,
  },
  trendTextWhite: {
    fontSize: 10,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
    color: COLORS.white,
    marginLeft: 2,
  },
});

export default StatCard;
