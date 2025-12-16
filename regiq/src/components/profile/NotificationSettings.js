import React, { useState } from 'react';
import {
  View,
  Text,
  Switch,
  StyleSheet,
  ScrollView,
  TouchableOpacity
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { COLORS, SPACING, TYPOGRAPHY, BORDER_RADIUS } from '../../constants/theme';

const NotificationSettings = ({ notifications, onSave }) => {
  const [notificationPrefs, setNotificationPrefs] = useState({
    regulatoryUpdates: true,
    biasAlerts: true,
    riskWarnings: true,
    reportGeneration: true,
    systemMaintenance: false,
    email: true,
    push: true,
    sms: false
  });

  const toggleNotification = (key) => {
    setNotificationPrefs(prev => ({
      ...prev,
      [key]: !prev[key]
    }));
  };

  const handleSave = () => {
    onSave(notificationPrefs);
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Notification Types</Text>
        
        <View style={styles.notificationItem}>
          <View style={styles.notificationInfo}>
            <Text style={styles.notificationLabel}>Regulatory Updates</Text>
            <Text style={styles.notificationDescription}>New regulations and amendments</Text>
          </View>
          <Switch
            value={notificationPrefs.regulatoryUpdates}
            onValueChange={() => toggleNotification('regulatoryUpdates')}
            trackColor={{ false: COLORS.gray300, true: COLORS.primary }}
          />
        </View>

        <View style={styles.notificationItem}>
          <View style={styles.notificationInfo}>
            <Text style={styles.notificationLabel}>Bias Detection Alerts</Text>
            <Text style={styles.notificationDescription}>AI model bias detection warnings</Text>
          </View>
          <Switch
            value={notificationPrefs.biasAlerts}
            onValueChange={() => toggleNotification('biasAlerts')}
            trackColor={{ false: COLORS.gray300, true: COLORS.primary }}
          />
        </View>

        <View style={styles.notificationItem}>
          <View style={styles.notificationInfo}>
            <Text style={styles.notificationLabel}>Risk Assessment Warnings</Text>
            <Text style={styles.notificationDescription}>High-risk model predictions</Text>
          </View>
          <Switch
            value={notificationPrefs.riskWarnings}
            onValueChange={() => toggleNotification('riskWarnings')}
            trackColor={{ false: COLORS.gray300, true: COLORS.primary }}
          />
        </View>

        <View style={styles.notificationItem}>
          <View style={styles.notificationInfo}>
            <Text style={styles.notificationLabel}>Report Generation</Text>
            <Text style={styles.notificationDescription}>Completed report notifications</Text>
          </View>
          <Switch
            value={notificationPrefs.reportGeneration}
            onValueChange={() => toggleNotification('reportGeneration')}
            trackColor={{ false: COLORS.gray300, true: COLORS.primary }}
          />
        </View>

        <View style={styles.notificationItem}>
          <View style={styles.notificationInfo}>
            <Text style={styles.notificationLabel}>System Maintenance</Text>
            <Text style={styles.notificationDescription}>Scheduled maintenance alerts</Text>
          </View>
          <Switch
            value={notificationPrefs.systemMaintenance}
            onValueChange={() => toggleNotification('systemMaintenance')}
            trackColor={{ false: COLORS.gray300, true: COLORS.primary }}
          />
        </View>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Delivery Methods</Text>
        
        <View style={styles.notificationItem}>
          <View style={styles.notificationInfo}>
            <Text style={styles.notificationLabel}>Email</Text>
            <Text style={styles.notificationDescription}>Send notifications to email</Text>
          </View>
          <Switch
            value={notificationPrefs.email}
            onValueChange={() => toggleNotification('email')}
            trackColor={{ false: COLORS.gray300, true: COLORS.primary }}
          />
        </View>

        <View style={styles.notificationItem}>
          <View style={styles.notificationInfo}>
            <Text style={styles.notificationLabel}>Push Notifications</Text>
            <Text style={styles.notificationDescription}>In-app notifications</Text>
          </View>
          <Switch
            value={notificationPrefs.push}
            onValueChange={() => toggleNotification('push')}
            trackColor={{ false: COLORS.gray300, true: COLORS.primary }}
          />
        </View>

        <View style={styles.notificationItem}>
          <View style={styles.notificationInfo}>
            <Text style={styles.notificationLabel}>SMS</Text>
            <Text style={styles.notificationDescription}>Text message notifications</Text>
          </View>
          <Switch
            value={notificationPrefs.sms}
            onValueChange={() => toggleNotification('sms')}
            trackColor={{ false: COLORS.gray300, true: COLORS.primary }}
          />
        </View>
      </View>

      <TouchableOpacity style={styles.saveButton} onPress={handleSave}>
        <Text style={styles.saveButtonText}>Save Notification Settings</Text>
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
  notificationItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: SPACING.sm,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.gray100,
  },
  notificationInfo: {
    flex: 1,
    marginRight: SPACING.md,
  },
  notificationLabel: {
    fontSize: TYPOGRAPHY.fontSize.base,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
    color: COLORS.textPrimary,
    marginBottom: 2,
  },
  notificationDescription: {
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
  saveButtonText: {
    color: COLORS.white,
    fontSize: TYPOGRAPHY.fontSize.base,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
  },
});

export default NotificationSettings;