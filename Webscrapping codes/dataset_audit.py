
import os

BASE_DIR = "/home/ashirkhan/Updated Data set/Professional_Mushroom_Dataset"
TARGET_COUNT = 600

def audit():
    if not os.path.exists(BASE_DIR):
        print(f"Error: {BASE_DIR} not found.")
        return

    categories = sorted([d for d in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, d))])
    
    print("="*60)
    print(f"📊 Dataset Audit: {BASE_DIR}")
    print(f"Target: {TARGET_COUNT} images per species")
    print("="*60)
    
    total_images = 0
    
    for cat in categories:
        cat_path = os.path.join(BASE_DIR, cat)
        subfolders = [d for d in os.listdir(cat_path) if os.path.isdir(os.path.join(cat_path, d))]
        
        cat_total = 0
        if not subfolders:
            # Special case for flat categories if any (though we structured Class_Zero to have subfolders)
            images = [f for f in os.listdir(cat_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            cat_total = len(images)
            print(f"📁 Category: {cat} (Flat Structure)")
            print(f"   └── Count: {cat_total}")
        else:
            print(f"📁 Category: {cat}")
            for sub in sorted(subfolders):
                sub_path = os.path.join(cat_path, sub)
                images = [f for f in os.listdir(sub_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
                count = len(images)
                cat_total += count
                status = "✅ OK" if count >= TARGET_COUNT else f"⚠️ NEED {TARGET_COUNT - count} MORE"
                print(f"   ├── {sub:30}: {count:4} images [{status}]")
        
        total_images += cat_total
        print(f"   └── TOTAL FOR {cat}: {cat_total}")
        print("-" * 40)

    print(f"\n📈 TOTAL DATASET SIZE: {total_images} images")
    print("="*60)

if __name__ == "__main__":
    audit()
