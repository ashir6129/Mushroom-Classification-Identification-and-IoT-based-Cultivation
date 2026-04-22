import 'package:flutter/material.dart';
import '../../themes/app_colors.dart';
import '../../themes/app_text_styles.dart';
import '../../models/mushroom_model.dart';
import '../../services/db_helper.dart';
import '../explore/mushroom_details_screen.dart';
import '../../widgets/cards/mushroom_card.dart';

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
      print(" Error loading mushrooms: $e");
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

  // Moved _buildMushroomCard method inside the _SearchResultsScreenState class
  Widget _buildMushroomCard(Mushroom mushroom) {
    return MushroomCardWidget(
      mushroom: mushroom,
      onTap: () {
        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (_) => MushroomDetailsScreen(mushroom: mushroom),
          ),
        );
      },
    );
  }

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }
}
