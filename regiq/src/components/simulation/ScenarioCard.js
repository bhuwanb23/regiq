import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { COLORS, TYPOGRAPHY, SPACING, BORDER_RADIUS, SHADOWS } from '../../constants/theme';

const ScenarioCard = ({ 
  scenarioTitle = 'EU AI Act Implementation',
  scenarioDescription = 'New regulation effective Q2 2024',
  scenarioType = 'Compliance Scenario',
  riskLevel = 'medium',
  onChangeScenario 
}) => {
  const getRiskColor = () => {
    switch (riskLevel) {
      case 'low': return COLORS.success;
      case 'medium': return COLORS.warning;
      case 'high': return COLORS.error;
      default: return COLORS.warning;
    }
  };

  const getRiskBackground = () => {
    switch (riskLevel) {
      case 'low': return `${COLORS.success}15`;
      case 'medium': return `${COLORS.warning}15`;
      case 'high': return `${COLORS.error}15`;
      default: return `${COLORS.warning}15`;
    }
  };

  const getRiskIcon = () => {
    switch (riskLevel) {
      case 'low': return 'checkmark-circle';
      case 'medium': return 'warning';
      case 'high': return 'alert-circle';
      default: return 'warning';
    }
  };

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.title}>{scenarioType}</Text>
        <TouchableOpacity onPress={onChangeScenario} style={styles.changeButton}>
          <Text style={styles.changeButtonText}>Change</Text>
        </TouchableOpacity>
      </View>

      {/* Scenario Content */}
      <View style={[styles.scenarioContainer, { backgroundColor: getRiskBackground() }]}>
        <View style={styles.scenarioContent}>
          <View style={styles.scenarioHeader}>
            <Ionicons 
              name={getRiskIcon()} 
              size={18} 
              color={getRiskColor()} 
              style={styles.scenarioIcon}
            />
            <View style={styles.scenarioInfo}>
              <Text style={[styles.scenarioTitle, { color: getRiskColor() }]}>
                {scenarioTitle}
              </Text>
              <Text style={[styles.scenarioDescription, { color: getRiskColor() }]}>
                {scenarioDescription}
              </Text>
            </View>
          </View>

          {/* Risk Level Badge */}
          <View style={[styles.riskBadge, { backgroundColor: getRiskColor() }]}>
            <Text style={styles.riskBadgeText}>
              {riskLevel.charAt(0).toUpperCase() + riskLevel.slice(1)} Risk
            </Text>
          </View>
        </View>

        {/* Scenario Details */}
        <View style={styles.detailsContainer}>
          <View style={styles.detailItem}>
            <Ionicons name="calendar" size={14} color={getRiskColor()} />
            <Text style={[styles.detailText, { color: getRiskColor() }]}>
              Effective Q2 2024
            </Text>
          </View>
          
          <View style={styles.detailItem}>
            <Ionicons name="globe" size={14} color={getRiskColor()} />
            <Text style={[styles.detailText, { color: getRiskColor() }]}>
              European Union
            </Text>
          </View>
          
          <View style={styles.detailItem}>
            <Ionicons name="shield-checkmark" size={14} color={getRiskColor()} />
            <Text style={[styles.detailText, { color: getRiskColor() }]}>
              High-Risk AI Systems
            </Text>
          </View>
        </View>
      </View>

      {/* Impact Summary */}
      <View style={styles.impactContainer}>
        <Text style={styles.impactTitle}>Expected Impact</Text>
        <View style={styles.impactItems}>
          <View style={styles.impactItem}>
            <View style={styles.impactDot} />
            <Text style={styles.impactText}>Enhanced bias detection requirements</Text>
          </View>
          <View style={styles.impactItem}>
            <View style={styles.impactDot} />
            <Text style={styles.impactText}>Mandatory algorithmic auditing</Text>
          </View>
          <View style={styles.impactItem}>
            <View style={styles.impactDot} />
            <Text style={styles.impactText}>Increased documentation standards</Text>
          </View>
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
  changeButton: {
    paddingHorizontal: SPACING.sm,
    paddingVertical: SPACING.xs,
  },
  changeButtonText: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
    color: COLORS.secondary,
  },
  scenarioContainer: {
    borderRadius: BORDER_RADIUS.lg,
    padding: SPACING.md,
    marginBottom: SPACING.md,
    borderWidth: 1,
    borderColor: COLORS.warning,
  },
  scenarioContent: {
    marginBottom: SPACING.sm,
  },
  scenarioHeader: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    marginBottom: SPACING.sm,
  },
  scenarioIcon: {
    marginTop: 2,
    marginRight: SPACING.sm,
  },
  scenarioInfo: {
    flex: 1,
  },
  scenarioTitle: {
    fontSize: TYPOGRAPHY.fontSize.base,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    marginBottom: SPACING.xs,
  },
  scenarioDescription: {
    fontSize: TYPOGRAPHY.fontSize.sm,
  },
  riskBadge: {
    alignSelf: 'flex-start',
    paddingHorizontal: SPACING.sm,
    paddingVertical: SPACING.xs,
    borderRadius: BORDER_RADIUS.full,
  },
  riskBadgeText: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.white,
  },
  detailsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginTop: SPACING.sm,
  },
  detailItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginRight: SPACING.md,
    marginBottom: SPACING.xs,
  },
  detailText: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    marginLeft: SPACING.xs,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
  },
  impactContainer: {
    backgroundColor: COLORS.surfaceSecondary,
    borderRadius: BORDER_RADIUS.md,
    padding: SPACING.sm,
  },
  impactTitle: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.textPrimary,
    marginBottom: SPACING.sm,
  },
  impactItems: {
    gap: SPACING.xs,
  },
  impactItem: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  impactDot: {
    width: 4,
    height: 4,
    borderRadius: 2,
    backgroundColor: COLORS.primary,
    marginRight: SPACING.sm,
  },
  impactText: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.textSecondary,
    flex: 1,
  },
});

export default ScenarioCard;
