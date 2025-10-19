import React, { useState } from 'react';
import {
  View,
  Text,
  ScrollView,
  StyleSheet,
  TouchableOpacity,
  RefreshControl,
  FlatList,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';

import SearchFilters from '../../components/regulations/SearchFilters';
import RegulationCard from '../../components/regulations/RegulationCard';
import UpcomingDeadlines from '../../components/regulations/UpcomingDeadlines';
import useRegulationData from '../../hooks/useRegulationData';
import { COLORS, TYPOGRAPHY, SPACING, BORDER_RADIUS, SHADOWS } from '../../constants/theme';

const RegulationIntelligenceScreen = ({ navigation }) => {
  const {
    filteredRegulations,
    deadlines,
    loading,
    refreshing,
    searchQuery,
    selectedFilters,
    viewMode,
    refreshRegulations,
    handleSearch,
    handleFilterChange,
    setViewMode,
  } = useRegulationData();

  const [bookmarkedRegulations, setBookmarkedRegulations] = useState(new Set());
  const [showTimelineView, setShowTimelineView] = useState(false);

  const handleRegulationPress = (regulation) => {
    console.log('Regulation pressed:', regulation.id);
    // Show regulation details modal or navigate
    // navigation.navigate('RegulationDetails', { regulationId: regulation.id });
  };

  const handleReadMore = (regulation) => {
    console.log('Read more pressed:', regulation.id);
    // Open external document or navigate to full details
    // You could implement a WebView modal here
  };

  const handleBookmark = (regulation) => {
    const newBookmarks = new Set(bookmarkedRegulations);
    if (newBookmarks.has(regulation.id)) {
      newBookmarks.delete(regulation.id);
    } else {
      newBookmarks.add(regulation.id);
    }
    setBookmarkedRegulations(newBookmarks);
    console.log('Bookmarked regulations:', Array.from(newBookmarks));
  };

  const handleDeadlinePress = (deadline) => {
    console.log('Deadline pressed:', deadline.id);
    // Navigate to deadline details or compliance checklist
    // navigation.navigate('DeadlineDetails', { deadlineId: deadline.id });
  };

  const handleViewAllDeadlines = () => {
    console.log('View all deadlines pressed');
    // Navigate to full deadlines screen
    // navigation.navigate('AllDeadlines');
  };

  const handleViewModeChange = (mode) => {
    setViewMode(mode);
    setShowTimelineView(mode === 'timeline');
    console.log('View mode changed to:', mode);
  };

  const renderRegulationItem = ({ item, index }) => {
    if (showTimelineView) {
      return (
        <View style={styles.timelineItem}>
          <View style={styles.timelineLine} />
          <View style={styles.timelineDot} />
          <View style={styles.timelineCard}>
            <RegulationCard
              regulation={item}
              onPress={handleRegulationPress}
              onReadMore={handleReadMore}
              onBookmark={handleBookmark}
              isBookmarked={bookmarkedRegulations.has(item.id)}
            />
          </View>
        </View>
      );
    }
    
    return (
      <RegulationCard
        regulation={item}
        onPress={handleRegulationPress}
        onReadMore={handleReadMore}
        onBookmark={handleBookmark}
        isBookmarked={bookmarkedRegulations.has(item.id)}
      />
    );
  };

  const renderEmptyState = () => (
    <View style={styles.emptyState}>
      <Ionicons name="document-text-outline" size={48} color={COLORS.gray400} />
      <Text style={styles.emptyStateTitle}>No Regulations Found</Text>
      <Text style={styles.emptyStateText}>
        Try adjusting your search or filter criteria
      </Text>
    </View>
  );

  if (loading) {
    return (
      <View style={[styles.container, styles.centerContent]}>
        <Text style={styles.loadingText}>Loading regulations...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {/* Search and Filters */}
      <SearchFilters
        onSearch={handleSearch}
        onFilterChange={handleFilterChange}
        selectedFilters={selectedFilters}
      />

      {/* View Toggle */}
      <View style={styles.viewToggleContainer}>
        <View style={styles.viewToggleHeader}>
          <Text style={styles.sectionTitle}>Latest Regulations</Text>
          <View style={styles.viewToggle}>
            <TouchableOpacity
              style={[
                styles.toggleButton,
                viewMode === 'feed' && styles.toggleButtonActive
              ]}
              onPress={() => handleViewModeChange('feed')}
            >
              <Ionicons 
                name="list" 
                size={12} 
                color={viewMode === 'feed' ? COLORS.primary : COLORS.textSecondary}
                style={styles.toggleIcon}
              />
              <Text style={[
                styles.toggleText,
                viewMode === 'feed' && styles.toggleTextActive
              ]}>
                Feed
              </Text>
            </TouchableOpacity>
            <TouchableOpacity
              style={[
                styles.toggleButton,
                viewMode === 'timeline' && styles.toggleButtonActive
              ]}
              onPress={() => handleViewModeChange('timeline')}
            >
              <Ionicons 
                name="time" 
                size={12} 
                color={viewMode === 'timeline' ? COLORS.primary : COLORS.textSecondary}
                style={styles.toggleIcon}
              />
              <Text style={[
                styles.toggleText,
                viewMode === 'timeline' && styles.toggleTextActive
              ]}>
                Timeline
              </Text>
            </TouchableOpacity>
          </View>
        </View>
      </View>

      {/* Main Content */}
      <FlatList
        data={filteredRegulations}
        renderItem={renderRegulationItem}
        keyExtractor={(item) => item.id.toString()}
        contentContainerStyle={styles.listContainer}
        showsVerticalScrollIndicator={false}
        refreshControl={
          <RefreshControl
            refreshing={refreshing}
            onRefresh={refreshRegulations}
            colors={[COLORS.primary]}
            tintColor={COLORS.primary}
          />
        }
        ListHeaderComponent={() => (
          <>
            {/* Results Summary */}
            {searchQuery.trim() || !selectedFilters.includes('all') ? (
              <View style={styles.resultsHeader}>
                <Text style={styles.resultsText}>
                  {filteredRegulations.length} regulation{filteredRegulations.length !== 1 ? 's' : ''} found
                </Text>
                {(searchQuery.trim() || !selectedFilters.includes('all')) && (
                  <TouchableOpacity
                    onPress={() => {
                      handleSearch('');
                      handleFilterChange('all');
                    }}
                  >
                    <Text style={styles.clearFiltersText}>Clear filters</Text>
                  </TouchableOpacity>
                )}
              </View>
            ) : null}
          </>
        )}
        ListFooterComponent={() => (
          <>
            {/* Upcoming Deadlines */}
            <UpcomingDeadlines
              deadlines={deadlines}
              onDeadlinePress={handleDeadlinePress}
              onViewAll={handleViewAllDeadlines}
            />
            
            {/* Bottom Spacing */}
            <View style={styles.bottomSpacing} />
          </>
        )}
        ListEmptyComponent={renderEmptyState}
        extraData={bookmarkedRegulations} // Re-render when bookmarks change
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  centerContent: {
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    fontSize: TYPOGRAPHY.fontSize.base,
    color: COLORS.textSecondary,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
  },
  viewToggleContainer: {
    backgroundColor: COLORS.white,
    paddingHorizontal: SPACING.md,
    paddingVertical: SPACING.sm,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.gray200,
  },
  viewToggleHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  sectionTitle: {
    fontSize: TYPOGRAPHY.fontSize.base,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.textPrimary,
  },
  viewToggle: {
    flexDirection: 'row',
    backgroundColor: COLORS.surfaceSecondary,
    borderRadius: BORDER_RADIUS.md,
    padding: 2,
  },
  toggleButton: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: SPACING.sm,
    paddingVertical: SPACING.xs,
    borderRadius: BORDER_RADIUS.sm,
  },
  toggleIcon: {
    marginRight: 4,
  },
  toggleButtonActive: {
    backgroundColor: COLORS.white,
    ...SHADOWS.sm,
  },
  toggleText: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.textSecondary,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
  },
  toggleTextActive: {
    color: COLORS.textPrimary,
  },
  listContainer: {
    paddingHorizontal: SPACING.md,
    paddingTop: SPACING.sm,
  },
  resultsHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: SPACING.sm,
    paddingHorizontal: SPACING.xs,
  },
  resultsText: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    color: COLORS.textSecondary,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
  },
  clearFiltersText: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.primary,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
  },
  emptyState: {
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: SPACING['3xl'],
  },
  emptyStateTitle: {
    fontSize: TYPOGRAPHY.fontSize.lg,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.textPrimary,
    marginTop: SPACING.md,
    marginBottom: SPACING.xs,
  },
  emptyStateText: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    color: COLORS.textSecondary,
    textAlign: 'center',
    paddingHorizontal: SPACING.xl,
  },
  bottomSpacing: {
    height: SPACING.xl,
  },
  timelineItem: {
    flexDirection: 'row',
    marginBottom: SPACING.md,
  },
  timelineLine: {
    width: 2,
    backgroundColor: COLORS.gray300,
    marginLeft: 10,
    marginRight: SPACING.md,
  },
  timelineDot: {
    width: 12,
    height: 12,
    borderRadius: 6,
    backgroundColor: COLORS.primary,
    position: 'absolute',
    left: 4,
    top: 20,
    zIndex: 1,
  },
  timelineCard: {
    flex: 1,
  },
});

export default RegulationIntelligenceScreen;
