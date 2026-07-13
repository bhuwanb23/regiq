import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  ScrollView,
  StyleSheet,
  StatusBar,
  Alert,
  Linking,
} from 'react-native';
// Removed SafeAreaView import since it's handled by AppLayout
import { COLORS, TYPOGRAPHY, SPACING, BORDER_RADIUS, SHADOWS } from '../../constants/theme';

// Import components
import QuickActionsBanner from '../../components/reports/QuickActionsBanner';
import ReportsStatsCard from '../../components/reports/ReportsStatsCard';
import ReportsTabNavigation from '../../components/reports/ReportsTabNavigation';
import ReportTypesList from '../../components/reports/ReportTypesList';
import RecentReportsList from '../../components/reports/RecentReportsList';
import ReportGenerator from '../../components/reports/ReportGenerator';
import ReportTemplates from '../../components/reports/ReportTemplates';

// Import hook for report data
import useReportData from '../../hooks/useReportData';

const ReportsScreen = () => {
  const [activeTab, setActiveTab] = useState('generator');
  const [templates] = useState([
    {
      id: '1',
      name: 'Compliance Summary',
      description: 'Standard regulatory compliance report with charts and metrics',
      templateType: 'compliance',
      updatedAt: '2025-10-15T10:30:00Z'
    },
    {
      id: '2',
      name: 'Bias Analysis',
      description: 'Detailed AI model bias assessment with visualizations',
      templateType: 'bias',
      updatedAt: '2025-10-10T14:20:00Z'
    },
    {
      id: '3',
      name: 'Risk Simulation',
      description: 'Stress testing and scenario analysis report',
      templateType: 'risk',
      updatedAt: '2025-10-05T09:15:00Z'
    }
  ]);

  // Use the report data hook
  const {
    loading,
    error,
    reports,
    selectedReport,
    fetchReports,
    createReport,
    scheduleReportGeneration,
    setSelectedReport,
  } = useReportData();

  // Refresh data on mount
  useEffect(() => {
    fetchReports();
  }, []);

  const handleNewReport = () => {
    console.log('New report pressed');
    setActiveTab('generator');
  };

  const handleGenerateReport = async (reportData) => {
    try {
      await createReport(reportData);
      Alert.alert('Success', 'Report generated successfully');
      // Switch to recent reports tab
      setActiveTab('recent');
    } catch (err) {
      Alert.alert('Error', 'Failed to generate report');
    }
  };

  const handleScheduleReport = async (scheduleData) => {
    try {
      await scheduleReportGeneration(scheduleData);
      Alert.alert('Success', 'Report scheduled successfully');
    } catch (err) {
      Alert.alert('Error', 'Failed to schedule report');
    }
  };

  const handleReportCardPress = (report) => {
    console.log('Report card pressed:', report.title);
  };

  const handleExportPDF = async (report) => {
    try {
      // In a real implementation, this would download the PDF
      Alert.alert('Export PDF', `Would export ${report.title} as PDF`);
    } catch (err) {
      Alert.alert('Error', 'Failed to export PDF');
    }
  };

  const handleExportCSV = async (report) => {
    try {
      // In a real implementation, this would download the CSV
      Alert.alert('Export CSV', `Would export ${report.title} as CSV`);
    } catch (err) {
      Alert.alert('Error', 'Failed to export CSV');
    }
  };

  const handleViewAllReports = () => {
    console.log('View all reports pressed');
    setActiveTab('recent');
  };

  const handleReportPress = (report) => {
    console.log('Report pressed:', report.title);
    setSelectedReport(report);
  };

  const handleShareReport = (report) => {
    console.log('Share report:', report.title);
  };

  const handleDownloadReport = (report) => {
    console.log('Download report:', report.title);
  };

  const handleSelectTemplate = (template) => {
    console.log('Selected template:', template.name);
  };

  const handleManageTemplates = () => {
    console.log('Manage templates pressed');
  };

  const handleTabChange = (tabId) => {
    setActiveTab(tabId);
  };

  // Mock report types data
  const reportTypes = [
    {
      id: 1,
      title: 'Regulation Compliance Summary',
      description: 'Comprehensive overview of regulatory adherence',
      icon: 'shield-checkmark',
      iconColor: COLORS.secondary,
      iconBackground: `${COLORS.secondary}20`,
      stats: [
        { value: '98%', label: 'Compliance', color: COLORS.secondary },
        { value: '12', label: 'Regulations', color: COLORS.primary },
        { value: '2', label: 'Alerts', color: COLORS.accent },
      ],
      generatedDate: 'Oct 19, 2024',
    },
    {
      id: 2,
      title: 'AI Bias Audit',
      description: 'Algorithmic fairness and bias assessment',
      icon: 'hardware-chip',
      iconColor: COLORS.accent,
      iconBackground: `${COLORS.accent}20`,
      stats: [
        { value: '94%', label: 'Fair Score', color: COLORS.secondary },
        { value: '8', label: 'Models', color: COLORS.primary },
        { value: '1', label: 'High Risk', color: COLORS.accent },
      ],
      generatedDate: 'Oct 18, 2024',
    },
    {
      id: 3,
      title: 'Risk Simulation Report',
      description: 'Stress testing and scenario analysis',
      icon: 'trending-up',
      iconColor: COLORS.error,
      iconBackground: `${COLORS.error}20`,
      stats: [
        { value: '7.2%', label: 'Max Loss', color: COLORS.error },
        { value: '15', label: 'Scenarios', color: COLORS.primary },
        { value: '3', label: 'Critical', color: COLORS.accent },
      ],
      generatedDate: 'Oct 17, 2024',
    },
  ];

  return (
    // Removed SafeAreaView wrapper since it's handled by AppLayout
    <View style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor={COLORS.primary} />
      
      <ScrollView 
        style={styles.content}
        showsVerticalScrollIndicator={false}
        contentContainerStyle={styles.scrollContent}
      >
        {/* Quick Actions Banner */}
        <QuickActionsBanner onNewReport={handleNewReport} />

        {/* Stats Card - Always Visible */}
        <ReportsStatsCard />

        {/* Tab Navigation */}
        <ReportsTabNavigation 
          activeTab={activeTab}
          onTabChange={handleTabChange}
        />

        {/* Tab Content */}
        {activeTab === 'generator' && (
          <>
            <ReportGenerator 
              onGenerateReport={handleGenerateReport}
              onScheduleReport={handleScheduleReport}
              loading={loading}
            />
            <ReportTemplates 
              templates={templates}
              onSelectTemplate={handleSelectTemplate}
              onManageTemplates={handleManageTemplates}
            />
          </>
        )}

        {activeTab === 'types' && (
          <ReportTypesList
            reportTypes={reportTypes}
            onReportCardPress={handleReportCardPress}
            onExportPDF={handleExportPDF}
            onExportCSV={handleExportCSV}
          />
        )}

        {activeTab === 'recent' && (
          <RecentReportsList
            reports={reports}
            onViewAll={handleViewAllReports}
            onReportPress={handleReportPress}
            onShareReport={handleShareReport}
            onDownloadReport={handleDownloadReport}
          />
        )}

        {/* Bottom Spacing */}
        <View style={styles.bottomSpacing} />
      </ScrollView>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  content: {
    flex: 1,
  },
  scrollContent: {
    paddingBottom: SPACING.lg,
    paddingTop: SPACING.sm, // Reduced top padding
  },
  bottomSpacing: {
    height: SPACING.md, // Reduced bottom spacing
  },
});

export default ReportsScreen;