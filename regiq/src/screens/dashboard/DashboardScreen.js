import React from 'react';
import {
  View,
  Text,
  ScrollView,
  StyleSheet,
  TouchableOpacity,
  RefreshControl,
  StatusBar,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';

import ComplianceGauge from '../../components/common/ComplianceGauge';
import ActionButton from '../../components/common/ActionButton';
import StatCard from '../../components/dashboard/StatCard';
import ComplianceMetrics from '../../components/dashboard/ComplianceMetrics';
import RecentActivity from '../../components/dashboard/RecentActivity';
import QuickActions from '../../components/dashboard/QuickActions';
import useDashboardData from '../../hooks/useDashboardData';
import { COLORS, TYPOGRAPHY, SPACING, BORDER_RADIUS, SHADOWS } from '../../constants/theme';

const DashboardScreen = ({ navigation }) => {
  const {
    dashboardData,
    loading,
    refreshing,
    refreshDashboard,
    updateComplianceScore,
    markAlertAsRead,
    addActivity,
  } = useDashboardData();

  const {
    complianceScore,
    user,
    quickStats,
    alerts,
    recentActivity,
    complianceMetrics,
  } = dashboardData;

  const handleActionPress = (action) => {
    console.log('Action pressed:', action.id);
    if (action.route) {
      navigation.navigate(action.route);
    }
  };

  const handleActivityPress = (activity) => {
    console.log('Activity pressed:', activity.id);
    // Navigate to activity details or handle action
  };

  const handleAlertPress = (alert) => {
    console.log('Alert pressed:', alert.id);
    markAlertAsRead(alert.id);
    navigation.navigate('Alerts', { alertId: alert.id });
  };

  const handleGenerateReport = () => {
    console.log('Generate report pressed');
    navigation.navigate('Reports');
  };

  const handleViewComplianceDetails = () => {
    console.log('View compliance details pressed');
    navigation.navigate('Compliance');
  };

  const getAlertIcon = (type) => {
    switch (type) {
      case 'error':
        return 'alert-circle';
      case 'warning':
        return 'warning';
      case 'info':
        return 'information-circle';
      case 'success':
        return 'checkmark-circle';
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
      case 'low':
        return COLORS.success;
      default:
        return COLORS.gray500;
    }
  };

  if (loading) {
    return (
      <View style={[styles.container, styles.centerContent]}>
        <Text style={styles.loadingText}>Loading dashboard...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <ScrollView 
        style={styles.scrollView} 
        showsVerticalScrollIndicator={false}
        refreshControl={
          <RefreshControl
            refreshing={refreshing}
            onRefresh={refreshDashboard}
            colors={[COLORS.primary]}
            tintColor={COLORS.primary}
          />
        }
      >
        {/* Compliance Metrics */}
        <ComplianceMetrics
          complianceScore={complianceMetrics.overallScore}
          regulations={complianceMetrics.regulations}
          alerts={complianceMetrics.alerts}
          onViewDetails={handleViewComplianceDetails}
          onGenerateReport={handleGenerateReport}
        />

        {/* Quick Stats */}
        <View style={styles.statsSection}>
          <Text style={styles.sectionTitle}>Performance Overview</Text>
          <View style={styles.statsGrid}>
            {quickStats.map((stat, index) => (
              <StatCard
                key={stat.id}
                title={stat.title}
                value={stat.value}
                subtitle={stat.subtitle}
                icon={stat.icon}
                trend={stat.trend}
                trendValue={stat.trendValue}
                color={stat.color}
                variant={index === 0 ? 'gradient' : index === 1 ? 'minimal' : 'default'}
              />
            ))}
          </View>
        </View>

        {/* Recent Activity */}
        <RecentActivity
          activities={recentActivity}
          onViewAll={() => navigation.navigate('Activity')}
          onActivityPress={handleActivityPress}
        />

        {/* Recent Alerts */}
        <View style={styles.alertsSection}>
          <View style={styles.sectionHeader}>
            <Text style={styles.sectionTitle}>Priority Alerts</Text>
            <TouchableOpacity onPress={() => navigation.navigate('Alerts')}>
              <Text style={styles.viewAllText}>View All</Text>
            </TouchableOpacity>
          </View>
          
          {alerts.slice(0, 3).map((alert) => (
            <TouchableOpacity 
              key={alert.id} 
              style={styles.alertCard}
              onPress={() => handleAlertPress(alert)}
            >
              <View style={styles.alertContent}>
                <View style={styles.alertHeader}>
                  <View style={[
                    styles.alertIconContainer,
                    { backgroundColor: `${getAlertColor(alert.priority)}20` }
                  ]}>
                    <Ionicons 
                      name={getAlertIcon(alert.type)} 
                      size={16} 
                      color={getAlertColor(alert.priority)} 
                    />
                  </View>
                  <Text style={styles.alertTitle}>{alert.title}</Text>
                  {alert.actionRequired && (
                    <View style={styles.actionRequiredBadge}>
                      <Text style={styles.actionRequiredText}>Action</Text>
                    </View>
                  )}
                </View>
                <Text style={styles.alertDescription}>{alert.description}</Text>
                <View style={styles.alertFooter}>
                  <Text style={styles.alertTimestamp}>{alert.timestamp}</Text>
                  <Text style={[styles.alertCategory, { color: getAlertColor(alert.priority) }]}>
                    {alert.category?.replace('_', ' ').toUpperCase()}
                  </Text>
                </View>
              </View>
              <Ionicons name="chevron-forward" size={16} color={COLORS.gray400} />
            </TouchableOpacity>
          ))}
        </View>

        {/* Quick Actions */}
        <QuickActions onActionPress={handleActionPress} />
        
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
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    fontSize: TYPOGRAPHY.fontSize.base,
    color: COLORS.textSecondary,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
  },
  scrollView: {
    flex: 1,
    paddingHorizontal: SPACING.md,
    paddingTop: SPACING.sm,
  },
  statsSection: {
    marginBottom: SPACING.md,
  },
  sectionTitle: {
    fontSize: TYPOGRAPHY.fontSize.base,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.textPrimary,
    marginBottom: SPACING.sm,
    paddingHorizontal: SPACING.xs,
  },
  statsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginHorizontal: -SPACING.xs,
  },
  alertsSection: {
    backgroundColor: COLORS.white,
    borderRadius: BORDER_RADIUS.lg,
    padding: SPACING.md,
    marginBottom: SPACING.md,
    ...SHADOWS.sm,
  },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: SPACING.md,
  },
  viewAllText: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.primary,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
  },
  alertCard: {
    flexDirection: 'row',
    alignItems: 'flex-start',
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
    marginBottom: SPACING.xs,
  },
  alertIconContainer: {
    width: 24,
    height: 24,
    borderRadius: 12,
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: SPACING.sm,
  },
  alertTitle: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
    color: COLORS.textPrimary,
    flex: 1,
  },
  actionRequiredBadge: {
    backgroundColor: COLORS.error,
    paddingHorizontal: SPACING.xs,
    paddingVertical: 2,
    borderRadius: BORDER_RADIUS.sm,
  },
  actionRequiredText: {
    fontSize: 9,
    color: COLORS.white,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
  },
  alertDescription: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.textSecondary,
    lineHeight: 16,
    marginBottom: SPACING.xs,
  },
  alertFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  alertTimestamp: {
    fontSize: 10,
    color: COLORS.textTertiary,
  },
  alertCategory: {
    fontSize: 10,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
  },
  bottomSpacing: {
    height: SPACING.xl,
  },
});

export default DashboardScreen;
