import 'package:flutter/material.dart';

class MushroomDetailsScreen extends StatelessWidget {
  final Map<String, dynamic> mushroom;

  const MushroomDetailsScreen({super.key, required this.mushroom});

  @override
  Widget build(BuildContext context) {
    final subClass = mushroom['sub_class'] ?? 'Unknown';
    final description = mushroom['description'] ?? 'No description available';
    final pakistanStatus = mushroom['pakistan_status'] ?? 'Unknown';
    final regionsFound = mushroom['regions_found'] ?? 'Unknown';

    return Scaffold(
      appBar: AppBar(
        title: Text(subClass),
        backgroundColor: const Color.fromARGB(255, 191, 218, 192),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Mushroom Image
            Center(
              child: ClipRRect(
                borderRadius: BorderRadius.circular(12),
                child: Image.asset(
                  'assets/images/mushrooms/$subClass.png',
                  width: 200,
                  height: 200,
                  fit: BoxFit.cover,
                  errorBuilder: (context, error, stackTrace) {
                    return Container(
                      width: 200,
                      height: 200,
                      decoration: BoxDecoration(
                        color: Colors.grey.shade200,
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: const Icon(Icons.image_not_supported, size: 50),
                    );
                  },
                ),
              ),
            ),

            const SizedBox(height: 16),

            // Species Name
            _buildInfoSection(
              icon: Icons.eco,
              title: 'Species',
              content: subClass,
            ),

            const SizedBox(height: 16),

            // Description
            _buildInfoSection(
              icon: Icons.description,
              title: 'Description',
              content: description,
            ),

            const SizedBox(height: 16),

            // Pakistan Status
            _buildInfoSection(
              icon: Icons.location_on,
              title: 'Status in Pakistan',
              content: pakistanStatus,
            ),

            const SizedBox(height: 16),

            // Regions Found
            _buildInfoSection(
              icon: Icons.map,
              title: 'Regions Found',
              content: regionsFound,
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildInfoSection({
    required IconData icon,
    required String title,
    required String content,
  }) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.grey.shade100,
        borderRadius: BorderRadius.circular(12),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(icon, size: 20, color: Colors.green.shade700),
              const SizedBox(width: 8),
              Text(
                title,
                style: TextStyle(
                  fontSize: 14,
                  fontWeight: FontWeight.bold,
                  color: Colors.green.shade700,
                ),
              ),
            ],
          ),
          const SizedBox(height: 8),
          Text(
            content,
            style: const TextStyle(
              fontSize: 16,
              height: 1.5,
            ),
          ),
        ],
      ),
    );
  }
}
