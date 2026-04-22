#!/usr/bin/env python3
"""
=============================================================
 Mushroom Dataset Splitter — Hierarchical Train / Val
=============================================================
Splits the Professional_Mushroom_Dataset into:
    train  (80%)   |   val   (20%)

Structure:
main_data_set/
├── train/
│   ├── Background/ (contains images directly)
│   ├── Non_Poisnous_Edible/[species]/
│   └── ...
└── val/
    ├── Background/ (contains images directly)
    └── ...

Note: Class_Zero in source is mapped to Background in output.
=============================================================
"""

import os
import sys
import random
import shutil
from pathlib import Path
from collections import defaultdict

# ── Try importing tqdm; fall back to a no-op wrapper ────────
try:
    from tqdm import tqdm
except ImportError:
    print("⚠️  tqdm not found — installing now…")
    os.system(f"{sys.executable} -m pip install tqdm -q")
    from tqdm import tqdm

# ============================================================
# CONFIGURATION
# ============================================================
SOURCE_ROOT = Path("/home/ashirkhan/Updated Data set/Professional_Mushroom_Dataset")
OUTPUT_ROOT = Path("/home/ashirkhan/Updated Data set/main_data_set")

TRAIN_RATIO = 0.80
SEED = 42
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

# Map source folder name -> target folder name
CATEGORY_MAP = {
    "Background": "Background",
    "Class_Zero": "Background", # Backward compatibility check
    "Non_Poisnous_Edible": "Non_Poisnous_Edible",
    "Non_Poisnous_Non_Edible": "Non_Poisnous_Non_Edible",
    "Poisnous_Non_Useable": "Poisnous_Non_Useable",
    "Poisnous_Useable": "Poisnous_Useable",
}

# ============================================================
# HELPERS
# ============================================================

def get_image_files(directory: Path) -> list[Path]:
    """Gather image files in the immediate directory."""
    images = []
    if not directory.exists():
        return []
    for f in os.listdir(directory):
        if Path(f).suffix.lower() in IMAGE_EXTS:
            images.append(directory / f)
    return sorted(images)

def split_list(items: list, ratio: float, seed: int):
    """Split a list into train and val based on ratio."""
    rng = random.Random(seed)
    shuffled = list(items)
    rng.shuffle(shuffled)
    
    split_idx = int(len(shuffled) * ratio)
    return shuffled[:split_idx], shuffled[split_idx:]

def ensure_copy(src: Path, dst: Path):
    """Copy file to destination, creating parents if needed."""
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)

# ============================================================
# MAIN
# ============================================================

def main():
    print("=" * 62)
    print(f"🍄 Hierarchical Mushroom Dataset Splitter")
    print(f"   Source : {SOURCE_ROOT}")
    print(f"   Output : {OUTPUT_ROOT}")
    print(f"   Split  : {TRAIN_RATIO:.0%} Train / {1-TRAIN_RATIO:.0%} Val")
    print("=" * 62)

    if not SOURCE_ROOT.exists():
        print(f"❌ Source directory not found: {SOURCE_ROOT}")
        sys.exit(1)

    processed_count = 0
    
    # 1. Identify all categories in source
    source_categories = [d for d in os.listdir(SOURCE_ROOT) if (SOURCE_ROOT/d).is_dir()]
    
    for src_cat in source_categories:
        target_cat = CATEGORY_MAP.get(src_cat, src_cat)
        src_cat_path = SOURCE_ROOT / src_cat
        
        print(f"\n📂 Processing Category: {src_cat} -> {target_cat}")
        
        # Check if this category has sub-folders (species) or images directly
        sub_dirs = [d for d in os.listdir(src_cat_path) if (src_cat_path/d).is_dir()]
        
        if not sub_dirs:
            # Case A: Images directly in category (e.g., Background)
            images = get_image_files(src_cat_path)
            if not images:
                print(f"  ⚠️  No images found in {src_cat}")
                continue
                
            train_imgs, val_imgs = split_list(images, TRAIN_RATIO, SEED)
            
            for img in tqdm(train_imgs, desc=f"  [Train] {target_cat}", unit="img"):
                ensure_copy(img, OUTPUT_ROOT / "train" / target_cat / img.name)
                processed_count += 1
                
            for img in tqdm(val_imgs, desc=f"  [Val]   {target_cat}", unit="img"):
                ensure_copy(img, OUTPUT_ROOT / "val" / target_cat / img.name)
                processed_count += 1
                
        else:
            # Case B: Images in species sub-folders
            for species in sorted(sub_dirs):
                species_path = src_cat_path / species
                images = get_image_files(species_path)
                
                if not images:
                    continue
                    
                train_imgs, val_imgs = split_list(images, TRAIN_RATIO, SEED)
                
                for img in tqdm(train_imgs, desc=f"  [Train] {species[:15]:<15}", unit="img", leave=False):
                    ensure_copy(img, OUTPUT_ROOT / "train" / target_cat / species / img.name)
                    processed_count += 1
                    
                for img in tqdm(val_imgs, desc=f"  [Val]   {species[:15]:<15}", unit="img", leave=False):
                    ensure_copy(img, OUTPUT_ROOT / "val" / target_cat / species / img.name)
                    processed_count += 1
            
            print(f"  ✅ Processed {len(sub_dirs)} species sub-folders")

    print("\n" + "=" * 62)
    print(f"✅ DONE! Total files processed: {processed_count:,}")
    print(f"   Location: {OUTPUT_ROOT}")
    print("=" * 62)

if __name__ == "__main__":
    main()
