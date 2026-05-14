import React, { useState } from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { StatusBar } from 'expo-status-bar';
import AppLayout from './src/components/navigation/AppLayout';

// Import screens
import LandingScreen from './src/screens/landing/LandingScreen';
import DashboardScreen from './src/screens/dashboard/DashboardScreen';
import RegulationIntelligenceScreen from './src/screens/regulations/RegulationIntelligenceScreen';
import AIAuditScreen from './src/screens/ai-audit/AIAuditScreen';
import AIRiskSimulationScreen from './src/screens/simulation/AIRiskSimulationScreen';
import ReportsScreen from './src/screens/reports/ReportsScreen';
import AlertsScreen from './src/screens/alerts/AlertsScreen';
import ProfileScreen from './src/screens/profile/ProfileScreen';

// Map known route names from screens to internal tab/state targets.
// Any route not in this list falls back to a Dashboard navigation no-op so
// stray `navigation.navigate('Foo')` calls do not crash the app.
const TAB_ROUTES = new Set([
  'Dashboard',
  'Regulations',
  'AI Audit',
  'Simulation',
  'Reports',
]);

const ROUTE_ALIASES = {
  Compliance: 'Reports',
  Activity: 'Dashboard',
  AIAudit: 'AI Audit',
};

export default function App() {
  const [showLanding, setShowLanding] = useState(true);
  const [activeTab, setActiveTab] = useState('Dashboard');
  const [showProfile, setShowProfile] = useState(false);
  const [showAlerts, setShowAlerts] = useState(false);
  const [notificationCount] = useState(5); // Mock notification count

  const handleLandingFinish = () => {
    setShowLanding(false);
  };

  const handleTabPress = (tabName) => {
    setActiveTab(tabName);
  };

  const handleNotificationPress = () => {
    setShowAlerts(true);
  };

  const handleSettingsPress = () => {
    setShowProfile(true);
  };

  const handleProfileBack = () => {
    setShowProfile(false);
  };

  const handleAlertsBack = () => {
    setShowAlerts(false);
  };

  // Synthetic navigation object passed to every active screen.
  // Bridges react-navigation-style `navigation.navigate(...)` calls into the
  // tab/modal state we manage manually in App.js.
  const navigation = {
    navigate: (routeName, params) => {
      if (routeName === 'Alerts') {
        setShowAlerts(true);
        return;
      }
      if (routeName === 'Profile' || routeName === 'Settings') {
        setShowProfile(true);
        return;
      }
      const target = ROUTE_ALIASES[routeName] || routeName;
      if (TAB_ROUTES.has(target)) {
        setActiveTab(target);
      } else if (__DEV__) {
        console.warn(`navigation.navigate: unknown route "${routeName}" - ignored`);
      }
    },
    goBack: () => {
      if (showAlerts) setShowAlerts(false);
      else if (showProfile) setShowProfile(false);
    },
  };

  const renderActiveScreen = () => {
    switch (activeTab) {
      case 'Dashboard':
        return <DashboardScreen navigation={navigation} />;
      case 'Regulations':
        return <RegulationIntelligenceScreen navigation={navigation} />;
      case 'AI Audit':
        return <AIAuditScreen navigation={navigation} />;
      case 'Simulation':
        return <AIRiskSimulationScreen navigation={navigation} />;
      case 'Reports':
        return <ReportsScreen navigation={navigation} />;
      default:
        return <DashboardScreen navigation={navigation} />;
    }
  };

  // Show landing screen first
  if (showLanding) {
    return (
      <>
        <StatusBar style="light" />
        <LandingScreen onFinish={handleLandingFinish} />
      </>
    );
  }

  // Show alerts screen
  if (showAlerts) {
    return (
      <>
        <StatusBar style="light" />
        <AlertsScreen navigation={{ goBack: handleAlertsBack }} />
      </>
    );
  }

  // Show profile screen
  if (showProfile) {
    return (
      <>
        <StatusBar style="dark" />
        <ProfileScreen navigation={{ goBack: handleProfileBack }} />
      </>
    );
  }

  // Show main app after landing
  return (
    <>
      <StatusBar style="light" />
      <AppLayout
        headerTitle="REGIQ"
        showNotifications={true}
        notificationCount={notificationCount}
        onNotificationPress={handleNotificationPress}
        showSettings={true}
        onSettingsPress={handleSettingsPress}
        activeTab={activeTab}
        onTabPress={handleTabPress}
        showNavbar={true}
      >
        {renderActiveScreen()}
      </AppLayout>
    </>
  );
}