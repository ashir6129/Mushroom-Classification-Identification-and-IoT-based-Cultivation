class Mushroom {
  final String mainClass;
  final String subClass;
  final String scientificName;
  final String kingdom;
  final String family;
  final String edibility;
  final String description;
  final String occurrence;
  final String pricePkr;
  final String recipes;
  final String images;

  Mushroom({
    required this.mainClass,
    required this.subClass,
    required this.scientificName,
    required this.kingdom,
    required this.family,
    required this.edibility,
    required this.description,
    required this.occurrence,
    required this.pricePkr,
    required this.recipes,
    this.images = '',
  });

  // UI Aliases for backward compatibility
  String get speciesName => subClass;
  String get type => edibility;
  String get frequency => occurrence;
  String get price => pricePkr;
  
  // Legacy aliases to prevent search/UI breakage
  String get tasteSmell => description; // Use description as fallback
  String get habitat => occurrence;      // Use occurrence as fallback
  String get cap => '';
  String get gills => '';
  String get stem => '';
  String get found => occurrence;

  // Split recipes for list display
  List<String> get recipesList {
    if (recipes.isEmpty) return [];
    if (recipes.contains('. ')) {
      return recipes.split('. ').map((r) => r.trim()).where((r) => r.isNotEmpty).toList();
    }
    return [recipes];
  }

  // Split images for list display
  List<String> get imagePaths {
    if (images.isEmpty) return [];
    return images.split(';').map((i) => i.trim()).where((i) => i.isNotEmpty).toList();
  }

  factory Mushroom.fromMap(Map<String, dynamic> json) => Mushroom(
        mainClass: json['main_class'] ?? '',
        subClass: json['sub_class'] ?? '',
        scientificName: json['scientific_name'] ?? '',
        kingdom: json['kingdom'] ?? '',
        family: json['family'] ?? '',
        edibility: json['edibility'] ?? '',
        description: json['description'] ?? '',
        occurrence: json['occurrence'] ?? '',
        pricePkr: json['price_pkr'] ?? '',
        recipes: json['recipes'] ?? '',
        images: json['images'] ?? '',
      );

  Map<String, dynamic> toMap() {
    return {
      'main_class': mainClass,
      'sub_class': subClass,
      'scientific_name': scientificName,
      'kingdom': kingdom,
      'family': family,
      'edibility': edibility,
      'description': description,
      'occurrence': occurrence,
      'price_pkr': pricePkr,
      'recipes': recipes,
      'images': images,
    };
  }
}
