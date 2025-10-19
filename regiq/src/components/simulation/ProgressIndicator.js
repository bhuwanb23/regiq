import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { COLORS, TYPOGRAPHY, SPACING, BORDER_RADIUS } from '../../constants/theme';

const ProgressIndicator = ({ currentStep = 4, totalSteps = 4, steps = ['Model', 'Scenario', 'Parameters', 'Results'] }) => {
  const progressPercentage = (currentStep / totalSteps) * 100;

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.title}>Simulation Progress</Text>
        <Text style={styles.stepText}>Step {currentStep} of {totalSteps}</Text>
      </View>

      {/* Progress Bar */}
      <View style={styles.progressBarContainer}>
        <View style={styles.progressBarBackground}>
          <View 
            style={[
              styles.progressBarFill,
              { width: `${progressPercentage}%` }
            ]}
          />
        </View>
      </View>

      {/* Step Labels */}
      <View style={styles.stepsContainer}>
        {steps.map((step, index) => (
          <View key={index} style={styles.stepItem}>
            <View style={[
              styles.stepDot,
              index < currentStep ? styles.stepDotCompleted : 
              index === currentStep - 1 ? styles.stepDotActive : styles.stepDotInactive
            ]}>
              {index < currentStep && (
                <View style={styles.checkmark} />
              )}
            </View>
            <Text style={[
              styles.stepLabel,
              index < currentStep ? styles.stepLabelCompleted :
              index === currentStep - 1 ? styles.stepLabelActive : styles.stepLabelInactive
            ]}>
              {step}
            </Text>
          </View>
        ))}
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: COLORS.white,
    paddingHorizontal: SPACING.md,
    paddingVertical: SPACING.md,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.gray200,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: SPACING.sm,
  },
  title: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.primary,
  },
  stepText: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.textSecondary,
  },
  progressBarContainer: {
    marginBottom: SPACING.md,
  },
  progressBarBackground: {
    height: 8,
    backgroundColor: COLORS.gray200,
    borderRadius: BORDER_RADIUS.full,
    overflow: 'hidden',
  },
  progressBarFill: {
    height: 8,
    backgroundColor: COLORS.secondary,
    borderRadius: BORDER_RADIUS.full,
  },
  stepsContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  stepItem: {
    alignItems: 'center',
    flex: 1,
  },
  stepDot: {
    width: 12,
    height: 12,
    borderRadius: 6,
    marginBottom: SPACING.xs,
    alignItems: 'center',
    justifyContent: 'center',
  },
  stepDotCompleted: {
    backgroundColor: COLORS.secondary,
  },
  stepDotActive: {
    backgroundColor: COLORS.secondary,
  },
  stepDotInactive: {
    backgroundColor: COLORS.gray300,
  },
  checkmark: {
    width: 6,
    height: 6,
    borderRadius: 3,
    backgroundColor: COLORS.white,
  },
  stepLabel: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    textAlign: 'center',
  },
  stepLabelCompleted: {
    color: COLORS.secondary,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
  },
  stepLabelActive: {
    color: COLORS.secondary,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
  },
  stepLabelInactive: {
    color: COLORS.textSecondary,
  },
});

export default ProgressIndicator;
