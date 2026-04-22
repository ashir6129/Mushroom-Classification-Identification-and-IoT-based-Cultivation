
import os
import time
import json
import hashlib
import requests
import logging
import sys
from datetime import datetime
from PIL import Image
from io import BytesIO

# ============================================================
# CONFIGURATION
# ============================================================
# Where to save these high-quality images
DATASET_DIR = "/home/ashirkhan/Updated Data set/Professional_Mushroom_Dataset"
# Source directory to get the mushroom names from
SOURCE_DIR = "/home/ashirkhan/Updated Data set/raw_images_renamed"
# Target count per class
TARGET_COUNT = 600
# Save progress here
PROGRESS_FILE = "/home/ashirkhan/Updated Data set/inat_progress.json"
# iNaturalist API settings
API_URL = "https://api.inaturalist.org/v1/observations"
# How many images per page on API
PER_PAGE = 200
# Quality grade ('research' = expert-verified, highest quality)
QUALITY_GRADE = "research"

# Logging setup
log_file = "/home/ashirkhan/Updated Data set/inat_download_log.txt"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def clean_name_for_search(folder_name):
    # Convert 'almond_mushroom' -> 'almond mushroom' or 'amanita_gemmata' -> 'amanita gemmata'
    return folder_name.replace('_', ' ').replace('-', ' ').strip()

def get_existing_hashes(path):
    hashes = set()
    if not os.path.exists(path):
        return hashes
    for f in os.listdir(path):
        # We assume files are named with hashes or we hash them now
        # For speed, let's just use filenames if they are hash-based
        if f.lower().endswith(('.jpg', '.jpeg', '.png')):
            hashes.add(os.path.splitext(f)[0])
    return hashes

def download_image(url, target_path):
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            # Check if it's a valid image
            img = Image.open(BytesIO(response.content))
            img.verify() # Basic check
            
            # Re-open for saving & resizing (to save space)
            img = Image.open(BytesIO(response.content))
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Resize if very large (preserving aspect ratio)
            max_size = 800
            if max(img.size) > max_size:
                img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
                
            img.save(target_path, "JPEG", quality=85)
            return True
    except Exception as e:
        logger.debug(f"Failed to download {url}: {e}")
    return False

def fetch_inat_data(query, page=1):
    params = {
        "taxon_name": query,
        "quality_grade": QUALITY_GRADE,
        "per_page": PER_PAGE,
        "page": page,
        "order": "desc",
        "order_by": "created_at",
        "photos": "true"
    }
    try:
        response = requests.get(API_URL, params=params, timeout=20)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        logger.error(f"API Error: {e}")
    return None

def main():
    os.makedirs(DATASET_DIR, exist_ok=True)
    
    # Load progress
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as f:
            progress = json.load(f)
    else:
        progress = {}

    # Get categories to process
    categories = sorted([d for d in os.listdir(SOURCE_DIR) if os.path.isdir(os.path.join(SOURCE_DIR, d))])
    
    logger.info("="*60)
    logger.info(f"🍄 iNaturalist High-Quality Downloader")
    logger.info(f"Target: {TARGET_COUNT} images per class")
    logger.info(f"Categories to process: {len(categories)}")
    logger.info("="*60)

    for cat_idx, cat in enumerate(categories, 1):
        # Skip if already finished
        if cat in progress and progress[cat].get('completed', False):
            if progress[cat].get('current_count', 0) >= TARGET_COUNT:
                logger.info(f"[{cat_idx}/{len(categories)}] ⏭️  Skipping {cat} (Already done)")
                continue

        cat_folder = os.path.join(DATASET_DIR, cat)
        os.makedirs(cat_folder, exist_ok=True)
        
        search_query = clean_name_for_search(cat)
        logger.info(f"\n[{cat_idx}/{len(categories)}] 🍄 Processing: {search_query}")
        
        # Track already downloaded (to avoid duplicates)
        existing_photos = get_existing_hashes(cat_folder)
        start_count = len(existing_photos)
        current_count = start_count
        
        logger.info(f"   Currently have {start_count} images. Need {TARGET_COUNT - start_count} more.")

        page = 1
        no_more_results = False
        
        while current_count < TARGET_COUNT and not no_more_results:
            data = fetch_inat_data(search_query, page)
            if not data or not data.get('results'):
                logger.warning(f"   No more records found for {cat}. (Found total {current_count})")
                no_more_results = True
                break
                
            results = data['results']
            logger.info(f"   Page {page}: Processing {len(results)} potential observations...")
            
            for obs in results:
                if current_count >= TARGET_COUNT: break
                
                # Each observation can have multiple photos
                for p in obs.get('photos', []):
                    if current_count >= TARGET_COUNT: break
                    
                    photo_id = str(p['id'])
                    # iNaturalist URLs: .../square.jpg, .../medium.jpg, .../original.jpg
                    # We want 'medium' or 'large' for quality
                    url = p['url'].replace('square', 'medium')
                    
                    if photo_id in existing_photos:
                        continue
                        
                    target_filename = f"{photo_id}.jpg"
                    target_path = os.path.join(cat_folder, target_filename)
                    
                    if download_image(url, target_path):
                        existing_photos.add(photo_id)
                        current_count += 1
                        if current_count % 20 == 0:
                            logger.info(f"      Progress: {current_count}/{TARGET_COUNT}")
                            
            page += 1
            if len(results) < PER_PAGE:
                no_more_results = True
            
            # API Rate limiting
            time.sleep(1) 

        # Update progress
        progress[cat] = {
            'completed': current_count >= TARGET_COUNT or no_more_results,
            'current_count': current_count,
            'last_updated': datetime.now().isoformat(),
            'search_query': search_query
        }
        with open(PROGRESS_FILE, 'w') as f:
            json.dump(progress, f, indent=2)

        logger.info(f"   ✅ Finished processing {cat}. (Final: {current_count})")

    logger.info("\n" + "="*60)
    logger.info("🎉 DATASET DOWNLOAD COMPLETE!")
    logger.info("="*60)

if __name__ == "__main__":
    main()
