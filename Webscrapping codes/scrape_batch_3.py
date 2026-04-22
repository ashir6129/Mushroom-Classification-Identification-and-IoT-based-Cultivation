
import os
import time
import requests
import logging
import sys
import re
from PIL import Image
from io import BytesIO

# ============================================================
# TARGET MUSHROOMS CONFIG - BATCH 3
# ============================================================
MUSHROOMS = [
    {"id": "63489", "name": "14)_bitter_bolete"},
    {"id": "83419", "name": "15)_black_bulgar"},
    {"id": "133686", "name": "16)_black_morel"},
    {"id": "194414", "name": "17)_blackening_brittlegill"},
    {"id": "125738", "name": "18)_blackening_polypore"}
]

BASE_DIR = "/home/ashirkhan/Updated Data set/Professional_Mushroom_Dataset"
TARGET_COUNT = 600
API_URL = "https://api.inaturalist.org/v1/observations"
PER_PAGE = 200

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

def get_downloaded_ids(log_file):
    if not os.path.exists(log_file):
        return set()
    with open(log_file, "r") as f:
        return set(line.strip() for line in f if line.strip())

def save_downloaded_id(log_file, photo_id):
    with open(log_file, "a") as f:
        f.write(f"{photo_id}\n")

def get_next_sequential_index(save_dir, name):
    if not os.path.exists(save_dir):
        return 1
    files = [f for f in os.listdir(save_dir) if f.startswith(f"{name}_") and f.endswith(".jpg")]
    indices = []
    pattern = re.compile(rf".*?(\d+)\.jpg$")
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
    except Exception:
        pass
    return False

def scrape_species(species):
    taxon_id = species["id"]
    name = species["name"]
    save_dir = os.path.join(BASE_DIR, name)
    os.makedirs(save_dir, exist_ok=True)
    
    log_file = os.path.join(save_dir, "downloaded_ids.txt")
    downloaded_ids = get_downloaded_ids(log_file)
    next_idx = get_next_sequential_index(save_dir, name)
    
    logger.info(f"\n🚀 Starting Batch 3: {name} (ID: {taxon_id})")
    current_total = next_idx - 1
    page = 1
    
    while current_total < TARGET_COUNT:
        params = {
            "taxon_id": taxon_id,
            "quality_grade": "research",
            "per_page": PER_PAGE,
            "page": page,
            "photos": "true"
        }
        
        try:
            response = requests.get(API_URL, params=params, timeout=20)
            if response.status_code != 200:
                logger.error(f"   API Error status {response.status_code}")
                break
                
            results = response.json().get('results', [])
            if not results:
                logger.info(f"   🏁 End of verified data for {name}.")
                break
                
            for obs in results:
                if current_total >= TARGET_COUNT: break
                for photo in obs.get('photos', []):
                    if current_total >= TARGET_COUNT: break
                    
                    photo_id = str(photo['id'])
                    if photo_id in downloaded_ids: continue
                    
                    target_filename = f"{name}_{next_idx:03d}.jpg"
                    target_path = os.path.join(save_dir, target_filename)
                    
                    if download_image(photo['url'], target_path):
                        save_downloaded_id(log_file, photo_id)
                        downloaded_ids.add(photo_id)
                        current_total += 1
                        next_idx += 1
                        if current_total % 25 == 0:
                            logger.info(f"   ✅ {name}: {current_total}/{TARGET_COUNT}")
                            
            page += 1
            time.sleep(2) # Increased delay to be very safe with 3 concurrent batches
            
        except Exception as e:
            logger.error(f"   Error: {e}")
            break

def main():
    logger.info("🍄 Starting Batch 3 Downloader (Species 14-18)...")
    for species in MUSHROOMS:
        scrape_species(species)
    logger.info("\n✨ Batch 3 complete!")

if __name__ == "__main__":
    main()
