import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { COLORS, TYPOGRAPHY, SPACING, BORDER_RADIUS, SHADOWS } from '../../constants/theme';

const ModelCard = ({ model, onPress, onAudit }) => {
  const {
    id,
    name,
    type,
    status,
    lastAudit,
    biasScore,
    version,
    riskLevel,
  } = model;

  const getStatusColor = (status) => {
    switch (status?.toLowerCase()) {
      case 'active':
        return COLORS.success;
      case 'warning':
        return COLORS.warning;
      case 'error':
      case 'critical':
        return COLORS.error;
      case 'inactive':
        return COLORS.gray400;
      default:
        return COLORS.gray400;
    }
  };

  const getStatusBackground = (status) => {
    switch (status?.toLowerCase()) {
      case 'active':
        return `${COLORS.success}20`;
      case 'warning':
        return `${COLORS.warning}20`;
      case 'error':
      case 'critical':
        return `${COLORS.error}20`;
      case 'inactive':
        return `${COLORS.gray400}20`;
      default:
        return `${COLORS.gray400}20`;
    }
  };

  const getModelIcon = (type) => {
    switch (type?.toLowerCase()) {
      case 'credit assessment':
      case 'credit':
        return 'trending-up';
      case 'fraud prevention':
      case 'fraud':
        return 'shield';
      case 'payment processing':
      case 'payment':
        return 'card';
      case 'risk analysis':
        return 'analytics';
      default:
        return 'hardware-chip';
    }
  };

  const getModelIconColor = (type) => {
    switch (type?.toLowerCase()) {
      case 'credit assessment':
      case 'credit':
        return COLORS.info;
      case 'fraud prevention':
      case 'fraud':
        return COLORS.error;
      case 'payment processing':
      case 'payment':
        return COLORS.secondary;
      case 'risk analysis':
        return COLORS.accent;
      default:
        return COLORS.primary;
    }
  };

  const getBiasScoreColor = (score) => {
    if (score <= 0.1) return COLORS.success;
    if (score <= 0.2) return COLORS.warning;
    return COLORS.error;
  };

  const formatBiasScore = (score) => {
    return typeof score === 'number' ? score.toFixed(2) : score;
  };

  return (
    <TouchableOpacity 
      style={styles.container} 
      onPress={() => onPress?.(model)}
      activeOpacity={0.7}
    >
      {/* Header */}
      <View style={styles.header}>
        <View style={styles.modelInfo}>
          <View style={[
            styles.iconContainer,
            { backgroundColor: `${getModelIconColor(type)}20` }
          ]}>
            <Ionicons 
              name={getModelIcon(type)} 
              size={16} 
              color={getModelIconColor(type)} 
            />
          </View>
          
          <View style={styles.modelDetails}>
            <Text style={styles.modelName} numberOfLines={1}>{name}</Text>
            <Text style={styles.modelType}>{type}</Text>
          </View>
        </View>
        
        <View style={[
          styles.statusBadge,
          { backgroundColor: getStatusBackground(status) }
        ]}>
          <Text style={[
            styles.statusText,
            { color: getStatusColor(status) }
          ]}>
            {status}
          </Text>
        </View>
      </View>

      {/* Metrics Row */}
      <View style={styles.metricsRow}>
        <View style={styles.metricItem}>
          <Text style={styles.metricLabel}>Last Audit</Text>
          <Text style={styles.metricValue}>{lastAudit}</Text>
        </View>
        
        <View style={styles.metricDivider} />
        
        <View style={styles.metricItem}>
          <Text style={styles.metricLabel}>Bias Score</Text>
          <Text style={[
            styles.metricValue,
            { color: getBiasScoreColor(parseFloat(biasScore)) }
          ]}>
            {formatBiasScore(biasScore)}
          </Text>
        </View>
        
        {version && (
          <>
            <View style={styles.metricDivider} />
            <View style={styles.metricItem}>
              <Text style={styles.metricLabel}>Version</Text>
              <Text style={styles.metricValue}>{version}</Text>
            </View>
          </>
        )}
      </View>

      {/* Simple Footer - matching HTML structure */}
      <View style={styles.simpleFooter}>
        <Text style={styles.lastAuditText}>Last audit: {lastAudit}</Text>
        <Text style={styles.biasScoreText}>Bias score: {formatBiasScore(biasScore)}</Text>
      </View>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: COLORS.white,
    borderRadius: BORDER_RADIUS.lg,
    padding: SPACING.md,
    marginBottom: SPACING.sm,
    borderWidth: 1,
    borderColor: COLORS.gray200,
    ...SHADOWS.sm,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: SPACING.sm,
  },
  modelInfo: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  iconContainer: {
    width: 32,
    height: 32,
    borderRadius: BORDER_RADIUS.md,
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: SPACING.sm,
  },
  modelDetails: {
    flex: 1,
  },
  modelName: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.textPrimary,
    marginBottom: 2,
  },
  modelType: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.textSecondary,
  },
  statusBadge: {
    paddingHorizontal: SPACING.xs,
    paddingVertical: 4,
    borderRadius: BORDER_RADIUS.full,
  },
  statusText: {
    fontSize: 10,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
    textTransform: 'capitalize',
  },
  metricsRow: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: COLORS.surfaceSecondary,
    borderRadius: BORDER_RADIUS.sm,
    paddingVertical: SPACING.xs,
    paddingHorizontal: SPACING.sm,
    marginBottom: SPACING.sm,
  },
  metricItem: {
    flex: 1,
    alignItems: 'center',
  },
  metricLabel: {
    fontSize: 9,
    color: COLORS.textTertiary,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
    textTransform: 'uppercase',
    letterSpacing: 0.5,
    marginBottom: 2,
  },
  metricValue: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.textPrimary,
  },
  metricDivider: {
    width: 1,
    height: 24,
    backgroundColor: COLORS.gray300,
    marginHorizontal: SPACING.xs,
  },
  simpleFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  lastAuditText: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.textSecondary,
  },
  biasScoreText: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.textSecondary,
  },
});

export default ModelCard;
