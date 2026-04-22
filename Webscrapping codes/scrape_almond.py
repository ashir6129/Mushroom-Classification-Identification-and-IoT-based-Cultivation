
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
# ============================================================
TAXON_ID = "179249"
MUSHROOM_NAME = "almond_mushroom"
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
    
    logger.info(f"🚀 Starting/Resuming download for: {MUSHROOM_NAME}")
    logger.info(f"📊 Current sequential index: {next_idx - 1}")
    
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
                logger.info("🏁 No more verified images found on iNaturalist.")
                break
                
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
                        logger.info(f"✅ Saved: {target_filename} (Total: {current_total})")
                        next_idx += 1
            
            page += 1
            time.sleep(1)
            
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            break

    logger.info(f"✨ Finished! Total images: {current_total}")

if __name__ == "__main__":
    main()
