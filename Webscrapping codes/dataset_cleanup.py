import os
import sys
from PIL import Image

# dataset_cleanup.py — Remove bad images not suitable for training
BASE_DIR = "/home/ashirkhan/Updated Data set/Professional_Mushroom_Dataset"
TARGET_COUNT = 600
Image.MAX_IMAGE_PIXELS = None

MIN_SIZE_KB = 5        # Images smaller than 5KB are likely corrupt/blank
MIN_RESOLUTION = 50    # Images smaller than 50x50 are useless
MAX_ASPECT_RATIO = 5   # Extreme aspect ratios (banners, strips) are bad

stats = {"removed": 0, "kept": 0, "corrupt": 0}

def is_bad_image(filepath):
    """Check if an image is unsuitable for training."""
    try:
        # Check file size
        size_kb = os.path.getsize(filepath) / 1024
        if size_kb < MIN_SIZE_KB:
            return True, "too_small_file"

        # Check if image opens and is valid
        img = Image.open(filepath)
        img.verify()  # Verify it's a real image

        # Re-open after verify (verify closes it)
        img = Image.open(filepath)
        w, h = img.size

        # Too small resolution
        if w < MIN_RESOLUTION or h < MIN_RESOLUTION:
            return True, "low_resolution"

        # Extreme aspect ratio (likely not a mushroom photo)
        ratio = max(w, h) / max(min(w, h), 1)
        if ratio > MAX_ASPECT_RATIO:
            return True, "bad_aspect_ratio"

        # Check if image is mostly one color (blank/placeholder)
        if w > 10 and h > 10:
            small = img.resize((10, 10)).convert('RGB')
            pixels = list(small.getdata())
            avg_r = sum(p[0] for p in pixels) / len(pixels)
            avg_g = sum(p[1] for p in pixels) / len(pixels)
            avg_b = sum(p[2] for p in pixels) / len(pixels)
            # Pure white, pure black, or near-uniform = placeholder
            if (avg_r > 250 and avg_g > 250 and avg_b > 250):
                return True, "blank_white"
            if (avg_r < 5 and avg_g < 5 and avg_b < 5):
                return True, "blank_black"

        return False, "ok"
    except Exception as e:
        return True, "corrupt"

def cleanup_dataset():
    folders = sorted([d for d in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, d))])
    print(f"🧹 Starting Dataset Cleanup across {len(folders)} classes...")

    for folder in folders:
        path = os.path.join(BASE_DIR, folder)
        files = [f for f in os.listdir(path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        removed_count = 0

        for f in files:
            filepath = os.path.join(path, f)

            # Skip augmented images (they were generated from good ones)
            if '_AUG_' in f:
                continue

            bad, reason = is_bad_image(filepath)
            if bad:
                os.remove(filepath)
                removed_count += 1
                stats["removed"] += 1
                stats["corrupt"] += (1 if reason == "corrupt" else 0)
            else:
                stats["kept"] += 1

        # Also remove ALL old augmented images (will re-generate fresh)
        aug_files = [f for f in os.listdir(path) if '_AUG_' in f]
        for f in aug_files:
            os.remove(os.path.join(path, f))
            stats["removed"] += 1

        # Also remove downloaded_ids.txt and other non-image files
        misc_files = [f for f in os.listdir(path) if not f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        for f in misc_files:
            fp = os.path.join(path, f)
            if os.path.isfile(fp):
                os.remove(fp)

        remaining = len([f for f in os.listdir(path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
        if removed_count > 0:
            print(f"🗑️  {folder}: Removed {removed_count} bad images. Remaining: {remaining}")

    print(f"\n📊 Cleanup Summary:")
    print(f"   Removed: {stats['removed']} images")
    print(f"   Corrupt: {stats['corrupt']} images")
    print(f"   Kept: {stats['kept']} good images")
    print(f"✅ Cleanup Complete!")

if __name__ == "__main__":
    cleanup_dataset()
