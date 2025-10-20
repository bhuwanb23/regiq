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
        colors={['#8B5CF6', '#7C3AED']}
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
                    color={isActive ? '#8B5CF6' : '#FFFFFF'}
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
    backgroundColor: '#8B5CF6',
  },
  navbarContainer: {
    borderTopWidth: 0,
    paddingTop: 8,
    paddingBottom: 8,
    paddingHorizontal: 8,
    elevation: 8,
    shadowColor: '#8B5CF6',
    shadowOffset: {
      width: 0,
      height: -4,
    },
    shadowOpacity: 0.3,
    shadowRadius: 8,
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
    backgroundColor: '#FFFFFF',
    borderRadius: 19,
    shadowColor: '#000000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.15,
    shadowRadius: 4,
    elevation: 4,
  },
  bottomSafeArea: {
    backgroundColor: '#8B5CF6',
  },
});

export default AppNavbar;
