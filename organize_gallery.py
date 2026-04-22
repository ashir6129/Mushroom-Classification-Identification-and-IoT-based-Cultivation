import os
import shutil
from PIL import Image

# Paths
SRC_DIR = "frontend/4class"
DEST_DIR = "frontend/assets/mushrooms_gallery"

def organize_images():
    if not os.path.exists(DEST_DIR):
        os.makedirs(DEST_DIR)
        print(f"Created {DEST_DIR}")

    classes = ["Non_Poisnous_Edible", "Non_Poisnous_Non_Edible", "Poisnous_Non_Useable", "Poisnous_Useable"]
    
    total_converted = 0
    mushrooms_processed = 0

    for class_name in classes:
        class_path = os.path.join(SRC_DIR, class_name)
        if not os.path.exists(class_path):
            print(f"Warning: Class path {class_path} not found.")
            continue
            
        print(f"Processing class: {class_name}...")
        
        # Each mushroom has its own folder inside the class folder
        for mushroom_name in os.listdir(class_path):
            mushroom_path = os.path.join(class_path, mushroom_name)
            if os.path.isdir(mushroom_path):
                # Sort images numerically (001, 002, etc.)
                images = sorted([f for f in os.listdir(mushroom_path) if f.endswith(('.png', '.jpg', '.jpeg'))])
                
                # Take top 4
                top_4 = images[:4]
                
                for i, img_name in enumerate(top_4):
                    src_img_path = os.path.join(mushroom_path, img_name)
                    # Force convert to .jpg for maximum compatibility and smaller size
                    dest_img_name = f"{mushroom_name}_{i+1}.jpg"
                    dest_img_path = os.path.join(DEST_DIR, dest_img_name)
                    
                    try:
                        with Image.open(src_img_path) as img:
                            # Convert to RGB (removes alpha channel which can cause decoders to fail)
                            if img.mode in ("RGBA", "P"):
                                img = img.convert("RGB")
                            img.save(dest_img_path, "JPEG", quality=85)
                        total_converted += 1
                    except Exception as e:
                        print(f"Error converting {src_img_path}: {e}")
                
                mushrooms_processed += 1

    print(f"\nDone! Processed {mushrooms_processed} mushrooms.")
    print(f"Converted {total_converted} images to JPEG in {DEST_DIR}.")

if __name__ == "__main__":
    organize_images()
