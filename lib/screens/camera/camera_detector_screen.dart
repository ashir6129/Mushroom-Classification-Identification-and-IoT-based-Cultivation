import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import '../../themes/app_colors.dart';
import '../../themes/app_text_styles.dart';
import '../../services/ai_service.dart';
import '../../services/db_helper.dart';
import '../../models/mushroom_model.dart';
import '../explore/mushroom_details_screen.dart';

class CameraDetectorScreen extends StatefulWidget {
  const CameraDetectorScreen({super.key});

  @override
  State<CameraDetectorScreen> createState() => _CameraDetectorScreenState();
}

class _CameraDetectorScreenState extends State<CameraDetectorScreen> {
  XFile? _selectedImage;
  Map<String, dynamic>? _predictionResult;
  String? _detectedSpecies;
  bool _isLoading = false;
  String? _errorMessage;

  final ImagePicker _picker = ImagePicker();

  Future<void> _openCamera() async {
    // image_picker handles camera permission internally
    try {
      final image = await _picker.pickImage(source: ImageSource.camera);
      if (image != null) {
        setState(() {
          _selectedImage = image;
          _predictionResult = null;
          _detectedSpecies = null;
          _errorMessage = null;
        });
      }
    } catch (e) {
      // Permission denied or camera not available
      _showPermissionDeniedDialog('Camera');
    }
  }

  Future<void> _openGallery() async {
    // Android 13+ doesn't require storage permission for image picker
    // The system photo picker handles permissions automatically
    final image = await _picker.pickImage(source: ImageSource.gallery);
    if (image != null) {
      setState(() {
        _selectedImage = image;
        _predictionResult = null;
        _detectedSpecies = null;
        _errorMessage = null;
      });
    }
  }

