
import os
import time
import requests
import logging
import sys
import re
from PIL import Image
from io import BytesIO

# ============================================================
# MASTER DOWNLOADER CONFIG
# ============================================================
LIST_FILE = "/home/ashirkhan/Updated Data set/numbered_mushroom_list.txt"
BASE_DIR = "/home/ashirkhan/Updated Data set/Professional_Mushroom_Dataset"
TARGET_COUNT = 600
API_URL = "https://api.inaturalist.org/v1/observations"
PER_PAGE = 200

# Hardcoded IDs for the first 8 (in case links are missing in file)
KNOWN_IDS = {
    "1) almond mushroom": "51221",
    "2) amanita gemmata": "350046",
    "3) amethyst chanterelle": "566555",
    "4) amethyst deceiver": "55899",
    "5) aniseed funnel": "1525546",
    "6) ascot hat": "875042",
    "7) bay bolete": "510854",
    "8) bearded milkcap": "382882"
}

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("/home/ashirkhan/Updated Data set/master_download.log")
    ]
)
logger = logging.getLogger(__name__)

def clean_name(name):
    """Converts '1) Almond Mushroom' -> '1)_almond_mushroom'"""
    name = name.strip().lower()
    # Replace spaces and hyphens with underscores
    name = re.sub(r'[\s\-]+', '_', name)
    # Ensure it's in the format N)_name
    if ')' in name and not name.startswith(name.split(')')[0] + ')_'):
        name = name.replace(')', ')_')
    # Cleanup double underscores
    name = name.replace('__', '_')
    return name

def parse_list():
    species_list = []
    if not os.path.exists(LIST_FILE):
        return species_list
        
    with open(LIST_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line: continue
            
            # Extract Taxon ID from link
            taxon_id = None
            link_match = re.search(r'taxa/(\d+)', line)
            if link_match:
                taxon_id = link_match.group(1)
            
            # Extract basic name/number
            name_part = line.split('http')[0].split('-')[0].strip()
            folder_name = clean_name(name_part)
            
            # Fallback for known IDs if link is missing
            if not taxon_id:
                lookup_key = name_part.lower()
                if lookup_key in KNOWN_IDS:
                    taxon_id = KNOWN_IDS[lookup_key]
                else:
                    # Try fuzzy match for known ids
                    for k, v in KNOWN_IDS.items():
                        if k in lookup_key:
                            taxon_id = v
                            break
            
            if taxon_id:
                species_list.append({"id": taxon_id, "name": folder_name})
            else:
                logger.warning(f"⚠️ Could not find Taxon ID for line: {line}")
                
    return species_list

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
    files = [f for f in os.listdir(save_dir) if f.endswith(".jpg")]
    indices = []
    # Match any trailing number before .jpg
    pattern = re.compile(rf".*?(\d+)\.jpg$")
    for f in files:
        match = pattern.match(f)
        if match:
            indices.append(int(match.group(1)))
    return max(indices) + 1 if indices else 1

def download_image(url, target_path):
    try:
        # Get high res version
        high_res_url = url.replace('square', 'large').replace('medium', 'large')
        response = requests.get(high_res_url, timeout=20)
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
    
    current_total = next_idx - 1
    
    # Initial API call to check how many are available
    logger.info(f"\n🌟 Processing: {species.get('name')} (ID: {taxon_id})")
    
    try:
        first_params = {
            "taxon_id": taxon_id,
            "quality_grade": "research", 
            "per_page": 1,
            "page": 1
        }
        res = requests.get(API_URL, params=first_params, timeout=20)
        if res.status_code == 200:
            total_available = res.json().get('total_results', 0)
            logger.info(f"📊 iNaturalist reports {total_available} total 'Research Grade' images for this species.")
            current_target = min(TARGET_COUNT, total_available)
        else:
            logger.warning("⚠️ Could not fetch total available. Defaulting to 600.")
            current_target = TARGET_COUNT
    except Exception:
        current_target = TARGET_COUNT

    if current_total >= current_target:
        logger.info(f"✅ Already reached target ({current_total}/{current_target}). Skipping.")
        return

    logger.info(f"📉 Starting download: index {next_idx} to target {current_target}")
    
    page = 1
    while current_total < current_target:
        params = {
            "taxon_id": taxon_id,
            "quality_grade": "research", 
            "per_page": PER_PAGE,
            "page": page,
            "photos": "true"
        }
        
        try:
            response = requests.get(API_URL, params=params, timeout=30)
            if response.status_code != 200:
                logger.error(f"   ❌ API error {response.status_code}. Sleeping...")
                time.sleep(60)
                continue
                
            data = response.json()
            results = data.get('results', [])
            
            if not results:
                logger.info(f"   🏁 End of available images for {name}. Total: {current_total}")
                break
                
            for obs in results:
                if current_total >= current_target: break
                
                for photo in obs.get('photos', []):
                    if current_total >= current_target: break
                    
                    photo_id = str(photo['id'])
                    if photo_id in downloaded_ids:
                        continue
                        
                    target_filename = f"{name}_{next_idx:03d}.jpg"
                    target_path = os.path.join(save_dir, target_filename)
                    
                    if download_image(photo['url'], target_path):
                        save_downloaded_id(log_file, photo_id)
                        downloaded_ids.add(photo_id)
                        current_total += 1
                        next_idx += 1
                        if current_total % 25 == 0:
                            logger.info(f"   📸 {name}: {current_total}/{current_target}")
            
            page += 1
            time.sleep(1) # IP safety
            
        except Exception as e:
            logger.error(f"   ⚠️ Error during scrape: {e}")
            time.sleep(5)
            break

def main():
    logger.info("🎬 Initializing Master Mushroom Downloader v2...")
    species_to_process = parse_list()
    logger.info(f"📋 Found {len(species_to_process)} mushroom species.")
    
    for species in species_to_process:
        if "almond_mushroom" in species['name']:
            logger.info(f"⏭️ Skipping {species['name']} (Wrong dataset target).")
            continue
            
        try:
            scrape_species(species)
        except Exception as e:
            logger.error(f"💥 Error on {species['name']}: {e}")
            continue

    logger.info("\n🎉 MISSION COMPLETE! All species processed.")

if __name__ == "__main__":
    main()
