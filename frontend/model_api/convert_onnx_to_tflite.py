"""
ONNX to TFLite Direct Converter
================================
Converts ONNX model to TFLite using TensorFlow.
"""

import onnx
from onnx import numpy_helper
import tensorflow as tf
import numpy as np
import os

# Input/output paths
onnx_path = "../assets/model/mushroom_model.onnx"
data_path = "../assets/model/mushroom_model.onnx.data"
output_dir = "../assets/model"
tflite_path = os.path.join(output_dir, "mushroom_model.tflite")

print("🔄 Loading ONNX model...")
onnx_model = onnx.load(onnx_path, load_external_data=True)

print(f"Model inputs: {[inp.name for inp in onnx_model.graph.input]}")
print(f"Model outputs: {[out.name for out in onnx_model.graph.output]}")

# Use onnx-tf to convert
print("\n🔄 Converting ONNX to TensorFlow...")
from onnx_tf.backend import prepare

tf_rep = prepare(onnx_model)
saved_model_path = os.path.join(output_dir, "tf_saved_model")
tf_rep.export_graph(saved_model_path)
print(f"✓ TensorFlow SavedModel saved to: {saved_model_path}")

# Convert to TFLite
print("\n🔄 Converting TensorFlow to TFLite...")
converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_path)

# Enable optimization for smaller model
converter.optimizations = [tf.lite.Optimize.DEFAULT]

# Use float16 quantization (good balance of size and accuracy)
converter.target_spec.supported_types = [tf.float16]

tflite_model = converter.convert()

with open(tflite_path, 'wb') as f:
    f.write(tflite_model)

# Report model size
model_size_mb = os.path.getsize(tflite_path) / (1024 * 1024)
print(f"\n✓ TFLite model saved to: {tflite_path}")
print(f"📊 Model size: {model_size_mb:.2f} MB")

# Cleanup intermediate files
import shutil
shutil.rmtree(saved_model_path)
print("✓ Cleaned up intermediate files")

print("\n🎉 Conversion complete!")
