import React from 'react';
import {
  View,
  Text,
  ScrollView,
  StyleSheet,
  TouchableOpacity,
  StatusBar,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { SafeAreaView } from 'react-native-safe-area-context';

import ComplianceGauge from '../../components/common/ComplianceGauge';
import ActionButton from '../../components/common/ActionButton';
import { COLORS, TYPOGRAPHY, SPACING, BORDER_RADIUS, SHADOWS } from '../../constants/theme';

const DashboardScreen = ({ navigation }) => {
  // Mock data - will be replaced with real data from API
  const complianceScore = 78;
  const alerts = [
    {
      id: 1,
      type: 'warning',
      title: 'New RBI Digital Lending Guidelines',
      description: 'Review required for KYC API compliance',
      priority: 'high',
      timestamp: '2 hours ago',
    },
    {
      id: 2,
      type: 'error',
      title: 'AI Model Bias Detected',
      description: 'Credit scoring model shows 6.7% gender bias',
      priority: 'critical',
      timestamp: '4 hours ago',
    },
    {
      id: 3,
      type: 'info',
      title: 'EU AI Act Update',
      description: 'New transparency requirements effective Jan 2025',
      priority: 'medium',
      timestamp: '1 day ago',
    },
  ];

  const quickStats = [
    { label: 'Active Models', value: '12', icon: 'analytics-outline', color: COLORS.primary },
    { label: 'Pending Tasks', value: '5', icon: 'checkmark-circle-outline', color: COLORS.warning },
    { label: 'Reports Generated', value: '23', icon: 'document-text-outline', color: COLORS.success },
    { label: 'Risk Score', value: 'Low', icon: 'shield-checkmark-outline', color: COLORS.secondary },
  ];

  const getAlertIcon = (type) => {
    switch (type) {
      case 'error':
        return 'alert-circle';
      case 'warning':
        return 'warning';
      case 'info':
        return 'information-circle';
      default:
        return 'notifications';
    }
  };

  const getAlertColor = (priority) => {
    switch (priority) {
      case 'critical':
        return COLORS.error;
      case 'high':
        return COLORS.warning;
      case 'medium':
        return COLORS.info;
      default:
        return COLORS.gray500;
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor={COLORS.primary} />
      
      <ScrollView style={styles.scrollView} showsVerticalScrollIndicator={false}>
        {/* Header */}
        <View style={styles.header}>
          <View>
            <Text style={styles.welcomeText}>Welcome back!</Text>
            <Text style={styles.companyText}>FinTech Solutions Inc.</Text>
          </View>
          <TouchableOpacity 
            style={styles.alertButton}
            onPress={() => navigation.navigate('Alerts')}
          >
            <Ionicons name="notifications-outline" size={24} color={COLORS.white} />
            {alerts.length > 0 && <View style={styles.alertBadge} />}
          </TouchableOpacity>
        </View>

        {/* Compliance Health Score */}
        <View style={styles.complianceSection}>
          <ComplianceGauge score={complianceScore} />
        </View>

        {/* Quick Stats */}
        <View style={styles.statsSection}>
          <Text style={styles.sectionTitle}>Quick Overview</Text>
          <View style={styles.statsGrid}>
            {quickStats.map((stat, index) => (
              <View key={index} style={styles.statCard}>
                <View style={[styles.statIcon, { backgroundColor: `${stat.color}20` }]}>
                  <Ionicons name={stat.icon} size={24} color={stat.color} />
                </View>
                <Text style={styles.statValue}>{stat.value}</Text>
                <Text style={styles.statLabel}>{stat.label}</Text>
              </View>
            ))}
          </View>
        </View>

        {/* Recent Alerts */}
        <View style={styles.alertsSection}>
          <View style={styles.sectionHeader}>
            <Text style={styles.sectionTitle}>Recent Alerts</Text>
            <TouchableOpacity onPress={() => navigation.navigate('Alerts')}>
              <Text style={styles.viewAllText}>View All</Text>
            </TouchableOpacity>
          </View>
          
          {alerts.slice(0, 3).map((alert) => (
            <TouchableOpacity key={alert.id} style={styles.alertCard}>
              <View style={styles.alertContent}>
                <View style={styles.alertHeader}>
                  <Ionicons 
                    name={getAlertIcon(alert.type)} 
                    size={20} 
                    color={getAlertColor(alert.priority)} 
                  />
                  <Text style={styles.alertTitle}>{alert.title}</Text>
                </View>
                <Text style={styles.alertDescription}>{alert.description}</Text>
                <Text style={styles.alertTimestamp}>{alert.timestamp}</Text>
              </View>
              <Ionicons name="chevron-forward" size={20} color={COLORS.gray400} />
            </TouchableOpacity>
          ))}
        </View>

        {/* Quick Actions */}
        <View style={styles.actionsSection}>
          <Text style={styles.sectionTitle}>Quick Actions</Text>
          <View style={styles.actionButtons}>
            <ActionButton
              title="Scan AI Model"
              icon="analytics-outline"
              onPress={() => navigation.navigate('AI Audit')}
              style={styles.actionButton}
            />
            <ActionButton
              title="Run Simulation"
              icon="flask-outline"
              variant="secondary"
              onPress={() => navigation.navigate('Simulation')}
              style={styles.actionButton}
            />
          </View>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  scrollView: {
    flex: 1,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    backgroundColor: COLORS.primary,
    paddingHorizontal: SPACING.md,
    paddingVertical: SPACING.lg,
  },
  welcomeText: {
    fontSize: TYPOGRAPHY.fontSize.lg,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.white,
  },
  companyText: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    color: COLORS.white,
    opacity: 0.8,
    marginTop: 2,
  },
  alertButton: {
    position: 'relative',
    padding: SPACING.xs,
  },
  alertBadge: {
    position: 'absolute',
    top: 4,
    right: 4,
    width: 8,
    height: 8,
    backgroundColor: COLORS.error,
    borderRadius: 4,
  },
  complianceSection: {
    backgroundColor: COLORS.white,
    paddingVertical: SPACING.xl,
    alignItems: 'center',
    marginBottom: SPACING.md,
  },
  statsSection: {
    backgroundColor: COLORS.white,
    padding: SPACING.md,
    marginBottom: SPACING.md,
  },
  sectionTitle: {
    fontSize: TYPOGRAPHY.fontSize.lg,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.textPrimary,
    marginBottom: SPACING.md,
  },
  statsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  statCard: {
    width: '48%',
    backgroundColor: COLORS.surfaceSecondary,
    padding: SPACING.md,
    borderRadius: BORDER_RADIUS.md,
    alignItems: 'center',
    marginBottom: SPACING.sm,
  },
  statIcon: {
    width: 48,
    height: 48,
    borderRadius: 24,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: SPACING.sm,
  },
  statValue: {
    fontSize: TYPOGRAPHY.fontSize['2xl'],
    fontWeight: TYPOGRAPHY.fontWeight.bold,
    color: COLORS.textPrimary,
  },
  statLabel: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    color: COLORS.textSecondary,
    textAlign: 'center',
    marginTop: 2,
  },
  alertsSection: {
    backgroundColor: COLORS.white,
    padding: SPACING.md,
    marginBottom: SPACING.md,
  },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: SPACING.md,
  },
  viewAllText: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    color: COLORS.primary,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
  },
  alertCard: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: SPACING.sm,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.gray200,
  },
  alertContent: {
    flex: 1,
  },
  alertHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 4,
  },
  alertTitle: {
    fontSize: TYPOGRAPHY.fontSize.base,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
    color: COLORS.textPrimary,
    marginLeft: SPACING.xs,
    flex: 1,
  },
  alertDescription: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    color: COLORS.textSecondary,
    marginBottom: 4,
  },
  alertTimestamp: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.textTertiary,
  },
  actionsSection: {
    backgroundColor: COLORS.white,
    padding: SPACING.md,
    marginBottom: SPACING.md,
  },
  actionButtons: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  actionButton: {
    flex: 1,
    marginHorizontal: SPACING.xs,
  },
});

export default DashboardScreen;
