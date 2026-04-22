import 'dart:io';
import 'dart:typed_data';
import 'package:flutter/services.dart';
import 'package:image/image.dart' as img;
import 'package:onnxruntime/onnxruntime.dart';
import 'package:path_provider/path_provider.dart';
import 'dart:math' as math;
import 'package:flutter/foundation.dart';

/// Offline AI service using ONNX Runtime for on-device inference.
class AiService {
  static OrtSession? _session;
  static List<String> _mainClasses = [];
  static List<String> _subClasses = [];
  static int _numMain = 0;
  static int _numSub = 0;
  static bool _isInitialized = false;

  /// Initialize the ONNX model.
  /// Call this once at app startup (e.g., in splash screen).
  static Future<void> initialize() async {
    if (_isInitialized) return;

    try {
      // Initialize ONNX Runtime environment
      OrtEnv.instance.init();

      // Load labels
      await _loadLabels();

      // Copy both model files to the same directory so external data is found
      await _copyAssetToFile('assets/model/mushroom_model.onnx.data');
      final modelPath = await _copyAssetToFile('assets/model/mushroom_model.onnx');
      
      // Create session options
      final sessionOptions = OrtSessionOptions();

      // Load from File (not buffer!) so onnxruntime can find external data
      _session = OrtSession.fromFile(File(modelPath), sessionOptions);

      _isInitialized = true;
      print('✓ ONNX model loaded successfully');
      print('  Main classes: $_numMain');
      print('  Sub classes: $_numSub');
    } catch (e) {
      print('Failed to initialize ONNX model: $e');
      rethrow;
    }
  }

  /// Load model bytes from assets.
  static Future<Uint8List> _loadModelBytes(String assetPath) async {
    final rawAssetFile = await rootBundle.load(assetPath);
    return rawAssetFile.buffer.asUint8List();
  }

  /// Copy asset file to app's document directory for external data.
  static Future<String> _copyAssetToFile(String assetPath) async {
    final directory = await getApplicationDocumentsDirectory();
    final filename = assetPath.split('/').last;
    final file = File('${directory.path}/$filename');

    // Always copy to ensure latest version
    final data = await rootBundle.load(assetPath);
    await file.writeAsBytes(data.buffer.asUint8List());

    return file.path;
  }

  /// Load class labels from the labels file.
  static Future<void> _loadLabels() async {
    final labelsData = await rootBundle.loadString('assets/model/mushroom_labels.txt');
    final lines = labelsData.split('\n').where((line) => line.trim().isNotEmpty).toList();

    if (lines.isEmpty) {
      throw Exception('Empty labels file');
    }

    // First line contains metadata: numMain,numSub
    final metadata = lines[0].split(',');
    _numMain = int.parse(metadata[0]);
    _numSub = int.parse(metadata[1]);

    // Next numMain lines are main classes
    _mainClasses = lines.sublist(1, 1 + _numMain);

    // Remaining lines are sub classes
    _subClasses = lines.sublist(1 + _numMain, 1 + _numMain + _numSub);
  }

  /// Preprocess image for model input.
  /// Matches the training transforms: resize, center crop, normalize.
  static Future<Float32List> _preprocessImage(File imageFile) async {
    // Read bytes on main thread (File access)
    final bytes = await imageFile.readAsBytes();
    
    // Offload heavy decoding and manipulation to background isolate
    return await compute(_processImageData, bytes);
  }

  /// Standalone function for background isolate processing.
  static Float32List _processImageData(Uint8List bytes) {
    var image = img.decodeImage(bytes);

    if (image == null) {
      throw Exception('Failed to decode image');
    }

    // Resize to 256 (maintaining aspect ratio, short side = 256)
    final shortSide = image.width < image.height ? image.width : image.height;
    final scale = 256.0 / shortSide;
    final newWidth = (image.width * scale).round();
    final newHeight = (image.height * scale).round();
    image = img.copyResize(image, width: newWidth, height: newHeight);

    // Center crop to 224x224
    final cropX = (image.width - 224) ~/ 2;
    final cropY = (image.height - 224) ~/ 2;
    image = img.copyCrop(image, x: cropX, y: cropY, width: 224, height: 224);

    // Convert to float tensor with normalization (NCHW format)
    // ImageNet normalization: mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
    final Float32List tensorData = Float32List(1 * 3 * 224 * 224);
    
    const mean = [0.485, 0.456, 0.406];
    const std = [0.229, 0.224, 0.225];

    int index = 0;
    for (int c = 0; c < 3; c++) {
      for (int y = 0; y < 224; y++) {
        for (int x = 0; x < 224; x++) {
          final pixel = image.getPixel(x, y);
          double value;
          if (c == 0) {
            value = pixel.r / 255.0;
          } else if (c == 1) {
            value = pixel.g / 255.0;
          } else {
            value = pixel.b / 255.0;
          }
          tensorData[index++] = (value - mean[c]) / std[c];
        }
      }
    }

    return tensorData;
  }

