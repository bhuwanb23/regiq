import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, Alert, Picker, Modal } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { COLORS, TYPOGRAPHY, SPACING, BORDER_RADIUS, SHADOWS } from '../../constants/theme';

const ReportGenerator = ({ 
  onGenerateReport, 
  onScheduleReport,
  loading = false 
}) => {
  const [reportType, setReportType] = useState('compliance');
  const [reportTitle, setReportTitle] = useState('');
  const [showScheduleModal, setShowScheduleModal] = useState(false);
  const [scheduleFrequency, setScheduleFrequency] = useState('weekly');
  const [scheduleTime, setScheduleTime] = useState('');

  const handleGenerateReport = () => {
    if (!reportTitle.trim()) {
      Alert.alert('Error', 'Please enter a report title');
      return;
    }

    onGenerateReport({
      title: reportTitle,
      reportType: reportType,
      format: 'pdf'
    });
  };

  const handleScheduleReport = () => {
    if (!reportTitle.trim()) {
      Alert.alert('Error', 'Please enter a report title');
      return;
    }

    if (!scheduleTime.trim()) {
      Alert.alert('Error', 'Please enter a schedule time');
      return;
    }

    onScheduleReport({
      title: reportTitle,
      reportType: reportType,
      frequency: scheduleFrequency,
      nextRunTime: scheduleTime,
      isActive: true
    });

    setShowScheduleModal(false);
    // Reset form
    setReportTitle('');
  };

  const reportTypes = [
    { value: 'compliance', label: 'Compliance Summary' },
    { value: 'bias', label: 'Bias Analysis' },
    { value: 'risk', label: 'Risk Simulation' },
    { value: 'audit', label: 'Audit Trail' }
  ];

  return (
    <View style={styles.container}>
      <Text style={styles.sectionTitle}>Report Generator</Text>
      
      <View style={styles.form}>
        <View style={styles.inputGroup}>
          <Text style={styles.label}>Report Title</Text>
          <TextInput
            style={styles.input}
            value={reportTitle}
            onChangeText={setReportTitle}
            placeholder="Enter report title"
            placeholderTextColor={COLORS.textSecondary}
          />
        </View>

        <View style={styles.inputGroup}>
          <Text style={styles.label}>Report Type</Text>
          <View style={styles.pickerContainer}>
            <Picker
              selectedValue={reportType}
              style={styles.picker}
              onValueChange={setReportType}
            >
              {reportTypes.map(type => (
                <Picker.Item 
                  key={type.value} 
                  label={type.label} 
                  value={type.value} 
                />
              ))}
            </Picker>
          </View>
        </View>

        <View style={styles.buttonGroup}>
          <TouchableOpacity
            style={[styles.generateButton, loading && styles.disabledButton]}
            onPress={handleGenerateReport}
            disabled={loading}
          >
            {loading ? (
              <Ionicons name="hourglass" size={16} color={COLORS.white} />
            ) : (
              <Ionicons name="document-text" size={16} color={COLORS.white} />
            )}
            <Text style={styles.buttonText}>
              {loading ? 'Generating...' : 'Generate Report'}
            </Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={[styles.scheduleButton, loading && styles.disabledButton]}
            onPress={() => setShowScheduleModal(true)}
            disabled={loading}
          >
            <Ionicons name="calendar" size={16} color={COLORS.primary} />
            <Text style={styles.scheduleButtonText}>Schedule</Text>
          </TouchableOpacity>
        </View>
      </View>

      {/* Schedule Modal */}
      <Modal
        animationType="slide"
        transparent={true}
        visible={showScheduleModal}
        onRequestClose={() => setShowScheduleModal(false)}
      >
        <View style={styles.modalContainer}>
          <View style={styles.modalContent}>
            <View style={styles.modalHeader}>
              <Text style={styles.modalTitle}>Schedule Report</Text>
              <TouchableOpacity onPress={() => setShowScheduleModal(false)}>
                <Ionicons name="close" size={24} color={COLORS.textSecondary} />
              </TouchableOpacity>
            </View>

            <View style={styles.modalBody}>
              <View style={styles.inputGroup}>
                <Text style={styles.label}>Frequency</Text>
                <View style={styles.pickerContainer}>
                  <Picker
                    selectedValue={scheduleFrequency}
                    style={styles.picker}
                    onValueChange={setScheduleFrequency}
                  >
                    <Picker.Item label="Daily" value="daily" />
                    <Picker.Item label="Weekly" value="weekly" />
                    <Picker.Item label="Monthly" value="monthly" />
                  </Picker>
                </View>
              </View>

              <View style={styles.inputGroup}>
                <Text style={styles.label}>Next Run Time</Text>
                <TextInput
                  style={styles.input}
                  value={scheduleTime}
                  onChangeText={setScheduleTime}
                  placeholder="YYYY-MM-DD HH:MM"
                  placeholderTextColor={COLORS.textSecondary}
                />
              </View>

              <View style={styles.modalButtonGroup}>
                <TouchableOpacity
                  style={styles.cancelButton}
                  onPress={() => setShowScheduleModal(false)}
                >
                  <Text style={styles.cancelButtonText}>Cancel</Text>
                </TouchableOpacity>

                <TouchableOpacity
                  style={styles.confirmButton}
                  onPress={handleScheduleReport}
                >
                  <Text style={styles.confirmButtonText}>Schedule</Text>
                </TouchableOpacity>
              </View>
            </View>
          </View>
        </View>
      </Modal>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: COLORS.white,
    borderRadius: BORDER_RADIUS.lg,
    padding: SPACING.lg,
    marginBottom: SPACING.md,
    ...SHADOWS.sm,
  },
  sectionTitle: {
    fontSize: TYPOGRAPHY.fontSize.base,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.textPrimary,
    marginBottom: SPACING.md,
  },
  form: {
    gap: SPACING.md,
  },
  inputGroup: {
    marginBottom: SPACING.sm,
  },
  label: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
    color: COLORS.textPrimary,
    marginBottom: SPACING.xs,
  },
  input: {
    backgroundColor: COLORS.surfaceSecondary,
    borderRadius: BORDER_RADIUS.md,
    padding: SPACING.sm,
    fontSize: TYPOGRAPHY.fontSize.sm,
    color: COLORS.textPrimary,
    borderWidth: 1,
    borderColor: COLORS.gray300,
  },
  pickerContainer: {
    backgroundColor: COLORS.surfaceSecondary,
    borderRadius: BORDER_RADIUS.md,
    borderWidth: 1,
    borderColor: COLORS.gray300,
  },
  picker: {
    height: 40,
    color: COLORS.textPrimary,
  },
  buttonGroup: {
    flexDirection: 'row',
    gap: SPACING.sm,
    marginTop: SPACING.md,
  },
  generateButton: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: COLORS.primary,
    borderRadius: BORDER_RADIUS.md,
    padding: SPACING.sm,
  },
  scheduleButton: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: COLORS.surfaceSecondary,
    borderRadius: BORDER_RADIUS.md,
    padding: SPACING.sm,
    borderWidth: 1,
    borderColor: COLORS.primary,
  },
  buttonText: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.white,
    marginLeft: SPACING.xs,
  },
  scheduleButtonText: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.primary,
    marginLeft: SPACING.xs,
  },
  disabledButton: {
    opacity: 0.6,
  },
  modalContainer: {
    flex: 1,
    justifyContent: 'flex-end',
    backgroundColor: 'rgba(0,0,0,0.5)',
  },
  modalContent: {
    backgroundColor: COLORS.white,
    borderTopLeftRadius: BORDER_RADIUS.xl,
    borderTopRightRadius: BORDER_RADIUS.xl,
    maxHeight: '70%',
  },
  modalHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: SPACING.md,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.gray200,
  },
  modalTitle: {
    fontSize: TYPOGRAPHY.fontSize.base,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.textPrimary,
  },
  modalBody: {
    padding: SPACING.md,
  },
  modalButtonGroup: {
    flexDirection: 'row',
    gap: SPACING.sm,
    marginTop: SPACING.lg,
  },
  cancelButton: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: COLORS.surfaceSecondary,
    borderRadius: BORDER_RADIUS.md,
    padding: SPACING.sm,
  },
  cancelButtonText: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.textSecondary,
  },
  confirmButton: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: COLORS.primary,
    borderRadius: BORDER_RADIUS.md,
    padding: SPACING.sm,
  },
  confirmButtonText: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.white,
  },
});

export default ReportGenerator;