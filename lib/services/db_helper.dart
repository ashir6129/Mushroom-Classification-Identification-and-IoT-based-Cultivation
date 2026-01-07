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
    try {
      Directory documentsDirectory = await getApplicationDocumentsDirectory();
      String path = join(documentsDirectory.path, "mushrooms.db");
      print("📂 DB Path: $path");

      // Always copy fresh database to ensure latest data
      print("📥 Copying mushrooms.db from assets...");
      ByteData data = await rootBundle.load("assets/db/mushrooms.db");
      List<int> bytes =
          data.buffer.asUint8List(data.offsetInBytes, data.lengthInBytes);
      await File(path).writeAsBytes(bytes, flush: true);
      print("✅ DB copied successfully!");

      Database db = await openDatabase(path);
      print("🟢 DB opened successfully");

      final tables = await db
          .rawQuery("SELECT name FROM sqlite_master WHERE type='table'");
      print("📋 Tables in DB: ${tables.map((e) => e['name']).toList()}");

      return db;
    } catch (e) {
      print("❌ Error initializing DB: $e");
      rethrow;
    }
  }

  Future<List<Map<String, dynamic>>> getMushrooms() async {
    try {
      final db = await database;
      final rows = await db.query("mushrooms");
      print("🍄 Rows fetched: ${rows.length}");
      return rows;
    } catch (e) {
      print("❌ Error fetching mushrooms: $e");
      return [];
    }
  }

  /// Get mushroom details by species_name
  Future<Map<String, dynamic>?> getMushroomBySubClass(String speciesName) async {
    try {
      final db = await database;
      final rows = await db.query(
        "mushrooms",
        where: "species_name = ?",
        whereArgs: [speciesName],
        limit: 1,
      );
      if (rows.isNotEmpty) {
        print("🍄 Found mushroom: ${rows.first['species_name']}");
        return rows.first;
      }
      print("⚠️ Mushroom not found: $speciesName");
      return null;
    } catch (e) {
      print("❌ Error fetching mushroom by species_name: $e");
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
        print("🗑️ Database reset");
      }
    } catch (e) {
      print("❌ Error resetting database: $e");
    }
  }
}
