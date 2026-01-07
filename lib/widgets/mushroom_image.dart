import 'package:flutter/material.dart';
import '../themes/app_colors.dart';

/// Optimized mushroom image widget with caching and loading states
class MushroomImage extends StatelessWidget {
  final String subClass;
  final double width;
  final double height;
  final double borderRadius;
  final BoxFit fit;

  const MushroomImage({
    super.key,
    required this.subClass,
    this.width = 60,
    this.height = 60,
    this.borderRadius = 12,
    this.fit = BoxFit.cover,
  });

  @override
  Widget build(BuildContext context) {
    return ClipRRect(
      borderRadius: BorderRadius.circular(borderRadius),
      child: Image.asset(
        'assets/images/mushrooms/$subClass.png',
        width: width,
        height: height,
        fit: fit,
        cacheWidth: (width * 2).toInt(), // Cache at 2x for retina
        cacheHeight: (height * 2).toInt(),
        errorBuilder: (context, error, stackTrace) {
          return Container(
            width: width,
            height: height,
            decoration: BoxDecoration(
              color: AppColors.primary.withOpacity(0.1),
              borderRadius: BorderRadius.circular(borderRadius),
            ),
            child: Icon(
              Icons.eco_rounded,
              color: AppColors.primary,
              size: width * 0.5,
            ),
          );
        },
        frameBuilder: (context, child, frame, wasSynchronouslyLoaded) {
          if (wasSynchronouslyLoaded) {
            return child;
          }
          return AnimatedOpacity(
            opacity: frame == null ? 0 : 1,
            duration: const Duration(milliseconds: 200),
            curve: Curves.easeOut,
            child: child,
          );
        },
      ),
    );
  }
}

/// Placeholder widget for loading states
class MushroomImagePlaceholder extends StatelessWidget {
  final double width;
  final double height;
  final double borderRadius;

  const MushroomImagePlaceholder({
    super.key,
    this.width = 60,
    this.height = 60,
    this.borderRadius = 12,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      width: width,
      height: height,
      decoration: BoxDecoration(
        color: AppColors.primary.withOpacity(0.1),
        borderRadius: BorderRadius.circular(borderRadius),
      ),
      child: Icon(
        Icons.eco_rounded,
        color: AppColors.primary.withOpacity(0.5),
        size: width * 0.5,
      ),
    );
  }
}
