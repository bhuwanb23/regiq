import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  ScrollView,
  StyleSheet,
  StatusBar,
  TouchableOpacity,
  Alert,
  Image,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { COLORS, SPACING, TYPOGRAPHY, BORDER_RADIUS } from '../../constants/theme';
import useUserProfile from '../../hooks/useUserProfile';
import useNotificationPreferences from '../../hooks/useNotificationPreferences';
import EditProfileForm from '../../components/profile/EditProfileForm';
import PreferencesManager from '../../components/profile/PreferencesManager';
import NotificationSettings from '../../components/profile/NotificationSettings';

const ProfileScreen = ({ navigation }) => {
  const [activeTab, setActiveTab] = useState('profile'); // profile, preferences, notifications
  const [isEditing, setIsEditing] = useState(false);
  const { profile, preferences, loading, error, fetchProfile, fetchPreferences, updateProfile, updatePreferences } = useUserProfile();
  const { preferences: notificationPrefs, fetchPreferences: fetchNotificationPrefs, updatePreferences: updateNotificationPrefs } = useNotificationPreferences();

  useEffect(() => {
    fetchProfile();
    fetchPreferences();
    fetchNotificationPrefs();
  }, []);

  const handleBack = () => {
    if (navigation?.goBack) {
      navigation.goBack();
    } else {
      console.log('Navigate back');
    }
  };

  const handleSaveProfile = async (profileData) => {
    try {
      await updateProfile(profileData);
      setIsEditing(false);
      Alert.alert('Success', 'Profile updated successfully');
    } catch (err) {
      Alert.alert('Error', 'Failed to update profile: ' + err.message);
    }
  };

  const handleSavePreferences = async (preferencesData) => {
    try {
      await updatePreferences(preferencesData);
      Alert.alert('Success', 'Preferences saved successfully');
    } catch (err) {
      Alert.alert('Error', 'Failed to save preferences: ' + err.message);
    }
  };

  const handleSaveNotifications = async (notificationData) => {
    try {
      await updateNotificationPrefs(notificationData);
      Alert.alert('Success', 'Notification settings saved successfully');
    } catch (err) {
      Alert.alert('Error', 'Failed to save notification settings: ' + err.message);
    }
  };

  // Role-based UI elements
  const isAdmin = profile?.role === 'admin';
  const isComplianceOfficer = profile?.role === 'compliance_officer';

  const renderProfileContent = () => {
    if (isEditing) {
      return (
        <EditProfileForm
          profile={profile}
          onSave={handleSaveProfile}
          onCancel={() => setIsEditing(false)}
          loading={loading}
        />
      );
    }

    return (
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
          </View>
          
          <View style={styles.userInfo}>
            <Text style={styles.userName}>{profile?.firstName} {profile?.lastName}</Text>
            <Text style={styles.userRole}>{profile?.role ? profile.role.replace('_', ' ') : 'User'}</Text>
            <Text style={styles.userEmail}>{profile?.email}</Text>
            
            {/* Role badge for admin users */}
            {isAdmin && (
              <View style={styles.adminBadge}>
                <Text style={styles.adminBadgeText}>ADMIN</Text>
              </View>
            )}
          </View>
        </View>

        {/* Profile Details */}
        <View style={styles.detailsSection}>
          <View style={styles.detailItem}>
            <Ionicons name="call" size={20} color={COLORS.textSecondary} />
            <Text style={styles.detailText}>{profile?.phone || 'Not provided'}</Text>
          </View>
          
          <View style={styles.detailItem}>
            <Ionicons name="business" size={20} color={COLORS.textSecondary} />
            <Text style={styles.detailText}>{profile?.department || 'Not provided'}</Text>
          </View>
          
          <View style={styles.detailItem}>
            <Ionicons name="briefcase" size={20} color={COLORS.textSecondary} />
            <Text style={styles.detailText}>{profile?.position || 'Not provided'}</Text>
          </View>
        </View>

        {/* Admin-specific features */}
        {isAdmin && (
          <View style={styles.adminSection}>
            <Text style={styles.sectionTitle}>Administrator Features</Text>
            <TouchableOpacity style={styles.adminFeatureItem}>
              <Ionicons name="people" size={20} color={COLORS.primary} />
              <Text style={styles.adminFeatureText}>User Management</Text>
              <Ionicons name="chevron-forward" size={16} color={COLORS.textSecondary} />
            </TouchableOpacity>
            
            <TouchableOpacity style={styles.adminFeatureItem}>
              <Ionicons name="settings" size={20} color={COLORS.primary} />
              <Text style={styles.adminFeatureText}>System Configuration</Text>
              <Ionicons name="chevron-forward" size={16} color={COLORS.textSecondary} />
            </TouchableOpacity>
            
            <TouchableOpacity style={styles.adminFeatureItem}>
              <Ionicons name="bar-chart" size={20} color={COLORS.primary} />
              <Text style={styles.adminFeatureText}>System Analytics</Text>
              <Ionicons name="chevron-forward" size={16} color={COLORS.textSecondary} />
            </TouchableOpacity>
          </View>
        )}

        {/* Compliance Officer features */}
        {isComplianceOfficer && (
          <View style={styles.complianceSection}>
            <Text style={styles.sectionTitle}>Compliance Features</Text>
            <TouchableOpacity style={styles.complianceFeatureItem}>
              <Ionicons name="document-text" size={20} color={COLORS.secondary} />
              <Text style={styles.complianceFeatureText}>Audit Trail</Text>
              <Ionicons name="chevron-forward" size={16} color={COLORS.textSecondary} />
            </TouchableOpacity>
            
            <TouchableOpacity style={styles.complianceFeatureItem}>
              <Ionicons name="checkmark-circle" size={20} color={COLORS.secondary} />
              <Text style={styles.complianceFeatureText}>Compliance Reports</Text>
              <Ionicons name="chevron-forward" size={16} color={COLORS.textSecondary} />
            </TouchableOpacity>
          </View>
        )}

        {/* Edit Button */}
        <TouchableOpacity 
          style={styles.editButton}
          onPress={() => setIsEditing(true)}
        >
          <Ionicons name="create" size={20} color={COLORS.white} />
          <Text style={styles.editButtonText}>Edit Profile</Text>
        </TouchableOpacity>
      </ScrollView>
    );
  };

  const renderPreferencesContent = () => {
    return (
      <PreferencesManager
        preferences={preferences}
        onSave={handleSavePreferences}
        loading={loading}
      />
    );
  };

  const renderNotificationsContent = () => {
    return (
      <NotificationSettings
        notifications={notificationPrefs}
        onSave={handleSaveNotifications}
      />
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
          <Text style={styles.headerTitle}>My Profile</Text>
        </View>
      </View>

      {/* Tab Navigation */}
      <View style={styles.tabContainer}>
        <TouchableOpacity 
          style={[styles.tab, activeTab === 'profile' && styles.activeTab]}
          onPress={() => setActiveTab('profile')}
        >
          <Text style={[styles.tabText, activeTab === 'profile' && styles.activeTabText]}>
            Profile
          </Text>
        </TouchableOpacity>
        
        <TouchableOpacity 
          style={[styles.tab, activeTab === 'preferences' && styles.activeTab]}
          onPress={() => setActiveTab('preferences')}
        >
          <Text style={[styles.tabText, activeTab === 'preferences' && styles.activeTabText]}>
            Preferences
          </Text>
        </TouchableOpacity>

        <TouchableOpacity 
          style={[styles.tab, activeTab === 'notifications' && styles.activeTab]}
          onPress={() => setActiveTab('notifications')}
        >
          <Text style={[styles.tabText, activeTab === 'notifications' && styles.activeTabText]}>
            Notifications
          </Text>
        </TouchableOpacity>
      </View>

      {/* Content */}
      {activeTab === 'profile' && renderProfileContent()}
      {activeTab === 'preferences' && renderPreferencesContent()}
      {activeTab === 'notifications' && renderNotificationsContent()}
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
  tabContainer: {
    flexDirection: 'row',
    backgroundColor: COLORS.white,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.gray200,
  },
  tab: {
    flex: 1,
    paddingVertical: SPACING.md,
    alignItems: 'center',
  },
  activeTab: {
    borderBottomWidth: 2,
    borderBottomColor: COLORS.primary,
  },
  tabText: {
    fontSize: TYPOGRAPHY.fontSize.base,
    color: COLORS.textSecondary,
  },
  activeTabText: {
    color: COLORS.primary,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
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
    marginBottom: 4,
    textTransform: 'capitalize',
  },
  userEmail: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    color: COLORS.textSecondary,
  },
  adminBadge: {
    backgroundColor: COLORS.danger,
    paddingHorizontal: SPACING.xs,
    paddingVertical: 2,
    borderRadius: BORDER_RADIUS.sm,
    alignSelf: 'flex-start',
    marginTop: SPACING.xs,
  },
  adminBadgeText: {
    color: COLORS.white,
    fontSize: TYPOGRAPHY.fontSize.xs,
    fontWeight: TYPOGRAPHY.fontWeight.bold,
  },
  detailsSection: {
    backgroundColor: COLORS.white,
    marginTop: SPACING.sm,
    padding: SPACING.lg,
  },
  detailItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: SPACING.md,
  },
  detailText: {
    fontSize: TYPOGRAPHY.fontSize.base,
    color: COLORS.textPrimary,
    marginLeft: SPACING.md,
    flex: 1,
  },
  sectionTitle: {
    fontSize: TYPOGRAPHY.fontSize.lg,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.primary,
    marginBottom: SPACING.md,
  },
  adminSection: {
    backgroundColor: COLORS.white,
    marginTop: SPACING.sm,
    padding: SPACING.lg,
    borderTopWidth: 1,
    borderTopColor: COLORS.gray200,
  },
  adminFeatureItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: SPACING.sm,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.gray100,
  },
  adminFeatureText: {
    fontSize: TYPOGRAPHY.fontSize.base,
    color: COLORS.textPrimary,
    marginLeft: SPACING.md,
    flex: 1,
  },
  complianceSection: {
    backgroundColor: COLORS.white,
    marginTop: SPACING.sm,
    padding: SPACING.lg,
    borderTopWidth: 1,
    borderTopColor: COLORS.gray200,
  },
  complianceFeatureItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: SPACING.sm,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.gray100,
  },
  complianceFeatureText: {
    fontSize: TYPOGRAPHY.fontSize.base,
    color: COLORS.textPrimary,
    marginLeft: SPACING.md,
    flex: 1,
  },
  editButton: {
    flexDirection: 'row',
    backgroundColor: COLORS.primary,
    padding: SPACING.md,
    borderRadius: BORDER_RADIUS.md,
    alignItems: 'center',
    justifyContent: 'center',
    margin: SPACING.lg,
  },
  editButtonText: {
    color: COLORS.white,
    fontSize: TYPOGRAPHY.fontSize.base,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
    marginLeft: SPACING.xs,
  },
});

export default ProfileScreen;