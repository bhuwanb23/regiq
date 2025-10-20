import React, { useState } from 'react';
import {
  View,
  Text,
  ScrollView,
  StyleSheet,
  StatusBar,
  TouchableOpacity,
  Alert,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { COLORS, SPACING, TYPOGRAPHY, BORDER_RADIUS } from '../../constants/theme';

const ProfileScreen = ({ navigation }) => {
  const handleBack = () => {
    if (navigation?.goBack) {
      navigation.goBack();
    } else {
      console.log('Navigate back');
    }
  };

  const handleProfileInfo = () => {
    Alert.alert(
      'Profile Information',
      'Edit your personal details including name, email, and phone number.',
      [
        { text: 'Cancel', style: 'cancel' },
        { text: 'Edit Profile', onPress: () => console.log('Edit Profile') },
      ]
    );
  };

  const handleCompanyInfo = () => {
    Alert.alert(
      'Company Information',
      'Update your company details, industry, and region.',
      [
        { text: 'Cancel', style: 'cancel' },
        { text: 'Edit Company', onPress: () => console.log('Edit Company') },
      ]
    );
  };

  const handleAIModels = () => {
    Alert.alert(
      'AI Models',
      'Manage your connected AI models and configurations.',
      [
        { text: 'Cancel', style: 'cancel' },
        { text: 'Manage Models', onPress: () => console.log('Manage AI Models') },
      ]
    );
  };

  const handleNotifications = () => {
    Alert.alert(
      'Notifications',
      'Configure your notification preferences for different types of alerts.',
      [
        { text: 'Cancel', style: 'cancel' },
        { text: 'Configure', onPress: () => console.log('Configure Notifications') },
      ]
    );
  };

  const handleSecurity = () => {
    Alert.alert(
      'Security Settings',
      'Manage your security settings, sessions, and authentication methods.',
      [
        { text: 'Cancel', style: 'cancel' },
        { text: 'Security Settings', onPress: () => console.log('Security Settings') },
      ]
    );
  };

  const handleEditAvatar = () => {
    Alert.alert(
      'Change Profile Picture',
      'Choose how you want to update your profile picture',
      [
        { text: 'Cancel', style: 'cancel' },
        { text: 'Camera', onPress: () => console.log('Open camera') },
        { text: 'Gallery', onPress: () => console.log('Open gallery') },
      ]
    );
  };

  return (
    <SafeAreaView style={styles.container} edges={['top', 'left', 'right']}>
      <StatusBar barStyle="dark-content" backgroundColor={COLORS.white} />
      
      {/* Header */}
      <View style={styles.header}>
        <View style={styles.headerLeft}>
          <TouchableOpacity 
            style={styles.backButton}
            onPress={handleBack}
            activeOpacity={0.7}
          >
            <Ionicons name="arrow-back" size={24} color={COLORS.primary} />
          </TouchableOpacity>
          <Text style={styles.headerTitle}>Settings</Text>
        </View>
        
        <TouchableOpacity style={styles.moreButton}>
          <Ionicons name="ellipsis-vertical" size={20} color={COLORS.textSecondary} />
        </TouchableOpacity>
      </View>

      {/* Content */}
      <ScrollView 
        style={styles.content}
        showsVerticalScrollIndicator={false}
        contentContainerStyle={styles.scrollContent}
      >
        {/* Profile Section */}
        <View style={styles.profileSection}>
          <View style={styles.avatarContainer}>
            <View style={styles.avatar}>
              <Ionicons name="person" size={32} color={COLORS.primary} />
            </View>
            <TouchableOpacity 
              style={styles.editButton}
              onPress={handleEditAvatar}
              activeOpacity={0.8}
            >
              <Ionicons name="camera" size={12} color={COLORS.white} />
            </TouchableOpacity>
          </View>
          
          <View style={styles.userInfo}>
            <Text style={styles.userName}>John Anderson</Text>
            <Text style={styles.userRole}>Compliance Manager</Text>
          </View>
        </View>

        {/* Settings Options */}
        <View style={styles.settingsSection}>
          <TouchableOpacity 
            style={styles.settingItem}
            onPress={handleProfileInfo}
            activeOpacity={0.7}
          >
            <View style={styles.settingIcon}>
              <Ionicons name="person" size={20} color={COLORS.primary} />
            </View>
            <View style={styles.settingContent}>
              <Text style={styles.settingTitle}>Profile Information</Text>
              <Text style={styles.settingSubtitle}>Manage your personal details</Text>
            </View>
            <Ionicons name="chevron-forward" size={16} color={COLORS.textSecondary} />
          </TouchableOpacity>

          <TouchableOpacity 
            style={styles.settingItem}
            onPress={handleCompanyInfo}
            activeOpacity={0.7}
          >
            <View style={styles.settingIcon}>
              <Ionicons name="business" size={20} color={COLORS.secondary} />
            </View>
            <View style={styles.settingContent}>
              <Text style={styles.settingTitle}>Company Information</Text>
              <Text style={styles.settingSubtitle}>Update company details</Text>
            </View>
            <Ionicons name="chevron-forward" size={16} color={COLORS.textSecondary} />
          </TouchableOpacity>

          <TouchableOpacity 
            style={styles.settingItem}
            onPress={handleAIModels}
            activeOpacity={0.7}
          >
            <View style={styles.settingIcon}>
              <Ionicons name="hardware-chip" size={20} color={COLORS.accent} />
            </View>
            <View style={styles.settingContent}>
              <Text style={styles.settingTitle}>AI Models</Text>
              <Text style={styles.settingSubtitle}>Manage connected AI models</Text>
            </View>
            <Ionicons name="chevron-forward" size={16} color={COLORS.textSecondary} />
          </TouchableOpacity>

          <TouchableOpacity 
            style={styles.settingItem}
            onPress={handleNotifications}
            activeOpacity={0.7}
          >
            <View style={styles.settingIcon}>
              <Ionicons name="notifications" size={20} color={COLORS.warning} />
            </View>
            <View style={styles.settingContent}>
              <Text style={styles.settingTitle}>Notifications</Text>
              <Text style={styles.settingSubtitle}>Configure notification preferences</Text>
            </View>
            <Ionicons name="chevron-forward" size={16} color={COLORS.textSecondary} />
          </TouchableOpacity>

          <TouchableOpacity 
            style={styles.settingItem}
            onPress={handleSecurity}
            activeOpacity={0.7}
          >
            <View style={styles.settingIcon}>
              <Ionicons name="shield-checkmark" size={20} color={COLORS.success} />
            </View>
            <View style={styles.settingContent}>
              <Text style={styles.settingTitle}>Security</Text>
              <Text style={styles.settingSubtitle}>Security settings and sessions</Text>
            </View>
            <Ionicons name="chevron-forward" size={16} color={COLORS.textSecondary} />
          </TouchableOpacity>
        </View>

        {/* Bottom Spacing */}
        <View style={styles.bottomSpacing} />
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: SPACING.md,
    paddingVertical: SPACING.sm,
    backgroundColor: COLORS.white,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.gray200,
  },
  headerLeft: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  backButton: {
    padding: SPACING.xs,
    marginRight: SPACING.sm,
  },
  headerTitle: {
    fontSize: TYPOGRAPHY.fontSize.lg,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.primary,
  },
  moreButton: {
    padding: SPACING.xs,
  },
  content: {
    flex: 1,
  },
  scrollContent: {
    paddingBottom: SPACING.lg,
  },
  profileSection: {
    backgroundColor: COLORS.white,
    padding: SPACING.lg,
    flexDirection: 'row',
    alignItems: 'center',
    borderBottomWidth: 1,
    borderBottomColor: COLORS.gray200,
  },
  avatarContainer: {
    position: 'relative',
    marginRight: SPACING.md,
  },
  avatar: {
    width: 64,
    height: 64,
    borderRadius: 32,
    backgroundColor: COLORS.surfaceSecondary,
    alignItems: 'center',
    justifyContent: 'center',
  },
  editButton: {
    position: 'absolute',
    bottom: -2,
    right: -2,
    backgroundColor: COLORS.secondary,
    width: 24,
    height: 24,
    borderRadius: 12,
    alignItems: 'center',
    justifyContent: 'center',
    borderWidth: 2,
    borderColor: COLORS.white,
  },
  userInfo: {
    flex: 1,
  },
  userName: {
    fontSize: TYPOGRAPHY.fontSize.lg,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.primary,
    marginBottom: 4,
  },
  userRole: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    color: COLORS.textSecondary,
  },
  settingsSection: {
    backgroundColor: COLORS.white,
    marginTop: SPACING.sm,
  },
  settingItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: SPACING.md,
    paddingVertical: SPACING.md,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.gray200,
  },
  settingIcon: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: COLORS.surfaceSecondary,
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: SPACING.sm,
  },
  settingContent: {
    flex: 1,
  },
  settingTitle: {
    fontSize: TYPOGRAPHY.fontSize.base,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
    color: COLORS.textPrimary,
    marginBottom: 2,
  },
  settingSubtitle: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    color: COLORS.textSecondary,
  },
  bottomSpacing: {
    height: SPACING.xl,
  },
});

export default ProfileScreen;
