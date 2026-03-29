import React from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  Modal,
  ScrollView,
  ActivityIndicator,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { COLORS, TYPOGRAPHY, SPACING, BORDER_RADIUS, SHADOWS } from '../../constants/theme';

const RegulationDetailModal = ({ 
  visible, 
  regulation, 
  onClose,
  loading = false
}) => {
  // Get priority color function
  const getPriorityColor = (priority) => {
    switch (priority?.toLowerCase()) {
      case 'critical':
        return COLORS.error;
      case 'high':
        return COLORS.warning;
      case 'medium':
        return COLORS.info;
      case 'low':
        return COLORS.success;
      default:
        return COLORS.gray400;
    }
  };

  // Get category icon function
  const getCategoryIcon = (category) => {
    switch (category?.toLowerCase()) {
      case 'ai/ml':
        return 'hardware-chip';
      case 'banking':
        return 'business';
      case 'crypto':
        return 'logo-bitcoin';
      case 'payments':
        return 'card';
      default:
        return 'document-text';
    }
  };

  return (
    <Modal
      animationType="slide"
      transparent={true}
      visible={visible}
      onRequestClose={onClose}
    >
      <View style={styles.modalOverlay}>
        <View style={styles.modalContainer}>
          {/* Header with close button */}
          <View style={styles.modalHeader}>
            <TouchableOpacity 
              style={styles.closeButton}
              onPress={onClose}
            >
              <Ionicons name="close" size={24} color={COLORS.textSecondary} />
            </TouchableOpacity>
            <Text style={styles.modalTitle}>Regulation Details</Text>
            <View style={styles.placeholder} /> {/* Balance the header */}
          </View>

          {/* Content */}
          <ScrollView 
            style={styles.modalContent}
            showsVerticalScrollIndicator={false}
          >
            {loading ? (
              <View style={styles.loadingContainer}>
                <ActivityIndicator size="large" color={COLORS.primary} />
                <Text style={styles.loadingText}>Loading regulation details...</Text>
              </View>
            ) : regulation ? (
              <>
                {/* Regulation Title */}
                <Text style={styles.regulationTitle}>{regulation.title}</Text>
                
                {/* Regulation Metadata */}
                <View style={styles.metadataContainer}>
                  <View style={styles.metadataItem}>
                    <Text style={styles.metadataLabel}>Region</Text>
                    <Text style={styles.metadataValue}>{regulation.region}</Text>
                  </View>
                  
                  <View style={styles.metadataItem}>
                    <Text style={styles.metadataLabel}>Category</Text>
                    <View style={styles.categoryContainer}>
                      <Ionicons 
                        name={getCategoryIcon(regulation.category)} 
                        size={12} 
                        color={COLORS.gray500} 
                      />
                      <Text style={styles.metadataValue}>{regulation.category}</Text>
                    </View>
                  </View>
                  
                  <View style={styles.metadataItem}>
                    <Text style={styles.metadataLabel}>Effective Date</Text>
                    <Text style={styles.metadataValue}>{regulation.effectiveDate}</Text>
                  </View>
                  
                  <View style={styles.metadataItem}>
                    <Text style={styles.metadataLabel}>Priority</Text>
                    <View style={styles.priorityContainer}>
                      <View style={[
                        styles.priorityDot, 
                        { backgroundColor: getPriorityColor(regulation.priority) }
                      ]} />
                      <Text style={[styles.metadataValue, { color: getPriorityColor(regulation.priority) }]}>
                        {regulation.priority}
                      </Text>
                    </View>
                  </View>
                </View>

                {/* Description */}
                <View style={styles.section}>
                  <Text style={styles.sectionTitle}>Description</Text>
                  <Text style={styles.description}>{regulation.description}</Text>
                </View>

                {/* Key Requirements */}
                <View style={styles.section}>
                  <Text style={styles.sectionTitle}>Key Requirements</Text>
                  <ScrollView 
                    style={styles.requirementsScroll}
                    contentContainerStyle={styles.requirementsContent}
                  >
                    <Text style={styles.requirementsText}>
                      {String(regulation.fullDetails || '').trim()}
                    </Text>
                  </ScrollView>
                </View>

                {/* Tags */}
                {regulation.tags && regulation.tags.length > 0 && (
                  <View style={styles.section}>
                    <Text style={styles.sectionTitle}>Tags</Text>
                    <View style={styles.tagsContainer}>
                      {regulation.tags.map((tag, index) => (
                        <View key={index} style={styles.tag}>
                          <Text style={styles.tagText}>{tag}</Text>
                        </View>
                      ))}
                    </View>
                  </View>
                )}

                {/* Action Button */}
                <TouchableOpacity style={styles.actionButton}>
                  <Ionicons name="document-text" size={16} color={COLORS.white} />
                  <Text style={styles.actionButtonText}>View Full Regulation Document</Text>
                </TouchableOpacity>
              </>
            ) : (
              <View style={styles.emptyState}>
                <Ionicons name="document-text-outline" size={48} color={COLORS.gray400} />
                <Text style={styles.emptyStateTitle}>No Data Available</Text>
                <Text style={styles.emptyStateText}>
                  Regulation details could not be loaded
                </Text>
              </View>
            )}
          </ScrollView>
        </View>
      </View>
    </Modal>
  );
};

