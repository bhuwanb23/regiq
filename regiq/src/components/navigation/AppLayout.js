import React from 'react';
import {
  View,
  StyleSheet,
} from 'react-native';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import AppHeader from './AppHeader';
import AppNavbar from './AppNavbar';

const AppLayout = ({ 
  children,
  headerTitle = "REGIQ",
  showBackButton = false,
  onBackPress,
  showNotifications = true,
  notificationCount = 0,
  onNotificationPress,
  showSettings = true,
  onSettingsPress,
  activeTab = 'Dashboard',
  onTabPress,
  showNavbar = true,
}) => {
  return (
    <SafeAreaProvider>
      <View style={styles.container}>
        <AppHeader
          title={headerTitle}
          showBackButton={showBackButton}
          onBackPress={onBackPress}
          showNotifications={showNotifications}
          notificationCount={notificationCount}
          onNotificationPress={onNotificationPress}
          showSettings={showSettings}
          onSettingsPress={onSettingsPress}
        />
        
        <View style={styles.content}>
          {children}
        </View>
        
        {showNavbar && (
          <AppNavbar
            activeTab={activeTab}
            onTabPress={onTabPress}
          />
        )}
      </View>
    </SafeAreaProvider>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F9FAFB',
  },
  content: {
    flex: 1,
    backgroundColor: '#F9FAFB',
  },
});

export default AppLayout;
