
import os
import time
import requests
import logging
import sys
import re
from PIL import Image
from io import BytesIO

# ============================================================
# TARGET MUSHROOMS CONFIG
# ============================================================
MUSHROOMS = [
    {"id": "55899", "name": "4)_amethyst_deceiver"},
    {"id": "1525546", "name": "5)_aniseed_funnel"},
    {"id": "875042", "name": "6)_ascot_hat"},
    {"id": "510854", "name": "7)_bay_bolete"},
    {"id": "382882", "name": "8)_bearded_milkcap"}
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
    files = [f for f in os.listdir(save_dir) if f.startswith(f"{name}_") and f.endswith(".jpg")]
    indices = []
    # Pattern to match 4)_amethyst_deceiver_001.jpg -> handle name prefix carefully
    clean_name = name.split(')_')[-1] # extract 'amethyst_deceiver'
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
    
    logger.info(f"\n🚀 Starting: {name} (ID: {taxon_id})")
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
                    
                    # File naming: e.g. 4)_amethyst_deceiver_001.jpg
                    target_filename = f"{name}_{next_idx:03d}.jpg"
                    target_path = os.path.join(save_dir, target_filename)
                    
                    if download_image(photo['url'], target_path):
                        save_downloaded_id(log_file, photo_id)
                        downloaded_ids.add(photo_id)
                        current_total += 1
                        next_idx += 1
                        if current_total % 10 == 0:
                            logger.info(f"   ✅ {name}: {current_total}/{TARGET_COUNT}")
                            
            page += 1
            time.sleep(1) # IP safety
            
        except Exception as e:
            logger.error(f"   Error: {e}")
            break

def main():
    logger.info("🍄 Starting Batch Downloader for 5 species...")
    for species in MUSHROOMS:
        # We run them sequentially to avoid hammering the API too hard from one IP
        scrape_species(species)
    logger.info("\n✨ All batches complete!")

if __name__ == "__main__":
    main()
