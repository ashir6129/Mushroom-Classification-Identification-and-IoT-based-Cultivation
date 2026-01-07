import 'package:flutter/material.dart';
import '../../themes/app_colors.dart';
import '../../themes/app_text_styles.dart';
import '../../models/mushroom_model.dart';
import '../../services/db_helper.dart';
import '../explore/mushroom_details_screen.dart';

class SearchResultsScreen extends StatefulWidget {
  final String? initialQuery;

  const SearchResultsScreen({super.key, this.initialQuery});

  @override
  State<SearchResultsScreen> createState() => _SearchResultsScreenState();
}

class _SearchResultsScreenState extends State<SearchResultsScreen> {
  final TextEditingController _searchController = TextEditingController();
  List<Mushroom> _allMushrooms = [];
  List<Mushroom> _filteredMushrooms = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _searchController.text = widget.initialQuery ?? '';
    _loadMushrooms();
  }

  Future<void> _loadMushrooms() async {
    setState(() => _isLoading = true);
    try {
      final rows = await DatabaseHelper.instance.getMushrooms();
      final mushrooms = rows.map((row) => Mushroom.fromMap(row)).toList();

      setState(() {
        _allMushrooms = mushrooms;
        _isLoading = false;
      });

      // Apply initial search if provided
      if (widget.initialQuery != null && widget.initialQuery!.isNotEmpty) {
        _filterMushrooms(widget.initialQuery!);
      }
    } catch (e) {
      print("❌ Error loading mushrooms: $e");
      setState(() => _isLoading = false);
    }
  }

  void _filterMushrooms(String query) {
    if (query.isEmpty) {
      setState(() => _filteredMushrooms = []);
      return;
    }

    final lowerQuery = query.toLowerCase();
    setState(() {
      _filteredMushrooms = _allMushrooms.where((m) {
        return m.speciesName.toLowerCase().contains(lowerQuery) ||
            m.mainClass.toLowerCase().contains(lowerQuery) ||
            m.description.toLowerCase().contains(lowerQuery) ||
            m.tasteSmell.toLowerCase().contains(lowerQuery) ||
            m.recipes.toLowerCase().contains(lowerQuery) ||
            m.habitat.toLowerCase().contains(lowerQuery);
      }).toList();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Search Mushrooms"),
        backgroundColor: AppColors.backgroundGradientStart,
      ),
      body: Column(
        children: [
          // Search bar
          Padding(
            padding: const EdgeInsets.all(16),
            child: TextField(
              controller: _searchController,
              autofocus: widget.initialQuery == null || widget.initialQuery!.isEmpty,
              onChanged: _filterMushrooms,
              decoration: InputDecoration(
                hintText: 'Search by name, description, recipes...',
                filled: true,
                fillColor: Colors.white,
                prefixIcon: const Icon(Icons.search, color: AppColors.iconColor),
                suffixIcon: _searchController.text.isNotEmpty
                    ? IconButton(
                        icon: const Icon(Icons.clear),
                        onPressed: () {
                          _searchController.clear();
                          _filterMushrooms('');
                        },
                      )
                    : null,
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(15),
                  borderSide: BorderSide.none,
                ),
                enabledBorder: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(15),
                  borderSide: BorderSide(color: Colors.grey.shade300),
                ),
                focusedBorder: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(15),
                  borderSide: const BorderSide(color: AppColors.primary),
                ),
              ),
            ),
          ),

          // Results count
          if (_searchController.text.isNotEmpty)
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16),
              child: Align(
                alignment: Alignment.centerLeft,
                child: Text(
                  '${_filteredMushrooms.length} results found',
                  style: AppTextStyles.caption.copyWith(
                    color: Colors.grey.shade600,
                  ),
                ),
              ),
            ),

          const SizedBox(height: 8),

          // Results list
          Expanded(
            child: _isLoading
                ? const Center(child: CircularProgressIndicator())
                : _searchController.text.isEmpty
                    ? Center(
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Icon(Icons.search, size: 64, color: Colors.grey.shade400),
                            const SizedBox(height: 16),
                            Text(
                              'Start typing to search mushrooms',
                              style: AppTextStyles.bodyMedium.copyWith(
                                color: Colors.grey.shade600,
                              ),
                            ),
                          ],
                        ),
                      )
                    : _filteredMushrooms.isEmpty
                        ? Center(
                            child: Column(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                Icon(Icons.search_off, size: 64, color: Colors.grey.shade400),
                                const SizedBox(height: 16),
                                Text(
                                  'No mushrooms found',
                                  style: AppTextStyles.bodyMedium.copyWith(
                                    color: Colors.grey.shade600,
                                  ),
                                ),
                              ],
                            ),
                          )
                        : ListView.builder(
                            padding: const EdgeInsets.all(16),
                            itemCount: _filteredMushrooms.length,
                            itemBuilder: (context, index) {
                              final mushroom = _filteredMushrooms[index];
                              return _buildMushroomCard(mushroom);
                            },
                          ),
          ),
        ],
      ),
    );
  }

  Widget _buildMushroomCard(Mushroom mushroom) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 12),
      child: InkWell(
        borderRadius: BorderRadius.circular(12),
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
            borderRadius: BorderRadius.circular(12),
            boxShadow: AppColors.softShadow,
          ),
          child: Row(
            children: [
              ClipRRect(
                borderRadius: BorderRadius.circular(8),
                child: Image.asset(
                  'assets/images/mushrooms/${mushroom.speciesName}.png',
                  width: 60,
                  height: 60,
                  fit: BoxFit.cover,
                  errorBuilder: (context, error, stackTrace) {
                    return Container(
                      width: 60,
                      height: 60,
                      decoration: BoxDecoration(
                        color: AppColors.primary.withOpacity(0.1),
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: Icon(Icons.eco, color: AppColors.primary),
                    );
                  },
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      mushroom.speciesName.replaceAll('_', ' '),
                      style: AppTextStyles.labelMedium,
                    ),
                    const SizedBox(height: 4),
                    Text(
                      mushroom.description.isNotEmpty
                          ? mushroom.description
                          : (mushroom.tasteSmell.isNotEmpty ? mushroom.tasteSmell : 'Tap for details'),
                      style: AppTextStyles.caption,
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                    ),
                  ],
                ),
              ),
              const Icon(Icons.chevron_right, color: AppColors.iconColor),
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
