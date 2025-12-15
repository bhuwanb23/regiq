import React from 'react'; // Added missing React import
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
            <Ionicons name="add" size={14} color={COLORS.primary} />
            <Text style={styles.buttonText}>New Report</Text>
          </TouchableOpacity>
        </View>
        
        <View style={styles.iconContainer}>
          <Ionicons name="document-text" size={24} color={`${COLORS.white}80`} />
        </View>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    paddingHorizontal: SPACING.sm,
    paddingVertical: SPACING.md,
  },
  banner: {
    backgroundColor: COLORS.primary,
    borderRadius: BORDER_RADIUS.xl,
    padding: SPACING.md,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    ...SHADOWS.sm,
  },
  content: {
    flex: 1,
  },
  title: {
    fontSize: TYPOGRAPHY.fontSize.base,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.white,
    marginBottom: SPACING.xs,
  },
  subtitle: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: `${COLORS.white}CC`,
    marginBottom: SPACING.sm,
    lineHeight: 16,
  },
  actionButton: {
    backgroundColor: COLORS.white,
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: SPACING.sm,
    paddingVertical: SPACING.xs,
    borderRadius: BORDER_RADIUS.lg,
    alignSelf: 'flex-start',
  },
  buttonText: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.primary,
    marginLeft: SPACING.xs,
  },
  iconContainer: {
    marginLeft: SPACING.sm,
  },
});

export default QuickActionsBanner;