import 'package:flutter/material.dart';
import '../../themes/app_colors.dart';
import '../../themes/app_text_styles.dart';
import '../../models/mushroom_model.dart';
import '../../services/saved_mushrooms_service.dart';

class MushroomDetailsScreen extends StatefulWidget {
  final Mushroom mushroom;

  const MushroomDetailsScreen({super.key, required this.mushroom});

  @override
  State<MushroomDetailsScreen> createState() => _MushroomDetailsScreenState();
}

class _MushroomDetailsScreenState extends State<MushroomDetailsScreen> {
  bool _isSaved = false;

  @override
  void initState() {
    super.initState();
    _checkIfSaved();
  }

  Future<void> _checkIfSaved() async {
    final saved = await SavedMushroomsService().isSaved(widget.mushroom.speciesName);
    if (mounted) {
      setState(() => _isSaved = saved);
    }
  }

  Future<void> _toggleSave() async {
    if (_isSaved) {
      await SavedMushroomsService().removeMushroom(widget.mushroom.speciesName);
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: const Text('Removed from saved'),
          backgroundColor: AppColors.textSecondary,
          behavior: SnackBarBehavior.floating,
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
        ),
      );
    } else {
      await SavedMushroomsService().saveMushroom(widget.mushroom.toMap());
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: const Text('Saved to favorites'),
          backgroundColor: AppColors.success,
          behavior: SnackBarBehavior.floating,
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
        ),
      );
    }
    setState(() => _isSaved = !_isSaved);
  }

  Color _getClassColor() {
    final lower = widget.mushroom.mainClass.toLowerCase();
    if (lower.contains('poisnous') && lower.contains('useable')) {
      return AppColors.warning;
    } else if (lower.contains('poisnous')) {
      return AppColors.danger;
    } else if (lower.contains('edible')) {
      return AppColors.success;
    } else {
      return AppColors.info;
    }
  }

  IconData _getClassIcon() {
    final lower = widget.mushroom.mainClass.toLowerCase();
    if (lower.contains('poisnous')) {
      return Icons.warning_rounded;
    } else if (lower.contains('edible')) {
      return Icons.eco_rounded;
    } else {
      return Icons.science_rounded;
    }
  }

  @override
  Widget build(BuildContext context) {
    final recipes = widget.mushroom.recipesList;
    final classColor = _getClassColor();
    
    return Scaffold(
      backgroundColor: AppColors.backgroundGradientStart,
      body: CustomScrollView(
        slivers: [
          // Custom App Bar with Image
          SliverAppBar(
            expandedHeight: 280,
            pinned: true,
            backgroundColor: AppColors.primary,
            foregroundColor: Colors.white,
            actions: [
              GestureDetector(
                onTap: _toggleSave,
                child: Container(
                  margin: const EdgeInsets.only(right: 16),
                  padding: const EdgeInsets.all(10),
                  decoration: BoxDecoration(
                    color: Colors.white.withOpacity(0.2),
                    shape: BoxShape.circle,
                  ),
                  child: Icon(
                    _isSaved ? Icons.bookmark_rounded : Icons.bookmark_outline_rounded,
                    color: Colors.white,
                    size: 22,
                  ),
                ),
              ),
            ],
            flexibleSpace: FlexibleSpaceBar(
              background: Stack(
                fit: StackFit.expand,
                children: [
                  Image.asset(
                    'assets/images/mushrooms/${widget.mushroom.speciesName}.png',
                    fit: BoxFit.cover,
                    errorBuilder: (context, error, stackTrace) {
                      return Container(
                        color: AppColors.primary.withOpacity(0.1),
                        child: Icon(
                          Icons.eco_rounded,
                          size: 80,
                          color: AppColors.primary,
                        ),
                      );
                    },
                  ),
                  // Gradient overlay
                  Container(
                    decoration: BoxDecoration(
                      gradient: LinearGradient(
                        begin: Alignment.topCenter,
                        end: Alignment.bottomCenter,
                        colors: [
                          Colors.transparent,
                          Colors.black.withOpacity(0.6),
                        ],
                      ),
                    ),
                  ),
                  // Title at bottom
                  Positioned(
                    bottom: 16,
                    left: 16,
                    right: 16,
                    child: Text(
                      widget.mushroom.speciesName.replaceAll('_', ' '),
                      style: AppTextStyles.heading2.copyWith(color: Colors.white),
                    ),
                  ),
                ],
              ),
            ),
          ),

          // Content
          SliverToBoxAdapter(
            child: Container(
              padding: const EdgeInsets.all(20),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Classification Card
                  _buildInfoCard(
                    icon: _getClassIcon(),
                    title: 'Classification',
                    content: widget.mushroom.mainClass.replaceAll('_', ' '),
                    color: classColor,
                  ),

                  const SizedBox(height: 12),

                  // Scientific Name Card
                  if (widget.mushroom.scientificName.isNotEmpty)
                    Padding(
                      padding: const EdgeInsets.only(bottom: 12),
                      child: _buildInfoCard(
                        icon: Icons.science_outlined,
                        title: 'Scientific Name',
                        content: widget.mushroom.scientificName,
                        color: AppColors.primary,
                      ),
                    ),

                  // Description Card
                  if (widget.mushroom.description.isNotEmpty)
                    Padding(
                      padding: const EdgeInsets.only(bottom: 12),
                      child: _buildInfoCard(
                        icon: Icons.description_outlined,
                        title: 'Description',
                        content: widget.mushroom.description,
                        color: AppColors.info,
                      ),
                    ),

                  // Habitat Card
                  if (widget.mushroom.habitat.isNotEmpty)
                    Padding(
                      padding: const EdgeInsets.only(bottom: 12),
                      child: _buildInfoCard(
                        icon: Icons.forest_rounded,
                        title: 'Habitat',
                        content: widget.mushroom.habitat,
                        color: AppColors.success,
                      ),
                    ),

                  // Taste & Smell Card
                  if (widget.mushroom.tasteSmell.isNotEmpty)
                    Padding(
                      padding: const EdgeInsets.only(bottom: 12),
                      child: _buildInfoCard(
                        icon: Icons.restaurant_rounded,
                        title: 'Taste & Smell',
                        content: widget.mushroom.tasteSmell,
                        color: AppColors.accent,
                      ),
                    ),

                  // Cap Card
                  if (widget.mushroom.cap.isNotEmpty)
                    Padding(
                      padding: const EdgeInsets.only(bottom: 12),
                      child: _buildInfoCard(
                        icon: Icons.circle,
                        title: 'Cap',
                        content: widget.mushroom.cap,
                        color: const Color(0xFF8B4513),
                      ),
                    ),

                  // Gills Card
                  if (widget.mushroom.gills.isNotEmpty)
                    Padding(
                      padding: const EdgeInsets.only(bottom: 12),
                      child: _buildInfoCard(
                        icon: Icons.view_list_rounded,
                        title: 'Gills',
                        content: widget.mushroom.gills,
                        color: const Color(0xFF9B59B6),
                      ),
                    ),

                  // Stem Card
                  if (widget.mushroom.stem.isNotEmpty)
                    Padding(
                      padding: const EdgeInsets.only(bottom: 12),
                      child: _buildInfoCard(
                        icon: Icons.straighten_rounded,
                        title: 'Stem',
                        content: widget.mushroom.stem,
                        color: const Color(0xFF27AE60),
                      ),
                    ),

                  // Frequency Card
                  if (widget.mushroom.frequency.isNotEmpty)
                    Padding(
                      padding: const EdgeInsets.only(bottom: 12),
                      child: _buildInfoCard(
                        icon: Icons.bar_chart_rounded,
                        title: 'Frequency',
                        content: widget.mushroom.frequency,
                        color: const Color(0xFF3498DB),
                      ),
                    ),

                  // Found Card
                  if (widget.mushroom.found.isNotEmpty)
                    Padding(
                      padding: const EdgeInsets.only(bottom: 12),
                      child: _buildInfoCard(
                        icon: Icons.location_on_rounded,
                        title: 'Found',
                        content: widget.mushroom.found,
                        color: AppColors.warning,
                      ),
                    ),

                  const SizedBox(height: 12),

                  // Recipes Section
                  Text('Recipes', style: AppTextStyles.heading3),
                  const SizedBox(height: 12),
                  
                  if (recipes.isEmpty)
                    Container(
                      width: double.infinity,
                      padding: const EdgeInsets.all(16),
                      decoration: BoxDecoration(
                        color: AppColors.white,
                        borderRadius: BorderRadius.circular(16),
                        boxShadow: AppColors.softShadow,
                      ),
                      child: Row(
                        children: [
                          Container(
                            padding: const EdgeInsets.all(12),
                            decoration: BoxDecoration(
                              color: AppColors.textHint.withOpacity(0.1),
                              borderRadius: BorderRadius.circular(12),
                            ),
                            child: Icon(Icons.no_food_rounded, color: AppColors.textHint, size: 24),
                          ),
                          const SizedBox(width: 16),
                          Expanded(
                            child: Text(
                              'No recipes available for this mushroom',
                              style: AppTextStyles.bodyMedium.copyWith(color: AppColors.textSecondary),
                            ),
                          ),
                        ],
                      ),
                    )
                  else
                    Container(
                      width: double.infinity,
                      padding: const EdgeInsets.all(16),
                      decoration: BoxDecoration(
                        color: AppColors.white,
                        borderRadius: BorderRadius.circular(16),
                        boxShadow: AppColors.softShadow,
                      ),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            children: [
                              Container(
                                padding: const EdgeInsets.all(10),
                                decoration: BoxDecoration(
                                  color: AppColors.accent.withOpacity(0.1),
                                  borderRadius: BorderRadius.circular(10),
                                ),
                                child: Icon(Icons.menu_book_rounded, color: AppColors.accent, size: 20),
                              ),
                              const SizedBox(width: 12),
                              Text(
                                '${recipes.length} Recipe${recipes.length > 1 ? 's' : ''} Available',
                                style: AppTextStyles.labelMedium,
                              ),
                            ],
                          ),
                          const SizedBox(height: 16),
                          ...recipes.map((recipe) => Padding(
                            padding: const EdgeInsets.only(bottom: 10),
                            child: Row(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Container(
                                  margin: const EdgeInsets.only(top: 6),
                                  width: 8,
                                  height: 8,
                                  decoration: BoxDecoration(
                                    color: AppColors.accent,
                                    shape: BoxShape.circle,
                                  ),
                                ),
                                const SizedBox(width: 12),
                                Expanded(
                                  child: Text(
                                    recipe,
                                    style: AppTextStyles.bodyMedium.copyWith(height: 1.4),
                                  ),
                                ),
                              ],
                            ),
                          )).toList(),
                        ],
                      ),
                    ),

                  const SizedBox(height: 32),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildInfoCard({
    required IconData icon,
    required String title,
    required String content,
    required Color color,
  }) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: AppColors.white,
        borderRadius: BorderRadius.circular(16),
        boxShadow: AppColors.softShadow,
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: color.withOpacity(0.1),
              borderRadius: BorderRadius.circular(12),
            ),
            child: Icon(icon, color: color, size: 24),
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(title, style: AppTextStyles.caption),
                const SizedBox(height: 4),
                Text(
                  content,
                  style: AppTextStyles.bodyMedium.copyWith(height: 1.4),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
