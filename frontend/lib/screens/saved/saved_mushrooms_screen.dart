import 'package:flutter/material.dart';
import '../../themes/app_colors.dart';
import '../../themes/app_text_styles.dart';
import '../../models/mushroom_model.dart';
import '../../services/saved_mushrooms_service.dart';
import '../explore/mushroom_details_screen.dart';
import '../../widgets/cards/mushroom_card.dart';

class SavedMushroomsScreen extends StatefulWidget {
  const SavedMushroomsScreen({super.key});

  @override
  State<SavedMushroomsScreen> createState() => _SavedMushroomsScreenState();
}

class _SavedMushroomsScreenState extends State<SavedMushroomsScreen>
    with SingleTickerProviderStateMixin {
  late TabController _tabController;
  List<Map<String, dynamic>> _savedMushrooms = [];
  List<String> _recentSearches = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 2, vsync: this);
    _loadData();
  }

  Future<void> _loadData() async {
    setState(() => _isLoading = true);
    try {
      final saved = await SavedMushroomsService().getSavedMushrooms();
      final recent = await SavedMushroomsService().getRecentSearches();
      setState(() {
        _savedMushrooms = saved;
        _recentSearches = recent;
        _isLoading = false;
      });
    } catch (e) {
      setState(() => _isLoading = false);
    }
  }

  Future<void> _removeSavedMushroom(String speciesName) async {
    await SavedMushroomsService().removeMushroom(speciesName);
    _loadData();
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: const Text('Removed from saved'),
        backgroundColor: AppColors.textSecondary,
        behavior: SnackBarBehavior.floating,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
      ),
    );
  }

  Future<void> _clearRecentSearches() async {
    await SavedMushroomsService().clearRecentSearches();
    _loadData();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.backgroundGradientStart,
      appBar: AppBar(
        title: const Text('Saved'),
        backgroundColor: Colors.transparent,
        elevation: 0,
        foregroundColor: AppColors.textPrimary,
        bottom: TabBar(
          controller: _tabController,
          labelColor: AppColors.primary,
          unselectedLabelColor: AppColors.textSecondary,
          indicatorColor: AppColors.primary,
          indicatorWeight: 3,
          tabs: const [
            Tab(text: 'Favorites'),
            Tab(text: 'Recent Searches'),
          ],
        ),
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator(color: AppColors.primary))
          : TabBarView(
              controller: _tabController,
              children: [
                _buildFavoritesTab(),
                _buildRecentSearchesTab(),
              ],
            ),
    );
  }

  Widget _buildFavoritesTab() {
    if (_savedMushrooms.isEmpty) {
      return _buildEmptyState(
        icon: Icons.bookmark_outline_rounded,
        title: 'No saved mushrooms',
        subtitle: 'Save mushrooms from details screen\nto see them here',
      );
    }

    return ListView.builder(
      padding: const EdgeInsets.all(20),
      itemCount: _savedMushrooms.length,
      itemBuilder: (context, index) {
        final mushroom = _savedMushrooms[index];
        return _buildMushroomTile(mushroom);
      },
    );
  }

  Widget _buildRecentSearchesTab() {
    if (_recentSearches.isEmpty) {
      return _buildEmptyState(
        icon: Icons.history_rounded,
        title: 'No recent searches',
        subtitle: 'Your search history will appear here',
      );
    }

    return Column(
      children: [
        Padding(
          padding: const EdgeInsets.all(20),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text('${_recentSearches.length} searches', style: AppTextStyles.labelSmall),
              GestureDetector(
                onTap: _clearRecentSearches,
                child: Text(
                  'Clear All',
                  style: AppTextStyles.labelSmall.copyWith(color: AppColors.danger),
                ),
              ),
            ],
          ),
        ),
        Expanded(
          child: ListView.builder(
            padding: const EdgeInsets.symmetric(horizontal: 20),
            itemCount: _recentSearches.length,
            itemBuilder: (context, index) {
              final query = _recentSearches[index];
              return _buildSearchTile(query);
            },
          ),
        ),
      ],
    );
  }

  Widget _buildEmptyState({
    required IconData icon,
    required String title,
    required String subtitle,
  }) {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Container(
            padding: const EdgeInsets.all(24),
            decoration: BoxDecoration(
              color: AppColors.primary.withOpacity(0.1),
              shape: BoxShape.circle,
            ),
            child: Icon(icon, size: 48, color: AppColors.primary),
          ),
          const SizedBox(height: 24),
          Text(title, style: AppTextStyles.heading3),
          const SizedBox(height: 8),
          Text(
            subtitle,
            style: AppTextStyles.bodySmall,
            textAlign: TextAlign.center,
          ),
        ],
      ),
    );
  }

  Widget _buildMushroomTile(Map<String, dynamic> mushroomData) {
    final speciesName = mushroomData['species_name'] ?? mushroomData['sub_class'] ?? 'Unknown';

    return Dismissible(
      key: Key(speciesName),
      direction: DismissDirection.endToStart,
      onDismissed: (_) => _removeSavedMushroom(speciesName),
      background: Container(
        alignment: Alignment.centerRight,
        margin: const EdgeInsets.only(bottom: 12),
        padding: const EdgeInsets.only(right: 20),
        decoration: BoxDecoration(
          color: AppColors.danger,
          borderRadius: BorderRadius.circular(16),
        ),
        child: const Icon(Icons.delete_rounded, color: Colors.white),
      ),
      child: MushroomCardWidget(
        mushroom: Mushroom.fromMap(mushroomData),
        onTap: () {
          final mushroom = Mushroom.fromMap(mushroomData);
          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (_) => MushroomDetailsScreen(mushroom: mushroom),
            ),
          );
        },
      ),
    );
  }

  Widget _buildSearchTile(String query) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 8),
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
        decoration: BoxDecoration(
          color: AppColors.white,
          borderRadius: BorderRadius.circular(12),
          boxShadow: AppColors.softShadow,
        ),
        child: Row(
          children: [
            Icon(Icons.history_rounded, color: AppColors.iconColorLight, size: 20),
            const SizedBox(width: 12),
            Expanded(
              child: Text(query, style: AppTextStyles.bodyMedium),
            ),
          ],
        ),
      ),
    );
  }

  @override
  void dispose() {
    _tabController.dispose();
    super.dispose();
  }
}
