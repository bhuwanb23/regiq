import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  RefreshControl,
  TouchableOpacity,
  ActivityIndicator,
  Alert,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { COLORS, TYPOGRAPHY, SPACING, BORDER_RADIUS, SHADOWS } from '../../constants/theme';
import useBiasData from '../../hooks/useBiasData';
import BiasHeatmapChart from '../../components/ai-audit/charts/BiasHeatmapChart';
import FeatureImportanceChart from '../../components/ai-audit/charts/FeatureImportanceChart';
import ModelDriftChart from '../../components/ai-audit/charts/ModelDriftChart';

const ModelAuditScreen = ({ route }) => {
  const { modelId } = route.params || {};
  const {
    loading,
    error,
    reports,
    selectedReport,
    mitigationStrategies,
    fetchBiasReports,
    fetchBiasReportById,
    runBiasAnalysis,
    fetchMitigationStrategies,
    setSelectedReport,
  } = useBiasData(modelId);

  const [refreshing, setRefreshing] = useState(false);
  const [activeTab, setActiveTab] = useState('overview');

  // Refresh data
  const onRefresh = async () => {
    setRefreshing(true);
    try {
      await fetchBiasReports();
      if (modelId) {
        await fetchMitigationStrategies(modelId);
      }
    } catch (err) {
      console.error('Error refreshing data:', err);
    } finally {
      setRefreshing(false);
    }
  };

  // Load initial data
  useEffect(() => {
    fetchBiasReports({ modelId });
    if (modelId) {
      fetchMitigationStrategies(modelId);
    }
  }, [modelId]);

  // Handle report selection
  const handleReportSelect = async (reportId) => {
    try {
      await fetchBiasReportById(reportId);
      setActiveTab('details');
    } catch (err) {
      Alert.alert('Error', 'Failed to load report details');
    }
  };

  // Run new bias analysis
  const handleRunAnalysis = async () => {
    try {
      await runBiasAnalysis({ modelId });
      Alert.alert('Success', 'Bias analysis started successfully');
    } catch (err) {
      Alert.alert('Error', 'Failed to start bias analysis');
    }
  };

  // Render loading state
  if (loading && !refreshing) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.centerContent}>
          <ActivityIndicator size="large" color={COLORS.primary} />
          <Text style={styles.loadingText}>Loading bias analysis...</Text>
        </View>
      </SafeAreaView>
    );
  }

  // Render error state
  if (error) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.centerContent}>
          <Ionicons name="warning" size={48} color={COLORS.error} />
          <Text style={styles.errorText}>Error loading bias data</Text>
          <Text style={styles.errorSubtext}>{error}</Text>
          <TouchableOpacity style={styles.retryButton} onPress={onRefresh}>
            <Text style={styles.retryButtonText}>Retry</Text>
          </TouchableOpacity>
        </View>
      </SafeAreaView>
    );
  }

  // Render report list
  const renderReportList = () => (
    <View style={styles.section}>
      <View style={styles.sectionHeader}>
        <Text style={styles.sectionTitle}>Bias Analysis Reports</Text>
        <TouchableOpacity style={styles.refreshButton} onPress={onRefresh}>
          <Ionicons name="refresh" size={16} color={COLORS.primary} />
        </TouchableOpacity>
      </View>
      
      {reports.length === 0 ? (
        <View style={styles.emptyState}>
          <Ionicons name="document-text-outline" size={48} color={COLORS.gray400} />
          <Text style={styles.emptyStateTitle}>No Bias Reports</Text>
          <Text style={styles.emptyStateText}>
            Run a bias analysis to generate reports for this model
          </Text>
        </View>
      ) : (
        <View style={styles.reportList}>
          {reports.map((report) => (
            <TouchableOpacity
              key={report.id}
              style={styles.reportCard}
              onPress={() => handleReportSelect(report.id)}
            >
              <View style={styles.reportHeader}>
                <Text style={styles.reportTitle}>{report.modelName || 'Model Analysis'}</Text>
                <View style={[
                  styles.statusBadge,
                  { backgroundColor: report.status === 'completed' ? `${COLORS.success}20` : `${COLORS.warning}20` }
                ]}>
                  <Text style={[
                    styles.statusText,
                    { color: report.status === 'completed' ? COLORS.success : COLORS.warning }
                  ]}>
                    {report.status}
                  </Text>
                </View>
              </View>
              <Text style={styles.reportDate}>
                {new Date(report.createdAt).toLocaleDateString()}
              </Text>
              <View style={styles.reportMetrics}>
                <View style={styles.metricItem}>
                  <Text style={styles.metricLabel}>Bias Score</Text>
                  <Text style={styles.metricValue}>
                    {(report.overallBiasScore || 0).toFixed(2)}
                  </Text>
                </View>
                <View style={styles.metricItem}>
                  <Text style={styles.metricLabel}>Features</Text>
                  <Text style={styles.metricValue}>
                    {report.featureCount || 0}
                  </Text>
                </View>
              </View>
            </TouchableOpacity>
          ))}
        </View>
      )}
    </View>
  );

  // Render bias details
  const renderBiasDetails = () => {
    if (!selectedReport) {
      return (
        <View style={styles.centerContent}>
          <Text style={styles.placeholderText}>Select a report to view details</Text>
        </View>
      );
    }

    return (
      <ScrollView style={styles.detailsContainer}>
        <View style={styles.reportHeader}>
          <Text style={styles.detailTitle}>{selectedReport.modelName || 'Bias Analysis Report'}</Text>
          <TouchableOpacity onPress={() => setSelectedReport(null)}>
            <Ionicons name="close" size={24} color={COLORS.textSecondary} />
          </TouchableOpacity>
        </View>
        
        <View style={styles.scoreCard}>
          <Text style={styles.scoreLabel}>Overall Bias Score</Text>
          <Text style={styles.scoreValue}>
            {(selectedReport.overallBiasScore || 0).toFixed(2)}
          </Text>
          <View style={styles.scoreBar}>
            <View 
              style={[
                styles.scoreFill,
                {
                  width: `${(selectedReport.overallBiasScore || 0) * 100}%`,
                  backgroundColor: selectedReport.overallBiasScore > 0.7 ? COLORS.success :
                                  selectedReport.overallBiasScore > 0.4 ? COLORS.warning : COLORS.error
                }
              ]}
            />
          </View>
        </View>

        <BiasHeatmapChart data={selectedReport} />
        <FeatureImportanceChart data={selectedReport} />
        <ModelDriftChart data={selectedReport} />

        <View style={styles.actionsContainer}>
          <TouchableOpacity style={styles.actionButton} onPress={handleRunAnalysis}>
            <Ionicons name="play" size={16} color={COLORS.white} />
            <Text style={styles.actionButtonText}>Run New Analysis</Text>
          </TouchableOpacity>
        </View>
      </ScrollView>
    );
  };

  // Render mitigation strategies
  const renderMitigation = () => (
    <View style={styles.section}>
      <Text style={styles.sectionTitle}>Mitigation Strategies</Text>
      {mitigationStrategies.length === 0 ? (
        <View style={styles.emptyState}>
          <Ionicons name="bulb-outline" size={48} color={COLORS.gray400} />
          <Text style={styles.emptyStateTitle}>No Mitigation Strategies</Text>
          <Text style={styles.emptyStateText}>
            No mitigation strategies available for this model
          </Text>
        </View>
      ) : (
        <View style={styles.mitigationList}>
          {mitigationStrategies.map((strategy, index) => (
            <View key={index} style={styles.mitigationCard}>
              <View style={styles.mitigationHeader}>
                <Text style={styles.mitigationTitle}>{strategy.title}</Text>
                <View style={[
                  styles.priorityBadge,
                  { backgroundColor: strategy.priority === 'high' ? `${COLORS.error}20` : 
                                    strategy.priority === 'medium' ? `${COLORS.warning}20` : 
                                    `${COLORS.info}20` }
                ]}>
                  <Text style={[
                    styles.priorityText,
                    { color: strategy.priority === 'high' ? COLORS.error : 
                              strategy.priority === 'medium' ? COLORS.warning : COLORS.info }
                  ]}>
                    {strategy.priority}
                  </Text>
                </View>
              </View>
              <Text style={styles.mitigationDescription}>{strategy.description}</Text>
              <View style={styles.mitigationActions}>
                <TouchableOpacity style={styles.applyButton}>
                  <Text style={styles.applyButtonText}>Apply Strategy</Text>
                </TouchableOpacity>
              </View>
            </View>
          ))}
        </View>
      )}
    </View>
  );

  // Render tabs
  const renderTabs = () => (
    <View style={styles.tabsContainer}>
      <TouchableOpacity
        style={[styles.tab, activeTab === 'overview' && styles.activeTab]}
        onPress={() => setActiveTab('overview')}
      >
        <Text style={[styles.tabText, activeTab === 'overview' && styles.activeTabText]}>
          Reports
        </Text>
      </TouchableOpacity>
      
      <TouchableOpacity
        style={[styles.tab, activeTab === 'details' && styles.activeTab]}
        onPress={() => setActiveTab('details')}
      >
        <Text style={[styles.tabText, activeTab === 'details' && styles.activeTabText]}>
          Analysis
        </Text>
      </TouchableOpacity>
      
      <TouchableOpacity
        style={[styles.tab, activeTab === 'mitigation' && styles.activeTab]}
        onPress={() => setActiveTab('mitigation')}
      >
        <Text style={[styles.tabText, activeTab === 'mitigation' && styles.activeTabText]}>
          Mitigation
        </Text>
      </TouchableOpacity>
    </View>
  );

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Bias Analysis</Text>
        <Text style={styles.subtitle}>Monitor and mitigate AI model bias</Text>
      </View>

      {renderTabs()}

      <ScrollView
        style={styles.content}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
      >
        {activeTab === 'overview' && renderReportList()}
        {activeTab === 'details' && renderBiasDetails()}
        {activeTab === 'mitigation' && renderMitigation()}
      </ScrollView>

      {activeTab === 'overview' && (
        <View style={styles.fabContainer}>
          <TouchableOpacity style={styles.fab} onPress={handleRunAnalysis}>
            <Ionicons name="play" size={24} color={COLORS.white} />
          </TouchableOpacity>
        </View>
      )}
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  header: {
    paddingHorizontal: SPACING.lg,
    paddingVertical: SPACING.md,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.gray200,
  },
  title: {
    fontSize: TYPOGRAPHY.fontSize['2xl'],
    fontWeight: TYPOGRAPHY.fontWeight.bold,
    color: COLORS.textPrimary,
  },
  subtitle: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    color: COLORS.textSecondary,
    marginTop: 4,
  },
  tabsContainer: {
    flexDirection: 'row',
    backgroundColor: COLORS.white,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.gray200,
  },
  tab: {
    flex: 1,
    paddingVertical: SPACING.md,
    alignItems: 'center',
  },
  activeTab: {
    borderBottomWidth: 2,
    borderBottomColor: COLORS.primary,
  },
  tabText: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    color: COLORS.textSecondary,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
  },
  activeTabText: {
    color: COLORS.primary,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
  },
  content: {
    flex: 1,
  },
  centerContent: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: SPACING.xl,
  },
  loadingText: {
    fontSize: TYPOGRAPHY.fontSize.base,
    color: COLORS.textSecondary,
    marginTop: SPACING.md,
  },
  errorText: {
    fontSize: TYPOGRAPHY.fontSize.lg,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.textPrimary,
    marginTop: SPACING.md,
  },
  errorSubtext: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    color: COLORS.textSecondary,
    textAlign: 'center',
    marginTop: SPACING.sm,
    marginBottom: SPACING.lg,
  },
  retryButton: {
    backgroundColor: COLORS.primary,
    paddingHorizontal: SPACING.lg,
    paddingVertical: SPACING.sm,
    borderRadius: BORDER_RADIUS.md,
  },
  retryButtonText: {
    color: COLORS.white,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
  },
  section: {
    padding: SPACING.lg,
  },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: SPACING.md,
  },
  sectionTitle: {
    fontSize: TYPOGRAPHY.fontSize.lg,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.textPrimary,
  },
  refreshButton: {
    padding: SPACING.xs,
  },
  emptyState: {
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: SPACING['2xl'],
  },
  emptyStateTitle: {
    fontSize: TYPOGRAPHY.fontSize.base,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.textPrimary,
    marginTop: SPACING.md,
  },
  emptyStateText: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    color: COLORS.textSecondary,
    textAlign: 'center',
    marginTop: SPACING.xs,
    paddingHorizontal: SPACING.lg,
  },
  reportList: {
    gap: SPACING.md,
  },
  reportCard: {
    backgroundColor: COLORS.white,
    borderRadius: BORDER_RADIUS.lg,
    padding: SPACING.lg,
    ...SHADOWS.sm,
  },
  reportHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: SPACING.sm,
  },
  reportTitle: {
    fontSize: TYPOGRAPHY.fontSize.base,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.textPrimary,
    flex: 1,
  },
  statusBadge: {
    paddingHorizontal: SPACING.xs,
    paddingVertical: 2,
    borderRadius: BORDER_RADIUS.full,
  },
  statusText: {
    fontSize: 10,
    fontWeight: TYPOGRAPHY.fontWeight.bold,
    textTransform: 'uppercase',
  },
  reportDate: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.textSecondary,
    marginBottom: SPACING.sm,
  },
  reportMetrics: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  metricItem: {
    alignItems: 'center',
  },
  metricLabel: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.textSecondary,
    marginBottom: 4,
  },
  metricValue: {
    fontSize: TYPOGRAPHY.fontSize.base,
    fontWeight: TYPOGRAPHY.fontWeight.bold,
    color: COLORS.textPrimary,
  },
  detailsContainer: {
    padding: SPACING.lg,
  },
  detailTitle: {
    fontSize: TYPOGRAPHY.fontSize['2xl'],
    fontWeight: TYPOGRAPHY.fontWeight.bold,
    color: COLORS.textPrimary,
    flex: 1,
  },
  scoreCard: {
    backgroundColor: COLORS.white,
    borderRadius: BORDER_RADIUS.lg,
    padding: SPACING.lg,
    marginBottom: SPACING.lg,
    ...SHADOWS.sm,
  },
  scoreLabel: {
    fontSize: TYPOGRAPHY.fontSize.base,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.textPrimary,
    marginBottom: SPACING.sm,
  },
  scoreValue: {
    fontSize: TYPOGRAPHY.fontSize['3xl'],
    fontWeight: TYPOGRAPHY.fontWeight.bold,
    color: COLORS.textPrimary,
    marginBottom: SPACING.sm,
  },
  scoreBar: {
    height: 8,
    backgroundColor: COLORS.gray200,
    borderRadius: 4,
    overflow: 'hidden',
  },
  scoreFill: {
    height: '100%',
    borderRadius: 4,
  },
  actionsContainer: {
    marginTop: SPACING.lg,
    alignItems: 'center',
  },
  actionButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: COLORS.primary,
    paddingHorizontal: SPACING.lg,
    paddingVertical: SPACING.md,
    borderRadius: BORDER_RADIUS.md,
  },
  actionButtonText: {
    color: COLORS.white,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
    marginLeft: SPACING.xs,
  },
  mitigationList: {
    gap: SPACING.md,
  },
  mitigationCard: {
    backgroundColor: COLORS.white,
    borderRadius: BORDER_RADIUS.lg,
    padding: SPACING.lg,
    ...SHADOWS.sm,
  },
  mitigationHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: SPACING.sm,
  },
  mitigationTitle: {
    fontSize: TYPOGRAPHY.fontSize.base,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.textPrimary,
    flex: 1,
  },
  priorityBadge: {
    paddingHorizontal: SPACING.xs,
    paddingVertical: 2,
    borderRadius: BORDER_RADIUS.full,
  },
  priorityText: {
    fontSize: 10,
    fontWeight: TYPOGRAPHY.fontWeight.bold,
    textTransform: 'uppercase',
  },
  mitigationDescription: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    color: COLORS.textSecondary,
    lineHeight: 20,
    marginBottom: SPACING.md,
  },
  mitigationActions: {
    alignItems: 'flex-start',
  },
  applyButton: {
    backgroundColor: COLORS.primary,
    paddingHorizontal: SPACING.md,
    paddingVertical: SPACING.sm,
    borderRadius: BORDER_RADIUS.md,
  },
  applyButtonText: {
    color: COLORS.white,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
    fontSize: TYPOGRAPHY.fontSize.sm,
  },
  fabContainer: {
    position: 'absolute',
    right: SPACING.lg,
    bottom: SPACING.lg,
  },
  fab: {
    width: 56,
    height: 56,
    borderRadius: 28,
    backgroundColor: COLORS.primary,
    justifyContent: 'center',
    alignItems: 'center',
    ...SHADOWS.lg,
  },
  placeholderText: {
    fontSize: TYPOGRAPHY.fontSize.base,
    color: COLORS.textSecondary,
  },
});

export default ModelAuditScreen;