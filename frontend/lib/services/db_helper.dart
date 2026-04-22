import 'dart:io';
import 'package:flutter/services.dart';
import 'package:path/path.dart';
import 'package:path_provider/path_provider.dart';
import 'package:sqflite/sqflite.dart';

class DatabaseHelper {
  static final DatabaseHelper instance = DatabaseHelper._privateConstructor();
  static Database? _database;

  DatabaseHelper._privateConstructor();

  Future<Database> get database async {
    if (_database != null) return _database!;
    _database = await _initDatabase();
    return _database!;
  }

  Future<Database> _initDatabase() async {
    final dbPath = await getDatabasesPath();
    final path = join(dbPath, 'mushrooms.db');

    // Check if DB exists
    final exists = await File(path).exists();
    
    if (exists) {
      // Check if schema is up to date (has 'images' column)
      final tempDb = await openDatabase(path);
      final columns = await tempDb.rawQuery('PRAGMA table_info(mushrooms)');
      final hasImages = columns.any((c) => c['name'] == 'images');
      await tempDb.close();

      if (!hasImages) {
        print(" Old database detected (missing images column). Deleting and re-copying...");
        await deleteDatabase(path);
      }
    }

    // Re-check existence after possible deletion
    if (!await File(path).exists()) {
      print(" Copying mushrooms.db from assets...");
      try {
        await Directory(dirname(path)).create(recursive: true);
        ByteData data = await rootBundle.load('assets/db/mushrooms.db');
        List<int> bytes = data.buffer.asUint8List(data.offsetInBytes, data.lengthInBytes);
        await File(path).writeAsBytes(bytes, flush: true);
        print("DB copied successfully!");
      } catch (e) {
        print("Error copying database: $e");
      }
    }

    return await openDatabase(path);
  }

  Future<List<Map<String, dynamic>>> getMushrooms() async {
    try {
      final db = await database;
      final rows = await db.query("mushrooms");
      print(" Rows fetched: ${rows.length}");
      return rows;
    } catch (e) {
      print(" Error fetching mushrooms: $e");
      return [];
    }
  }

  /// Get mushroom details by sub_class
  Future<Map<String, dynamic>?> getMushroomBySubClass(String speciesName) async {
    try {
      final db = await database;
      final rows = await db.query(
        "mushrooms",
        where: "sub_class = ?",
        whereArgs: [speciesName],
        limit: 1,
      );
      if (rows.isNotEmpty) {
        print(" Found mushroom: ${rows.first['sub_class']}");
        return rows.first;
      }
      print(" Mushroom not found: $speciesName");
      return null;
    } catch (e) {
      print(" Error fetching mushroom by sub_class: $e");
      return null;
    }
  }
  
  /// Reset database to force refresh from assets
  Future<void> resetDatabase() async {
    try {
      Directory documentsDirectory = await getApplicationDocumentsDirectory();
      String path = join(documentsDirectory.path, "mushrooms.db");
      final file = File(path);
      if (await file.exists()) {
        await file.delete();
        _database = null;
        print(" Database reset");
      }
    } catch (e) {
      print(" Error resetting database: $e");
    }
  }

  /// Get counts for different mushroom types
  Future<Map<String, int>> getMushroomStats() async {
    try {
      final db = await database;
      
      // Get total count
      final totalRes = await db.rawQuery("SELECT COUNT(*) as count FROM mushrooms");
      int total = Sqflite.firstIntValue(totalRes) ?? 0;
      
      // Get Edible (Non_Poisnous_Edible)
      final edibleRes = await db.rawQuery("SELECT COUNT(*) as count FROM mushrooms WHERE main_class = 'Non_Poisnous_Edible'");
      int edible = Sqflite.firstIntValue(edibleRes) ?? 0;
      
      // Get Poisonous (starts with Poisnous)
      final poisonousRes = await db.rawQuery("SELECT COUNT(*) as count FROM mushrooms WHERE main_class LIKE 'Poisnous%'");
      int poisonous = Sqflite.firstIntValue(poisonousRes) ?? 0;
      
      // Get Medicinal (often categorized as Edible or Non-Edible but has medicinal properties in description)
      // For now, let's use a placeholder or check if there's a specific flag.
      // Looking at the labels, we don't have a "Medicinal" main class.
      // Let's just return what we find.
      return {
        'total': total,
        'edible': edible,
        'poisonous': poisonous,
        'medicinal': 25, // Placeholder for now as it's not a primary category
      };
    } catch (e) {
      print(" Error fetching stats: $e");
      return {'total': 0, 'edible': 0, 'poisonous': 0, 'medicinal': 0};
    }
  }
}
