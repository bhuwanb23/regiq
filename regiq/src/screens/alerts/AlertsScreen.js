import React, { useState, useMemo } from 'react';
import {
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  StyleSheet,
  StatusBar,
  Dimensions,
  TextInput,
  ActivityIndicator,
  RefreshControl,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import useAlertsData from '../../hooks/useAlertsData';
import { COLORS, TYPOGRAPHY, SPACING, BORDER_RADIUS, SHADOWS } from '../../constants/theme';

const { width: screenWidth } = Dimensions.get('window');

// Map backend notification.type / category to the UI's filter buckets + visuals.
const TYPE_MAP = {
  regulation: { type: 'regulation', icon: 'scale', color: COLORS.primary },
  regulatory: { type: 'regulation', icon: 'scale', color: COLORS.primary },
  compliance: { type: 'regulation', icon: 'scale', color: COLORS.primary },
  bias: { type: 'ai-bias', icon: 'hardware-chip', color: COLORS.warning },
  ai_ethics: { type: 'ai-bias', icon: 'hardware-chip', color: COLORS.warning },
  'ai-bias': { type: 'ai-bias', icon: 'hardware-chip', color: COLORS.warning },
  risk: { type: 'risk', icon: 'trending-up', color: COLORS.info },
  default: { type: 'general', icon: 'notifications', color: COLORS.textSecondary },
};

const severityFromPriority = (priority) => {
  if (!priority) return 'low';
  const p = String(priority).toLowerCase();
  if (p === 'critical' || p === 'urgent' || p === 'high') return 'high';
  if (p === 'medium') return 'medium';
  return 'low';
};

const formatRelativeTime = (input) => {
  if (!input) return '';
  const d = typeof input === 'string' ? new Date(input) : input;
  if (Number.isNaN(d.getTime())) return String(input);
  const diff = Date.now() - d.getTime();
  const sec = Math.floor(diff / 1000);
  if (sec < 60) return `${sec}s ago`;
  const min = Math.floor(sec / 60);
  if (min < 60) return `${min} min ago`;
  const hr = Math.floor(min / 60);
  if (hr < 24) return `${hr} hour${hr === 1 ? '' : 's'} ago`;
  const day = Math.floor(hr / 24);
  return `${day} day${day === 1 ? '' : 's'} ago`;
};

const normalizeAlert = (n) => {
  const rawType = (n.type || n.category || 'default').toString().toLowerCase();
  const meta = TYPE_MAP[rawType] || TYPE_MAP.default;
  const severity = severityFromPriority(n.priority || n.severity);
  return {
    id: n.id,
    type: meta.type,
    severity,
    title: n.title || n.subject || 'Notification',
    description: n.description || n.message || n.body || '',
    time: formatRelativeTime(n.createdAt || n.created_at || n.timestamp),
    icon: meta.icon,
    color: severity === 'high' ? COLORS.error : severity === 'medium' ? COLORS.warning : meta.color,
    isRead: Boolean(n.isRead || n.status === 'read'),
    details: {
      explanation: n.details?.explanation || n.body || n.message || n.description || 'No additional details available.',
      actions: Array.isArray(n.details?.actions)
        ? n.details.actions
        : Array.isArray(n.actions)
          ? n.actions
          : [],
    },
  };
};

const AlertsScreen = ({ navigation }) => {
  const [activeFilter, setActiveFilter] = useState('all');
  const [expandedAlert, setExpandedAlert] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [showSearch, setShowSearch] = useState(false);

  const {
    alerts: rawAlerts,
    loading,
    refreshing,
    error,
    refreshAlerts,
    markAsRead,
    snooze,
  } = useAlertsData();

  const alerts = useMemo(() => (rawAlerts || []).map(normalizeAlert), [rawAlerts]);

  const filters = useMemo(() => {
    const count = (t) => alerts.filter((a) => a.type === t).length;
    return [
      { id: 'all', label: 'All', count: alerts.length, icon: null },
      { id: 'regulation', label: 'Regulation', count: count('regulation'), icon: 'scale' },
      { id: 'ai-bias', label: 'AI Bias', count: count('ai-bias'), icon: 'hardware-chip' },
      { id: 'risk', label: 'Risk Simulation', count: count('risk'), icon: 'trending-up' },
    ];
  }, [alerts]);

  const handleBack = () => {
    if (navigation?.goBack) {
      navigation.goBack();
    }
  };

  const handleFilterPress = (filterId) => {
    setActiveFilter(filterId);
  };

  const handleExpandAlert = (alertId) => {
    setExpandedAlert(expandedAlert === alertId ? null : alertId);
  };

  const handleSnoozeAlert = (alertId) => {
    snooze(alertId);
  };

  const handleMarkAsRead = (alertId) => {
    markAsRead(alertId);
  };

  const handleSearchPress = () => {
    setShowSearch(!showSearch);
    if (showSearch) {
      setSearchQuery('');
    }
  };

  const handleSearchChange = (text) => {
    setSearchQuery(text);
  };

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'high': return COLORS.error;
      case 'medium': return COLORS.warning;
      case 'low': return COLORS.success;
      default: return COLORS.textSecondary;
    }
  };

  const getSeverityBg = (severity) => {
    switch (severity) {
      case 'high': return COLORS.errorLight;
      case 'medium': return COLORS.warningLight;
      case 'low': return COLORS.successLight;
      default: return COLORS.surfaceSecondary;
    }
  };

  const filteredAlerts = alerts
    .filter(alert => activeFilter === 'all' || alert.type === activeFilter)
    .filter(alert => 
      searchQuery === '' || 
      alert.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      alert.description.toLowerCase().includes(searchQuery.toLowerCase())
    );

  return (
    <SafeAreaView style={styles.container} edges={['top', 'left', 'right']}>
      <StatusBar barStyle="light-content" backgroundColor={COLORS.primary} />
      
      {/* Header */}
      <View style={styles.header}>
        <View style={styles.headerLeft}>
          <TouchableOpacity 
            style={styles.backButton}
            onPress={handleBack}
            activeOpacity={0.7}
          >
            <Ionicons name="arrow-back" size={24} color={COLORS.white} />
          </TouchableOpacity>
          <Text style={styles.headerTitle}>Alerts</Text>
        </View>
        
        <View style={styles.headerRight}>
          <TouchableOpacity 
            style={styles.headerButton}
            onPress={handleSearchPress}
          >
            <Ionicons name="search" size={20} color={COLORS.white} />
          </TouchableOpacity>
          <TouchableOpacity style={styles.headerButton}>
            <Ionicons name="filter" size={20} color={COLORS.white} />
          </TouchableOpacity>
        </View>
      </View>

      {/* Search Bar */}
      {showSearch && (
        <View style={styles.searchContainer}>
          <View style={styles.searchInputContainer}>
            <Ionicons name="search" size={16} color={COLORS.textSecondary} style={styles.searchIcon} />
            <TextInput
              style={styles.searchInput}
              placeholder="Search alerts..."
              placeholderTextColor={COLORS.textSecondary}
              value={searchQuery}
              onChangeText={handleSearchChange}
              autoFocus={true}
            />
            {searchQuery.length > 0 && (
              <TouchableOpacity onPress={() => setSearchQuery('')}>
                <Ionicons name="close-circle" size={16} color={COLORS.textSecondary} />
              </TouchableOpacity>
            )}
          </View>
        </View>
      )}

      {/* Filter Section */}
      <View style={styles.filterSection}>
        <ScrollView 
          horizontal 
          showsHorizontalScrollIndicator={false}
          contentContainerStyle={styles.filterScrollContent}
        >
          {filters.map((filter) => (
            <TouchableOpacity
              key={filter.id}
              style={[
                styles.filterButton,
                activeFilter === filter.id && styles.filterButtonActive
              ]}
              onPress={() => handleFilterPress(filter.id)}
              activeOpacity={0.7}
            >
              {filter.icon && (
                <Ionicons 
                  name={filter.icon} 
                  size={14} 
                  color={activeFilter === filter.id ? COLORS.white : COLORS.textSecondary} 
                />
              )}
              <Text style={[
                styles.filterButtonText,
                activeFilter === filter.id && styles.filterButtonTextActive
              ]}>
                {filter.label}
              </Text>
              <View style={[
                styles.filterBadge,
                activeFilter === filter.id && styles.filterBadgeActive
              ]}>
                <Text style={[
                  styles.filterBadgeText,
                  activeFilter === filter.id && styles.filterBadgeTextActive
                ]}>
                  {filter.count}
                </Text>
              </View>
            </TouchableOpacity>
          ))}
        </ScrollView>
      </View>

      {/* Alerts List */}
      <ScrollView 
        style={styles.content}
        showsVerticalScrollIndicator={false}
        contentContainerStyle={styles.scrollContent}
        refreshControl={
          <RefreshControl
            refreshing={refreshing}
            onRefresh={refreshAlerts}
            colors={[COLORS.primary]}
            tintColor={COLORS.primary}
          />
        }
      >
        {loading && filteredAlerts.length === 0 && (
          <View style={{ paddingVertical: SPACING.xl, alignItems: 'center' }}>
            <ActivityIndicator size="large" color={COLORS.primary} />
            <Text style={{ marginTop: SPACING.sm, color: COLORS.textSecondary }}>Loading alerts...</Text>
          </View>
        )}

        {!loading && error && (
          <View style={{ paddingVertical: SPACING.xl, alignItems: 'center' }}>
            <Ionicons name="alert-circle" size={32} color={COLORS.error} />
            <Text style={{ marginTop: SPACING.sm, color: COLORS.error }}>{error}</Text>
            <TouchableOpacity onPress={refreshAlerts} style={{ marginTop: SPACING.sm }}>
              <Text style={{ color: COLORS.primary, fontWeight: '600' }}>Retry</Text>
            </TouchableOpacity>
          </View>
        )}

        {!loading && !error && filteredAlerts.length === 0 && (
          <View style={{ paddingVertical: SPACING.xl, alignItems: 'center' }}>
            <Ionicons name="checkmark-done" size={32} color={COLORS.success} />
            <Text style={{ marginTop: SPACING.sm, color: COLORS.textSecondary }}>No alerts to show</Text>
          </View>
        )}

        {filteredAlerts.map((alert) => (
          <TouchableOpacity 
            key={alert.id} 
            style={styles.alertCard}
            activeOpacity={0.95}
            onPress={() => handleExpandAlert(alert.id)}
          >
            <View style={styles.alertHeader}>
              <View style={[styles.severityDot, { backgroundColor: alert.color }]} />
              <View style={styles.alertHeaderContent}>
                <View style={styles.alertHeaderTop}>
                  <View style={styles.alertHeaderLeft}>
                    <View style={[styles.iconContainer, { backgroundColor: `${alert.color}15` }]}>
                      <Ionicons name={alert.icon} size={14} color={alert.color} />
                    </View>
                    <View style={[styles.severityBadge, { backgroundColor: getSeverityBg(alert.severity) }]}>
                      <Text style={[styles.severityBadgeText, { color: getSeverityColor(alert.severity) }]}>
                        {alert.severity.toUpperCase()}
                      </Text>
                    </View>
                  </View>
                  <Text style={styles.alertTime}>{alert.time}</Text>
                </View>
                
                <Text style={styles.alertTitle} numberOfLines={2}>
                  {alert.title}
                </Text>
                <Text style={styles.alertDescription} numberOfLines={3}>
                  {alert.description}
                </Text>
                
                <View style={styles.alertActions}>
                  <View style={styles.expandButtonContainer}>
                    <Text style={styles.expandButtonText}>
                      {expandedAlert === alert.id ? 'Hide Details' : 'View Details'}
                    </Text>
                    <Ionicons 
                      name={expandedAlert === alert.id ? "chevron-up" : "chevron-down"} 
                      size={14} 
                      color={COLORS.secondary} 
                      style={styles.expandIcon}
                    />
                  </View>
                  
                  <View style={styles.actionButtons}>
                    <TouchableOpacity 
                      style={styles.actionButton}
                      onPress={(e) => {
                        e.stopPropagation();
                        handleSnoozeAlert(alert.id);
                      }}
                      activeOpacity={0.7}
                    >
                      <Ionicons name="time" size={16} color={COLORS.textSecondary} />
                    </TouchableOpacity>
                    <TouchableOpacity 
                      style={styles.actionButton}
                      onPress={(e) => {
                        e.stopPropagation();
                        handleMarkAsRead(alert.id);
                      }}
                      activeOpacity={0.7}
                    >
                      <Ionicons name="checkmark" size={16} color={COLORS.success} />
                    </TouchableOpacity>
                  </View>
                </View>
              </View>
            </View>

            {/* Expanded Details */}
            {expandedAlert === alert.id && (
              <View style={styles.alertDetails}>
                <View style={styles.detailSection}>
                  <Text style={styles.detailSectionTitle}>💡 Detailed Explanation</Text>
                  <Text style={styles.detailSectionText}>{alert.details.explanation}</Text>
                </View>
                
                <View style={styles.detailSection}>
                  <Text style={styles.detailSectionTitle}>🎯 Suggested Actions</Text>
                  {alert.details.actions.map((action, index) => (
                    <View key={index} style={styles.actionItem}>
                      <View style={styles.actionBullet} />
                      <Text style={styles.actionText}>{action}</Text>
                    </View>
                  ))}
                </View>
              </View>
            )}
          </TouchableOpacity>
        ))}
        
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
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: SPACING.md,
    paddingVertical: SPACING.md,
    backgroundColor: COLORS.primary,
    elevation: 4,
    shadowColor: COLORS.primary,
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.2,
    shadowRadius: 4,
  },
  headerLeft: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  backButton: {
    padding: SPACING.xs,
    marginRight: SPACING.sm,
  },
  headerTitle: {
    fontSize: TYPOGRAPHY.fontSize.xl,
    fontWeight: TYPOGRAPHY.fontWeight.bold,
    color: COLORS.white,
  },
  headerRight: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  headerButton: {
    padding: SPACING.xs,
    marginLeft: SPACING.xs,
  },
  searchContainer: {
    backgroundColor: COLORS.white,
    paddingHorizontal: SPACING.md,
    paddingVertical: SPACING.sm,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.gray100,
  },
  searchInputContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: COLORS.surfaceSecondary,
    borderRadius: BORDER_RADIUS.lg,
    paddingHorizontal: SPACING.sm,
    paddingVertical: SPACING.xs,
  },
  searchIcon: {
    marginRight: SPACING.xs,
  },
  searchInput: {
    flex: 1,
    fontSize: TYPOGRAPHY.fontSize.base,
    color: COLORS.textPrimary,
    paddingVertical: SPACING.xs,
  },
  filterSection: {
    backgroundColor: COLORS.white,
    paddingVertical: SPACING.sm,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.gray100,
  },
  filterScrollContent: {
    paddingHorizontal: SPACING.md,
  },
  filterButton: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 12,
    paddingVertical: 8,
    marginRight: 8,
    backgroundColor: COLORS.surfaceSecondary,
    borderRadius: 20,
    minWidth: screenWidth < 350 ? 75 : 90,
    elevation: 1,
    shadowColor: COLORS.primary,
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 2,
  },
  filterButtonActive: {
    backgroundColor: COLORS.primary,
    elevation: 3,
    shadowOpacity: 0.15,
    shadowRadius: 4,
    transform: [{ scale: 1.02 }],
  },
  filterButtonText: {
    fontSize: 12,
    fontWeight: '600',
    color: COLORS.textSecondary,
    marginLeft: 4,
    marginRight: 4,
    letterSpacing: 0.2,
  },
  filterButtonTextActive: {
    color: COLORS.white,
  },
  filterBadge: {
    backgroundColor: COLORS.gray200,
    paddingHorizontal: 6,
    paddingVertical: 2,
    borderRadius: 12,
    minWidth: 18,
    alignItems: 'center',
    elevation: 1,
    shadowColor: COLORS.textSecondary,
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 1,
  },
  filterBadgeActive: {
    backgroundColor: 'rgba(255, 255, 255, 0.3)',
    elevation: 2,
    shadowOpacity: 0.2,
  },
  filterBadgeText: {
    fontSize: 10,
    color: COLORS.textSecondary,
    fontWeight: '600',
  },
  filterBadgeTextActive: {
    color: COLORS.white,
  },
  content: {
    flex: 1,
  },
  scrollContent: {
    padding: SPACING.md,
  },
  alertCard: {
    backgroundColor: COLORS.white,
    borderRadius: 16,
    marginBottom: 12,
    marginHorizontal: 4,
    elevation: 4,
    shadowColor: COLORS.primary,
    shadowOffset: { width: 0, height: 3 },
    shadowOpacity: 0.12,
    shadowRadius: 12,
    overflow: 'hidden',
    borderWidth: 0,
    transform: [{ scale: 1 }],
  },
  alertHeader: {
    padding: SPACING.sm,
  },
  severityDot: {
    position: 'absolute',
    top: SPACING.sm + 6,
    left: SPACING.sm,
    width: 8,
    height: 8,
    borderRadius: 4,
  },
  alertHeaderContent: {
    marginLeft: SPACING.md,
  },
  alertHeaderTop: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 4,
  },
  alertHeaderLeft: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  iconContainer: {
    width: 24,
    height: 24,
    borderRadius: 12,
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: 8,
  },
  severityBadge: {
    paddingHorizontal: 6,
    paddingVertical: 1,
    borderRadius: BORDER_RADIUS.full,
    marginLeft: 6,
  },
  severityBadgeText: {
    fontSize: 10,
    fontWeight: '600',
    letterSpacing: 0.3,
  },
  alertTime: {
    fontSize: 11,
    color: COLORS.textSecondary,
    fontWeight: '400',
  },
  alertTitle: {
    fontSize: 15,
    fontWeight: '700',
    color: COLORS.primary,
    marginBottom: 4,
    lineHeight: 20,
    letterSpacing: -0.2,
  },
  alertDescription: {
    fontSize: 13,
    color: COLORS.textSecondary,
    marginBottom: 8,
    lineHeight: 18,
    fontWeight: '400',
  },
  alertActions: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  expandButtonContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  expandButtonText: {
    fontSize: 13,
    fontWeight: '600',
    color: COLORS.secondary,
    letterSpacing: 0.2,
  },
  expandIcon: {
    marginLeft: 4,
  },
  actionButtons: {
    flexDirection: 'row',
  },
  actionButton: {
    padding: 8,
    marginLeft: 6,
    borderRadius: 8,
    backgroundColor: COLORS.surfaceSecondary,
    alignItems: 'center',
    justifyContent: 'center',
  },
  alertDetails: {
    paddingHorizontal: SPACING.sm,
    paddingBottom: SPACING.sm,
    paddingTop: SPACING.sm,
    backgroundColor: `${COLORS.primary}05`,
    borderTopWidth: 1,
    borderTopColor: COLORS.gray100,
  },
  detailSection: {
    marginBottom: 10,
  },
  detailSectionTitle: {
    fontSize: 14,
    fontWeight: '700',
    color: COLORS.primary,
    marginBottom: 6,
    letterSpacing: -0.1,
  },
  detailSectionText: {
    fontSize: 13,
    color: COLORS.textSecondary,
    lineHeight: 19,
    fontWeight: '400',
  },
  actionItem: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    marginBottom: 6,
  },
  actionBullet: {
    width: 4,
    height: 4,
    borderRadius: 2,
    backgroundColor: COLORS.secondary,
    marginTop: 7,
    marginRight: 10,
    elevation: 1,
    shadowColor: COLORS.secondary,
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.3,
    shadowRadius: 1,
  },
  actionText: {
    fontSize: 13,
    color: COLORS.textSecondary,
    flex: 1,
    lineHeight: 19,
    fontWeight: '400',
  },
  bottomSpacing: {
    height: SPACING.xl,
  },
});

export default AlertsScreen;
