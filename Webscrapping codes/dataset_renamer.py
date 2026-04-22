import os

# dataset_renamer.py
BASE_DIR = "/home/ashirkhan/Updated Data set/Professional_Mushroom_Dataset"

def rename_dataset():
    folders = sorted([d for d in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, d))])
    
    print(f"🚀 Starting dataset renaming in {BASE_DIR}...")
    
    for folder in folders:
        # Extract class name from folder name (e.g., "1)_almond_mushroom" -> "almond_mushroom")
        if ")_" in folder:
            class_name = folder.split(")_")[1]
        else:
            class_name = folder
            
        folder_path = os.path.join(BASE_DIR, folder)
        
        # Get all image files
        images = sorted([f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
        
        if not images:
            print(f"⚠️ Skipping empty folder: {folder}")
            continue
            
        print(f"📦 Renaming {len(images)} images in {folder} to {class_name}_XXX.jpg")
        
        # Step 1: Rename to temporary names to avoid collisions
        temp_names = []
        for i, img in enumerate(images):
            ext = os.path.splitext(img)[1].lower()
            if not ext: ext = ".jpg" # Fallback
            
            old_path = os.path.join(folder_path, img)
            temp_name = f"__tmp_rename_{i}{ext}"
            temp_path = os.path.join(folder_path, temp_name)
            
            os.rename(old_path, temp_path)
            temp_names.append(temp_name)
            
        # Step 2: Rename to final standardized format
        for i, temp_name in enumerate(temp_names):
            ext = os.path.splitext(temp_name)[1].lower()
            new_name = f"{class_name}_{i+1:03d}{ext}"
            
            old_path = os.path.join(folder_path, temp_name)
            new_path = os.path.join(folder_path, new_name)
            
            os.rename(old_path, new_path)

    print("🏁 Renaming Complete!")

if __name__ == "__main__":
    rename_dataset()
