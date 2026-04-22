import os
import random
from PIL import Image, ImageEnhance

# fast_augmentator.py
BASE_DIR = "/home/ashirkhan/Updated Data set/Professional_Mushroom_Dataset"
TARGET_COUNT = 600

# Handle extremely large images
Image.MAX_IMAGE_PIXELS = None

def augment_image(image_path, save_path):
    try:
        img = Image.open(image_path)
        img = img.convert('RGB')
        w, h = img.size
        
        # Select a random augmentation from the pipeline
        choice = random.choice(['flip', 'rotate', 'zoom', 'brightness', 'crop'])
        
        if choice == 'flip':
            aug_img = img.transpose(Image.FLIP_LEFT_RIGHT)
            
        elif choice == 'rotate':
            # Subtle rotation (-15 to 15 degrees)
            angle = random.uniform(-15, 15)
            aug_img = img.rotate(angle, resample=Image.BICUBIC, expand=False)
            
        elif choice == 'zoom':
            # Subtle zoom (90% to 100% of the image)
            zoom_factor = random.uniform(0.9, 0.95)
            left = w * (1 - zoom_factor) / 2
            top = h * (1 - zoom_factor) / 2
            aug_img = img.crop((left, top, w - left, h - top)).resize((w, h), Image.LANCZOS)
            
        elif choice == 'brightness':
            # Subtle brightness adjustment
            factor = random.uniform(0.8, 1.2)
            enhancer = ImageEnhance.Brightness(img)
            aug_img = enhancer.enhance(factor)
            
        elif choice == 'crop':
            # Small random crop (max 10% off each side)
            left = random.randint(0, int(w * 0.1))
            top = random.randint(0, int(h * 0.1))
            right = w - random.randint(0, int(w * 0.1))
            bottom = h - random.randint(0, int(h * 0.1))
            aug_img = img.crop((left, top, right, bottom)).resize((w, h), Image.LANCZOS)
            
        aug_img.save(save_path, 'JPEG', quality=95)
        return True
    except Exception:
        return False

def process_dataset():
    categories = [d for d in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, d))]
    
    print(f"🚀 Starting Fast Data Augmentation to reach {TARGET_COUNT} images per class...")
    
    for cat in categories:
        cat_path = os.path.join(BASE_DIR, cat)
        species_folders = [d for d in os.listdir(cat_path) if os.path.isdir(os.path.join(cat_path, d))]
        species_folders.sort()
        
        for folder in species_folders:
            path = os.path.join(cat_path, folder)
            images = [f for f in os.listdir(path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            current_count = len(images)
            
            if current_count == 0:
                print(f"⚠️ Skipping {cat}/{folder} (0 images found).")
                continue
                
            if current_count < TARGET_COUNT:
                needed = TARGET_COUNT - current_count
                print(f"📈 Augmenting {cat}/{folder}: {current_count} -> {TARGET_COUNT} (+{needed})")
                
                for i in range(needed):
                    source_img = random.choice(images)
                    source_path = os.path.join(path, source_img)
                    # Create name: original_name_AUG_001.jpg
                    new_name = f"{source_img.split('.')[0]}_AUG_{i:03d}.jpg"
                    new_path = os.path.join(path, new_name)
                    
                    augment_image(source_path, new_path)
            elif current_count > TARGET_COUNT:
                print(f"✂️ Trimming {cat}/{folder}: {current_count} -> {TARGET_COUNT}")
                excess = images[TARGET_COUNT:]
                for f in excess:
                    os.remove(os.path.join(path, f))

    print("🏁 Dataset Balancing Complete!")

if __name__ == "__main__":
    process_dataset()
