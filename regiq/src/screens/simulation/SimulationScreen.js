import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
// Removed SafeAreaView import since it's handled by AppLayout
import { COLORS, TYPOGRAPHY } from '../../constants/theme';

const SimulationScreen = () => {
  return (
    // Removed SafeAreaView wrapper since it's handled by AppLayout
    <View style={styles.container}>
      <View style={styles.content}>
        <Text style={styles.title}>Risk Simulation</Text>
        <Text style={styles.subtitle}>
          Test your models against new regulations and scenarios
        </Text>
        <Text style={styles.placeholder}>
          🧪 Coming Soon: Synthetic data generation and compliance testing
        </Text>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  content: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  title: {
    fontSize: TYPOGRAPHY.fontSize.xl,
    fontWeight: TYPOGRAPHY.fontWeight.bold,
    color: COLORS.textPrimary,
    marginBottom: 8,
  },
  subtitle: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    color: COLORS.textSecondary,
    textAlign: 'center',
    marginBottom: 24,
  },
  placeholder: {
    fontSize: TYPOGRAPHY.fontSize.base,
    color: COLORS.textTertiary,
    textAlign: 'center',
  },
});

export default SimulationScreen;