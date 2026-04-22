import 'package:flutter/material.dart';
import '../../themes/app_colors.dart';
import '../../themes/app_text_styles.dart';
import '../../models/mushroom_model.dart';

String _toTitleCase(String text) {
  return text.split(' ').map((word) {
    if (word.isEmpty) return word;
    return word[0].toUpperCase() + word.substring(1).toLowerCase();
  }).join(' ');
}

class MushroomCardWidget extends StatelessWidget {
  final Mushroom mushroom;
  final VoidCallback? onTap;

  const MushroomCardWidget({
    super.key,
    required this.mushroom,
    this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    // Determine the theme color based on mainClass
    Color accentColor = AppColors.primary;
    final mc = mushroom.mainClass.toLowerCase();
    if (mc == 'non_poisnous_edible') {
      accentColor = AppColors.success;
    } else if (mc == 'non_poisnous_non_edible') {
      accentColor = const Color(0xFF2C3E50);
    } else if (mc.contains('poisnous')) {
      accentColor = AppColors.danger;
    }

    // Get thumbnail from DB imagePaths
    final thumbnail = mushroom.imagePaths.isNotEmpty 
        ? 'assets/mushrooms_gallery/${mushroom.imagePaths.first}' 
        : 'assets/mushrooms_dataset/${mushroom.mainClass}/${mushroom.speciesName.toLowerCase().replaceAll(' ', '_')}.jpg';

    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 4, vertical: 6),
      child: GestureDetector(
        onTap: onTap,
        child: Container(
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.circular(20),
            boxShadow: [
              BoxShadow(
                color: accentColor.withOpacity(0.08),
                blurRadius: 12,
                offset: const Offset(0, 4),
              ),
            ],
          ),
          child: ClipRRect(
            borderRadius: BorderRadius.circular(20),
            child: Stack(
              children: [
                Row(
                  children: [
                    // Professional Image Section with Hero
                    Container(
                      width: 100,
                      height: 100,
                      decoration: BoxDecoration(
                        gradient: LinearGradient(
                          begin: Alignment.topLeft,
                          end: Alignment.bottomRight,
                          colors: [
                            accentColor.withOpacity(0.1),
                            accentColor.withOpacity(0.02),
                          ],
                        ),
                      ),
                      child: Hero(
                        tag: 'mushroom-${mushroom.speciesName}',
                        child: Image.asset(
                          thumbnail,
                          width: 100,
                          height: 100,
                          cacheWidth: 300, // Optimize for list
                          fit: BoxFit.cover,
                          errorBuilder: (context, error, stackTrace) {
                            return Container(
                              color: accentColor.withOpacity(0.05),
                              child: Center(
                                child: Icon(Icons.eco_rounded, color: accentColor, size: 32),
                              ),
                            );
                          },
                        ),
                      ),
                    ),
                    const SizedBox(width: 16),
                    // Content Section
                    Expanded(
                      child: Padding(
                        padding: const EdgeInsets.only(right: 12),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              mushroom.speciesName,
                              style: AppTextStyles.labelLarge.copyWith(fontSize: 16),
                              maxLines: 1,
                              overflow: TextOverflow.ellipsis,
                            ),
                            const SizedBox(height: 4),
                            Text(
                              mushroom.description,
                              style: AppTextStyles.bodySmall.copyWith(fontSize: 12),
                              maxLines: 2,
                              overflow: TextOverflow.ellipsis,
                            ),
                          ],
                        ),
                      ),
                    ),
                    // Action Indicator
                    Padding(
                      padding: const EdgeInsets.only(right: 12),
                      child: Icon(
                        Icons.arrow_forward_ios_rounded,
                        color: AppColors.iconColorLight.withOpacity(0.5),
                        size: 16,
                      ),
                    ),
                  ],
                ),
                // Accent Bar for categorization
                Positioned(
                  left: 0,
                  top: 0,
                  bottom: 0,
                  width: 4,
                  child: Container(color: accentColor),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
