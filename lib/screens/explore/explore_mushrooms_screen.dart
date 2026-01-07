//version jango - updated with search and premium design
import 'package:flutter/material.dart';
import '../../themes/app_colors.dart';
import '../../themes/app_text_styles.dart';
import '../../models/mushroom_model.dart';
import '../../services/db_helper.dart';
import '../search/search_results_screen.dart';
import 'mushroom_details_screen.dart';

class ExploreMushroomsScreen extends StatefulWidget {
  const ExploreMushroomsScreen({super.key});

  @override
  State<ExploreMushroomsScreen> createState() => _ExploreMushroomsScreenState();
}

class _ExploreMushroomsScreenState extends State<ExploreMushroomsScreen> {
  Map<String, List<Mushroom>> _groupedMushrooms = {};
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadMushrooms();
  }

  Future<void> _loadMushrooms() async {
    setState(() => _isLoading = true);
    try {
      final rows = await DatabaseHelper.instance.getMushrooms();
      final mushrooms = rows.map((row) => Mushroom.fromMap(row)).toList();

      Map<String, List<Mushroom>> grouped = {};
      for (var m in mushrooms) {
        if (!grouped.containsKey(m.mainClass)) {
          grouped[m.mainClass] = [];
        }
        grouped[m.mainClass]!.add(m);
      }

      setState(() {
        _groupedMushrooms = grouped;
        _isLoading = false;
      });
    } catch (e) {
      print("❌ Error loading mushrooms: $e");
      setState(() => _isLoading = false);
    }
  }

  Color _getCardColor(String mainClass) {
    final lower = mainClass.toLowerCase();
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

  IconData _getCardIcon(String mainClass) {
    final lower = mainClass.toLowerCase();
    if (lower.contains('poisnous')) {
      return Icons.warning_rounded;
    } else if (lower.contains('edible')) {
      return Icons.eco_rounded;
    } else {
      return Icons.science_rounded;
    }
  }

  void _openMushroomList(String mainClass, List<Mushroom> mushrooms) {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (_) => MushroomListScreen(
          mainClass: mainClass,
          mushrooms: mushrooms,
        ),
      ),
    );
  }

  void _openSearch() {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (_) => const SearchResultsScreen(),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.backgroundGradientStart,
      appBar: AppBar(
        title: const Text("Explore"),
        backgroundColor: Colors.transparent,
        elevation: 0,
        foregroundColor: AppColors.textPrimary,
        actions: [
          IconButton(
            icon: const Icon(Icons.search_rounded),
            onPressed: _openSearch,
          ),
        ],
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator(color: AppColors.primary))
          : SingleChildScrollView(
              padding: const EdgeInsets.all(20),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Search bar
                  GestureDetector(
                    onTap: _openSearch,
                    child: Container(
                      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
                      decoration: BoxDecoration(
                        color: AppColors.white,
                        borderRadius: BorderRadius.circular(14),
                        boxShadow: AppColors.softShadow,
                      ),
                      child: Row(
                        children: [
                          Icon(Icons.search_rounded, color: AppColors.iconColorLight),
                          const SizedBox(width: 12),
                          Text(
                            'Search all mushrooms...',
                            style: AppTextStyles.bodyMedium.copyWith(color: AppColors.textHint),
                          ),
                        ],
                      ),
                    ),
                  ),
                  
                  const SizedBox(height: 28),
                  
                  Text('Categories', style: AppTextStyles.heading3),
                  const SizedBox(height: 16),
                  
                  // Category cards
                  ..._groupedMushrooms.entries.map((entry) {
                    final mainClass = entry.key;
                    final mushrooms = entry.value;
                    final color = _getCardColor(mainClass);
                    final icon = _getCardIcon(mainClass);

                    return Padding(
                      padding: const EdgeInsets.only(bottom: 16),
                      child: _buildCategoryCard(
                        title: mainClass.replaceAll('_', ' '),
                        count: mushrooms.length,
                        color: color,
                        icon: icon,
                        onTap: () => _openMushroomList(mainClass, mushrooms),
                      ),
                    );
                  }).toList(),
                ],
              ),
            ),
    );
  }

  Widget _buildCategoryCard({
    required String title,
    required int count,
    required Color color,
    required IconData icon,
    required VoidCallback onTap,
  }) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.all(20),
        decoration: BoxDecoration(
          color: AppColors.white,
          borderRadius: BorderRadius.circular(20),
          boxShadow: AppColors.cardShadow,
        ),
        child: Row(
          children: [
            Container(
              padding: const EdgeInsets.all(14),
              decoration: BoxDecoration(
                color: color.withOpacity(0.1),
                borderRadius: BorderRadius.circular(14),
              ),
              child: Icon(icon, color: color, size: 28),
            ),
            const SizedBox(width: 16),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    title,
                    style: AppTextStyles.labelLarge,
                  ),
                  const SizedBox(height: 4),
                  Text(
                    '$count species',
                    style: AppTextStyles.bodySmall,
                  ),
                ],
              ),
            ),
            Container(
              padding: const EdgeInsets.all(8),
              decoration: BoxDecoration(
                color: color.withOpacity(0.1),
                shape: BoxShape.circle,
              ),
              child: Icon(
                Icons.arrow_forward_ios_rounded,
                color: color,
                size: 16,
              ),
            ),
          ],
        ),
      ),
    );
  }
}

