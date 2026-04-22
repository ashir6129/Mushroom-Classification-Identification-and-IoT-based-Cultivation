
import os

DATASET_DIR = "/home/ashirkhan/Updated Data set/raw_images_renamed"
VALID_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.webp', '.tiff'}
TARGET_LIMIT = 50

def get_image_count(folder_path):
    count = 0
    if not os.path.exists(folder_path):
        return 0
    for f in os.listdir(folder_path):
        ext = os.path.splitext(f)[1].lower()
        if ext in VALID_EXTENSIONS:
            count += 1
    return count

def main():
    if not os.path.exists(DATASET_DIR):
        print(f"Directory {DATASET_DIR} not found.")
        return

    categories = sorted(os.listdir(DATASET_DIR))
    below_target = []
    at_or_above = []
    
    for category in categories:
        path = os.path.join(DATASET_DIR, category)
        if os.path.isdir(path):
            count = get_image_count(path)
            if count < TARGET_LIMIT:
                below_target.append((category, count))
            else:
                at_or_above.append((category, count))
    
    print(f"Total categories: {len(below_target) + len(at_or_above)}")
    print(f"Categories at or above {TARGET_LIMIT}: {len(at_or_above)}")
    print(f"Categories below {TARGET_LIMIT}: {len(below_target)}")
    
    if below_target:
        print("\nCategories below target:")
        for name, count in below_target:
            print(f"  {name}: {count}")

if __name__ == "__main__":
    main()
