import 'package:flutter/material.dart';
import '../../themes/app_colors.dart';
import '../../themes/app_text_styles.dart';
import '../../models/mushroom_model.dart';
import '../../services/saved_mushrooms_service.dart';

String _toTitleCase(String text) {
  return text.split(' ').map((word) {
    if (word.isEmpty) return word;
    return word[0].toUpperCase() + word.substring(1).toLowerCase();
  }).join(' ');
}

class MushroomDetailsScreen extends StatefulWidget {
  final Mushroom mushroom;

  const MushroomDetailsScreen({super.key, required this.mushroom});

  @override
  State<MushroomDetailsScreen> createState() => _MushroomDetailsScreenState();
}

class _MushroomDetailsScreenState extends State<MushroomDetailsScreen> {
  bool _isSaved = false;
  late PageController _pageController;
  int _currentPage = 0;
  final List<String> _imagePaths = [];

  @override
  void initState() {
    super.initState();
    _pageController = PageController();
    _checkIfSaved();
    _initImages();
  }

  void _initImages() {
    // Fetch image filenames stored in the offline database
    final filenames = widget.mushroom.imagePaths;
    
    if (filenames.isNotEmpty) {
      for (final file in filenames) {
        final path = 'assets/mushrooms_gallery/$file';
        _imagePaths.add(path);
      }
    } else {
      // Fallback if no images in DB
      final name = widget.mushroom.subClass.toLowerCase().replaceAll(' ', '_');
      _imagePaths.add('assets/mushrooms_gallery/${name}_1.jpg');
    }
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    // Pre-cache primary images for smoother carousel movement
    for (var i = 0; i < _imagePaths.length; i++) {
      precacheImage(AssetImage(_imagePaths[i]), context);
    }
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
    } else {
      await SavedMushroomsService().saveMushroom(widget.mushroom.toMap());
    }
    setState(() => _isSaved = !_isSaved);
    if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(_isSaved ? 'Added to favorites' : 'Removed from favorites'),
          duration: const Duration(seconds: 1),
          backgroundColor: AppColors.primary,
          behavior: SnackBarBehavior.floating,
        ),
      );
    }
  }

  @override
  void dispose() {
    _pageController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    Color classColor = AppColors.primary;
    final mc = widget.mushroom.mainClass.toLowerCase();
    if (mc == 'non_poisnous_edible') {
      classColor = AppColors.success;
    } else if (mc == 'non_poisnous_non_edible') {
      classColor = const Color(0xFF2C3E50);
    } else if (mc.contains('poisnous')) {
      classColor = AppColors.danger;
    }

    final recipes = widget.mushroom.recipesList;

    return Scaffold(
      backgroundColor: AppColors.white,
      body: CustomScrollView(
        physics: const BouncingScrollPhysics(),
        slivers: [
          SliverAppBar(
            expandedHeight: 350,
            pinned: true,
            stretch: true,
            backgroundColor: classColor,
            elevation: 0,
            leading: Padding(
              padding: const EdgeInsets.all(8.0),
              child: CircleAvatar(
                backgroundColor: Colors.black26,
                child: IconButton(
                  icon: const Icon(Icons.arrow_back_ios_new_rounded, color: Colors.white, size: 20),
                  onPressed: () => Navigator.pop(context),
                ),
              ),
            ),
            actions: [
              Padding(
                padding: const EdgeInsets.all(8.0),
                child: CircleAvatar(
                  backgroundColor: Colors.black26,
                  child: IconButton(
                    icon: Icon(_isSaved ? Icons.favorite_rounded : Icons.favorite_border_rounded, color: Colors.white),
                    onPressed: _toggleSave,
                  ),
                ),
              ),
            ],
            flexibleSpace: FlexibleSpaceBar(
              background: Stack(
                fit: StackFit.expand,
                children: [
                  PageView.builder(
                    controller: _pageController,
                    onPageChanged: (index) => setState(() => _currentPage = index),
                    itemCount: _imagePaths.length,
                    itemBuilder: (context, index) {
                      final imageWidget = Image.asset(
                        _imagePaths[index],
                        fit: BoxFit.cover,
                        cacheWidth: 800, // Optimize for detail view
                        errorBuilder: (context, error, stackTrace) {
                          return Container(
                            color: classColor.withOpacity(0.1),
                            child: Column(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                Icon(Icons.eco_rounded, color: classColor, size: 64),
                                const SizedBox(height: 12),
                                Text(
                                  'Gallery Preview',
                                  style: AppTextStyles.labelLarge.copyWith(color: classColor),
                                ),
                              ],
                            ),
                          );
                        },
                      );

                      // Only Hero the first image to avoid conflicts and maintain smooth transition from list
                      if (index == 0) {
                        return Hero(
                          tag: 'mushroom-${widget.mushroom.speciesName}',
                          child: imageWidget,
                        );
                      }
                      return imageWidget;
                    },
                  ),
                  // Gradient Overlay
                  Container(
                    decoration: BoxDecoration(
                      gradient: LinearGradient(
                        begin: Alignment.topCenter,
                        end: Alignment.bottomCenter,
                        colors: [Colors.black.withOpacity(0.3), Colors.transparent, Colors.black.withOpacity(0.7)],
                      ),
                    ),
                  ),
                  // Image Indicators (Dots)
                  Positioned(
                    bottom: 50,
                    left: 0,
                    right: 0,
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: List.generate(_imagePaths.length, (index) {
                        return AnimatedContainer(
                          duration: const Duration(milliseconds: 300),
                          margin: const EdgeInsets.symmetric(horizontal: 4),
                          width: _currentPage == index ? 20 : 8,
                          height: 8,
                          decoration: BoxDecoration(
                            color: _currentPage == index ? Colors.white : Colors.white.withOpacity(0.4),
                            borderRadius: BorderRadius.circular(4),
                          ),
                        );
                      }),
                    ),
                  ),
                ],
              ),
            ),
          ),
          SliverToBoxAdapter(
            child: Transform.translate(
              offset: const Offset(0, -30),
              child: Container(
                decoration: const BoxDecoration(
                  color: AppColors.backgroundGradientStart,
                  borderRadius: BorderRadius.vertical(top: Radius.circular(32)),
                ),
                padding: const EdgeInsets.fromLTRB(24, 32, 24, 40),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      _toTitleCase(widget.mushroom.speciesName.replaceAll('_', ' ')),
                      style: AppTextStyles.heading1.copyWith(fontSize: 32, letterSpacing: -1),
                    ),
                    const SizedBox(height: 8),
                    Row(
                      children: [
                        Icon(Icons.location_on_rounded, size: 16, color: classColor),
                        const SizedBox(width: 4),
                        Text(widget.mushroom.mainClass.replaceAll('_', ' '), style: AppTextStyles.labelSmall.copyWith(color: classColor)),
                      ],
                    ),
                    const SizedBox(height: 32),
                    
                    // Classification Grid
                    _buildInfoGrid(classColor),
                    
                    const SizedBox(height: 32),
                    
                    // Description Section
                    Text("About species", style: AppTextStyles.heading3),
                    const SizedBox(height: 12),
                    Text(widget.mushroom.description, style: AppTextStyles.bodyMedium.copyWith(color: AppColors.textSecondary, height: 1.6)),
                    
                    const SizedBox(height: 32),
                    
                    // Occurrence Section
                    _buildSectionCard(Icons.map_rounded, "Natural Habitat / Occurrence", widget.mushroom.occurrence, const Color(0xFF3498DB)),
                    
                    const SizedBox(height: 24),
                    
                    // Price / Commercial Info
                    if (widget.mushroom.pricePkr.isNotEmpty)
                      _buildSectionCard(Icons.monetization_on_rounded, "Commercial Value (PKR)", widget.mushroom.pricePkr, const Color(0xFF27AE60)),
                    
                    const SizedBox(height: 32),
                    
                    // Uses & Recipes
                    if (recipes.isNotEmpty) ...[
                      Text(widget.mushroom.mainClass.contains('Pois') ? "Usability" : "Usage & Recipes", style: AppTextStyles.heading3),
                      const SizedBox(height: 16),
                      ...recipes.map((r) => _buildRecipeItem(r, classColor)).toList(),
                    ],
                  ],
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildInfoGrid(Color color) {
    return GridView.count(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      crossAxisCount: 2,
      mainAxisSpacing: 12,
      crossAxisSpacing: 12,
      childAspectRatio: 2.2,
      children: [
        _buildMiniCard(Icons.science_rounded, "Scientific", widget.mushroom.scientificName, color),
        _buildMiniCard(Icons.health_and_safety_rounded, "Edibility", widget.mushroom.edibility, color),
        _buildMiniCard(Icons.category_rounded, "Kingdom", widget.mushroom.kingdom, color),
        _buildMiniCard(Icons.family_restroom_rounded, "Family", widget.mushroom.family, color),
      ],
    );
  }

  Widget _buildMiniCard(IconData icon, String label, String value, Color color) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        boxShadow: [BoxShadow(color: color.withOpacity(0.04), blurRadius: 10, offset: const Offset(0, 4))],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Row(
            children: [
              Icon(icon, size: 14, color: color),
              const SizedBox(width: 8),
              Text(label, style: AppTextStyles.caption.copyWith(fontSize: 10, fontWeight: FontWeight.bold)),
            ],
          ),
          const SizedBox(height: 4),
          Text(
            value.isNotEmpty ? value : "N/A",
            style: AppTextStyles.bodySmall.copyWith(fontWeight: FontWeight.bold, color: AppColors.textPrimary),
            maxLines: 1,
            overflow: TextOverflow.ellipsis,
          ),
        ],
      ),
    );
  }

  Widget _buildSectionCard(IconData icon, String title, String content, Color color) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: color.withOpacity(0.1)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(icon, color: color, size: 20),
              const SizedBox(width: 12),
              Text(title, style: AppTextStyles.labelMedium.copyWith(color: color)),
            ],
          ),
          const SizedBox(height: 12),
          Text(content, style: AppTextStyles.bodyMedium.copyWith(color: AppColors.textPrimary, height: 1.5)),
        ],
      ),
    );
  }

  Widget _buildRecipeItem(String text, Color color) {
    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: color.withOpacity(0.05),
        borderRadius: BorderRadius.circular(16),
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(Icons.check_circle_rounded, color: color, size: 18),
          const SizedBox(width: 12),
          Expanded(child: Text(text, style: AppTextStyles.bodyMedium.copyWith(height: 1.5))),
        ],
      ),
    );
  }
}
