import React from 'react';
import { TouchableOpacity, Text, StyleSheet, ActivityIndicator } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { COLORS, TYPOGRAPHY, SPACING, BORDER_RADIUS, SHADOWS } from '../../constants/theme';

const ActionButton = ({
  title,
  onPress,
  variant = 'primary', // primary, secondary, outline, danger
  size = 'medium', // small, medium, large
  icon,
  iconPosition = 'left', // left, right
  loading = false,
  disabled = false,
  style,
  textStyle,
  ...props
}) => {
  const getButtonStyle = () => {
    const baseStyle = [styles.button];
    
    // Size styles
    switch (size) {
      case 'small':
        baseStyle.push(styles.buttonSmall);
        break;
      case 'large':
        baseStyle.push(styles.buttonLarge);
        break;
      default:
        baseStyle.push(styles.buttonMedium);
    }
    
    // Variant styles
    switch (variant) {
      case 'secondary':
        baseStyle.push(styles.buttonSecondary);
        break;
      case 'outline':
        baseStyle.push(styles.buttonOutline);
        break;
      case 'danger':
        baseStyle.push(styles.buttonDanger);
        break;
      default:
        baseStyle.push(styles.buttonPrimary);
    }
    
    // Disabled state
    if (disabled || loading) {
      baseStyle.push(styles.buttonDisabled);
    }
    
    return baseStyle;
  };

  const getTextStyle = () => {
    const baseStyle = [styles.buttonText];
    
    // Size text styles
    switch (size) {
      case 'small':
        baseStyle.push(styles.buttonTextSmall);
        break;
      case 'large':
        baseStyle.push(styles.buttonTextLarge);
        break;
      default:
        baseStyle.push(styles.buttonTextMedium);
    }
    
    // Variant text styles
    switch (variant) {
      case 'secondary':
        baseStyle.push(styles.buttonTextSecondary);
        break;
      case 'outline':
        baseStyle.push(styles.buttonTextOutline);
        break;
      case 'danger':
        baseStyle.push(styles.buttonTextDanger);
        break;
      default:
        baseStyle.push(styles.buttonTextPrimary);
    }
    
    return baseStyle;
  };

  const getIconColor = () => {
    if (disabled || loading) return COLORS.gray400;
    
    switch (variant) {
      case 'outline':
        return COLORS.primary;
      case 'secondary':
        return COLORS.secondary;
      case 'danger':
        return COLORS.white;
      default:
        return COLORS.white;
    }
  };

  const renderContent = () => {
    if (loading) {
      return (
        <ActivityIndicator 
          size="small" 
          color={variant === 'outline' ? COLORS.primary : COLORS.white} 
        />
      );
    }

    const iconColor = getIconColor();
    const iconSize = size === 'small' ? 16 : size === 'large' ? 24 : 20;

    if (icon && iconPosition === 'left') {
      return (
        <>
          <Ionicons name={icon} size={iconSize} color={iconColor} style={styles.iconLeft} />
          <Text style={[getTextStyle(), textStyle]}>{title}</Text>
        </>
      );
    }

    if (icon && iconPosition === 'right') {
      return (
        <>
          <Text style={[getTextStyle(), textStyle]}>{title}</Text>
          <Ionicons name={icon} size={iconSize} color={iconColor} style={styles.iconRight} />
        </>
      );
    }

    return <Text style={[getTextStyle(), textStyle]}>{title}</Text>;
  };

  return (
    <TouchableOpacity
      style={[getButtonStyle(), style]}
      onPress={onPress}
      disabled={disabled || loading}
      activeOpacity={0.8}
      {...props}
    >
      {renderContent()}
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  button: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    borderRadius: BORDER_RADIUS.md,
    ...SHADOWS.sm,
  },
  
  // Size styles
  buttonSmall: {
    paddingHorizontal: SPACING.sm,
    paddingVertical: SPACING.xs,
    minHeight: 32,
  },
  buttonMedium: {
    paddingHorizontal: SPACING.md,
    paddingVertical: SPACING.sm,
    minHeight: 44,
  },
  buttonLarge: {
    paddingHorizontal: SPACING.lg,
    paddingVertical: SPACING.md,
    minHeight: 52,
  },
  
  // Variant styles
  buttonPrimary: {
    backgroundColor: COLORS.primary,
  },
  buttonSecondary: {
    backgroundColor: COLORS.secondary,
  },
  buttonOutline: {
    backgroundColor: 'transparent',
    borderWidth: 1,
    borderColor: COLORS.primary,
  },
  buttonDanger: {
    backgroundColor: COLORS.error,
  },
  buttonDisabled: {
    backgroundColor: COLORS.gray300,
    opacity: 0.6,
  },
  
  // Text styles
  buttonText: {
    fontWeight: TYPOGRAPHY.fontWeight.semibold,
    textAlign: 'center',
  },
  buttonTextSmall: {
    fontSize: TYPOGRAPHY.fontSize.sm,
  },
  buttonTextMedium: {
    fontSize: TYPOGRAPHY.fontSize.base,
  },
  buttonTextLarge: {
    fontSize: TYPOGRAPHY.fontSize.lg,
  },
  buttonTextPrimary: {
    color: COLORS.white,
  },
  buttonTextSecondary: {
    color: COLORS.white,
  },
  buttonTextOutline: {
    color: COLORS.primary,
  },
  buttonTextDanger: {
    color: COLORS.white,
  },
  
  // Icon styles
  iconLeft: {
    marginRight: SPACING.xs,
  },
  iconRight: {
    marginLeft: SPACING.xs,
  },
});

export default ActionButton;
