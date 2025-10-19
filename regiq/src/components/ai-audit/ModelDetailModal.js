import React, { useState } from 'react';
import {
  View,
  Text,
  Modal,
  ScrollView,
  TouchableOpacity,
  StyleSheet,
  Dimensions,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { COLORS, TYPOGRAPHY, SPACING, BORDER_RADIUS, SHADOWS } from '../../constants/theme';

// Import all the rich components
import BiasHeatmapChart from './charts/BiasHeatmapChart';
import FeatureImportanceChart from './charts/FeatureImportanceChart';
import ModelDriftChart from './charts/ModelDriftChart';
import PerformanceMetrics from './metrics/PerformanceMetrics';
import ExplainabilityInsights from './insights/ExplainabilityInsights';
import RiskAssessment from './insights/RiskAssessment';

const { height: SCREEN_HEIGHT } = Dimensions.get('window');

const ModelDetailModal = ({ visible, model, onClose, onGenerateReport, onRunSimulation }) => {
  const [activeTab, setActiveTab] = useState('overview');

  if (!model) return null;

  const {
    name = 'Credit Risk Model v3',
    type = 'Credit Assessment',
    status = 'Active',
    version = '3.2.1',
    lastUpdated = 'Oct 15, 2024',
    biasScore = 0.12,
  } = model;

  const BiasHeatmapPlaceholder = () => (
    <View style={styles.chartPlaceholder}>
      <View style={styles.heatmapGrid}>
        {['Age', 'Gender', 'Region', 'Income'].map((category, index) => (
          <View key={category} style={styles.heatmapRow}>
            <Text style={styles.heatmapLabel}>{category}</Text>
            <View style={styles.heatmapCells}>
              {[0.1, 0.3, 0.2].map((value, cellIndex) => (
                <View
                  key={cellIndex}
                  style={[
                    styles.heatmapCell,
                    {
                      backgroundColor: value <= 0.15 ? COLORS.success : 
                                     value <= 0.25 ? COLORS.warning : COLORS.error,
                      opacity: 0.3 + (value * 0.7),
                    }
                  ]}
                >
                  <Text style={styles.heatmapValue}>{value}</Text>
                </View>
              ))}
            </View>
          </View>
        ))}
      </View>
    </View>
  );

  const FeatureImportanceChart = () => (
    <View style={styles.chartPlaceholder}>
      {[
        { name: 'Income', value: 0.35 },
        { name: 'Credit History', value: 0.32 },
        { name: 'Age', value: 0.15 },
        { name: 'Employment', value: 0.12 },
        { name: 'Debt Ratio', value: 0.06 },
      ].map((feature, index) => (
        <View key={feature.name} style={styles.featureRow}>
          <Text style={styles.featureName}>{feature.name}</Text>
          <View style={styles.featureBarContainer}>
            <View
              style={[
                styles.featureBar,
                { width: `${feature.value * 100}%` }
              ]}
            />
            <Text style={styles.featureValue}>{(feature.value * 100).toFixed(0)}%</Text>
          </View>
        </View>
      ))}
    </View>
  );

  const DriftChart = () => (
    <View style={styles.chartPlaceholder}>
      <View style={styles.driftContainer}>
        <View style={styles.driftLine}>
          {[0.02, 0.04, 0.03, 0.05].map((value, index) => (
            <View key={index} style={styles.driftPoint}>
              <View
                style={[
                  styles.driftDot,
                  { backgroundColor: value > 0.04 ? COLORS.warning : COLORS.primary }
                ]}
              />
              <Text style={styles.driftValue}>{value}</Text>
            </View>
          ))}
        </View>
        <View style={styles.driftLabels}>
          {['Week 1', 'Week 2', 'Week 3', 'Week 4'].map((week, index) => (
            <Text key={index} style={styles.driftLabel}>{week}</Text>
          ))}
        </View>
      </View>
    </View>
  );

  const TabButton = ({ id, title, isActive, onPress, icon }) => (
    <TouchableOpacity
      style={[styles.tabButton, isActive && styles.tabButtonActive]}
      onPress={() => onPress(id)}
    >
      <Ionicons 
        name={icon} 
        size={14} 
        color={isActive ? COLORS.primary : COLORS.textSecondary}
        style={styles.tabIcon}
      />
      <Text style={[styles.tabText, isActive && styles.tabTextActive]}>
        {title}
      </Text>
    </TouchableOpacity>
  );

  const renderTabContent = () => {
    switch (activeTab) {
      case 'overview':
        return (
          <View>
            {/* Model Info */}
            <View style={styles.section}>
              <View style={styles.modelInfoCard}>
                <View style={styles.modelInfoHeader}>
                  <View style={styles.modelIconContainer}>
                    <Ionicons name="hardware-chip" size={24} color={COLORS.primary} />
                  </View>
                  <View style={styles.modelTitleContainer}>
                    <Text style={styles.modelInfoTitle}>{name}</Text>
                    <Text style={styles.modelInfoSubtitle}>{type}</Text>
                  </View>
                  <View style={[styles.statusBadge, { backgroundColor: `${COLORS.success}20` }]}>
                    <Text style={[styles.statusText, { color: COLORS.success }]}>{status}</Text>
                  </View>
                </View>
                
                <View style={styles.modelInfoGrid}>
                  <View style={styles.modelInfoItem}>
                    <Ionicons name="code-working" size={14} color={COLORS.textSecondary} />
                    <Text style={styles.modelInfoLabel}>Version:</Text>
                    <Text style={styles.modelInfoValue}>{version}</Text>
                  </View>
                  <View style={styles.modelInfoItem}>
                    <Ionicons name="calendar" size={14} color={COLORS.textSecondary} />
                    <Text style={styles.modelInfoLabel}>Last Updated:</Text>
                    <Text style={styles.modelInfoValue}>{lastUpdated}</Text>
                  </View>
                  <View style={styles.modelInfoItem}>
                    <Ionicons name="analytics" size={14} color={COLORS.textSecondary} />
                    <Text style={styles.modelInfoLabel}>Predictions:</Text>
                    <Text style={styles.modelInfoValue}>1.2M+ daily</Text>
                  </View>
                  <View style={styles.modelInfoItem}>
                    <Ionicons name="server" size={14} color={COLORS.textSecondary} />
                    <Text style={styles.modelInfoLabel}>Environment:</Text>
                    <Text style={styles.modelInfoValue}>Production</Text>
                  </View>
                </View>
              </View>
            </View>

            {/* Quick Metrics */}
            <View style={styles.section}>
              <Text style={styles.sectionTitle}>Quick Metrics</Text>
              <View style={styles.quickMetricsContainer}>
                <View style={styles.quickMetricCard}>
                  <View style={[styles.metricIconContainer, { backgroundColor: `${COLORS.success}15` }]}>
                    <Ionicons name="checkmark-circle" size={18} color={COLORS.success} />
                  </View>
                  <Text style={styles.quickMetricValue}>94.2%</Text>
                  <Text style={styles.quickMetricLabel}>Accuracy</Text>
                  <View style={styles.metricTrend}>
                    <Ionicons name="arrow-up" size={10} color={COLORS.success} />
                    <Text style={[styles.trendText, { color: COLORS.success }]}>+2.1%</Text>
                  </View>
                </View>
                
                <View style={styles.quickMetricCard}>
                  <View style={[styles.metricIconContainer, { backgroundColor: `${COLORS.warning}15` }]}>
                    <Ionicons name="people" size={18} color={COLORS.warning} />
                  </View>
                  <Text style={styles.quickMetricValue}>{biasScore}</Text>
                  <Text style={styles.quickMetricLabel}>Bias Score</Text>
                  <View style={styles.metricTrend}>
                    <Ionicons name="arrow-down" size={10} color={COLORS.success} />
                    <Text style={[styles.trendText, { color: COLORS.success }]}>-0.02</Text>
                  </View>
                </View>
              </View>
              
              <View style={styles.quickMetricsContainer}>
                <View style={styles.quickMetricCard}>
                  <View style={[styles.metricIconContainer, { backgroundColor: `${COLORS.info}15` }]}>
                    <Ionicons name="trending-up" size={18} color={COLORS.info} />
                  </View>
                  <Text style={styles.quickMetricValue}>0.03</Text>
                  <Text style={styles.quickMetricLabel}>Drift Score</Text>
                  <View style={styles.metricTrend}>
                    <Ionicons name="remove" size={10} color={COLORS.gray400} />
                    <Text style={[styles.trendText, { color: COLORS.gray400 }]}>Stable</Text>
                  </View>
                </View>
                
                <View style={styles.quickMetricCard}>
                  <View style={[styles.metricIconContainer, { backgroundColor: `${COLORS.primary}15` }]}>
                    <Ionicons name="shield-checkmark" size={18} color={COLORS.primary} />
                  </View>
                  <Text style={styles.quickMetricValue}>A+</Text>
                  <Text style={styles.quickMetricLabel}>Overall Grade</Text>
                  <View style={styles.metricTrend}>
                    <Ionicons name="arrow-up" size={10} color={COLORS.success} />
                    <Text style={[styles.trendText, { color: COLORS.success }]}>Improved</Text>
                  </View>
                </View>
              </View>
            </View>

            {/* Recent Activity */}
            <View style={styles.section}>
              <Text style={styles.sectionTitle}>Recent Activity</Text>
              <View style={styles.activityContainer}>
                <View style={styles.activityItem}>
                  <View style={[styles.activityIcon, { backgroundColor: `${COLORS.success}20` }]}>
                    <Ionicons name="checkmark" size={12} color={COLORS.success} />
                  </View>
                  <View style={styles.activityContent}>
                    <Text style={styles.activityTitle}>Audit Completed</Text>
                    <Text style={styles.activityTime}>2 hours ago</Text>
                  </View>
                </View>
                <View style={styles.activityItem}>
                  <View style={[styles.activityIcon, { backgroundColor: `${COLORS.info}20` }]}>
                    <Ionicons name="refresh" size={12} color={COLORS.info} />
                  </View>
                  <View style={styles.activityContent}>
                    <Text style={styles.activityTitle}>Model Retrained</Text>
                    <Text style={styles.activityTime}>1 day ago</Text>
                  </View>
                </View>
                <View style={styles.activityItem}>
                  <View style={[styles.activityIcon, { backgroundColor: `${COLORS.warning}20` }]}>
                    <Ionicons name="warning" size={12} color={COLORS.warning} />
                  </View>
                  <View style={styles.activityContent}>
                    <Text style={styles.activityTitle}>Bias Alert Triggered</Text>
                    <Text style={styles.activityTime}>3 days ago</Text>
                  </View>
                </View>
              </View>
            </View>
          </View>
        );

      case 'performance':
        return (
          <View>
            <PerformanceMetrics modelData={model} />
          </View>
        );

      case 'bias':
        return (
          <View>
            <BiasHeatmapChart data={model} />
            <FeatureImportanceChart data={model} />
          </View>
        );

      case 'drift':
        return (
          <View>
            <ModelDriftChart data={model} />
          </View>
        );

      case 'explainability':
        return (
          <View>
            <ExplainabilityInsights modelData={model} />
          </View>
        );

      case 'risk':
        return (
          <View>
            <RiskAssessment modelData={model} />
          </View>
        );

      default:
        return null;
    }
  };

  return (
    <Modal
      visible={visible}
      animationType="slide"
      presentationStyle="pageSheet"
      onRequestClose={onClose}
    >
      <View style={styles.modalContainer}>
        {/* Header */}
        <View style={styles.modalHeader}>
          <Text style={styles.modalTitle}>Model Audit Details</Text>
          <TouchableOpacity onPress={onClose} style={styles.closeButton}>
            <Ionicons name="close" size={24} color={COLORS.textSecondary} />
          </TouchableOpacity>
        </View>

        {/* Tabs */}
        <View style={styles.tabsContainer}>
          <ScrollView horizontal showsHorizontalScrollIndicator={false}>
            <TabButton
              id="overview"
              title="Overview"
              icon="information-circle"
              isActive={activeTab === 'overview'}
              onPress={setActiveTab}
            />
            <TabButton
              id="performance"
              title="Performance"
              icon="speedometer"
              isActive={activeTab === 'performance'}
              onPress={setActiveTab}
            />
            <TabButton
              id="bias"
              title="Bias Analysis"
              icon="people"
              isActive={activeTab === 'bias'}
              onPress={setActiveTab}
            />
            <TabButton
              id="drift"
              title="Drift Detection"
              icon="trending-up"
              isActive={activeTab === 'drift'}
              onPress={setActiveTab}
            />
            <TabButton
              id="explainability"
              title="Explainability"
              icon="bulb"
              isActive={activeTab === 'explainability'}
              onPress={setActiveTab}
            />
            <TabButton
              id="risk"
              title="Risk Assessment"
              icon="shield"
              isActive={activeTab === 'risk'}
              onPress={setActiveTab}
            />
          </ScrollView>
        </View>

        {/* Content */}
        <ScrollView style={styles.content} showsVerticalScrollIndicator={false}>
          {renderTabContent()}
        </ScrollView>

        {/* Action Buttons */}
        <View style={styles.actionButtons}>
          <TouchableOpacity
            style={[styles.actionButton, styles.primaryButton]}
            onPress={() => onGenerateReport?.(model)}
          >
            <Ionicons name="document-text" size={16} color={COLORS.white} />
            <Text style={styles.primaryButtonText}>Generate Report</Text>
          </TouchableOpacity>
          
          <TouchableOpacity
            style={[styles.actionButton, styles.secondaryButton]}
            onPress={() => onRunSimulation?.(model)}
          >
            <Ionicons name="flask" size={16} color={COLORS.accent} />
            <Text style={styles.secondaryButtonText}>Run Simulation</Text>
          </TouchableOpacity>
        </View>
      </View>
    </Modal>
  );
};

const styles = StyleSheet.create({
  modalContainer: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  modalHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: SPACING.md,
    paddingVertical: SPACING.md,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.gray200,
    backgroundColor: COLORS.white,
  },
  modalTitle: {
    fontSize: TYPOGRAPHY.fontSize.lg,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.textPrimary,
  },
  closeButton: {
    padding: SPACING.xs,
  },
  tabsContainer: {
    backgroundColor: COLORS.white,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.gray200,
  },
  tabButton: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: SPACING.md,
    paddingVertical: SPACING.sm,
    marginHorizontal: SPACING.xs,
  },
  tabIcon: {
    marginRight: 4,
  },
  tabButtonActive: {
    borderBottomWidth: 2,
    borderBottomColor: COLORS.primary,
  },
  tabText: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    color: COLORS.textSecondary,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
  },
  tabTextActive: {
    color: COLORS.primary,
  },
  content: {
    flex: 1,
    paddingHorizontal: SPACING.md,
  },
  section: {
    marginVertical: SPACING.md,
  },
  sectionTitle: {
    fontSize: TYPOGRAPHY.fontSize.lg,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.textPrimary,
    marginBottom: SPACING.sm,
  },
  modelInfoCard: {
    backgroundColor: COLORS.surfaceSecondary,
    borderRadius: BORDER_RADIUS.lg,
    padding: SPACING.md,
  },
  modelInfoHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: SPACING.md,
  },
  modelIconContainer: {
    width: 48,
    height: 48,
    borderRadius: 24,
    backgroundColor: `${COLORS.primary}20`,
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: SPACING.md,
  },
  modelTitleContainer: {
    flex: 1,
  },
  modelInfoSubtitle: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    color: COLORS.textSecondary,
    marginTop: 2,
  },
  statusBadge: {
    paddingHorizontal: SPACING.sm,
    paddingVertical: SPACING.xs,
    borderRadius: BORDER_RADIUS.full,
  },
  statusText: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
  },
  modelInfoTitle: {
    fontSize: TYPOGRAPHY.fontSize.lg,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.textPrimary,
  },
  modelInfoGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
  },
  modelInfoItem: {
    flexDirection: 'row',
    alignItems: 'center',
    width: '50%',
    marginBottom: SPACING.xs,
  },
  modelInfoLabel: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.textSecondary,
    marginLeft: 4,
  },
  modelInfoValue: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
    color: COLORS.textPrimary,
    marginLeft: 4,
  },
  quickMetricsContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: SPACING.sm,
  },
  quickMetricCard: {
    backgroundColor: COLORS.white,
    borderRadius: BORDER_RADIUS.lg,
    padding: SPACING.md,
    alignItems: 'center',
    flex: 1,
    marginHorizontal: SPACING.xs,
    minHeight: 100,
    justifyContent: 'space-between',
    ...SHADOWS.sm,
  },
  metricIconContainer: {
    width: 36,
    height: 36,
    borderRadius: 18,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: SPACING.xs,
  },
  quickMetricValue: {
    fontSize: TYPOGRAPHY.fontSize.xl,
    fontWeight: TYPOGRAPHY.fontWeight.bold,
    color: COLORS.textPrimary,
    marginBottom: 4,
  },
  quickMetricLabel: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.textSecondary,
    textAlign: 'center',
    marginBottom: SPACING.xs,
  },
  metricTrend: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  trendText: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
    marginLeft: SPACING.xs,
  },
  activityContainer: {
    backgroundColor: COLORS.white,
    borderRadius: BORDER_RADIUS.md,
    padding: SPACING.sm,
  },
  activityItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: SPACING.xs,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.gray200,
  },
  activityIcon: {
    width: 24,
    height: 24,
    borderRadius: 12,
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: SPACING.sm,
  },
  activityContent: {
    flex: 1,
  },
  activityTitle: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
    color: COLORS.textPrimary,
    marginBottom: SPACING.xs,
  },
  activityTime: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.textSecondary,
  },
  metricsGrid: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  metricCard: {
    flex: 1,
    backgroundColor: COLORS.white,
    borderRadius: BORDER_RADIUS.md,
    padding: SPACING.sm,
    marginHorizontal: SPACING.xs,
    alignItems: 'center',
    ...SHADOWS.sm,
  },
  metricValue: {
    fontSize: TYPOGRAPHY.fontSize.lg,
    fontWeight: TYPOGRAPHY.fontWeight.bold,
    color: COLORS.textPrimary,
    marginBottom: 4,
  },
  metricLabel: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.textSecondary,
    textAlign: 'center',
  },
  chartPlaceholder: {
    backgroundColor: COLORS.white,
    borderRadius: BORDER_RADIUS.lg,
    padding: SPACING.md,
    minHeight: 200,
    ...SHADOWS.sm,
  },
  heatmapGrid: {
    flex: 1,
  },
  heatmapRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: SPACING.sm,
  },
  heatmapLabel: {
    width: 80,
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.textSecondary,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
  },
  heatmapCells: {
    flexDirection: 'row',
    flex: 1,
  },
  heatmapCell: {
    flex: 1,
    height: 30,
    marginHorizontal: 2,
    borderRadius: 4,
    alignItems: 'center',
    justifyContent: 'center',
  },
  heatmapValue: {
    fontSize: 10,
    color: COLORS.white,
    fontWeight: TYPOGRAPHY.fontWeight.bold,
  },
  featureRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: SPACING.sm,
  },
  featureName: {
    width: 100,
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.textSecondary,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
  },
  featureBarContainer: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
  },
  featureBar: {
    height: 20,
    backgroundColor: COLORS.secondary,
    borderRadius: 10,
    marginRight: SPACING.sm,
  },
  featureValue: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.textPrimary,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    minWidth: 35,
  },
  driftContainer: {
    flex: 1,
  },
  driftLine: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-end',
    height: 120,
    marginBottom: SPACING.sm,
  },
  driftPoint: {
    alignItems: 'center',
  },
  driftDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    marginBottom: 4,
  },
  driftValue: {
    fontSize: 10,
    color: COLORS.textSecondary,
  },
  driftLabels: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  driftLabel: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.textSecondary,
  },
  explainabilityCard: {
    backgroundColor: COLORS.white,
    borderRadius: BORDER_RADIUS.md,
    padding: SPACING.sm,
    marginBottom: SPACING.sm,
    borderLeftWidth: 4,
    borderLeftColor: COLORS.info,
    ...SHADOWS.sm,
  },
  explainabilityHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: SPACING.xs,
  },
  explainabilityTitle: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.textPrimary,
    marginLeft: SPACING.xs,
  },
  explainabilityText: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.textSecondary,
    lineHeight: 16,
  },
  actionButtons: {
    flexDirection: 'row',
    paddingHorizontal: SPACING.md,
    paddingVertical: SPACING.md,
    backgroundColor: COLORS.white,
    borderTopWidth: 1,
    borderTopColor: COLORS.gray200,
  },
  actionButton: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: SPACING.sm,
    borderRadius: BORDER_RADIUS.md,
    marginHorizontal: SPACING.xs,
  },
  primaryButton: {
    backgroundColor: COLORS.primary,
  },
  secondaryButton: {
    backgroundColor: `${COLORS.accent}20`,
    borderWidth: 1,
    borderColor: COLORS.accent,
  },
  primaryButtonText: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
    color: COLORS.white,
    marginLeft: SPACING.xs,
  },
  secondaryButtonText: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
    color: COLORS.accent,
    marginLeft: SPACING.xs,
  },
});

export default ModelDetailModal;
