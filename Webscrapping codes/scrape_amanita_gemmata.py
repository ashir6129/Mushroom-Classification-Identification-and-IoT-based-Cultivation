
import os
import time
import requests
import logging
import sys
import re
from PIL import Image
from io import BytesIO

# ============================================================
# CONFIGURATION
# ============================================
# Taxon ID extracted from: https://www.inaturalist.org/taxa/350046-Amanita-junquillea/
TAXON_ID = "350046" 
MUSHROOM_NAME = "amanita_gemmata"
SAVE_DIR = f"/home/ashirkhan/Updated Data set/Professional_Mushroom_Dataset/{MUSHROOM_NAME}"
TARGET_COUNT = 600
ID_LOG_FILE = os.path.join(SAVE_DIR, "downloaded_ids.txt")

# API Settings
API_URL = "https://api.inaturalist.org/v1/observations"
PER_PAGE = 200

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

def get_downloaded_ids():
    if not os.path.exists(ID_LOG_FILE):
        return set()
    with open(ID_LOG_FILE, "r") as f:
        return set(line.strip() for line in f if line.strip())

def save_downloaded_id(photo_id):
    with open(ID_LOG_FILE, "a") as f:
        f.write(f"{photo_id}\n")

def get_next_sequential_index():
    if not os.path.exists(SAVE_DIR):
        return 1
    files = [f for f in os.listdir(SAVE_DIR) if f.startswith(f"{MUSHROOM_NAME}_") and f.endswith(".jpg")]
    indices = []
    pattern = re.compile(rf"^{MUSHROOM_NAME}_(\d+)\.jpg$")
    for f in files:
        match = pattern.match(f)
        if match:
            indices.append(int(match.group(1)))
    return max(indices) + 1 if indices else 1

def download_image(url, target_path):
    try:
        # Get high res version
        high_res_url = url.replace('square', 'large').replace('medium', 'large')
        response = requests.get(high_res_url, timeout=15)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            if img.mode != 'RGB':
                img = img.convert('RGB')
            img.save(target_path, "JPEG", quality=90)
            return True
    except Exception as e:
        logger.debug(f"Failed to download {url}: {e}")
    return False

def main():
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)
    
    downloaded_ids = get_downloaded_ids()
    next_idx = get_next_sequential_index()
    
    logger.info(f"🚀 Starting download for: {MUSHROOM_NAME} (Taxon ID: {TAXON_ID})")
    logger.info(f"📊 Starting from index: {next_idx}")
    
    current_total = next_idx - 1
    page = 1
    
    while current_total < TARGET_COUNT:
        params = {
            "taxon_id": TAXON_ID,
            "quality_grade": "research", 
            "per_page": PER_PAGE,
            "page": page,
            "photos": "true"
        }
        
        try:
            response = requests.get(API_URL, params=params, timeout=20)
            if response.status_code != 200:
                logger.error(f"API Error: Status {response.status_code}")
                break
                
            data = response.json()
            results = data.get('results', [])
            
            if not results:
                logger.info("🏁 No more verified images found for this species.")
                break
                
            logger.info(f"📄 Page {page}: Processing {len(results)} observations...")
            
            for obs in results:
                if current_total >= TARGET_COUNT: break
                
                for photo in obs.get('photos', []):
                    if current_total >= TARGET_COUNT: break
                    
                    photo_id = str(photo['id'])
                    if photo_id in downloaded_ids:
                        continue
                        
                    target_filename = f"{MUSHROOM_NAME}_{next_idx:03d}.jpg"
                    target_path = os.path.join(SAVE_DIR, target_filename)
                    
                    url = photo['url']
                    if download_image(url, target_path):
                        save_downloaded_id(photo_id)
                        downloaded_ids.add(photo_id)
                        current_total += 1
                        if current_total % 5 == 0:
                            logger.info(f"✅ Saved: {target_filename} (Total: {current_total}/{TARGET_COUNT})")
                        next_idx += 1
            
            page += 1
            time.sleep(1) # Be patient with the API
            
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            break

    logger.info(f"✨ Finished! Total images for {MUSHROOM_NAME}: {current_total}")

if __name__ == "__main__":
    main()