  /// Predict mushroom classification from image.
  /// Returns a map with classification results and confidence.
  static Future<Map<String, dynamic>> predictMushroom(File imageFile, {double threshold = 0.50}) async {
    if (!_isInitialized) {
      try {
        await initialize();
      } catch (e) {
        return {"error": "Model initialization failed: $e"};
      }
    }

    if (_session == null) {
      return {"error": "Model not initialized"};
    }

    try {
      // Preprocess image
      final inputData = await _preprocessImage(imageFile);

      // Create input tensor
      final inputShape = [1, 3, 224, 224];
      final inputTensor = OrtValueTensor.createTensorWithDataList(
        inputData,
        inputShape,
      );

      // Run inference
      final inputs = {'input': inputTensor};
      final runOptions = OrtRunOptions();
      final outputs = await _session!.runAsync(runOptions, inputs);

      if (outputs == null || outputs.length < 2) {
        inputTensor.release();
        runOptions.release();
        return {"error": "Invalid model output"};
      }

      // Get output tensors (usage and species)
      final usageTensor = outputs[0];
      final speciesTensor = outputs[1];
      
      if (usageTensor == null || speciesTensor == null) {
        inputTensor.release();
        runOptions.release();
        return {"error": "Missing output heads"};
      }

      final usageData = usageTensor.value as List<List<double>>;
      final usageProbs = usageData[0];
      
      final speciesData = speciesTensor.value as List<List<double>>;
      final speciesProbs = speciesData[0];

      // Find best predictions
      int mainIdx = 0;
      double mainConf = usageProbs[0];
      for (int i = 1; i < usageProbs.length; i++) {
        if (usageProbs[i] > mainConf) {
          mainConf = usageProbs[i];
          mainIdx = i;
        }
      }

      int subIdx = 0;
      double subConf = speciesProbs[0];
      for (int i = 1; i < speciesProbs.length; i++) {
        if (speciesProbs[i] > subConf) {
          subConf = speciesProbs[i];
          subIdx = i;
        }
      }

      // Release resources
      inputTensor.release();
      runOptions.release();
      for (final tensor in outputs) {
        tensor?.release();
      }

      // Return result
      final mainClass = _mainClasses[mainIdx];
      final species = _subClasses[subIdx];

      // If EITHER confidence is below threshold, OR top class is Background -> unrecognized
      final bool isBackground = mainClass.toLowerCase() == 'background' || 
                                species.toLowerCase() == 'background';
      if (isBackground || mainConf < threshold || subConf < threshold) {
        return {
          "Main Class": "Unrecognized",
          "Main Confidence (%)": double.parse((mainConf * 100).toStringAsFixed(2)),
          "Species": "Not a Mushroom",
          "Species Confidence (%)": double.parse((subConf * 100).toStringAsFixed(2)),
          "is_poisonous": null,
          "is_unrecognized": true,
        };
      }

      return {
        "Main Class": mainClass,
        "Main Confidence (%)": double.parse((mainConf * 100).toStringAsFixed(2)),
        "Species": species,
        "Species Confidence (%)": double.parse((subConf * 100).toStringAsFixed(2)),
        "is_poisonous": mainClass.contains("Poisnous"),
        "is_unrecognized": false,
      };
    } catch (e) {
      return {"error": e.toString()};
    }
  }

  /// Dispose the ONNX session.
  static void dispose() {
    _session?.release();
    OrtEnv.instance.release();
    _isInitialized = false;
  }
}
