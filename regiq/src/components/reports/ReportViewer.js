import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet, Alert } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { COLORS, TYPOGRAPHY, SPACING, BORDER_RADIUS, SHADOWS } from '../../constants/theme';

const ReportViewer = ({ 
  report,
  onExportPDF,
  onExportCSV,
  onExportJSON,
  onShare,
  loading = false
}) => {
  if (!report) {
    return (
      <View style={styles.container}>
        <View style={styles.emptyState}>
          <Ionicons name="document-text" size={48} color={COLORS.gray400} />
          <Text style={styles.emptyStateTitle}>No Report Selected</Text>
          <Text style={styles.emptyStateText}>
            Select a report to view details and export options
          </Text>
        </View>
      </View>
    );
  }

  const handleExport = async (exportFunc, format) => {
    if (loading) return;
    
    try {
      await exportFunc(report);
      Alert.alert('Success', `${format} export initiated`);
    } catch (err) {
      Alert.alert('Error', `Failed to export as ${format}`);
    }
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <View style={styles.titleContainer}>
          <Text style={styles.title}>{report.title}</Text>
          <Text style={styles.type}>{report.reportType}</Text>
        </View>
        
        <TouchableOpacity 
          style={styles.shareButton}
          onPress={() => onShare && onShare(report)}
        >
          <Ionicons name="share-outline" size={16} color={COLORS.primary} />
        </TouchableOpacity>
      </View>

      <View style={styles.metadata}>
        <View style={styles.metaItem}>
          <Ionicons name="calendar" size={14} color={COLORS.textSecondary} />
          <Text style={styles.metaText}>
            {new Date(report.createdAt).toLocaleDateString()}
          </Text>
        </View>
        
        <View style={styles.metaItem}>
          <Ionicons name="time" size={14} color={COLORS.textSecondary} />
          <Text style={styles.metaText}>
            {new Date(report.createdAt).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </Text>
        </View>
        
        <View style={styles.metaItem}>
          <Ionicons name="stats-chart" size={14} color={COLORS.textSecondary} />
          <Text style={styles.metaText}>{report.status}</Text>
        </View>
      </View>

      {report.content?.summary && (
        <View style={styles.summaryCard}>
          <Text style={styles.sectionTitle}>Summary</Text>
          <View style={styles.summaryGrid}>
            <View style={styles.summaryItem}>
              <Text style={styles.summaryValue}>
                {report.content.summary.totalRegulations || 0}
              </Text>
              <Text style={styles.summaryLabel}>Total Regulations</Text>
            </View>
            
            <View style={styles.summaryItem}>
              <Text style={[styles.summaryValue, { color: COLORS.success }]}>
                {report.content.summary.compliant || 0}
              </Text>
              <Text style={styles.summaryLabel}>Compliant</Text>
            </View>
            
            <View style={styles.summaryItem}>
              <Text style={[styles.summaryValue, { color: COLORS.warning }]}>
                {report.content.summary.pending || 0}
              </Text>
              <Text style={styles.summaryLabel}>Pending</Text>
            </View>
            
            <View style={styles.summaryItem}>
              <Text style={[styles.summaryValue, { color: COLORS.error }]}>
                {report.content.summary.nonCompliant || 0}
              </Text>
              <Text style={styles.summaryLabel}>Non-Compliant</Text>
            </View>
          </View>
        </View>
      )}

      <View style={styles.exportSection}>
        <Text style={styles.sectionTitle}>Export Options</Text>
        <View style={styles.exportButtons}>
          <TouchableOpacity
            style={[styles.exportButton, styles.pdfButton]}
            onPress={() => handleExport(onExportPDF, 'PDF')}
            disabled={loading}
          >
            <Ionicons name="document" size={16} color={COLORS.white} />
            <Text style={styles.exportButtonText}>PDF</Text>
          </TouchableOpacity>
          
          <TouchableOpacity
            style={[styles.exportButton, styles.csvButton]}
            onPress={() => handleExport(onExportCSV, 'CSV')}
            disabled={loading}
          >
            <Ionicons name="grid" size={16} color={COLORS.white} />
            <Text style={styles.exportButtonText}>CSV</Text>
          </TouchableOpacity>
          
          <TouchableOpacity
            style={[styles.exportButton, styles.jsonButton]}
            onPress={() => handleExport(onExportJSON, 'JSON')}
            disabled={loading}
          >
            <Ionicons name="code" size={16} color={COLORS.white} />
            <Text style={styles.exportButtonText}>JSON</Text>
          </TouchableOpacity>
        </View>
      </View>
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
  emptyState: {
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: SPACING['3xl'],
  },
  emptyStateTitle: {
    fontSize: TYPOGRAPHY.fontSize.base,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.textPrimary,
    marginTop: SPACING.md,
  },
  emptyStateText: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    color: COLORS.textSecondary,
    textAlign: 'center',
    marginTop: SPACING.xs,
    paddingHorizontal: SPACING.lg,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: SPACING.md,
  },
  titleContainer: {
    flex: 1,
    marginRight: SPACING.sm,
  },
  title: {
    fontSize: TYPOGRAPHY.fontSize.lg,
    fontWeight: TYPOGRAPHY.fontWeight.bold,
    color: COLORS.textPrimary,
    marginBottom: SPACING.xs,
  },
  type: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    color: COLORS.primary,
    textTransform: 'capitalize',
  },
  shareButton: {
    width: 32,
    height: 32,
    borderRadius: BORDER_RADIUS.full,
    backgroundColor: COLORS.surfaceSecondary,
    alignItems: 'center',
    justifyContent: 'center',
  },
  metadata: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: SPACING.md,
    marginBottom: SPACING.lg,
  },
  metaItem: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  metaText: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.textSecondary,
    marginLeft: SPACING.xs,
  },
  summaryCard: {
    backgroundColor: COLORS.surfaceSecondary,
    borderRadius: BORDER_RADIUS.md,
    padding: SPACING.md,
    marginBottom: SPACING.lg,
  },
  sectionTitle: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.textPrimary,
    marginBottom: SPACING.md,
  },
  summaryGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  summaryItem: {
    alignItems: 'center',
    minWidth: 70,
    marginBottom: SPACING.sm,
  },
  summaryValue: {
    fontSize: TYPOGRAPHY.fontSize.lg,
    fontWeight: TYPOGRAPHY.fontWeight.bold,
    color: COLORS.textPrimary,
    marginBottom: SPACING.xs,
  },
  summaryLabel: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.textSecondary,
    textAlign: 'center',
  },
  exportSection: {
    marginBottom: SPACING.sm,
  },
  exportButtons: {
    flexDirection: 'row',
    gap: SPACING.sm,
  },
  exportButton: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    padding: SPACING.sm,
    borderRadius: BORDER_RADIUS.md,
  },
  pdfButton: {
    backgroundColor: COLORS.primary,
  },
  csvButton: {
    backgroundColor: COLORS.secondary,
  },
  jsonButton: {
    backgroundColor: COLORS.accent,
  },
  exportButtonText: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.white,
    marginLeft: SPACING.xs,
  },
});

export default ReportViewer;