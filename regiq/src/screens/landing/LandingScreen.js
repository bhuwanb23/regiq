import React, { useEffect, useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  Animated,
  Dimensions,
  StatusBar,
  Image,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';

const { width, height } = Dimensions.get('window');

const LandingScreen = ({ onFinish }) => {
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const scaleAnim = useRef(new Animated.Value(0.8)).current;
  const iconAnims = useRef([
    new Animated.Value(0),
    new Animated.Value(0),
    new Animated.Value(0),
    new Animated.Value(0),
    new Animated.Value(0),
    new Animated.Value(0),
  ]).current;

  useEffect(() => {
    // Start animations
    const startAnimations = () => {
      // Logo animation
      Animated.parallel([
        Animated.timing(fadeAnim, {
          toValue: 1,
          duration: 1000,
          useNativeDriver: true,
        }),
        Animated.spring(scaleAnim, {
          toValue: 1,
          tension: 50,
          friction: 7,
          useNativeDriver: true,
        }),
      ]).start();

      // Staggered icon animations
      iconAnims.forEach((anim, index) => {
        Animated.timing(anim, {
          toValue: 1,
          duration: 800,
          delay: 500 + index * 150,
          useNativeDriver: true,
        }).start();
      });

      // Auto navigate after animations
      setTimeout(() => {
        if (onFinish) onFinish();
      }, 3000);
    };

    startAnimations();
  }, []);

  const fintechIcons = [
    { name: 'shield-checkmark', top: '15%', left: '10%', size: 32 },
    { name: 'analytics', top: '20%', right: '15%', size: 28 },
    { name: 'card', top: '35%', left: '8%', size: 30 },
    { name: 'trending-up', top: '65%', right: '12%', size: 34 },
    { name: 'lock-closed', top: '75%', left: '15%', size: 26 },
    { name: 'globe', top: '80%', right: '20%', size: 30 },
  ];

  return (
    <>
      <StatusBar barStyle="light-content" backgroundColor="#6B46C1" />
      <LinearGradient
        colors={['#8B5CF6', '#7C3AED', '#6B46C1', '#5B21B6']}
        start={{ x: 0, y: 0 }}
        end={{ x: 1, y: 1 }}
        style={styles.container}
      >
        {/* Floating Background Shapes */}
        <View style={styles.backgroundShapes}>
          <View style={[styles.circle, styles.circle1]} />
          <View style={[styles.circle, styles.circle2]} />
          <View style={[styles.circle, styles.circle3]} />
          <View style={[styles.rectangle, styles.rectangle1]} />
          <View style={[styles.rectangle, styles.rectangle2]} />
        </View>

        {/* Fintech Icons */}
        {fintechIcons.map((icon, index) => (
          <Animated.View
            key={index}
            style={[
              styles.floatingIcon,
              {
                top: icon.top,
                left: icon.left,
                right: icon.right,
                opacity: iconAnims[index],
                transform: [
                  {
                    translateY: iconAnims[index].interpolate({
                      inputRange: [0, 1],
                      outputRange: [20, 0],
                    }),
                  },
                ],
              },
            ]}
          >
            <Ionicons
              name={icon.name}
              size={icon.size}
              color="rgba(255, 255, 255, 0.3)"
            />
          </Animated.View>
        ))}

        {/* Main Content */}
        <Animated.View
          style={[
            styles.content,
            {
              opacity: fadeAnim,
              transform: [{ scale: scaleAnim }],
            },
          ]}
        >
          {/* Logo Container */}
          <View style={styles.logoContainer}>
            <View style={styles.logoBackground}>
              <Image
                source={require('../../../assets/REGIQ.png')}
                style={styles.logo}
                resizeMode="contain"
              />
            </View>
          </View>

          {/* App Name */}
          <Text style={styles.appName}>REGIQ</Text>
          <Text style={styles.tagline}>Regulation Intelligence Quotient</Text>
        </Animated.View>

        {/* Loading Indicator */}
        <Animated.View style={[styles.loadingContainer, { opacity: fadeAnim }]}>
          <View style={styles.loadingBar}>
            <Animated.View
              style={[
                styles.loadingProgress,
                {
                  width: fadeAnim.interpolate({
                    inputRange: [0, 1],
                    outputRange: ['0%', '100%'],
                  }),
                },
              ]}
            />
          </View>
          <Text style={styles.loadingText}>Initializing AI Copilot...</Text>
        </Animated.View>
      </LinearGradient>
    </>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    position: 'relative',
  },
  backgroundShapes: {
    position: 'absolute',
    width: '100%',
    height: '100%',
  },
  circle: {
    position: 'absolute',
    backgroundColor: 'rgba(255, 255, 255, 0.05)',
    borderRadius: 1000,
  },
  circle1: {
    width: 200,
    height: 200,
    top: -50,
    right: -50,
  },
  circle2: {
    width: 150,
    height: 150,
    bottom: 100,
    left: -30,
  },
  circle3: {
    width: 80,
    height: 80,
    top: '40%',
    left: '10%',
  },
  rectangle: {
    position: 'absolute',
    backgroundColor: 'rgba(255, 255, 255, 0.03)',
    borderRadius: 20,
  },
  rectangle1: {
    width: 100,
    height: 60,
    top: '25%',
    right: '20%',
    transform: [{ rotate: '15deg' }],
  },
  rectangle2: {
    width: 80,
    height: 40,
    bottom: '30%',
    left: '15%',
    transform: [{ rotate: '-20deg' }],
  },
  floatingIcon: {
    position: 'absolute',
  },
  content: {
    alignItems: 'center',
    paddingHorizontal: 40,
  },
  logoContainer: {
    marginBottom: 30,
  },
  logoBackground: {
    width: 120,
    height: 120,
    backgroundColor: '#FFFFFF',
    borderRadius: 60,
    alignItems: 'center',
    justifyContent: 'center',
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 10,
    },
    shadowOpacity: 0.3,
    shadowRadius: 20,
    elevation: 10,
  },
  logo: {
    width: 80,
    height: 80,
  },
  appName: {
    fontSize: 42,
    fontWeight: '900',
    color: '#FFFFFF',
    letterSpacing: 3,
    marginBottom: 8,
    textShadowColor: 'rgba(0, 0, 0, 0.3)',
    textShadowOffset: { width: 0, height: 2 },
    textShadowRadius: 4,
  },
  tagline: {
    fontSize: 16,
    fontWeight: '600',
    color: '#E5E7EB',
    marginBottom: 60,
    letterSpacing: 1,
    textAlign: 'center',
  },
  loadingContainer: {
    position: 'absolute',
    bottom: 80,
    alignItems: 'center',
  },
  loadingBar: {
    width: 200,
    height: 4,
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
    borderRadius: 2,
    marginBottom: 12,
    overflow: 'hidden',
  },
  loadingProgress: {
    height: '100%',
    backgroundColor: '#FFFFFF',
    borderRadius: 2,
  },
  loadingText: {
    color: '#E5E7EB',
    fontSize: 12,
    fontWeight: '500',
  },
});

export default LandingScreen;
