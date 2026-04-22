import 'package:flutter/material.dart';
import '../../themes/app_colors.dart';
import '../../themes/app_text_styles.dart';
import '../../models/mushroom_model.dart';
import '../../services/db_helper.dart';
import '../search/search_results_screen.dart';
import 'mushroom_details_screen.dart';
import '../../widgets/cards/mushroom_card.dart';

class ExploreMushroomsScreen extends StatefulWidget {
  const ExploreMushroomsScreen({super.key});

  @override
  State<ExploreMushroomsScreen> createState() => _ExploreMushroomsScreenState();
}

class _ExploreMushroomsScreenState extends State<ExploreMushroomsScreen> with SingleTickerProviderStateMixin {
  Map<String, List<Mushroom>> _groupedMushrooms = {};
  bool _isLoading = true;
  late AnimationController _animationController;

  @override
  void initState() {
    super.initState();
    _animationController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 800),
    );
    _loadMushrooms();
  }

  @override
  void dispose() {
    _animationController.dispose();
    super.dispose();
  }

  Future<void> _loadMushrooms() async {
    if (_groupedMushrooms.isNotEmpty) {
      setState(() => _isLoading = false);
      _animationController.forward();
      return;
    }
    
    setState(() => _isLoading = true);
    try {
      final rows = await DatabaseHelper.instance.getMushrooms();
      
      // Perform grouping in a single pass
      final Map<String, List<Mushroom>> grouped = {};
      for (final row in rows) {
        final mushroom = Mushroom.fromMap(row);
        grouped.putIfAbsent(mushroom.mainClass, () => []).add(mushroom);
      }

      if (mounted) {
        setState(() {
          _groupedMushrooms = grouped;
          _isLoading = false;
        });
        _animationController.forward();
      }
    } catch (e) {
      debugPrint("Error loading mushrooms: $e");
      if (mounted) setState(() => _isLoading = false);
    }
  }

  String _formatClassName(String dbValue) {
    switch (dbValue) {
      case 'Non_Poisnous_Edible': return 'Non-Poisonous, Edible';
      case 'Non_Poisnous_Non_Edible': return 'Non-Poisonous, Non-Edible';
      case 'Poisnous_Non_Useable': return 'Poisonous, Non-Useable';
      case 'Poisnous_Useable': return 'Poisonous, Useable';
      default: return dbValue.replaceAll('_', ' ');
    }
  }

  Color _getCardColor(String mainClass) {
    final lower = mainClass.toLowerCase();
    if (lower == 'non_poisnous_edible') {
      return AppColors.success;
    } else if (lower == 'non_poisnous_non_edible') {
      return const Color(0xFF2C3E50); // Dark Blue/Slate
    } else if (lower == 'poisnous_useable') {
      return AppColors.danger;
    } else if (lower == 'poisnous_non_useable') {
      return const Color(0xFFC0392B); // Deeper Red
    }
    return AppColors.info;
  }

  IconData _getCardIcon(String mainClass) {
    final lower = mainClass.toLowerCase();
    if (lower == 'non_poisnous_edible') {
      return Icons.eco_rounded;
    } else if (lower == 'non_poisnous_non_edible') {
      return Icons.biotech_rounded;
    } else if (lower == 'poisnous_useable') {
      return Icons.warning_amber_rounded;
    } else {
      return Icons.dangerous_rounded;
    }
  }

  void _openMushroomList(String mainClass, List<Mushroom> mushrooms) {
    Navigator.push(
      context,
      PageRouteBuilder(
        transitionDuration: const Duration(milliseconds: 400),
        pageBuilder: (context, animation, secondaryAnimation) => MushroomListScreen(
          mainClass: mainClass,
          mushrooms: mushrooms,
        ),
        transitionsBuilder: (context, animation, secondaryAnimation, child) {
          return FadeTransition(
            opacity: animation,
            child: SlideTransition(
              position: Tween<Offset>(
                begin: const Offset(0.05, 0),
                end: Offset.zero,
              ).animate(CurvedAnimation(parent: animation, curve: Curves.easeOutQuart)),
              child: child,
            ),
          );
        },
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.backgroundGradientStart,
      body: CustomScrollView(
        physics: const BouncingScrollPhysics(),
        slivers: [
          SliverAppBar(
            expandedHeight: 120,
            floating: true,
            pinned: true,
            elevation: 0,
            backgroundColor: AppColors.backgroundGradientStart,
            flexibleSpace: FlexibleSpaceBar(
              titlePadding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
              title: Text(
                "Explore Nature",
                style: AppTextStyles.heading2.copyWith(color: AppColors.textPrimary, fontSize: 22),
              ),
              centerTitle: false,
            ),
            actions: [
              Padding(
                padding: const EdgeInsets.only(right: 12),
                child: IconButton(
                  icon: const Icon(Icons.search_rounded, color: AppColors.textPrimary),
                  onPressed: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const SearchResultsScreen())),
                ),
              ),
            ],
          ),
          SliverToBoxAdapter(
            child: _isLoading
                ? const Center(child: Padding(padding: EdgeInsets.only(top: 100), child: CircularProgressIndicator(color: AppColors.primary)))
                : Padding(
                    padding: const EdgeInsets.all(20),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text('Discovery Categories', style: AppTextStyles.caption.copyWith(letterSpacing: 1.2, fontWeight: FontWeight.bold)),
                        const SizedBox(height: 16),
                        ...List.generate(_groupedMushrooms.length, (index) {
                          final entry = _groupedMushrooms.entries.elementAt(index);
                          return _buildCategoryCard(
                            title: _formatClassName(entry.key),
                            count: entry.value.length,
                            color: _getCardColor(entry.key),
                            icon: _getCardIcon(entry.key),
                            onTap: () => _openMushroomList(entry.key, entry.value),
                            index: index,
                          );
                        }),
                      ],
                    ),
                  ),
          ),
        ],
      ),
    );
  }

  Widget _buildCategoryCard({
    required String title,
    required int count,
    required Color color,
    required IconData icon,
    required VoidCallback onTap,
    required int index,
  }) {
    return AnimatedBuilder(
      animation: _animationController,
      builder: (context, child) {
        final animationVal = Curves.easeOutQuart.transform(
          ((_animationController.value - (index * 0.1)).clamp(0.0, 1.0)),
        );
        return Opacity(
          opacity: animationVal,
          child: Transform.translate(
            offset: Offset(0, 40 * (1 - animationVal)),
            child: child,
          ),
        );
      },
      child: GestureDetector(
        onTap: onTap,
        child: Container(
          margin: const EdgeInsets.only(bottom: 16),
          padding: const EdgeInsets.all(24),
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.circular(24),
            boxShadow: [
              BoxShadow(
                color: color.withOpacity(0.06),
                blurRadius: 20,
                offset: const Offset(0, 10),
              ),
            ],
          ),
          child: Row(
            children: [
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  gradient: LinearGradient(
                    colors: [color.withOpacity(0.2), color.withOpacity(0.05)],
                    begin: Alignment.topLeft,
                    end: Alignment.bottomRight,
                  ),
                  borderRadius: BorderRadius.circular(18),
                ),
                child: Icon(icon, color: color, size: 32),
              ),
              const SizedBox(width: 20),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(title, style: AppTextStyles.labelLarge.copyWith(fontSize: 18)),
                    const SizedBox(height: 4),
                    Text('$count Species cataloged', style: AppTextStyles.bodySmall.copyWith(color: AppColors.textSecondary)),
                  ],
                ),
              ),
              Container(
                padding: const EdgeInsets.all(10),
                decoration: BoxDecoration(
                  color: AppColors.backgroundGradientEnd,
                  shape: BoxShape.circle,
                ),
                child: Icon(Icons.arrow_forward_ios_rounded, color: color, size: 14),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class MushroomListScreen extends StatefulWidget {
  final String mainClass;
  final List<Mushroom> mushrooms;

  const MushroomListScreen({
    super.key,
    required this.mainClass,
    required this.mushrooms,
  });

  @override
  State<MushroomListScreen> createState() => _MushroomListScreenState();
}

class _MushroomListScreenState extends State<MushroomListScreen> {
  final TextEditingController _searchController = TextEditingController();
  List<Mushroom> _filteredMushrooms = [];

  @override
  void initState() {
    super.initState();
    _filteredMushrooms = widget.mushrooms;
  }

  void _filterMushrooms(String query) {
    if (query.isEmpty) {
      setState(() => _filteredMushrooms = widget.mushrooms);
      return;
    }
    final lowerQuery = query.toLowerCase();
    setState(() {
      _filteredMushrooms = widget.mushrooms.where((m) => m.speciesName.toLowerCase().contains(lowerQuery)).toList();
    });
  }

  String _formatClassName(String dbValue) {
    switch (dbValue) {
      case 'Non_Poisnous_Edible': return 'Edible Species';
      case 'Non_Poisnous_Non_Edible': return 'Non-Edible Species';
      case 'Poisnous_Non_Useable': return 'Highly Toxic';
      case 'Poisnous_Useable': return 'Medicinal / Toxic';
      default: return dbValue.replaceAll('_', ' ');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.backgroundGradientStart,
      appBar: AppBar(
        title: Text(_formatClassName(widget.mainClass), style: AppTextStyles.heading3),
        backgroundColor: Colors.transparent,
        elevation: 0,
        centerTitle: true,
        foregroundColor: AppColors.textPrimary,
      ),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
            child: Container(
              decoration: BoxDecoration(
                boxShadow: [
                  BoxShadow(color: Colors.black.withOpacity(0.04), blurRadius: 15, offset: const Offset(0, 8)),
                ],
              ),
              child: TextField(
                controller: _searchController,
                onChanged: _filterMushrooms,
                decoration: InputDecoration(
                  hintText: 'Search species...',
                  filled: true,
                  fillColor: Colors.white,
                  prefixIcon: const Icon(Icons.search_rounded, color: AppColors.primary),
                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(16), borderSide: BorderSide.none),
                  contentPadding: const EdgeInsets.symmetric(vertical: 16),
                ),
              ),
            ),
          ),
          Expanded(
            child: ListView.builder(
              physics: const BouncingScrollPhysics(),
              padding: const EdgeInsets.fromLTRB(16, 12, 16, 40),
              itemCount: _filteredMushrooms.length,
              itemBuilder: (context, index) {
                final mushroom = _filteredMushrooms[index];
                return MushroomCardWidget(
                  mushroom: mushroom,
                  onTap: () {
                    Navigator.push(
                      context,
                      PageRouteBuilder(
                        transitionDuration: const Duration(milliseconds: 500),
                        pageBuilder: (context, animation, secondaryAnimation) => MushroomDetailsScreen(mushroom: mushroom),
                        transitionsBuilder: (context, animation, secondaryAnimation, child) {
                          return FadeTransition(opacity: animation, child: child);
                        },
                      ),
                    );
                  },
                );
              },
            ),
          ),
        ],
      ),
    );
  }

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }
}
