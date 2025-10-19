import React from 'react';
import { View, StyleSheet } from 'react-native';
import { SPACING } from '../../constants/theme';
import ReportTypeCard from './ReportTypeCard';

const ReportTypesList = ({ 
  reportTypes,
  onReportCardPress,
  onExportPDF,
  onExportCSV
}) => {
  return (
    <View style={styles.container}>
      {reportTypes.map((report) => (
        <ReportTypeCard
          key={report.id}
          title={report.title}
          description={report.description}
          icon={report.icon}
          iconColor={report.iconColor}
          iconBackground={report.iconBackground}
          stats={report.stats}
          generatedDate={report.generatedDate}
          onCardPress={() => onReportCardPress(report)}
          onExportPDF={() => onExportPDF(report)}
          onExportCSV={() => onExportCSV(report)}
        />
      ))}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    paddingHorizontal: SPACING.md,
  },
});

export default ReportTypesList;