  void _showPermissionDeniedDialog(String permissionName) {
    showDialog(
      context: context,
      builder: (_) => AlertDialog(
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
        title: Row(
          children: [
            Icon(Icons.warning_rounded, color: AppColors.warning),
            const SizedBox(width: 12),
            Text('Permission Required', style: AppTextStyles.heading3),
          ],
        ),
        content: Text(
          'Please enable $permissionName permission from settings to use this feature.',
          style: AppTextStyles.bodyMedium,
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: Text('OK', style: TextStyle(color: AppColors.primary)),
          ),
        ],
      ),
    );
  }

  Future<void> _identifyMushroom() async {
    if (_selectedImage == null) return;

    setState(() {
      _isLoading = true;
      _predictionResult = null;
      _detectedSpecies = null;
      _errorMessage = null;
    });

    try {
      final result = await AiService.predictMushroom(File(_selectedImage!.path));

      if (!mounted) return;

      if (result.containsKey("error")) {
        setState(() {
          _errorMessage = result['error'].toString();
        });
      } else {
        setState(() {
          _predictionResult = result;
          _detectedSpecies = result['Species'] as String?;
        });
      }
    } catch (e) {
      if (!mounted) return;
      setState(() {
        _errorMessage = e.toString();
      });
    } finally {
      if (mounted) {
        setState(() {
          _isLoading = false;
        });
      }
    }
  }

  Future<void> _showMoreDetails() async {
    if (_detectedSpecies == null) return;

    setState(() => _isLoading = true);

    try {
      final mushroomData = await DatabaseHelper.instance.getMushroomBySubClass(_detectedSpecies!);

      if (!mounted) return;

      setState(() => _isLoading = false);

      if (mushroomData != null) {
        // Convert Map to Mushroom model
        final mushroom = Mushroom.fromMap(mushroomData);
        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (context) => MushroomDetailsScreen(mushroom: mushroom),
          ),
        );
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Details not found for: $_detectedSpecies'),
            backgroundColor: AppColors.warning,
            behavior: SnackBarBehavior.floating,
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
          ),
        );
      }
    } catch (e) {
      if (!mounted) return;
      setState(() => _isLoading = false);
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Error: $e'),
          backgroundColor: AppColors.danger,
          behavior: SnackBarBehavior.floating,
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.backgroundGradientStart,
      appBar: AppBar(
        title: const Text('Identify Mushroom'),
        backgroundColor: Colors.transparent,
        elevation: 0,
        foregroundColor: AppColors.textPrimary,
        centerTitle: true,
      ),
      body: SafeArea(
        child: Column(
          children: [
            Expanded(
              child: SingleChildScrollView(
                padding: const EdgeInsets.all(20),
                child: Column(
                  children: [
                    // Image Display Area
                    _buildImageArea(),

                    const SizedBox(height: 24),

                    // Results Card
                    if (_predictionResult != null || _errorMessage != null || _isLoading)
                      _buildResultsCard(),
                  ],
                ),
              ),
            ),

            // Bottom Action Buttons
            _buildActionButtons(),
          ],
        ),
      ),
    );
  }

  Widget _buildImageArea() {
    return Container(
      width: double.infinity,
      height: 320,
      decoration: BoxDecoration(
        color: AppColors.white,
        borderRadius: BorderRadius.circular(24),
        boxShadow: AppColors.cardShadow,
      ),
      child: _selectedImage == null
          ? _buildEmptyImagePlaceholder()
          : _buildSelectedImage(),
    );
  }

  Widget _buildEmptyImagePlaceholder() {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Container(
          padding: const EdgeInsets.all(24),
          decoration: BoxDecoration(
            color: AppColors.primary.withOpacity(0.1),
            shape: BoxShape.circle,
          ),
          child: Icon(
            Icons.add_photo_alternate_rounded,
            size: 48,
            color: AppColors.primary,
          ),
        ),
        const SizedBox(height: 20),
        Text(
          'Add a Mushroom Photo',
          style: AppTextStyles.heading3,
        ),
        const SizedBox(height: 8),
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 40),
          child: Text(
            'Take a photo or select from gallery to identify',
            style: AppTextStyles.bodySmall,
            textAlign: TextAlign.center,
          ),
        ),
      ],
    );
  }

  Widget _buildSelectedImage() {
    return ClipRRect(
      borderRadius: BorderRadius.circular(24),
      child: Stack(
        fit: StackFit.expand,
        children: [
          Image.file(
            File(_selectedImage!.path),
            fit: BoxFit.cover,
          ),
          // Gradient overlay at bottom
          Positioned(
            bottom: 0,
            left: 0,
            right: 0,
            child: Container(
              height: 80,
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  begin: Alignment.topCenter,
                  end: Alignment.bottomCenter,
                  colors: [
                    Colors.transparent,
                    Colors.black.withOpacity(0.5),
                  ],
                ),
              ),
            ),
          ),
          // Change photo button
          Positioned(
            bottom: 12,
            right: 12,
            child: GestureDetector(
              onTap: () => setState(() {
                _selectedImage = null;
                _predictionResult = null;
                _detectedSpecies = null;
                _errorMessage = null;
              }),
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
                decoration: BoxDecoration(
                  color: Colors.white.withOpacity(0.9),
                  borderRadius: BorderRadius.circular(20),
                ),
                child: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Icon(Icons.refresh_rounded, size: 18, color: AppColors.textPrimary),
                    const SizedBox(width: 6),
                    Text('Change', style: AppTextStyles.labelSmall),
                  ],
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildResultsCard() {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: AppColors.white,
        borderRadius: BorderRadius.circular(20),
        boxShadow: AppColors.cardShadow,
      ),
      child: _isLoading
          ? _buildLoadingState()
          : _errorMessage != null
              ? _buildErrorState()
              : _buildSuccessState(),
    );
  }

  Widget _buildLoadingState() {
    return Column(
      children: [
        const SizedBox(
          width: 40,
          height: 40,
          child: CircularProgressIndicator(
            color: AppColors.primary,
            strokeWidth: 3,
          ),
        ),
        const SizedBox(height: 16),
        Text('Analyzing mushroom...', style: AppTextStyles.labelMedium),
        const SizedBox(height: 8),
        Text('This may take a few seconds', style: AppTextStyles.caption),
      ],
    );
  }

  Widget _buildErrorState() {
    return Column(
      children: [
        Container(
          padding: const EdgeInsets.all(12),
          decoration: BoxDecoration(
            color: AppColors.danger.withOpacity(0.1),
            shape: BoxShape.circle,
          ),
          child: Icon(Icons.error_outline_rounded, color: AppColors.danger, size: 32),
        ),
        const SizedBox(height: 16),
        Text('Identification Failed', style: AppTextStyles.labelLarge),
        const SizedBox(height: 8),
        Text(
          _errorMessage ?? 'Unknown error',
          style: AppTextStyles.bodySmall,
          textAlign: TextAlign.center,
        ),
      ],
    );
  }

  Widget _buildSuccessState() {
    final mainClass = _predictionResult!['Main Class'] ?? 'Unknown';
    final mainConf = _predictionResult!['Main Confidence (%)'] ?? 0;
    final species = _predictionResult!['Species'] ?? 'Unknown';
    final speciesConf = _predictionResult!['Species Confidence (%)'] ?? 0;
    final isPoisonous = mainClass.toString().toLowerCase().contains('poisnous');

    return Column(
      children: [
        // Status Badge
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
          decoration: BoxDecoration(
            color: isPoisonous ? AppColors.danger.withOpacity(0.1) : AppColors.success.withOpacity(0.1),
            borderRadius: BorderRadius.circular(20),
          ),
          child: Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(
                isPoisonous ? Icons.warning_rounded : Icons.check_circle_rounded,
                color: isPoisonous ? AppColors.danger : AppColors.success,
                size: 18,
              ),
              const SizedBox(width: 6),
              Text(
                mainClass.toString().replaceAll('_', ' '),
                style: AppTextStyles.labelSmall.copyWith(
                  color: isPoisonous ? AppColors.danger : AppColors.success,
                ),
              ),
            ],
          ),
        ),

        const SizedBox(height: 16),

        // Species Name
        Text(
          species.toString().replaceAll('_', ' '),
          style: AppTextStyles.heading2,
          textAlign: TextAlign.center,
        ),

        const SizedBox(height: 16),

        // Confidence Bars
        _buildConfidenceBar('Classification', mainConf),
        const SizedBox(height: 10),
        _buildConfidenceBar('Species Match', speciesConf),

        const SizedBox(height: 20),

        // More Details Button
        if (_detectedSpecies != null)
          SizedBox(
            width: double.infinity,
            child: ElevatedButton(
              onPressed: _showMoreDetails,
              style: ElevatedButton.styleFrom(
                backgroundColor: AppColors.primary,
                foregroundColor: Colors.white,
                padding: const EdgeInsets.symmetric(vertical: 16),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(14),
                ),
                elevation: 0,
              ),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Icon(Icons.info_outline_rounded, size: 20),
                  const SizedBox(width: 8),
                  Text('View Full Details', style: AppTextStyles.button),
                ],
              ),
            ),
          ),
      ],
    );
  }

  Widget _buildConfidenceBar(String label, dynamic confidence) {
    final confValue = confidence is num ? confidence.toDouble() : 0.0;
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(label, style: AppTextStyles.caption),
            Text('${confValue.toStringAsFixed(1)}%', style: AppTextStyles.labelSmall),
          ],
        ),
        const SizedBox(height: 6),
        ClipRRect(
          borderRadius: BorderRadius.circular(4),
          child: LinearProgressIndicator(
            value: confValue / 100,
            backgroundColor: AppColors.textHint.withOpacity(0.2),
            valueColor: AlwaysStoppedAnimation<Color>(
              confValue > 70 ? AppColors.success : confValue > 40 ? AppColors.warning : AppColors.danger,
            ),
            minHeight: 6,
          ),
        ),
      ],
    );
  }

  Widget _buildActionButtons() {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: AppColors.white,
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.05),
            blurRadius: 20,
            offset: const Offset(0, -5),
          ),
        ],
      ),
      child: SafeArea(
        child: Row(
          children: [
            Expanded(
              child: _buildActionButton(
                icon: Icons.camera_alt_rounded,
                label: 'Camera',
                onTap: _openCamera,
                isPrimary: false,
              ),
            ),
            const SizedBox(width: 12),
            Expanded(
              child: _buildActionButton(
                icon: Icons.photo_library_rounded,
                label: 'Gallery',
                onTap: _openGallery,
                isPrimary: false,
              ),
            ),
            const SizedBox(width: 12),
            Expanded(
              flex: 2,
              child: _buildActionButton(
                icon: Icons.search_rounded,
                label: 'Identify',
                onTap: _selectedImage != null ? _identifyMushroom : null,
                isPrimary: true,
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildActionButton({
    required IconData icon,
    required String label,
    required VoidCallback? onTap,
    required bool isPrimary,
  }) {
    final isDisabled = onTap == null;
    final showLabel = isPrimary; // Only show label for primary (Identify) button
    
    return GestureDetector(
      onTap: isDisabled ? null : onTap,
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 14),
        decoration: BoxDecoration(
          gradient: isPrimary && !isDisabled
              ? LinearGradient(
                  colors: [AppColors.primary, AppColors.primaryLight],
                  begin: Alignment.topLeft,
                  end: Alignment.bottomRight,
                )
              : null,
          color: isPrimary
              ? (isDisabled ? AppColors.textHint.withOpacity(0.3) : null)
              : AppColors.backgroundGradientStart,
          borderRadius: BorderRadius.circular(14),
          border: !isPrimary
              ? Border.all(color: AppColors.primary.withOpacity(0.3))
              : null,
        ),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              icon,
              size: showLabel ? 20 : 24,
              color: isPrimary
                  ? (isDisabled ? AppColors.textSecondary : Colors.white)
                  : AppColors.primary,
            ),
            if (showLabel) ...[
              const SizedBox(width: 8),
              Text(
                label,
                style: AppTextStyles.labelMedium.copyWith(
                  color: isPrimary
                      ? (isDisabled ? AppColors.textSecondary : Colors.white)
                      : AppColors.primary,
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }
}
