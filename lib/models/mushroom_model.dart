class Mushroom {
  final String mainClass;
  final String speciesName;
  final String recipes;
  final String tasteSmell;
  final String description;
  final String scientificName;
  final String habitat;
  final String cap;
  final String gills;
  final String stem;
  final String frequency;
  final String found;

  Mushroom({
    required this.mainClass,
    required this.speciesName,
    this.recipes = '',
    this.tasteSmell = '',
    this.description = '',
    this.scientificName = '',
    this.habitat = '',
    this.cap = '',
    this.gills = '',
    this.stem = '',
    this.frequency = '',
    this.found = '',
  });

  // For backward compatibility with code using subClass
  String get subClass => speciesName;

  // Parse recipes string into list
  List<String> get recipesList {
    if (recipes.isEmpty) return [];
    return recipes.split('|').map((r) => r.trim()).where((r) => r.isNotEmpty).toList();
  }

  // Convert from DB map to Mushroom object
  factory Mushroom.fromMap(Map<String, dynamic> json) => Mushroom(
        mainClass: json['main_class'] ?? '',
        speciesName: json['species_name'] ?? '',
        recipes: json['recipes'] ?? '',
        tasteSmell: json['taste_smell'] ?? '',
        description: json['description'] ?? '',
        scientificName: json['scientific_name'] ?? '',
        habitat: json['habitat'] ?? '',
        cap: json['cap'] ?? '',
        gills: json['gills'] ?? '',
        stem: json['stem'] ?? '',
        frequency: json['frequency'] ?? '',
        found: json['found'] ?? '',
      );

  // Convert Mushroom object to map for DB insertion
  Map<String, dynamic> toMap() {
    return {
      'main_class': mainClass,
      'species_name': speciesName,
      'recipes': recipes,
      'taste_smell': tasteSmell,
      'description': description,
      'scientific_name': scientificName,
      'habitat': habitat,
      'cap': cap,
      'gills': gills,
      'stem': stem,
      'frequency': frequency,
      'found': found,
    };
  }
}
