import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, ScrollView, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { COLORS, TYPOGRAPHY, SPACING, BORDER_RADIUS, SHADOWS } from '../../constants/theme';

const SearchFilters = ({ onSearch, onFilterChange, selectedFilters = ['all'] }) => {
  const [searchText, setSearchText] = useState('');
  const [isSearchFocused, setIsSearchFocused] = useState(false);

  const filters = [
    { id: 'all', label: 'All Regions', icon: 'earth' },
    { id: 'high', label: 'High Priority', icon: 'warning' },
    { id: 'ai', label: 'AI/ML', icon: 'hardware-chip' },
    { id: 'banking', label: 'Banking', icon: 'business' },
    { id: 'crypto', label: 'Crypto', icon: 'logo-bitcoin' },
    { id: 'payments', label: 'Payments', icon: 'card' },
  ];

  const handleSearch = (text) => {
    setSearchText(text);
    onSearch?.(text);
  };

  const handleFilterPress = (filterId) => {
    onFilterChange?.(filterId);
  };

  const clearSearch = () => {
    setSearchText('');
    onSearch?.('');
  };

  const getActiveFiltersCount = () => {
    return selectedFilters.includes('all') ? 0 : selectedFilters.length;
  };

  return (
    <View style={styles.container}>
      {/* Search Bar */}
      <View style={styles.searchContainer}>
        <View style={styles.searchInputContainer}>
          <Ionicons name="search" size={16} color={COLORS.gray400} style={styles.searchIcon} />
          <TextInput
            style={[
              styles.searchInput,
              isSearchFocused && styles.searchInputFocused
            ]}
            placeholder="Search regulations..."
            placeholderTextColor={COLORS.gray400}
            value={searchText}
            onChangeText={handleSearch}
            onFocus={() => setIsSearchFocused(true)}
            onBlur={() => setIsSearchFocused(false)}
            returnKeyType="search"
            autoCapitalize="none"
            autoCorrect={false}
          />
          {searchText.length > 0 && (
            <TouchableOpacity onPress={clearSearch} style={styles.clearButton}>
              <Ionicons name="close-circle" size={16} color={COLORS.gray400} />
            </TouchableOpacity>
          )}
        </View>
      </View>

      {/* Filter Chips */}
      <ScrollView 
        horizontal 
        showsHorizontalScrollIndicator={false}
        style={styles.filtersContainer}
        contentContainerStyle={styles.filtersContent}
      >
        {filters.map((filter) => {
          const isSelected = selectedFilters.includes(filter.id);
          return (
            <TouchableOpacity
              key={filter.id}
              style={[
                styles.filterChip,
                isSelected && styles.filterChipActive
              ]}
              onPress={() => handleFilterPress(filter.id)}
              activeOpacity={0.7}
            >
              <Ionicons 
                name={filter.icon} 
                size={12} 
                color={isSelected ? COLORS.white : COLORS.gray600}
                style={styles.filterIcon}
              />
              <Text style={[
                styles.filterText,
                isSelected && styles.filterTextActive
              ]}>
                {filter.label}
              </Text>
              {filter.id !== 'all' && isSelected && (
                <View style={styles.selectedIndicator}>
                  <Ionicons name="checkmark" size={10} color={COLORS.white} />
                </View>
              )}
            </TouchableOpacity>
          );
        })}
        
        {/* Active Filters Count */}
        {getActiveFiltersCount() > 0 && (
          <View style={styles.filterCountBadge}>
            <Text style={styles.filterCountText}>{getActiveFiltersCount()}</Text>
          </View>
        )}
      </ScrollView>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: COLORS.white,
    paddingHorizontal: SPACING.md,
    paddingVertical: SPACING.sm,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.gray200,
  },
  searchContainer: {
    marginBottom: SPACING.sm,
  },
  searchInputContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: COLORS.surfaceSecondary,
    borderRadius: BORDER_RADIUS.lg,
    paddingHorizontal: SPACING.sm,
    height: 40,
    borderWidth: 1,
    borderColor: 'transparent',
  },
  searchIcon: {
    marginRight: SPACING.xs,
  },
  searchInput: {
    flex: 1,
    fontSize: TYPOGRAPHY.fontSize.sm,
    color: COLORS.textPrimary,
    paddingVertical: 0,
  },
  searchInputFocused: {
    borderColor: COLORS.primary,
  },
  clearButton: {
    padding: SPACING.xs,
  },
  filtersContainer: {
    marginHorizontal: -SPACING.md,
  },
  filtersContent: {
    paddingHorizontal: SPACING.md,
    paddingRight: SPACING.lg,
  },
  filterChip: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: COLORS.surfaceSecondary,
    paddingHorizontal: SPACING.sm,
    paddingVertical: SPACING.xs,
    borderRadius: BORDER_RADIUS.full,
    marginRight: SPACING.xs,
    minHeight: 32,
  },
  filterChipActive: {
    backgroundColor: COLORS.primary,
  },
  filterIcon: {
    marginRight: 4,
  },
  filterText: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
    color: COLORS.gray600,
  },
  filterTextActive: {
    color: COLORS.white,
  },
  selectedIndicator: {
    marginLeft: 4,
    width: 16,
    height: 16,
    borderRadius: 8,
    backgroundColor: 'rgba(255, 255, 255, 0.3)',
    alignItems: 'center',
    justifyContent: 'center',
  },
  filterCountBadge: {
    backgroundColor: COLORS.primary,
    borderRadius: BORDER_RADIUS.full,
    paddingHorizontal: SPACING.xs,
    paddingVertical: 4,
    marginLeft: SPACING.xs,
    minWidth: 24,
    alignItems: 'center',
    justifyContent: 'center',
  },
  filterCountText: {
    fontSize: 10,
    fontWeight: TYPOGRAPHY.fontWeight.bold,
    color: COLORS.white,
  },
});

export default SearchFilters;