const styles = StyleSheet.create({
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    justifyContent: 'flex-end',
  },
  modalContainer: {
    backgroundColor: COLORS.white,
    borderTopLeftRadius: BORDER_RADIUS['2xl'],
    borderTopRightRadius: BORDER_RADIUS['2xl'],
    maxHeight: '80%',
    minHeight: '50%',
  },
  modalHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: SPACING.md,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.gray200,
  },
  closeButton: {
    padding: SPACING.xs,
    borderRadius: BORDER_RADIUS.full,
    backgroundColor: COLORS.gray100,
  },
  modalTitle: {
    fontSize: TYPOGRAPHY.fontSize.lg,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.textPrimary,
  },
  placeholder: {
    width: 32, // Matches close button width
  },
  modalContent: {
    padding: SPACING.md,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingVertical: SPACING['3xl'],
  },
  loadingText: {
    marginTop: SPACING.md,
    fontSize: TYPOGRAPHY.fontSize.sm,
    color: COLORS.textSecondary,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
  },
  regulationTitle: {
    fontSize: TYPOGRAPHY.fontSize.xl,
    fontWeight: TYPOGRAPHY.fontWeight.bold,
    color: COLORS.textPrimary,
    marginBottom: SPACING.md,
  },
  metadataContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginBottom: SPACING.lg,
  },
  metadataItem: {
    width: '50%',
    marginBottom: SPACING.sm,
    paddingHorizontal: SPACING.xs,
  },
  metadataLabel: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.textSecondary,
    marginBottom: SPACING.xs,
  },
  metadataValue: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
    color: COLORS.textPrimary,
  },
  categoryContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  priorityContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  priorityDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    marginRight: SPACING.xs,
  },
  section: {
    marginBottom: SPACING.lg,
  },
  sectionTitle: {
    fontSize: TYPOGRAPHY.fontSize.base,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.textPrimary,
    marginBottom: SPACING.sm,
  },
  description: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    color: COLORS.textSecondary,
    lineHeight: 20,
  },
  requirementsScroll: {
    height: 150,
  },
  requirementsContent: {
    paddingVertical: SPACING.xs,
  },
  requirementsText: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    color: COLORS.textSecondary,
    lineHeight: 20,
  },
  tagsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
  },
  tag: {
    backgroundColor: COLORS.gray100,
    borderRadius: BORDER_RADIUS.full,
    paddingHorizontal: SPACING.sm,
    paddingVertical: SPACING.xs,
    marginRight: SPACING.xs,
    marginBottom: SPACING.xs,
  },
  tagText: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.textSecondary,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
  },
  actionButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: COLORS.primary,
    borderRadius: BORDER_RADIUS.md,
    padding: SPACING.sm,
    justifyContent: 'center',
    marginBottom: SPACING.xl,
  },
  actionButtonText: {
    color: COLORS.white,
    fontSize: TYPOGRAPHY.fontSize.sm,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    marginLeft: SPACING.sm,
  },
  emptyState: {
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: SPACING['3xl'],
  },
  emptyStateTitle: {
    fontSize: TYPOGRAPHY.fontSize.lg,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.textPrimary,
    marginTop: SPACING.md,
    marginBottom: SPACING.xs,
  },
  emptyStateText: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    color: COLORS.textSecondary,
    textAlign: 'center',
    paddingHorizontal: SPACING.xl,
  },
});

export default RegulationDetailModal;