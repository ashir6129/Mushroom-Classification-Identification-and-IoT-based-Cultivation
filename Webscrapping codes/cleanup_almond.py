
import os
import re

DIR = "/home/ashirkhan/Updated Data set/Professional_Mushroom_Dataset/almond_mushroom"
PREFIX = "almond_mushroom_"

def cleanup():
    if not os.path.exists(DIR):
        print("Directory not found.")
        return
        
    files = os.listdir(DIR)
    pattern = re.compile(rf"^{PREFIX}(\d+)\.jpg$")
    
    deleted_count = 0
    for f in files:
        match = pattern.match(f)
        if match:
            idx = int(match.group(1))
            if idx > 308:
                try:
                    os.remove(os.path.join(DIR, f))
                    # print(f"Deleted: {f}")
                    deleted_count += 1
                except Exception as e:
                    print(f"Error deleting {f}: {e}")
    
    print(f"✅ Successfully deleted {deleted_count} images (from 309 onwards).")
    remaining = len([f for f in os.listdir(DIR) if f.endswith(".jpg")])
    print(f"📊 Remaining images in folder: {remaining}")

if __name__ == "__main__":
    cleanup()
