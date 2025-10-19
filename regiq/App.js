import React, { useState } from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { StatusBar } from 'expo-status-bar';
import AppLayout from './src/components/navigation/AppLayout';

// Import screens
import LandingScreen from './src/screens/landing/LandingScreen';
import DashboardScreen from './src/screens/dashboard/DashboardScreen';
import RegulationIntelligenceScreen from './src/screens/regulations/RegulationIntelligenceScreen';
import ModelAuditScreen from './src/screens/ai-audit/ModelAuditScreen';
import SimulationScreen from './src/screens/simulation/SimulationScreen';
import ReportsScreen from './src/screens/reports/ReportsScreen';

export default function App() {
  const [showLanding, setShowLanding] = useState(true);
  const [activeTab, setActiveTab] = useState('Dashboard');
  const [notificationCount] = useState(5); // Mock notification count

  const handleLandingFinish = () => {
    setShowLanding(false);
  };

  const handleTabPress = (tabName) => {
    setActiveTab(tabName);
  };

  const handleNotificationPress = () => {
    console.log('Notifications pressed');
    // Navigate to notifications screen
  };

  const handleSettingsPress = () => {
    console.log('Settings pressed');
    // Navigate to settings screen
  };

  const renderActiveScreen = () => {
    switch (activeTab) {
      case 'Dashboard':
        return <DashboardScreen />;
      case 'Regulations':
        return <RegulationIntelligenceScreen />;
      case 'AI Audit':
        return <ModelAuditScreen />;
      case 'Simulation':
        return <SimulationScreen />;
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
