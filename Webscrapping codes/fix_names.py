
import os
import re

DIR = "/home/ashirkhan/Updated Data set/Professional_Mushroom_Dataset/almond_mushroom"
PREFIX = "almond_mushroom_"

def rename_current():
    files = [f for f in os.listdir(DIR) if f.startswith(PREFIX) and f.endswith(".jpg")]
    # Avoid renaming files that are already in the 001 format
    p = re.compile(r'^' + PREFIX + r'\d{3}\.jpg$')
    to_rename = [f for f in files if not p.match(f)]
    
    to_rename.sort() # Sort by old ID to be consistent
    
    # Get current max index if some are already renamed
    existing_indices = []
    for f in files:
        m = p.match(f)
        if m:
            existing_indices.append(int(f.replace(PREFIX, "").replace(".jpg", "")))
    
    next_idx = max(existing_indices) + 1 if existing_indices else 1
    
    print(f"Renaming {len(to_rename)} files starting from index {next_idx}...")
    
    for filename in to_rename:
        old_path = os.path.join(DIR, filename)
        new_name = f"{PREFIX}{next_idx:03d}.jpg"
        new_path = os.path.join(DIR, new_name)
        
        # Ensure we don't overwrite
        while os.path.exists(new_path):
            next_idx += 1
            new_name = f"{PREFIX}{next_idx:03d}.jpg"
            new_path = os.path.join(DIR, new_name)
            
        os.rename(old_path, new_path)
        print(f"Renamed {filename} -> {new_name}")
        next_idx += 1

if __name__ == "__main__":
    if os.path.exists(DIR):
        rename_current()
    else:
        print("Directory not found.")
