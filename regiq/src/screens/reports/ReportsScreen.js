import React, { useState } from 'react';
import {
  View,
  Text,
  ScrollView,
  StyleSheet,
  StatusBar,
  SafeAreaView,
} from 'react-native';
import { COLORS, TYPOGRAPHY, SPACING, BORDER_RADIUS, SHADOWS } from '../../constants/theme';

// Import components
import QuickActionsBanner from '../../components/reports/QuickActionsBanner';
import ReportsStatsCard from '../../components/reports/ReportsStatsCard';
import ReportsTabNavigation from '../../components/reports/ReportsTabNavigation';
import ReportTypesList from '../../components/reports/ReportTypesList';
import RecentReportsList from '../../components/reports/RecentReportsList';

const ReportsScreen = () => {
  const [activeTab, setActiveTab] = useState('types');
  const [reportTypes] = useState([
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
  ]);

  const handleNewReport = () => {
    console.log('New report pressed');
  };

  const handleReportCardPress = (report) => {
    console.log('Report card pressed:', report.title);
  };

  const handleExportPDF = (report) => {
    console.log('Export PDF:', report.title);
  };

  const handleExportCSV = (report) => {
    console.log('Export CSV:', report.title);
  };

  const handleViewAllReports = () => {
    console.log('View all reports pressed');
  };

  const handleReportPress = (report) => {
    console.log('Report pressed:', report.title);
  };

  const handleShareReport = (report) => {
    console.log('Share report:', report.title);
  };

  const handleDownloadReport = (report) => {
    console.log('Download report:', report.title);
  };

  const handleTabChange = (tabId) => {
    setActiveTab(tabId);
  };

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="dark-content" backgroundColor={COLORS.background} />
      
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
        {activeTab === 'types' ? (
          <ReportTypesList
            reportTypes={reportTypes}
            onReportCardPress={handleReportCardPress}
            onExportPDF={handleExportPDF}
            onExportCSV={handleExportCSV}
          />
        ) : (
          <RecentReportsList
            onViewAll={handleViewAllReports}
            onReportPress={handleReportPress}
            onShareReport={handleShareReport}
            onDownloadReport={handleDownloadReport}
          />
        )}

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
  content: {
    flex: 1,
  },
  scrollContent: {
    paddingBottom: SPACING.lg,
  },
  bottomSpacing: {
    height: SPACING.xl,
  },
});

export default ReportsScreen;
