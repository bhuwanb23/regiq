import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { Svg, Circle, Text as SvgText } from 'react-native-svg';
import { COLORS, TYPOGRAPHY, COMPLIANCE_COLORS } from '../../constants/theme';

const ComplianceGauge = ({ score = 0, size = 120, strokeWidth = 8 }) => {
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const strokeDasharray = circumference;
  const strokeDashoffset = circumference - (score / 100) * circumference;
  
  // Determine color based on score
  const getScoreColor = (score) => {
    if (score >= 90) return COMPLIANCE_COLORS.excellent;
    if (score >= 70) return COMPLIANCE_COLORS.good;
    if (score >= 50) return COMPLIANCE_COLORS.fair;
    return COMPLIANCE_COLORS.poor;
  };

  const getScoreLabel = (score) => {
    if (score >= 90) return 'Excellent';
    if (score >= 70) return 'Good';
    if (score >= 50) return 'Fair';
    return 'Needs Attention';
  };

  const scoreColor = getScoreColor(score);
  const scoreLabel = getScoreLabel(score);

  return (
    <View style={styles.container}>
      <View style={[styles.gaugeContainer, { width: size, height: size }]}>
        <Svg width={size} height={size} style={styles.svg}>
          {/* Background Circle */}
          <Circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke={COLORS.gray200}
            strokeWidth={strokeWidth}
            fill="transparent"
          />
          
          {/* Progress Circle */}
          <Circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke={scoreColor}
            strokeWidth={strokeWidth}
            fill="transparent"
            strokeDasharray={strokeDasharray}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            transform={`rotate(-90 ${size / 2} ${size / 2})`}
          />
        </Svg>
        
        {/* Score Text Overlay */}
        <View style={styles.scoreContainer}>
          <Text style={[styles.scoreText, { color: scoreColor }]}>
            {Math.round(score)}
          </Text>
          <Text style={styles.scoreLabel}>
            {scoreLabel}
          </Text>
        </View>
      </View>
      
      <Text style={styles.title}>Compliance Health Score</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
  },
  gaugeContainer: {
    position: 'relative',
    justifyContent: 'center',
    alignItems: 'center',
  },
  svg: {
    position: 'absolute',
  },
  scoreContainer: {
    alignItems: 'center',
    justifyContent: 'center',
  },
  scoreText: {
    fontSize: TYPOGRAPHY.fontSize['3xl'],
    fontWeight: TYPOGRAPHY.fontWeight.bold,
    lineHeight: TYPOGRAPHY.fontSize['3xl'] * 1.2,
  },
  scoreLabel: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    color: COLORS.textSecondary,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
    marginTop: 2,
  },
  title: {
    fontSize: TYPOGRAPHY.fontSize.base,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.textPrimary,
    marginTop: 12,
    textAlign: 'center',
  },
});

export default ComplianceGauge;
