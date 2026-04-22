import 'package:flutter/material.dart';

class AppColors {
  // Primary palette - Natural green tones
  static const Color primary = Color(0xFF2E7D32);
  static const Color primaryLight = Color(0xFF4CAF50);
  static const Color primaryDark = Color(0xFF1B5E20);
  
  // Background gradients
  static const Color backgroundGradientStart = Color(0xFFE8F5E9);
  static const Color backgroundGradientEnd = Color(0xFFF1F8E9);
  
  // Accent colors
  static const Color accent = Color(0xFFFF7043);
  static const Color accentLight = Color(0xFFFFAB91);
  
  // Neutral colors
  static const Color white = Colors.white;
  static const Color surface = Color(0xFFFAFAFA);
  static const Color cardBackground = Colors.white;
  
  // Text colors
  static const Color textPrimary = Color(0xFF212121);
  static const Color textSecondary = Color(0xFF757575);
  static const Color textHint = Color(0xFFBDBDBD);
  
  // Icon colors
  static const Color iconColor = Color(0xFF424242);
  static const Color iconColorLight = Color(0xFF9E9E9E);
  
  // Status colors
  static const Color success = Color(0xFF4CAF50);
  static const Color warning = Color(0xFFFFA726);
  static const Color danger = Color(0xFFEF5350);
  static const Color info = Color(0xFF42A5F5);
  
  // Shadows
  static List<BoxShadow> get cardShadow => [
    BoxShadow(
      color: Colors.black.withOpacity(0.08),
      blurRadius: 16,
      offset: const Offset(0, 4),
    ),
  ];
  
  static List<BoxShadow> get softShadow => [
    BoxShadow(
      color: Colors.black.withOpacity(0.04),
      blurRadius: 8,
      offset: const Offset(0, 2),
    ),
  ];
  
  // Legacy support
  static const Color redAccent = Color(0xFFFF5C5C);
  static const Color bottomNavIcon = Color(0xFF9E9E9E);
}
