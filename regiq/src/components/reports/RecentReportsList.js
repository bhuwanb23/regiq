import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet, FlatList } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { COLORS, TYPOGRAPHY, SPACING, BORDER_RADIUS, SHADOWS } from '../../constants/theme';

const RecentReportItem = ({ 
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
      style={styles.reportItem}
      onPress={onPress}
      activeOpacity={0.7}
    >
      <View style={styles.reportHeader}>
        <View style={styles.reportTitleContainer}>
          <View style={[styles.statusDot, { backgroundColor: statusColor }]} />
          <Text style={styles.reportTitle}>{title}</Text>
        </View>
        <Text style={styles.reportDate}>{date}</Text>
      </View>
      
      <View style={styles.reportFooter}>
        <Text style={styles.reportStatus}>Status: {status}</Text>
        
        <View style={styles.reportActions}>
          <TouchableOpacity 
            style={styles.actionButton}
            onPress={onShare}
          >
            <Ionicons name="share" size={12} color={COLORS.secondary} />
            <Text style={styles.actionText}>Share</Text>
          </TouchableOpacity>
          
          <TouchableOpacity 
            style={styles.actionButton}
            onPress={onDownload}
          >
            <Ionicons name="download" size={12} color={COLORS.primary} />
            <Text style={styles.actionText}>Download</Text>
          </TouchableOpacity>
        </View>
      </View>
    </TouchableOpacity>
  );
};

const RecentReportsList = ({ 
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
    {
      id: 6,
      title: 'Data Quality Assessment',
      status: 'Approved',
      date: 'Oct 3',
      statusColor: COLORS.success,
    },
    {
      id: 7,
      title: 'Security Audit Report',
      status: 'Under Review',
      date: 'Oct 1',
      statusColor: COLORS.warning,
    },
    {
      id: 8,
      title: 'Financial Risk Analysis',
      status: 'Completed',
      date: 'Sep 28',
      statusColor: COLORS.success,
    },
  ];

  const reportData = reports.length > 0 ? reports : defaultReports;

  const renderReportItem = ({ item }) => (
    <RecentReportItem
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
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    paddingHorizontal: SPACING.md,
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
  reportItem: {
    backgroundColor: COLORS.white,
    borderRadius: BORDER_RADIUS.lg,
    padding: SPACING.md,
    marginBottom: SPACING.sm,
    borderWidth: 1,
    borderColor: COLORS.gray200,
    ...SHADOWS.sm,
  },
  reportHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: SPACING.sm,
  },
  reportTitleContainer: {
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
  reportTitle: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.textPrimary,
  },
  reportDate: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.textSecondary,
  },
  reportFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  reportStatus: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.textSecondary,
  },
  reportActions: {
    flexDirection: 'row',
    gap: SPACING.sm,
  },
  actionButton: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  actionText: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.textSecondary,
    marginLeft: SPACING.xs,
  },
});

export default RecentReportsList;