/// Screen showing all mushrooms of a selected class with search
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
      _filteredMushrooms = widget.mushrooms.where((m) {
        return m.speciesName.toLowerCase().contains(lowerQuery);
      }).toList();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.backgroundGradientStart,
      appBar: AppBar(
        title: Text(widget.mainClass.replaceAll('_', ' ')),
        backgroundColor: Colors.transparent,
        elevation: 0,
        foregroundColor: AppColors.textPrimary,
      ),
      body: Column(
        children: [
          // Search bar
          Padding(
            padding: const EdgeInsets.all(20),
            child: TextField(
              controller: _searchController,
              onChanged: _filterMushrooms,
              decoration: InputDecoration(
                hintText: 'Search ${widget.mushrooms.length} species...',
                hintStyle: AppTextStyles.bodyMedium.copyWith(color: AppColors.textHint),
                filled: true,
                fillColor: AppColors.white,
                prefixIcon: Icon(Icons.search_rounded, color: AppColors.iconColorLight),
                suffixIcon: _searchController.text.isNotEmpty
                    ? IconButton(
                        icon: Icon(Icons.clear_rounded, color: AppColors.iconColorLight),
                        onPressed: () {
                          _searchController.clear();
                          _filterMushrooms('');
                        },
                      )
                    : null,
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(14),
                  borderSide: BorderSide.none,
                ),
                contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
              ),
            ),
          ),

          // Results count
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 20),
            child: Row(
              children: [
                Text(
                  '${_filteredMushrooms.length} species',
                  style: AppTextStyles.labelSmall,
                ),
                const Spacer(),
              ],
            ),
          ),

          const SizedBox(height: 8),

          // Mushroom list
          Expanded(
            child: _filteredMushrooms.isEmpty
                ? Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Icon(Icons.search_off_rounded, size: 48, color: AppColors.textHint),
                        const SizedBox(height: 12),
                        Text(
                          'No mushrooms found',
                          style: AppTextStyles.bodyMedium.copyWith(color: AppColors.textSecondary),
                        ),
                      ],
                    ),
                  )
                : ListView.builder(
                    padding: const EdgeInsets.symmetric(horizontal: 20),
                    itemCount: _filteredMushrooms.length,
                    itemBuilder: (context, index) {
                      final mushroom = _filteredMushrooms[index];
                      return _buildMushroomTile(mushroom);
                    },
                  ),
          ),
        ],
      ),
    );
  }

  Widget _buildMushroomTile(Mushroom mushroom) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 12),
      child: GestureDetector(
        onTap: () {
          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (_) => MushroomDetailsScreen(mushroom: mushroom),
            ),
          );
        },
        child: Container(
          padding: const EdgeInsets.all(12),
          decoration: BoxDecoration(
            color: AppColors.white,
            borderRadius: BorderRadius.circular(16),
            boxShadow: AppColors.softShadow,
          ),
          child: Row(
            children: [
              ClipRRect(
                borderRadius: BorderRadius.circular(12),
                child: Image.asset(
                  'assets/images/mushrooms/${mushroom.speciesName}.png',
                  width: 60,
                  height: 60,
                  fit: BoxFit.cover,
                  cacheWidth: 120, // 2x for retina displays
                  cacheHeight: 120,
                  errorBuilder: (context, error, stackTrace) {
                    return Container(
                      width: 60,
                      height: 60,
                      decoration: BoxDecoration(
                        color: AppColors.primary.withOpacity(0.1),
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: Icon(Icons.eco, color: AppColors.primary),
                    );
                  },
                ),
              ),
              const SizedBox(width: 14),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      mushroom.speciesName.replaceAll('_', ' '),
                      style: AppTextStyles.labelMedium,
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                    ),
                    const SizedBox(height: 4),
                    Text(
                      mushroom.tasteSmell.isNotEmpty 
                          ? mushroom.tasteSmell 
                          : 'Tap for details',
                      style: AppTextStyles.caption,
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                    ),
                  ],
                ),
              ),
              Icon(Icons.chevron_right_rounded, color: AppColors.iconColorLight),
            ],
          ),
        ),
      ),
    );
  }

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }
}
