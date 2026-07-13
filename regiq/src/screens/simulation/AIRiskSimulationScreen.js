import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  StyleSheet,
  StatusBar,
  ActivityIndicator,
  Alert,
} from 'react-native';
// Removed SafeAreaView import since it's handled by AppLayout
import { Ionicons } from '@expo/vector-icons';
import { COLORS, TYPOGRAPHY, SPACING, BORDER_RADIUS, SHADOWS } from '../../constants/theme';

// Import components
import ProgressIndicator from '../../components/simulation/ProgressIndicator';
import ModelSelectionCard from '../../components/simulation/ModelSelectionCard';
import ScenarioCard from '../../components/simulation/ScenarioCard';
import ResultsOverview from '../../components/simulation/ResultsOverview';
import RiskImpactChart from '../../components/simulation/RiskImpactChart';
import InsightsRecommendations from '../../components/simulation/InsightsRecommendations';
import ActionButtons from '../../components/simulation/ActionButtons';

// Import hook for risk simulation data
import useRiskSimulationData from '../../hooks/useRiskSimulationData';

const AIRiskSimulationScreen = ({ navigation = null }) => {
  const [currentStep] = useState(4);
  const [timeframe, setTimeframe] = useState('7D');
  const [selectedScenario, setSelectedScenario] = useState(null);
  const [refreshing, setRefreshing] = useState(false);

  // Use the risk simulation hook
  const {
    loading,
    error,
    simulations,
    selectedSimulation,
    scenarios,
    fetchRiskSimulations,
    fetchRiskSimulationById,
    runRiskSimulation,
    fetchRiskScenarios,
    setSelectedSimulation,
  } = useRiskSimulationData();

  // Refresh data
  const onRefresh = async () => {
    setRefreshing(true);
    try {
      await fetchRiskSimulations();
      await fetchRiskScenarios();
    } catch (err) {
      console.error('Error refreshing data:', err);
    } finally {
      setRefreshing(false);
    }
  };

  // Handle model change
  const handleChangeModel = () => {
    // Handle model change
    console.log('Change model pressed');
  };

  // Handle scenario change
  const handleChangeScenario = (scenario) => {
    setSelectedScenario(scenario);
    console.log('Scenario changed to:', scenario);
  };

  const handleTimeframeChange = (newTimeframe) => {
    setTimeframe(newTimeframe);
    console.log('Timeframe changed to:', newTimeframe);
  };

  const handleInsightPress = (insight) => {
    console.log('Insight pressed:', insight);
  };

  const handleDownloadReport = () => {
    console.log('Download report pressed');
  };

  const handleShareResults = () => {
    console.log('Share results pressed');
  };

  const handleViewInAudit = () => {
    if (navigation) {
      navigation.navigate('AIAudit');
    } else {
      console.log('View in AI Audit pressed');
    }
  };

  const handleRunAgain = async () => {
    try {
      // Run simulation with current parameters
      await runRiskSimulation({
        scenarioId: selectedScenario?.id || scenarios[0]?.id,
        // Add other simulation parameters as needed
      });
      Alert.alert('Success', 'Risk simulation started successfully');
    } catch (err) {
      Alert.alert('Error', 'Failed to start risk simulation');
    }
  };

  const handleNewSimulation = () => {
    // Reset selection
    setSelectedSimulation(null);
    setSelectedScenario(null);
    console.log('New simulation pressed');
  };

  // Show loading indicator while fetching initial data
  if (loading && !refreshing) {
    return (
      <View style={styles.container}>
        <StatusBar barStyle="light-content" backgroundColor={COLORS.primary} />
        <View style={styles.centerContent}>
          <ActivityIndicator size="large" color={COLORS.primary} />
          <Text style={styles.loadingText}>Loading risk simulations...</Text>
        </View>
      </View>
    );
  }

  // Show error state
  if (error) {
    return (
      <View style={styles.container}>
        <StatusBar barStyle="light-content" backgroundColor={COLORS.primary} />
        <View style={styles.centerContent}>
          <Ionicons name="warning" size={48} color={COLORS.error} />
          <Text style={styles.errorText}>Error loading risk data</Text>
          <Text style={styles.errorSubtext}>{error}</Text>
          <TouchableOpacity style={styles.retryButton} onPress={onRefresh}>
            <Text style={styles.retryButtonText}>Retry</Text>
          </TouchableOpacity>
        </View>
      </View>
    );
  }

  return (
    // Removed SafeAreaView wrapper since it's handled by AppLayout
    <View style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor={COLORS.primary} />

      <ScrollView 
        style={styles.content}
        showsVerticalScrollIndicator={false}
        contentContainerStyle={styles.scrollContent}
        refreshControl={
          // Note: In a real implementation, we would use RefreshControl here
          undefined
        }
      >
        {/* Progress Indicator */}
        <ProgressIndicator currentStep={currentStep} />

        {/* Model and Scenario Setup */}
        <View style={styles.setupSection}>
          <ModelSelectionCard onChangeModel={handleChangeModel} />
          <ScenarioCard 
            scenarios={scenarios} 
            selectedScenario={selectedScenario}
            onChangeScenario={handleChangeScenario} 
          />
        </View>

        {/* Results Section */}
        <View style={styles.resultsSection}>
          {selectedSimulation ? (
            <>
              <ResultsOverview 
                complianceScore={selectedSimulation.complianceScore || 87}
                flaggedItems={selectedSimulation.flaggedItems || 23}
                riskLevel={selectedSimulation.riskLevel || "low"}
                additionalMetrics={[
                  { 
                    icon: 'speedometer', 
                    value: selectedSimulation.accuracy ? `${selectedSimulation.accuracy}%` : '94.2%', 
                    label: 'Accuracy', 
                    color: COLORS.success 
                  },
                  { 
                    icon: 'shield', 
                    value: selectedSimulation.biasScore || '0.12', 
                    label: 'Bias Score', 
                    color: COLORS.info 
                  },
                  { 
                    icon: 'trending-up', 
                    value: selectedSimulation.predictions || '1.2M', 
                    label: 'Predictions', 
                    color: COLORS.primary 
                  },
                ]}
              />

              <RiskImpactChart 
                timeframe={timeframe}
                onTimeframeChange={handleTimeframeChange}
                data={selectedSimulation.riskData || []}
              />

              <InsightsRecommendations 
                onInsightPress={handleInsightPress} 
                insights={selectedSimulation.insights || []}
              />
            </>
          ) : (
            <View style={styles.emptyState}>
              <Ionicons name="flask-outline" size={48} color={COLORS.gray400} />
              <Text style={styles.emptyStateTitle}>No Simulation Selected</Text>
              <Text style={styles.emptyStateText}>
                Select a scenario and run a simulation to view results
              </Text>
            </View>
          )}
        </View>

        {/* Action Buttons */}
        <ActionButtons
          onDownloadReport={handleDownloadReport}
          onShareResults={handleShareResults}
          onViewInAudit={handleViewInAudit}
          onRunAgain={handleRunAgain}
          onNewSimulation={handleNewSimulation}
        />

        {/* Bottom Spacing */}
        <View style={styles.bottomSpacing} />
      </ScrollView>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
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
  content: {
    flex: 1,
  },
  scrollContent: {
    paddingBottom: SPACING.lg,
  },
  setupSection: {
    paddingHorizontal: SPACING.md,
    paddingVertical: SPACING.md,
  },
  resultsSection: {
    paddingHorizontal: SPACING.md,
  },
  emptyState: {
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: SPACING['3xl'],
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
  bottomSpacing: {
    height: SPACING.xl,
  },
});

export default AIRiskSimulationScreen;