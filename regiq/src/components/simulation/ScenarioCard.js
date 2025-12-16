import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet, FlatList, Modal } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { COLORS, TYPOGRAPHY, SPACING, BORDER_RADIUS, SHADOWS } from '../../constants/theme';

const ScenarioCard = ({ 
  scenarios = [],
  selectedScenario = null,
  onChangeScenario 
}) => {
  const [modalVisible, setModalVisible] = React.useState(false);

  const getRiskColor = (riskLevel) => {
    switch (riskLevel?.toLowerCase()) {
      case 'low': return COLORS.success;
      case 'medium': return COLORS.warning;
      case 'high': return COLORS.error;
      default: return COLORS.warning;
    }
  };

  const getRiskBackground = (riskLevel) => {
    switch (riskLevel?.toLowerCase()) {
      case 'low': return `${COLORS.success}15`;
      case 'medium': return `${COLORS.warning}15`;
      case 'high': return `${COLORS.error}15`;
      default: return `${COLORS.warning}15`;
    }
  };

  const getRiskIcon = (riskLevel) => {
    switch (riskLevel?.toLowerCase()) {
      case 'low': return 'checkmark-circle';
      case 'medium': return 'warning';
      case 'high': return 'alert-circle';
      default: return 'warning';
    }
  };

  const handleScenarioSelect = (scenario) => {
    onChangeScenario(scenario);
    setModalVisible(false);
  };

  const renderScenarioOption = ({ item: scenario }) => (
    <TouchableOpacity 
      style={styles.scenarioOption}
      onPress={() => handleScenarioSelect(scenario)}
    >
      <View style={styles.optionHeader}>
        <Ionicons 
          name={getRiskIcon(scenario.scenarioType || 'warning')} 
          size={16} 
          color={getRiskColor(scenario.scenarioType)} 
          style={styles.optionIcon}
        />
        <View style={styles.optionInfo}>
          <Text style={styles.optionTitle}>{scenario.name}</Text>
          <Text style={styles.optionDescription} numberOfLines={2}>
            {scenario.description}
          </Text>
        </View>
      </View>
      <View style={[styles.optionRiskBadge, { backgroundColor: getRiskColor(scenario.scenarioType) }]}>
        <Text style={styles.optionRiskText}>
          {scenario.scenarioType ? scenario.scenarioType.charAt(0).toUpperCase() + scenario.scenarioType.slice(1) : 'Medium'} Risk
        </Text>
      </View>
    </TouchableOpacity>
  );

  const currentScenario = selectedScenario || scenarios[0] || {
    name: 'Select Scenario',
    description: 'Choose a risk scenario to simulate',
    scenarioType: 'medium'
  };

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.title}>Risk Scenario</Text>
        <TouchableOpacity 
          onPress={() => setModalVisible(true)} 
          style={styles.changeButton}
        >
          <Text style={styles.changeButtonText}>Change</Text>
        </TouchableOpacity>
      </View>

      {/* Scenario Content */}
      <View style={[styles.scenarioContainer, { backgroundColor: getRiskBackground(currentScenario.scenarioType) }]}>
        <View style={styles.scenarioContent}>
          <View style={styles.scenarioHeader}>
            <Ionicons 
              name={getRiskIcon(currentScenario.scenarioType)} 
              size={18} 
              color={getRiskColor(currentScenario.scenarioType)} 
              style={styles.scenarioIcon}
            />
            <View style={styles.scenarioInfo}>
              <Text style={[styles.scenarioTitle, { color: getRiskColor(currentScenario.scenarioType) }]}>
                {currentScenario.name}
              </Text>
              <Text style={[styles.scenarioDescription, { color: getRiskColor(currentScenario.scenarioType) }]} numberOfLines={2}>
                {currentScenario.description}
              </Text>
            </View>
          </View>

          {/* Risk Level Badge */}
          <View style={[styles.riskBadge, { backgroundColor: getRiskColor(currentScenario.scenarioType) }]}>
            <Text style={styles.riskBadgeText}>
              {currentScenario.scenarioType ? currentScenario.scenarioType.charAt(0).toUpperCase() + currentScenario.scenarioType.slice(1) : 'Medium'} Risk
            </Text>
          </View>
        </View>

        {/* Scenario Details */}
        <View style={styles.detailsContainer}>
          <View style={styles.detailItem}>
            <Ionicons name="calendar" size={14} color={getRiskColor(currentScenario.scenarioType)} />
            <Text style={[styles.detailText, { color: getRiskColor(currentScenario.scenarioType) }]}>
              {currentScenario.effectiveDate || 'Effective Date N/A'}
            </Text>
          </View>
          
          <View style={styles.detailItem}>
            <Ionicons name="globe" size={14} color={getRiskColor(currentScenario.scenarioType)} />
            <Text style={[styles.detailText, { color: getRiskColor(currentScenario.scenarioType) }]}>
              {currentScenario.region || 'Global'}
            </Text>
          </View>
          
          <View style={styles.detailItem}>
            <Ionicons name="shield-checkmark" size={14} color={getRiskColor(currentScenario.scenarioType)} />
            <Text style={[styles.detailText, { color: getRiskColor(currentScenario.scenarioType) }]}>
              {currentScenario.systemType || 'AI Systems'}
            </Text>
          </View>
        </View>
      </View>

      {/* Impact Summary */}
      <View style={styles.impactContainer}>
        <Text style={styles.impactTitle}>Expected Impact</Text>
        <View style={styles.impactItems}>
          <View style={styles.impactItem}>
            <View style={styles.impactDot} />
            <Text style={styles.impactText}>{currentScenario.impact1 || 'Potential regulatory compliance changes'}</Text>
          </View>
          <View style={styles.impactItem}>
            <View style={styles.impactDot} />
            <Text style={styles.impactText}>{currentScenario.impact2 || 'Updated model validation requirements'}</Text>
          </View>
          <View style={styles.impactItem}>
            <View style={styles.impactDot} />
            <Text style={styles.impactText}>{currentScenario.impact3 || 'Enhanced documentation standards'}</Text>
          </View>
        </View>
      </View>

      {/* Scenario Selection Modal */}
      <Modal
        animationType="slide"
        transparent={true}
        visible={modalVisible}
        onRequestClose={() => setModalVisible(false)}
      >
        <View style={styles.modalContainer}>
          <View style={styles.modalContent}>
            <View style={styles.modalHeader}>
              <Text style={styles.modalTitle}>Select Risk Scenario</Text>
              <TouchableOpacity onPress={() => setModalVisible(false)}>
                <Ionicons name="close" size={24} color={COLORS.textSecondary} />
              </TouchableOpacity>
            </View>
            
            <FlatList
              data={scenarios}
              renderItem={renderScenarioOption}
              keyExtractor={(item) => item.id}
              style={styles.scenarioList}
              showsVerticalScrollIndicator={false}
            />
          </View>
        </View>
      </Modal>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: COLORS.white,
    borderRadius: BORDER_RADIUS.lg,
    padding: SPACING.md,
    borderWidth: 1,
    borderColor: COLORS.gray200,
    marginBottom: SPACING.md,
    ...SHADOWS.sm,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: SPACING.md,
  },
  title: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.primary,
  },
  changeButton: {
    paddingHorizontal: SPACING.sm,
    paddingVertical: SPACING.xs,
  },
  changeButtonText: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
    color: COLORS.secondary,
  },
  scenarioContainer: {
    borderRadius: BORDER_RADIUS.lg,
    padding: SPACING.md,
    marginBottom: SPACING.md,
    borderWidth: 1,
    borderColor: COLORS.warning,
  },
  scenarioContent: {
    marginBottom: SPACING.sm,
  },
  scenarioHeader: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    marginBottom: SPACING.sm,
  },
  scenarioIcon: {
    marginTop: 2,
    marginRight: SPACING.sm,
  },
  scenarioInfo: {
    flex: 1,
  },
  scenarioTitle: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    marginBottom: SPACING.xs,
  },
  scenarioDescription: {
    fontSize: TYPOGRAPHY.fontSize.xs,
  },
  riskBadge: {
    alignSelf: 'flex-start',
    paddingHorizontal: SPACING.sm,
    paddingVertical: SPACING.xs,
    borderRadius: BORDER_RADIUS.full,
  },
  riskBadgeText: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.white,
  },
  detailsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginTop: SPACING.sm,
  },
  detailItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginRight: SPACING.md,
    marginBottom: SPACING.xs,
  },
  detailText: {
    fontSize: 9,
    marginLeft: SPACING.xs,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
  },
  impactContainer: {
    backgroundColor: COLORS.surfaceSecondary,
    borderRadius: BORDER_RADIUS.md,
    padding: SPACING.sm,
  },
  impactTitle: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.textPrimary,
    marginBottom: SPACING.sm,
  },
  impactItems: {
    gap: SPACING.xs,
  },
  impactItem: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  impactDot: {
    width: 4,
    height: 4,
    borderRadius: 2,
    backgroundColor: COLORS.primary,
    marginRight: SPACING.sm,
  },
  impactText: {
    fontSize: 9,
    color: COLORS.textSecondary,
    flex: 1,
  },
  modalContainer: {
    flex: 1,
    justifyContent: 'flex-end',
    backgroundColor: 'rgba(0,0,0,0.5)',
  },
  modalContent: {
    backgroundColor: COLORS.white,
    borderTopLeftRadius: BORDER_RADIUS.xl,
    borderTopRightRadius: BORDER_RADIUS.xl,
    maxHeight: '70%',
  },
  modalHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: SPACING.md,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.gray200,
  },
  modalTitle: {
    fontSize: TYPOGRAPHY.fontSize.base,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.textPrimary,
  },
  scenarioList: {
    padding: SPACING.sm,
  },
  scenarioOption: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: SPACING.md,
    backgroundColor: COLORS.surfaceSecondary,
    borderRadius: BORDER_RADIUS.md,
    marginBottom: SPACING.sm,
  },
  optionHeader: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    flex: 1,
  },
  optionIcon: {
    marginTop: 2,
    marginRight: SPACING.sm,
  },
  optionInfo: {
    flex: 1,
  },
  optionTitle: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.textPrimary,
    marginBottom: SPACING.xs,
  },
  optionDescription: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.textSecondary,
  },
  optionRiskBadge: {
    paddingHorizontal: SPACING.sm,
    paddingVertical: SPACING.xs,
    borderRadius: BORDER_RADIUS.full,
  },
  optionRiskText: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.white,
  },
});

export default ScenarioCard;