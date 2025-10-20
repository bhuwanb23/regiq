import React, { useState } from 'react';
import {
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  StyleSheet,
  StatusBar,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
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

const AIRiskSimulationScreen = ({ navigation = null }) => {
  const [currentStep] = useState(4);
  const [timeframe, setTimeframe] = useState('7D');


  const handleChangeModel = () => {
    // Handle model change
    console.log('Change model pressed');
  };

  const handleChangeScenario = () => {
    // Handle scenario change
    console.log('Change scenario pressed');
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

  const handleRunAgain = () => {
    console.log('Run again pressed');
  };

  const handleNewSimulation = () => {
    console.log('New simulation pressed');
  };

  return (
    <SafeAreaView style={styles.container} edges={['top', 'left', 'right']}>
      <StatusBar barStyle="light-content" backgroundColor={COLORS.primary} />

      <ScrollView 
        style={styles.content}
        showsVerticalScrollIndicator={false}
        contentContainerStyle={styles.scrollContent}
      >
        {/* Progress Indicator */}
        <ProgressIndicator currentStep={currentStep} />

        {/* Model and Scenario Setup */}
        <View style={styles.setupSection}>
          <ModelSelectionCard onChangeModel={handleChangeModel} />
          <ScenarioCard onChangeScenario={handleChangeScenario} />
        </View>

        {/* Results Section */}
        <View style={styles.resultsSection}>
          <ResultsOverview 
            complianceScore={87}
            flaggedItems={23}
            riskLevel="low"
            additionalMetrics={[
              { icon: 'speedometer', value: '94.2%', label: 'Accuracy', color: COLORS.success },
              { icon: 'shield', value: '0.12', label: 'Bias Score', color: COLORS.info },
              { icon: 'trending-up', value: '1.2M', label: 'Predictions', color: COLORS.primary },
            ]}
          />

          <RiskImpactChart 
            timeframe={timeframe}
            onTimeframeChange={handleTimeframeChange}
          />

          <InsightsRecommendations onInsightPress={handleInsightPress} />
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
  bottomSpacing: {
    height: SPACING.xl,
  },
});

export default AIRiskSimulationScreen;
