"""
PyTorch to ONNX Model Converter (Mobile Compatible)
====================================================
Exports with IR version 9 or lower for mobile ONNX Runtime compatibility.
"""

import torch
import torch.nn as nn
import pandas as pd
import os
import onnx

from efficientnet_pytorch import EfficientNet

# --------------------------
# LOAD CLASS STRUCTURE
# --------------------------
csv_path = "mushroom_structure.csv"
df = pd.read_csv(csv_path)

MAIN_CLASSES = sorted(df["main_class"].unique().tolist())
SUB_CLASSES = df["sub_class"].tolist()

NUM_MAIN = len(MAIN_CLASSES)
NUM_SUB = len(SUB_CLASSES)

print(f"Main Classes ({NUM_MAIN}): {MAIN_CLASSES}")
print(f"Total Sub Classes: {NUM_SUB}")

# --------------------------
# MODEL DEFINITION (Same as training)
# --------------------------
class HierarchicalEffNetB3(nn.Module):
    def __init__(self, num_main, num_sub):
        super().__init__()
        self.backbone = EfficientNet.from_pretrained('efficientnet-b3')
        
        in_features = self.backbone._fc.in_features
        self.backbone._fc = nn.Identity()
        
        self.main_head = nn.Linear(in_features, num_main)
        self.sub_head = nn.Linear(in_features, num_sub)
    
    def forward(self, x):
        feat = self.backbone(x)
        main_out = self.main_head(feat)
        sub_out = self.sub_head(feat)
        # Apply softmax for easier handling in Dart
        main_probs = torch.softmax(main_out, dim=1)
        sub_probs = torch.softmax(sub_out, dim=1)
        # Return concatenated output [main_probs (4), sub_probs (215)]
        return torch.cat([main_probs, sub_probs], dim=1)

# --------------------------
# LOAD MODEL
# --------------------------
model_path = "best_hierarchical_effnet_b3.pth"
print(f"\nLoading model from {model_path}...")

model = HierarchicalEffNetB3(num_main=NUM_MAIN, num_sub=NUM_SUB)
checkpoint = torch.load(model_path, map_location="cpu")
model.load_state_dict(checkpoint)
model.eval()

print("✓ Model loaded successfully!")

# --------------------------
# EXPORT TO ONNX (Mobile Compatible)
# --------------------------
sample_input = torch.randn(1, 3, 300, 300)

output_dir = "../assets/model"
os.makedirs(output_dir, exist_ok=True)

onnx_path = os.path.join(output_dir, "mushroom_model.onnx")

print("\n🔄 Exporting to ONNX format (mobile compatible, opset 11)...")

# Use opset_version 11 which produces IR version 6 (compatible with mobile)
# Also use export_params=True to embed weights in single file
torch.onnx.export(
    model,
    sample_input,
    onnx_path,
    input_names=['input'],
    output_names=['output'],
    opset_version=11,  # Lower opset for mobile compatibility
    do_constant_folding=True,
    export_params=True,  # Embed weights in model file
    verbose=False,
)

print(f"✓ ONNX model exported")

# --------------------------
# VERIFY AND FIX IR VERSION
# --------------------------
print("\n🔧 Checking and fixing IR version...")
onnx_model = onnx.load(onnx_path)
print(f"Original IR version: {onnx_model.ir_version}")

# Force IR version to 8 (widely supported on mobile)
if onnx_model.ir_version > 8:
    print(f"Downgrading IR version from {onnx_model.ir_version} to 8...")
    onnx_model.ir_version = 8
    onnx.save(onnx_model, onnx_path)
    print("✓ IR version set to 8")

# Verify model is valid
onnx.checker.check_model(onnx_model)
print("✓ ONNX model is valid!")

# --------------------------
# SAVE CLASS LABELS
# --------------------------
labels_path = os.path.join(output_dir, "mushroom_labels.txt")
with open(labels_path, 'w') as f:
    # First line: metadata
    f.write(f"{NUM_MAIN},{NUM_SUB}\n")
    # Write main classes
    for cls in MAIN_CLASSES:
        f.write(f"{cls}\n")
    # Write sub classes
    for cls in SUB_CLASSES:
        f.write(f"{cls}\n")

print(f"✓ Labels saved to: {labels_path}")

# --------------------------
# REPORT SIZES
# --------------------------
model_size_mb = os.path.getsize(onnx_path) / (1024 * 1024)
print(f"\n📊 ONNX Model size: {model_size_mb:.2f} MB")

# Check for external data file
external_data_path = onnx_path + ".data"
if os.path.exists(external_data_path):
    ext_size = os.path.getsize(external_data_path) / (1024 * 1024)
    print(f"📊 External data size: {ext_size:.2f} MB")
    print(f"📊 Total size: {model_size_mb + ext_size:.2f} MB")
    # Remove external data file since we embedded weights
    os.remove(external_data_path)
    print("✓ Removed external data file (weights embedded in main file)")

print("\n🎉 Export complete! Model is mobile-compatible.")
