import React, { useEffect, useState } from 'react';
import { View, ActivityIndicator } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createStackNavigator } from '@react-navigation/stack';
import { Ionicons } from '@expo/vector-icons';

import DashboardScreen from '../screens/dashboard/DashboardScreen';
import RegulationIntelligenceScreen from '../screens/regulations/RegulationIntelligenceScreen';
import ModelAuditScreen from '../screens/ai-audit/ModelAuditScreen';
import SimulationScreen from '../screens/simulation/SimulationScreen';
import ReportsScreen from '../screens/reports/ReportsScreen';
import AlertsScreen from '../screens/alerts/AlertsScreen';
import SettingsScreen from '../screens/settings/SettingsScreen';

// Onboarding screens
import WelcomeScreen from '../screens/onboarding/WelcomeScreen';
import AuthScreen from '../screens/onboarding/AuthScreen';
import ProfileSetupScreen from '../screens/onboarding/ProfileSetupScreen';

import { getToken } from '../utils/storage';
import { COLORS } from '../constants/theme';

const Tab = createBottomTabNavigator();
const Stack = createStackNavigator();

// Main Tab Navigator
function MainTabNavigator() {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        tabBarIcon: ({ focused, color, size }) => {
          let iconName;

          switch (route.name) {
            case 'Dashboard':
              iconName = focused ? 'home' : 'home-outline';
              break;
            case 'Regulations':
              iconName = focused ? 'document-text' : 'document-text-outline';
              break;
            case 'AI Audit':
              iconName = focused ? 'analytics' : 'analytics-outline';
              break;
            case 'Simulation':
              iconName = focused ? 'flask' : 'flask-outline';
              break;
            case 'Reports':
              iconName = focused ? 'folder' : 'folder-outline';
              break;
          }

          return <Ionicons name={iconName} size={size} color={color} />;
        },
        tabBarActiveTintColor: COLORS.primary,
        tabBarInactiveTintColor: COLORS.gray400,
        tabBarStyle: {
          backgroundColor: COLORS.white,
          borderTopColor: COLORS.gray200,
          paddingBottom: 5,
          paddingTop: 5,
          height: 60,
        },
        headerStyle: {
          backgroundColor: COLORS.primary,
        },
        headerTintColor: COLORS.white,
        headerTitleStyle: {
          fontWeight: '600',
        },
      })}
    >
      <Tab.Screen 
        name="Dashboard" 
        component={DashboardScreen}
        options={{
          title: 'REGIQ Dashboard',
        }}
      />
      <Tab.Screen 
        name="Regulations" 
        component={RegulationIntelligenceScreen}
        options={{
          title: 'Regulation Feed',
        }}
      />
      <Tab.Screen 
        name="AI Audit" 
        component={ModelAuditScreen}
        options={{
          title: 'Model Audit',
        }}
      />
      <Tab.Screen 
        name="Simulation" 
        component={SimulationScreen}
        options={{
          title: 'Risk Simulation',
        }}
      />
      <Tab.Screen 
        name="Reports" 
        component={ReportsScreen}
        options={{
          title: 'Reports & Audit',
        }}
      />
    </Tab.Navigator>
  );
}

// Root Stack Navigator
export default function AppNavigator() {
  // Auth state is sourced from persisted token storage. Once a token is
  // present we treat the user as authenticated and route them into the main
  // app stack; otherwise we show the onboarding/auth flow.
  const [authReady, setAuthReady] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const token = await getToken();
        if (!cancelled) setIsAuthenticated(Boolean(token));
      } catch (err) {
        if (!cancelled) setIsAuthenticated(false);
      } finally {
        if (!cancelled) setAuthReady(true);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  if (!authReady) {
    return (
      <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: COLORS.background }}>
        <ActivityIndicator size="large" color={COLORS.primary} />
      </View>
    );
  }

  return (
    <NavigationContainer>
      <Stack.Navigator
        screenOptions={{
          headerShown: false,
        }}
      >
        {!isAuthenticated ? (
          // Auth Stack
          <>
            <Stack.Screen name="Welcome" component={WelcomeScreen} />
            <Stack.Screen name="Auth" component={AuthScreen} />
            <Stack.Screen name="ProfileSetup" component={ProfileSetupScreen} />
          </>
        ) : (
          // Main App Stack
          <>
            <Stack.Screen name="MainTabs" component={MainTabNavigator} />
            <Stack.Screen 
              name="Alerts" 
              component={AlertsScreen}
              options={{
                headerShown: true,
                title: 'Alerts & Notifications',
                headerStyle: { backgroundColor: COLORS.primary },
                headerTintColor: COLORS.white,
              }}
            />
            <Stack.Screen 
              name="Settings" 
              component={SettingsScreen}
              options={{
                headerShown: true,
                title: 'Settings',
                headerStyle: { backgroundColor: COLORS.primary },
                headerTintColor: COLORS.white,
              }}
            />
          </>
        )}
      </Stack.Navigator>
    </NavigationContainer>
  );
}
