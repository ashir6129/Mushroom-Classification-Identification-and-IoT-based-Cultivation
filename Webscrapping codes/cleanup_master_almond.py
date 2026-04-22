
import os
import re

DIR = "/home/ashirkhan/Updated Data set/Professional_Mushroom_Dataset/1)_almond_mushroom"

def cleanup():
    if not os.path.exists(DIR):
        print("Directory not found.")
        return
        
    files = os.listdir(DIR)
    # Pattern to match the sequential suffix: e.g. 1)_almond_mushroom_325.jpg
    pattern = re.compile(r".*?(\d+)\.jpg$")
    
    deleted_count = 0
    for f in files:
        match = pattern.match(f)
        if match:
            idx = int(match.group(1))
            if idx > 308:
                try:
                    os.remove(os.path.join(DIR, f))
                    deleted_count += 1
                except Exception as e:
                    print(f"Error deleting {f}: {e}")
    
    print(f"✅ Successfully deleted {deleted_count} new images for Almond Mushroom (kept original 308).")

if __name__ == "__main__":
    cleanup()
