import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  Switch,
  TouchableOpacity,
  StyleSheet,
  ScrollView,
  Alert
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { COLORS, SPACING, TYPOGRAPHY, BORDER_RADIUS } from '../../constants/theme';

const PreferencesManager = ({ preferences, onSave, loading }) => {
  const [prefs, setPrefs] = useState({
    emailNotifications: true,
    smsNotifications: false,
    pushNotifications: true,
    darkMode: false,
    language: 'en',
    timezone: 'UTC',
    dateFormat: 'MM/DD/YYYY',
    theme: 'light'
  });

  // Initialize preferences when they change
  useEffect(() => {
    if (preferences) {
      setPrefs({
        emailNotifications: preferences.emailNotifications ?? true,
        smsNotifications: preferences.smsNotifications ?? false,
        pushNotifications: preferences.pushNotifications ?? true,
        darkMode: preferences.darkMode ?? false,
        language: preferences.language ?? 'en',
        timezone: preferences.timezone ?? 'UTC',
        dateFormat: preferences.dateFormat ?? 'MM/DD/YYYY',
        theme: preferences.theme ?? 'light'
      });
    }
  }, [preferences]);

  const togglePreference = (key) => {
    setPrefs(prev => ({
      ...prev,
      [key]: !prev[key]
    }));
  };

  const handleSave = () => {
    onSave(prefs);
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Notifications</Text>
        
        <View style={styles.preferenceItem}>
          <View style={styles.preferenceInfo}>
            <Text style={styles.preferenceLabel}>Email Notifications</Text>
            <Text style={styles.preferenceDescription}>Receive updates via email</Text>
          </View>
          <Switch
            value={prefs.emailNotifications}
            onValueChange={() => togglePreference('emailNotifications')}
            trackColor={{ false: COLORS.gray300, true: COLORS.primary }}
            thumbColor={prefs.emailNotifications ? COLORS.white : COLORS.white}
          />
        </View>

        <View style={styles.preferenceItem}>
          <View style={styles.preferenceInfo}>
            <Text style={styles.preferenceLabel}>SMS Notifications</Text>
            <Text style={styles.preferenceDescription}>Receive text messages</Text>
          </View>
          <Switch
            value={prefs.smsNotifications}
            onValueChange={() => togglePreference('smsNotifications')}
            trackColor={{ false: COLORS.gray300, true: COLORS.primary }}
            thumbColor={prefs.smsNotifications ? COLORS.white : COLORS.white}
          />
        </View>

        <View style={styles.preferenceItem}>
          <View style={styles.preferenceInfo}>
            <Text style={styles.preferenceLabel}>Push Notifications</Text>
            <Text style={styles.preferenceDescription}>Receive in-app notifications</Text>
          </View>
          <Switch
            value={prefs.pushNotifications}
            onValueChange={() => togglePreference('pushNotifications')}
            trackColor={{ false: COLORS.gray300, true: COLORS.primary }}
            thumbColor={prefs.pushNotifications ? COLORS.white : COLORS.white}
          />
        </View>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Appearance</Text>
        
        <View style={styles.preferenceItem}>
          <View style={styles.preferenceInfo}>
            <Text style={styles.preferenceLabel}>Dark Mode</Text>
            <Text style={styles.preferenceDescription}>Enable dark theme</Text>
          </View>
          <Switch
            value={prefs.darkMode}
            onValueChange={() => togglePreference('darkMode')}
            trackColor={{ false: COLORS.gray300, true: COLORS.primary }}
            thumbColor={prefs.darkMode ? COLORS.white : COLORS.white}
          />
        </View>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Localization</Text>
        
        <TouchableOpacity style={styles.preferenceItem}>
          <View style={styles.preferenceInfo}>
            <Text style={styles.preferenceLabel}>Language</Text>
            <Text style={styles.preferenceDescription}>{prefs.language.toUpperCase()}</Text>
          </View>
          <Ionicons name="chevron-forward" size={16} color={COLORS.textSecondary} />
        </TouchableOpacity>

        <TouchableOpacity style={styles.preferenceItem}>
          <View style={styles.preferenceInfo}>
            <Text style={styles.preferenceLabel}>Timezone</Text>
            <Text style={styles.preferenceDescription}>{prefs.timezone}</Text>
          </View>
          <Ionicons name="chevron-forward" size={16} color={COLORS.textSecondary} />
        </TouchableOpacity>

        <TouchableOpacity style={styles.preferenceItem}>
          <View style={styles.preferenceInfo}>
            <Text style={styles.preferenceLabel}>Date Format</Text>
            <Text style={styles.preferenceDescription}>{prefs.dateFormat}</Text>
          </View>
          <Ionicons name="chevron-forward" size={16} color={COLORS.textSecondary} />
        </TouchableOpacity>
      </View>

      <TouchableOpacity
        style={[styles.saveButton, loading && styles.saveButtonDisabled]}
        onPress={handleSave}
        disabled={loading}
      >
        {loading ? (
          <Ionicons name="hourglass" size={20} color={COLORS.white} />
        ) : (
          <Text style={styles.saveButtonText}>Save Preferences</Text>
        )}
      </TouchableOpacity>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: SPACING.md,
  },
  section: {
    backgroundColor: COLORS.white,
    borderRadius: BORDER_RADIUS.md,
    padding: SPACING.md,
    marginBottom: SPACING.md,
    borderWidth: 1,
    borderColor: COLORS.gray200,
  },
  sectionTitle: {
    fontSize: TYPOGRAPHY.fontSize.lg,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.primary,
    marginBottom: SPACING.md,
  },
  preferenceItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: SPACING.sm,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.gray100,
  },
  preferenceInfo: {
    flex: 1,
    marginRight: SPACING.md,
  },
  preferenceLabel: {
    fontSize: TYPOGRAPHY.fontSize.base,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
    color: COLORS.textPrimary,
    marginBottom: 2,
  },
  preferenceDescription: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    color: COLORS.textSecondary,
  },
  saveButton: {
    backgroundColor: COLORS.primary,
    padding: SPACING.md,
    borderRadius: BORDER_RADIUS.md,
    alignItems: 'center',
    justifyContent: 'center',
    marginVertical: SPACING.lg,
  },
  saveButtonDisabled: {
    opacity: 0.7,
  },
  saveButtonText: {
    color: COLORS.white,
    fontSize: TYPOGRAPHY.fontSize.base,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
  },
});

export default PreferencesManager;