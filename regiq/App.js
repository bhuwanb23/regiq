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

  const renderActiveScreen = () => {
    switch (activeTab) {
      case 'Dashboard':
        return <DashboardScreen />;
      case 'Regulations':
        return <RegulationIntelligenceScreen />;
      case 'AI Audit':
        return <AIAuditScreen />;
      case 'Simulation':
        return <AIRiskSimulationScreen />;
      case 'Reports':
        return <ReportsScreen />;
      default:
        return <DashboardScreen />;
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
