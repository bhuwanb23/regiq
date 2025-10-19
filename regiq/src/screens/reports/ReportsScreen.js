import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { COLORS, TYPOGRAPHY } from '../../constants/theme';

const ReportsScreen = () => {
  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.content}>
        <Text style={styles.title}>Reports & Audit</Text>
        <Text style={styles.subtitle}>
          Generate and manage compliance reports
        </Text>
        <Text style={styles.placeholder}>
          📊 Coming Soon: Audit reports, compliance summaries, and export options
        </Text>
      </View>
    </SafeAreaView>
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
    padding: 20,
  },
  title: {
    fontSize: TYPOGRAPHY.fontSize['2xl'],
    fontWeight: TYPOGRAPHY.fontWeight.bold,
    color: COLORS.textPrimary,
    marginBottom: 8,
  },
  subtitle: {
    fontSize: TYPOGRAPHY.fontSize.base,
    color: COLORS.textSecondary,
    textAlign: 'center',
    marginBottom: 24,
  },
  placeholder: {
    fontSize: TYPOGRAPHY.fontSize.lg,
    color: COLORS.textTertiary,
    textAlign: 'center',
  },
});

export default ReportsScreen;
