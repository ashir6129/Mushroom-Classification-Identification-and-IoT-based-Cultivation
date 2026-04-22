import os
import shutil

# dataset_restructurer.py
BASE_DIR = "/home/ashirkhan/Updated Data set/Professional_Mushroom_Dataset"
TEMPLATE_DIR = "/home/ashirkhan/Updated Data set/4class"

CATEGORIES = [
    "Non_Poisnous_Edible",
    "Non_Poisnous_Non_Edible",
    "Poisnous_Non_Useable",
    "Poisnous_Useable"
]

def restructure_dataset():
    # 1. Build Mapping from Template
    mapping = {} # species_name -> category
    for cat in CATEGORIES:
        cat_path = os.path.join(TEMPLATE_DIR, cat)
        if not os.path.exists(cat_path):
            continue
        species_list = [d for d in os.listdir(cat_path) if os.path.isdir(os.path.join(cat_path, d))]
        for species in species_list:
            mapping[species] = cat
            
    print(f"📊 Mapping built: {len(mapping)} species found in template.")

    # 2. Create Category Folders in Professional Dataset
    for cat in CATEGORIES:
        cat_path = os.path.join(BASE_DIR, cat)
        os.makedirs(cat_path, exist_ok=True)

    # 3. Process Professional Dataset Folders
    prof_folders = [d for d in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, d)) and d not in CATEGORIES]
    
    moved_count = 0
    missing_count = 0
    
    for folder in prof_folders:
        # Extract name from "1)_almond_mushroom"
        if ")_" in folder:
            clean_name = folder.split(")_")[1]
        else:
            clean_name = folder
            
        target_cat = mapping.get(clean_name)
        
        if target_cat:
            src_path = os.path.join(BASE_DIR, folder)
            # Final path: Professional_Mushroom_Dataset/Category/clean_name
            dst_path = os.path.join(BASE_DIR, target_cat, clean_name)
            
            # If destination already exists (e.g. from a previous run or template), handle it
            if os.path.exists(dst_path):
                # If it's a directory, merge or skip?
                # For safety, let's move contents if it exists, or just move the folder if not
                print(f"📁 Merging {folder} into {target_cat}/{clean_name}")
                for item in os.listdir(src_path):
                    s = os.path.join(src_path, item)
                    d = os.path.join(dst_path, item)
                    if not os.path.exists(d):
                        shutil.move(s, d)
                os.rmdir(src_path)
            else:
                shutil.move(src_path, dst_path)
            
            moved_count += 1
        else:
            print(f"❓ Could not map: {folder}")
            missing_count += 1

    print(f"\n🏁 Restructuring Complete!")
    print(f"✅ Successfully categorized: {moved_count}")
    print(f"⚠️  Missing from template: {missing_count}")

if __name__ == "__main__":
    restructure_dataset()
