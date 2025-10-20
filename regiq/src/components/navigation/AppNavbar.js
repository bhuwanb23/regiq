import React from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  Platform,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

const AppNavbar = ({ 
  activeTab = 'Dashboard',
  onTabPress,
  style 
}) => {
  const insets = useSafeAreaInsets();
  const tabs = [
    {
      name: 'Dashboard',
      icon: 'home',
      iconOutline: 'home-outline',
      label: 'Home',
    },
    {
      name: 'Regulations',
      icon: 'document-text',
      iconOutline: 'document-text-outline',
      label: 'Rules',
    },
    {
      name: 'AI Audit',
      icon: 'analytics',
      iconOutline: 'analytics-outline',
      label: 'Audit',
    },
    {
      name: 'Simulation',
      icon: 'flask',
      iconOutline: 'flask-outline',
      label: 'Test',
    },
    {
      name: 'Reports',
      icon: 'folder',
      iconOutline: 'folder-outline',
      label: 'Reports',
    },
  ];

  const handleTabPress = (tabName) => {
    if (onTabPress) {
      onTabPress(tabName);
    }
  };

  return (
    <View style={[styles.container, style]}>
      <LinearGradient
        colors={['#FFFFFF', '#F8FAFC']}
        style={styles.navbarContainer}
      >
        <View style={styles.tabsContainer}>
          {tabs.map((tab, index) => {
            const isActive = activeTab === tab.name;
            return (
              <TouchableOpacity
                key={tab.name}
                style={styles.tabButton}
                onPress={() => handleTabPress(tab.name)}
                activeOpacity={0.7}
              >
                <View style={[
                  styles.tabIconContainer,
                  isActive && styles.activeTabIconContainer
                ]}>
                  <Ionicons
                    name={isActive ? tab.icon : tab.iconOutline}
                    size={24}
                    color={isActive ? '#FFFFFF' : '#6B7280'}
                  />
                </View>
              </TouchableOpacity>
            );
          })}
        </View>
      </LinearGradient>
      
      {/* Bottom safe area for devices with home indicator */}
      <View style={[styles.bottomSafeArea, { height: insets.bottom }]} />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: '#FFFFFF',
  },
  navbarContainer: {
    borderTopWidth: 1,
    borderTopColor: '#E5E7EB',
    paddingTop: 8,
    paddingBottom: 6,
    paddingHorizontal: 8,
  },
  tabsContainer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    alignItems: 'center',
  },
  tabButton: {
    flex: 1,
    alignItems: 'center',
    paddingVertical: 4,
    paddingHorizontal: 4,
  },
  tabIconContainer: {
    alignItems: 'center',
    justifyContent: 'center',
    width: 38,
    height: 38,
    borderRadius: 19,
    overflow: 'hidden',
  },
  activeTabIconContainer: {
    backgroundColor: '#8B5CF6',
    borderRadius: 19,
    shadowColor: '#8B5CF6',
    shadowOffset: {
      width: 0,
      height: 4,
    },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 6,
  },
  bottomSafeArea: {
    backgroundColor: '#FFFFFF',
  },
});

export default AppNavbar;
