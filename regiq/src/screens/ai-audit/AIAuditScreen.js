import React from 'react';
import {
  View,
  Text,
  ScrollView,
  StyleSheet,
  RefreshControl,
  FlatList,
  TouchableOpacity,
  Alert,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';

import AuditOverview from '../../components/ai-audit/AuditOverview';
import ModelCard from '../../components/ai-audit/ModelCard';
import ModelDetailModal from '../../components/ai-audit/ModelDetailModal';
import useAIAuditData from '../../hooks/useAIAuditData';
import { COLORS, TYPOGRAPHY, SPACING, BORDER_RADIUS, SHADOWS } from '../../constants/theme';

const AIAuditScreen = ({ navigation }) => {
  const {
    auditData,
    loading,
    refreshing,
    selectedModel,
    modalVisible,
    refreshAuditData,
    handleModelPress,
    handleModelAudit,
    handleGenerateReport,
    handleRunSimulation,
    closeModal,
    getHighRiskModels,
  } = useAIAuditData();

  const renderModelItem = ({ item }) => (
    <ModelCard
      model={item}
      onPress={handleModelPress}
      onAudit={handleModelAudit}
    />
  );

  const renderEmptyState = () => (
    <View style={styles.emptyState}>
      <Ionicons name="hardware-chip-outline" size={48} color={COLORS.gray400} />
      <Text style={styles.emptyStateTitle}>No AI Models Found</Text>
      <Text style={styles.emptyStateText}>
        Add AI models to start monitoring their performance and bias
      </Text>
      <TouchableOpacity style={styles.addModelButton}>
        <Ionicons name="add" size={16} color={COLORS.white} />
        <Text style={styles.addModelButtonText}>Add Model</Text>
      </TouchableOpacity>
    </View>
  );

  const HighRiskAlert = () => {
    const highRiskModels = getHighRiskModels();
    
    if (highRiskModels.length === 0) return null;

    return (
      <View style={styles.alertContainer}>
        <View style={styles.alertHeader}>
          <Ionicons name="warning" size={16} color={COLORS.warning} />
          <Text style={styles.alertTitle}>High Risk Models Detected</Text>
        </View>
        <Text style={styles.alertText}>
          {highRiskModels.length} model{highRiskModels.length > 1 ? 's' : ''} require immediate attention due to high bias scores or risk levels.
        </Text>
        <TouchableOpacity style={styles.alertAction}>
          <Text style={styles.alertActionText}>Review Now</Text>
          <Ionicons name="chevron-forward" size={12} color={COLORS.warning} />
        </TouchableOpacity>
      </View>
    );
  };

  if (loading) {
    return (
      <View style={[styles.container, styles.centerContent]}>
        <Text style={styles.loadingText}>Loading AI models...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <FlatList
        data={auditData.models}
        renderItem={renderModelItem}
        keyExtractor={(item) => item.id}
        contentContainerStyle={styles.listContainer}
        showsVerticalScrollIndicator={false}
        refreshControl={
          <RefreshControl
            refreshing={refreshing}
            onRefresh={refreshAuditData}
            colors={[COLORS.primary]}
            tintColor={COLORS.primary}
          />
        }
        ListHeaderComponent={() => (
          <>
            {/* Overview Section */}
            <AuditOverview overviewData={auditData.overview} />
            
            {/* High Risk Alert */}
            <HighRiskAlert />
            
            {/* Models Section Header */}
            <View style={styles.sectionHeader}>
              <View style={styles.sectionTitleContainer}>
                <Text style={styles.sectionTitle}>AI Models</Text>
                <View style={styles.modelCount}>
                  <Text style={styles.modelCountText}>{auditData.models.length}</Text>
                </View>
              </View>
              
              <View style={styles.sectionActions}>
                <TouchableOpacity style={styles.filterButton}>
                  <Ionicons name="filter" size={14} color={COLORS.textSecondary} />
                  <Text style={styles.filterButtonText}>Filter</Text>
                </TouchableOpacity>
                
                <TouchableOpacity style={styles.sortButton}>
                  <Ionicons name="swap-vertical" size={14} color={COLORS.textSecondary} />
                  <Text style={styles.sortButtonText}>Sort</Text>
                </TouchableOpacity>
              </View>
            </View>

            {/* Quick Stats */}
            <View style={styles.quickStats}>
              <View style={styles.quickStatItem}>
                <Text style={styles.quickStatValue}>
                  {auditData.models.filter(m => m.status === 'Active').length}
                </Text>
                <Text style={styles.quickStatLabel}>Active</Text>
              </View>
              
              <View style={styles.quickStatDivider} />
              
              <View style={styles.quickStatItem}>
                <Text style={[
                  styles.quickStatValue,
                  { color: COLORS.warning }
                ]}>
                  {auditData.models.filter(m => m.status === 'Warning').length}
                </Text>
                <Text style={styles.quickStatLabel}>Warning</Text>
              </View>
              
              <View style={styles.quickStatDivider} />
              
              <View style={styles.quickStatItem}>
                <Text style={[
                  styles.quickStatValue,
                  { color: COLORS.error }
                ]}>
                  {getHighRiskModels().length}
                </Text>
                <Text style={styles.quickStatLabel}>High Risk</Text>
              </View>
            </View>
          </>
        )}
        ListEmptyComponent={renderEmptyState}
        ListFooterComponent={() => (
          <View style={styles.bottomSpacing} />
        )}
      />

      {/* Model Detail Modal */}
      <ModelDetailModal
        visible={modalVisible}
        model={selectedModel}
        onClose={closeModal}
        onGenerateReport={handleGenerateReport}
        onRunSimulation={handleRunSimulation}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  centerContent: {
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    fontSize: TYPOGRAPHY.fontSize.base,
    color: COLORS.textSecondary,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
  },
  listContainer: {
    paddingHorizontal: SPACING.md,
    paddingTop: SPACING.sm,
  },
  alertContainer: {
    backgroundColor: `${COLORS.warning}15`,
    borderRadius: BORDER_RADIUS.lg,
    padding: SPACING.md,
    marginBottom: SPACING.md,
    borderLeftWidth: 4,
    borderLeftColor: COLORS.warning,
  },
  alertHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: SPACING.xs,
  },
  alertTitle: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.warning,
    marginLeft: SPACING.xs,
  },
  alertText: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.textSecondary,
    lineHeight: 16,
    marginBottom: SPACING.sm,
  },
  alertAction: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  alertActionText: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.warning,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
    marginRight: 4,
  },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: SPACING.sm,
    paddingHorizontal: SPACING.xs,
  },
  sectionTitleContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  sectionTitle: {
    fontSize: TYPOGRAPHY.fontSize.base,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.textPrimary,
    marginRight: SPACING.xs,
  },
  modelCount: {
    backgroundColor: COLORS.primary,
    borderRadius: BORDER_RADIUS.full,
    paddingHorizontal: SPACING.xs,
    paddingVertical: 2,
    minWidth: 20,
    alignItems: 'center',
  },
  modelCountText: {
    fontSize: 10,
    color: COLORS.white,
    fontWeight: TYPOGRAPHY.fontWeight.bold,
  },
  sectionActions: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  filterButton: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: SPACING.sm,
    paddingVertical: SPACING.xs,
    backgroundColor: COLORS.surfaceSecondary,
    borderRadius: BORDER_RADIUS.sm,
    marginRight: SPACING.xs,
  },
  filterButtonText: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.textSecondary,
    marginLeft: 4,
  },
  sortButton: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: SPACING.sm,
    paddingVertical: SPACING.xs,
    backgroundColor: COLORS.surfaceSecondary,
    borderRadius: BORDER_RADIUS.sm,
  },
  sortButtonText: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.textSecondary,
    marginLeft: 4,
  },
  quickStats: {
    flexDirection: 'row',
    backgroundColor: COLORS.white,
    borderRadius: BORDER_RADIUS.lg,
    paddingVertical: SPACING.sm,
    paddingHorizontal: SPACING.md,
    marginBottom: SPACING.md,
    ...SHADOWS.sm,
  },
  quickStatItem: {
    flex: 1,
    alignItems: 'center',
  },
  quickStatValue: {
    fontSize: TYPOGRAPHY.fontSize.lg,
    fontWeight: TYPOGRAPHY.fontWeight.bold,
    color: COLORS.textPrimary,
    marginBottom: 2,
  },
  quickStatLabel: {
    fontSize: 10,
    color: COLORS.textSecondary,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
  },
  quickStatDivider: {
    width: 1,
    height: 30,
    backgroundColor: COLORS.gray300,
    marginHorizontal: SPACING.sm,
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
    marginBottom: SPACING.lg,
  },
  addModelButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: COLORS.primary,
    paddingHorizontal: SPACING.lg,
    paddingVertical: SPACING.sm,
    borderRadius: BORDER_RADIUS.md,
  },
  addModelButtonText: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    color: COLORS.white,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
    marginLeft: SPACING.xs,
  },
  bottomSpacing: {
    height: SPACING.xl,
  },
});

export default AIAuditScreen;
