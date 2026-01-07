import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';

class SavedMushroomsService {
  static const String _savedKey = 'saved_mushrooms';
  static const String _recentSearchKey = 'recent_searches';
  static const int _maxRecentSearches = 10;

  // Singleton pattern
  static final SavedMushroomsService _instance = SavedMushroomsService._internal();
  factory SavedMushroomsService() => _instance;
  SavedMushroomsService._internal();

  // Save a mushroom to favorites
  Future<void> saveMushroom(Map<String, dynamic> mushroom) async {
    final prefs = await SharedPreferences.getInstance();
    final saved = await getSavedMushrooms();
    
    // Check if already saved (by species_name, with backward compatibility for sub_class)
    final speciesName = mushroom['species_name'] ?? mushroom['sub_class'] ?? '';
    if (saved.any((m) => (m['species_name'] ?? m['sub_class']) == speciesName)) {
      return; // Already saved
    }
    
    saved.add(mushroom);
    await prefs.setString(_savedKey, jsonEncode(saved));
  }

  // Remove a mushroom from favorites
  Future<void> removeMushroom(String speciesName) async {
    final prefs = await SharedPreferences.getInstance();
    final saved = await getSavedMushrooms();
    
    // Support both species_name and sub_class for backward compatibility
    saved.removeWhere((m) => (m['species_name'] ?? m['sub_class']) == speciesName);
    await prefs.setString(_savedKey, jsonEncode(saved));
  }

  // Check if a mushroom is saved
  Future<bool> isSaved(String speciesName) async {
    final saved = await getSavedMushrooms();
    // Support both species_name and sub_class for backward compatibility
    return saved.any((m) => (m['species_name'] ?? m['sub_class']) == speciesName);
  }

  // Get all saved mushrooms
  Future<List<Map<String, dynamic>>> getSavedMushrooms() async {
    final prefs = await SharedPreferences.getInstance();
    final String? data = prefs.getString(_savedKey);
    
    if (data == null || data.isEmpty) {
      return [];
    }
    
    try {
      final List<dynamic> decoded = jsonDecode(data);
      return decoded.map((item) => Map<String, dynamic>.from(item)).toList();
    } catch (e) {
      return [];
    }
  }

  // Add to recent searches
  Future<void> addRecentSearch(String query) async {
    if (query.trim().isEmpty) return;
    
    final prefs = await SharedPreferences.getInstance();
    final recent = await getRecentSearches();
    
    // Remove if already exists (to move to top)
    recent.remove(query);
    
    // Add to beginning
    recent.insert(0, query);
    
    // Keep only max items
    if (recent.length > _maxRecentSearches) {
      recent.removeRange(_maxRecentSearches, recent.length);
    }
    
    await prefs.setStringList(_recentSearchKey, recent);
  }

  // Get recent searches
  Future<List<String>> getRecentSearches() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getStringList(_recentSearchKey) ?? [];
  }

  // Clear recent searches
  Future<void> clearRecentSearches() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_recentSearchKey);
  }

  // Clear all saved mushrooms
  Future<void> clearSavedMushrooms() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_savedKey);
  }
}
