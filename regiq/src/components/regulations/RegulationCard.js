import React, { useState } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, Animated } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { COLORS, TYPOGRAPHY, SPACING, BORDER_RADIUS, SHADOWS } from '../../constants/theme';

const RegulationCard = ({ regulation, onPress, onReadMore, onBookmark, isBookmarked = false }) => {
  const [expanded, setExpanded] = useState(false);
  const [animation] = useState(new Animated.Value(0));
  const [bookmarkAnimation] = useState(new Animated.Value(1));

  const {
    id,
    title,
    description,
    priority,
    region,
    category,
    effectiveDate,
    timeAgo,
    tags = [],
    fullDetails,
  } = regulation;

  const getPriorityColor = (priority) => {
    switch (priority?.toLowerCase()) {
      case 'critical':
        return COLORS.error;
      case 'high':
        return COLORS.warning;
      case 'medium':
        return COLORS.info;
      case 'low':
        return COLORS.success;
      default:
        return COLORS.gray400;
    }
  };

  const getCategoryIcon = (category) => {
    switch (category?.toLowerCase()) {
      case 'ai/ml':
        return 'hardware-chip';
      case 'banking':
        return 'business';
      case 'crypto':
        return 'logo-bitcoin';
      case 'payments':
        return 'card';
      default:
        return 'document-text';
    }
  };

  const toggleExpanded = () => {
    const toValue = expanded ? 0 : 1;
    setExpanded(!expanded);
    
    Animated.spring(animation, {
      toValue,
      tension: 100,
      friction: 8,
      useNativeDriver: false,
    }).start();
  };

  const handleBookmark = () => {
    // Animate bookmark button
    Animated.sequence([
      Animated.timing(bookmarkAnimation, {
        toValue: 1.3,
        duration: 150,
        useNativeDriver: true,
      }),
      Animated.timing(bookmarkAnimation, {
        toValue: 1,
        duration: 150,
        useNativeDriver: true,
      }),
    ]).start();
    
    onBookmark?.(regulation);
  };

  const handleCardPress = () => {
    onPress?.(regulation);
  };

  const handleReadMorePress = () => {
    onReadMore?.(regulation);
  };

  const expandedHeight = animation.interpolate({
    inputRange: [0, 1],
    outputRange: [0, 140], // Approximate height of expanded content
  });

  const rotateIcon = animation.interpolate({
    inputRange: [0, 1],
    outputRange: ['0deg', '180deg'],
  });

  const fadeIn = animation.interpolate({
    inputRange: [0, 1],
    outputRange: [0, 1],
  });

  return (
    <TouchableOpacity 
      style={styles.container} 
      onPress={handleCardPress}
      activeOpacity={0.95}
    >
      {/* Main Card Content */}
      <View style={styles.cardContent}>
        {/* Header with Priority, Region, and Bookmark */}
        <View style={styles.header}>
          <View style={styles.leftHeader}>
            <View style={styles.priorityContainer}>
              <View style={[
                styles.priorityDot, 
                { backgroundColor: getPriorityColor(priority) }
              ]} />
              <Text style={[
                styles.priorityText,
                { color: getPriorityColor(priority) }
              ]}>
                {priority}
              </Text>
            </View>
            <Text style={styles.regionText}>{region} • {timeAgo}</Text>
          </View>
          
          <TouchableOpacity 
            style={styles.bookmarkButton}
            onPress={handleBookmark}
            hitSlop={{ top: 10, bottom: 10, left: 10, right: 10 }}
          >
            <Animated.View style={{ transform: [{ scale: bookmarkAnimation }] }}>
              <Ionicons 
                name={isBookmarked ? 'bookmark' : 'bookmark-outline'} 
                size={16} 
                color={isBookmarked ? COLORS.accent : COLORS.gray400} 
              />
            </Animated.View>
          </TouchableOpacity>
        </View>

        {/* Title and Description */}
        <Text style={styles.title} numberOfLines={2}>{title}</Text>
        <Text style={styles.description} numberOfLines={3}>{description}</Text>

        {/* Footer with Category and Actions */}
        <View style={styles.footer}>
          <View style={styles.metaInfo}>
            <View style={styles.categoryContainer}>
              <Ionicons 
                name={getCategoryIcon(category)} 
                size={12} 
                color={COLORS.gray500} 
              />
              <Text style={styles.categoryText}>{category}</Text>
            </View>
            <View style={styles.dateContainer}>
              <Ionicons name="calendar" size={12} color={COLORS.gray500} />
              <Text style={styles.dateText}>{effectiveDate}</Text>
            </View>
          </View>
          
          <TouchableOpacity 
            style={styles.readMoreButton}
            onPress={toggleExpanded}
            hitSlop={{ top: 5, bottom: 5, left: 5, right: 5 }}
          >
            <Text style={styles.readMoreText}>
              {expanded ? 'Less' : 'More'}
            </Text>
            <Animated.View style={{ transform: [{ rotate: rotateIcon }] }}>
              <Ionicons 
                name="chevron-down" 
                size={12} 
                color={COLORS.primary} 
              />
            </Animated.View>
          </TouchableOpacity>
        </View>
      </View>

      {/* Expandable Details */}
      {fullDetails && (
        <Animated.View style={[styles.expandedContainer, { height: expandedHeight }]}>
          <Animated.View style={[styles.expandedContent, { opacity: fadeIn }]}>
            <Text style={styles.expandedTitle}>Key Requirements</Text>
            <Text style={styles.expandedText} numberOfLines={4}>
              {fullDetails}
            </Text>
            
            {tags.length > 0 && (
              <View style={styles.tagsContainer}>
                {tags.slice(0, 3).map((tag, index) => (
                  <TouchableOpacity key={index} style={styles.tag}>
                    <Text style={styles.tagText}>{tag}</Text>
                  </TouchableOpacity>
                ))}
              </View>
            )}
            
            <View style={styles.expandedActions}>
              <TouchableOpacity 
                style={styles.fullDocumentButton}
                onPress={handleReadMorePress}
              >
                <Ionicons name="document-text" size={12} color={COLORS.primary} />
                <Text style={styles.fullDocumentText}>View Document</Text>
              </TouchableOpacity>
              
              <TouchableOpacity 
                style={styles.shareButton}
                onPress={() => console.log('Share regulation:', regulation.id)}
              >
                <Ionicons name="share-outline" size={12} color={COLORS.secondary} />
                <Text style={styles.shareText}>Share</Text>
              </TouchableOpacity>
            </View>
          </Animated.View>
        </Animated.View>
      )}
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: COLORS.white,
    borderRadius: BORDER_RADIUS.lg,
    marginBottom: SPACING.sm,
    overflow: 'hidden',
    ...SHADOWS.sm,
  },
  cardContent: {
    padding: SPACING.md,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: SPACING.sm,
  },
  leftHeader: {
    flex: 1,
  },
  priorityContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  priorityDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    marginRight: SPACING.xs,
  },
  priorityText: {
    fontSize: 10,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
    textTransform: 'capitalize',
  },
  regionText: {
    fontSize: 10,
    color: COLORS.gray500,
    marginTop: 2,
  },
  bookmarkButton: {
    padding: SPACING.xs,
    marginTop: -SPACING.xs,
    marginRight: -SPACING.xs,
  },
  title: {
    fontSize: TYPOGRAPHY.fontSize.base,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.textPrimary,
    marginBottom: SPACING.xs,
    lineHeight: 20,
  },
  description: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    color: COLORS.textSecondary,
    lineHeight: 18,
    marginBottom: SPACING.sm,
  },
  footer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  metaInfo: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  categoryContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginRight: SPACING.md,
  },
  categoryText: {
    fontSize: 10,
    color: COLORS.gray500,
    marginLeft: 4,
  },
  dateContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  dateText: {
    fontSize: 10,
    color: COLORS.gray500,
    marginLeft: 4,
  },
  readMoreButton: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: SPACING.xs,
    paddingHorizontal: SPACING.sm,
    borderRadius: BORDER_RADIUS.sm,
    backgroundColor: `${COLORS.primary}10`,
  },
  readMoreText: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.primary,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
    marginRight: 4,
  },
  expandedContainer: {
    overflow: 'hidden',
    backgroundColor: COLORS.surfaceSecondary,
  },
  expandedContent: {
    padding: SPACING.md,
    paddingTop: SPACING.sm,
  },
  expandedTitle: {
    fontSize: TYPOGRAPHY.fontSize.sm,
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    color: COLORS.textPrimary,
    marginBottom: SPACING.xs,
  },
  expandedText: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.textSecondary,
    lineHeight: 16,
    marginBottom: SPACING.sm,
  },
  tagsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginBottom: SPACING.sm,
  },
  tag: {
    backgroundColor: `${COLORS.primary}20`,
    paddingHorizontal: SPACING.xs,
    paddingVertical: 2,
    borderRadius: BORDER_RADIUS.sm,
    marginRight: SPACING.xs,
    marginBottom: 4,
  },
  tagText: {
    fontSize: 9,
    color: COLORS.primary,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
  },
  expandedActions: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  fullDocumentButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: `${COLORS.primary}15`,
    paddingHorizontal: SPACING.sm,
    paddingVertical: SPACING.xs,
    borderRadius: BORDER_RADIUS.sm,
  },
  fullDocumentText: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.primary,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
    marginLeft: 4,
  },
  shareButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: `${COLORS.secondary}15`,
    paddingHorizontal: SPACING.sm,
    paddingVertical: SPACING.xs,
    borderRadius: BORDER_RADIUS.sm,
  },
  shareText: {
    fontSize: TYPOGRAPHY.fontSize.xs,
    color: COLORS.secondary,
    fontWeight: TYPOGRAPHY.fontWeight.medium,
    marginLeft: 4,
  },
});

export default RegulationCard;
