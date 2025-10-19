import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet, FlatList } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { COLORS, TYPOGRAPHY, SPACING, BORDER_RADIUS, SHADOWS } from '../../constants/theme';

const ReportHistoryItem = ({ 
  title,
  status,
  date,
  statusColor,
  onShare,
  onDownload,
  onPress
}) => {
  return (
    <TouchableOpacity 
      style={styles.historyItem}
      onPress={onPress}
      activeOpacity={0.7}
    >
      <View style={styles.historyHeader}>
        <View style={styles.historyTitleContainer}>
          <View style={[styles.statusDot, { backgroundColor: statusColor }]} />
          <Text style={styles.historyTitle}>{title}</Text>
        </View>
        <Text style={styles.historyDate}>{date}</Text>
      </View>
      
      <View style={styles.historyFooter}>
        <Text style={styles.historyStatus}>Status: {status}</Text>
        
        <View style={styles.historyActions}>
          <TouchableOpacity 
            style={styles.historyActionButton}
            onPress={onShare}
          >
            <Ionicons name="share" size={12} color={COLORS.secondary} />
            <Text style={styles.historyActionText}>Share</Text>
          </TouchableOpacity>
          
          <TouchableOpacity 
            style={styles.historyActionButton}
            onPress={onDownload}
          >
            <Ionicons name="download" size={12} color={COLORS.primary} />
            <Text style={styles.historyActionText}>Download</Text>
          </TouchableOpacity>
        </View>
      </View>
    </TouchableOpacity>
  );
};

const ReportHistory = ({ 
  reports = [],
  onViewAll,
  onReportPress,
  onShareReport,
  onDownloadReport
}) => {
  const defaultReports = [
    {
      id: 1,
      title: 'Compliance Summary',
      status: 'Approved',
      date: 'Oct 15',
      statusColor: COLORS.success,
    },
    {
      id: 2,
      title: 'AI Bias Audit',
      status: 'Under Review',
      date: 'Oct 12',
      statusColor: COLORS.warning,
    },
    {
      id: 3,
      title: 'Risk Simulation Report',
      status: 'Draft',
      date: 'Oct 10',
      statusColor: COLORS.info,
    },
    {
      id: 4,
      title: 'Model Performance Analysis',
      status: 'Completed',
      date: 'Oct 8',
      statusColor: COLORS.success,
    },
    {
      id: 5,
      title: 'Regulatory Compliance Check',
      status: 'Failed',
      date: 'Oct 5',
      statusColor: COLORS.error,
    },
  ];

  const reportData = reports.length > 0 ? reports : defaultReports;

  const renderReportItem = ({ item }) => (
    <ReportHistoryItem
      title={item.title}
      status={item.status}
      date={item.date}
      statusColor={item.statusColor}
      onPress={() => onReportPress?.(item)}
      onShare={() => onShareReport?.(item)}
      onDownload={() => onDownloadReport?.(item)}
    />
  );

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.sectionTitle}>Recent Reports</Text>
        <TouchableOpacity onPress={onViewAll}>
          <Text style={styles.viewAllButton}>View All</Text>
        </TouchableOpacity>
      </View>

      {/* Reports List */}
      <FlatList
        data={reportData}
        renderItem={renderReportItem}
        keyExtractor={(item) => item.id.toString()}
        showsVerticalScrollIndicator={false}
        scrollEnabled={false} // Disable scroll since it's inside a ScrollView
      />

      {/* Summary Stats */}
      <View style={styles.summaryContainer}>
        <View style={styles.summaryItem}>
          <Text style={styles.summaryValue}>
            {reportData.filter(r => r.status === 'Approved' || r.status === 'Completed').length}
          </Text>
          <Text style={styles.summaryLabel}>Completed</Text>
        </View>
        
        <View style={styles.summaryDivider} />
        
        <View style={styles.summaryItem}>
          <Text style={[styles.summaryValue, { color: COLORS.warning }]}>
            {reportData.filter(r => r.status === 'Under Review' || r.status === 'Draft').length}
          </Text>
          <Text style={styles.summaryLabel}>In Progress</Text>
        </View>
        
        <View style={styles.summaryDivider} />
        
        <View style={styles.summaryItem}>
          <Text style={[styles.summaryValue, { color: COLORS.error }]}>
            {reportData.filter(r => r.status === 'Failed').length}
          </Text>
          <Text style={styles.summaryLabel}>Failed</Text>
        </View>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    paddingHorizontal: SPACING.md,
    marginBottom: SPACING.lg,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: SPACING.md,
  },
  sectionTitle: {
    fontSize: TYPOGRAPHY.fontSize.lg,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.textPrimary,
  },
  viewAllButton: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.secondary,
  },
  historyItem: {
    backgroundColor: COLORS.white,
    borderRadius: BORDER_RADIUS.lg,
    padding: SPACING.md,
    marginBottom: SPACING.sm,
    borderWidth: 1,
    borderColor: COLORS.gray200,
    ...SHADOWS.sm,
  },
  historyHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: SPACING.sm,
  },
  historyTitleContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  statusDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    marginRight: SPACING.sm,
  },
  historyTitle: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.textPrimary,
  },
  historyDate: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.textSecondary,
  },
  historyFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  historyStatus: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.textSecondary,
  },
  historyActions: {
    flexDirection: 'row',
    gap: SPACING.sm,
  },
  historyActionButton: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  historyActionText: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.textSecondary,
    marginLeft: SPACING.xs,
  },
  summaryContainer: {
    flexDirection: 'row',
    backgroundColor: COLORS.white,
    borderRadius: BORDER_RADIUS.lg,
    paddingVertical: SPACING.sm,
    paddingHorizontal: SPACING.md,
    marginTop: SPACING.md,
    ...SHADOWS.sm,
  },
  summaryItem: {
    flex: 1,
    alignItems: 'center',
  },
  summaryValue: {
    fontSize: TYPOGRAPHY.fontSize.lg,
    fontWeight: TYPOGRAPHY.fontWeight.bold,
    color: COLORS.success,
    marginBottom: 2,
  },
  summaryLabel: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.textSecondary,
    textAlign: 'center',
  },
  summaryDivider: {
    width: 1,
    backgroundColor: COLORS.gray300,
    marginHorizontal: SPACING.sm,
  },
});

export default ReportHistory;
