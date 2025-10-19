import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { COLORS, TYPOGRAPHY, SPACING, BORDER_RADIUS, SHADOWS } from '../../constants/theme';

const QuickActionsBanner = ({ onNewReport }) => {
  return (
    <View style={styles.container}>
      <View style={styles.banner}>
        <View style={styles.content}>
          <Text style={styles.title}>Generate New Report</Text>
          <Text style={styles.subtitle}>Create audit-ready compliance documentation</Text>
          
          <TouchableOpacity 
            style={styles.actionButton}
            onPress={onNewReport}
            activeOpacity={0.8}
          >
            <Ionicons name="add" size={16} color={COLORS.primary} />
            <Text style={styles.buttonText}>New Report</Text>
          </TouchableOpacity>
        </View>
        
        <View style={styles.iconContainer}>
          <Ionicons name="document-text" size={32} color={`${COLORS.white}80`} />
        </View>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    paddingHorizontal: SPACING.md,
    paddingVertical: SPACING.lg,
  },
  banner: {
    backgroundColor: COLORS.primary,
    borderRadius: BORDER_RADIUS['2xl'],
    padding: SPACING.lg,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    ...SHADOWS.md,
  },
  content: {
    flex: 1,
  },
  title: {
    fontSize: TYPOGRAPHY.fontSize.lg,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.white,
    marginBottom: SPACING.xs,
  },
  subtitle: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    color: `${COLORS.white}CC`,
    marginBottom: SPACING.md,
    lineHeight: 18,
  },
  actionButton: {
    backgroundColor: COLORS.white,
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: SPACING.md,
    paddingVertical: SPACING.sm,
    borderRadius: BORDER_RADIUS.lg,
    alignSelf: 'flex-start',
  },
  buttonText: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.primary,
    marginLeft: SPACING.xs,
  },
  iconContainer: {
    marginLeft: SPACING.md,
  },
});

export default QuickActionsBanner;
