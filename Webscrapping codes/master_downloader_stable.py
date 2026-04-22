
import os
import time
import requests
import logging
import sys
import re
from PIL import Image
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor, as_completed

# ============================================================
# HIGH SPEC MUSHROOM DOWNLOADER (V4 - Fast & Stable)
# ============================================================
LIST_FILE = "/home/ashirkhan/Updated Data set/numbered_mushroom_list.txt"
BASE_DIR = "/home/ashirkhan/Updated Data set/Professional_Mushroom_Dataset"
TARGET_COUNT = 600
API_URL = "https://api.inaturalist.org/v1/observations"
PER_PAGE = 200

# SETTINGS
MAX_THREADS = 15             # Increased from 8 to 15 for extra speed
DELAY_BETWEEN_PAGES = 0.5   # Decreased from 1.0 to 0.5 for faster pagination
DELAY_BETWEEN_SPECIES = 2.0 # Decreased from 5.0 to 2.0

# Hardcoded IDs for the first few (if links are missing in file)
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
LOG_PATH = "/home/ashirkhan/Updated Data set/stable_download.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(LOG_PATH)
    ]
)
logger = logging.getLogger(__name__)

def clean_name(name):
    """Converts '1) Almond Mushroom' -> '1)_almond_mushroom'"""
    name = name.strip().lower()
    name = re.sub(r'[\s\-]+', '_', name)
    if ')' in name and not name.startswith(name.split(')')[0] + ')_'):
        name = name.replace(')', ')_')
    name = name.replace('__', '_')
    return name

def parse_list():
    species_list = []
    if not os.path.exists(LIST_FILE):
        return species_list
    
    # Custom fix for IDs that are known to be broken in the original list
    BROKEN_FIXES = {
        "30)_cauliflower_fungus": "63014",
        "31)_cedarwood_waxcap": "485130"
    }

    with open(LIST_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line: continue
            
            # Extract basic name/number first
            name_part = line.split('http')[0].split('-')[0].strip()
            folder_name = clean_name(name_part)
            
            # Extract Taxon ID from link
            taxon_id = None
            link_match = re.search(r'taxa/(\d+)', line)
            if link_match:
                taxon_id = link_match.group(1)
            
            # Application of manual fixes
            if folder_name in BROKEN_FIXES:
                taxon_id = BROKEN_FIXES[folder_name]

            # Fallback for known IDs if link is missing
            if not taxon_id:
                lookup_key = name_part.lower()
                for k, v in KNOWN_IDS.items():
                    if k in lookup_key:
                        taxon_id = v
                        break
            
            if taxon_id:
                species_list.append({"id": taxon_id, "name": folder_name})
    return species_list

def get_downloaded_ids(log_file):
    if not os.path.exists(log_file):
        return set()
    with open(log_file, "r") as f:
        return set(line.strip() for line in f if line.strip())

def save_downloaded_id(log_file, photo_id):
    try:
        with open(log_file, "a") as f:
            f.write(f"{photo_id}\n")
    except Exception as e:
        logger.error(f"Error saving ID to {log_file}: {e}")

def get_next_sequential_index(save_dir, name):
    if not os.path.exists(save_dir):
        return 1
    files = [f for f in os.listdir(save_dir) if f.endswith(".jpg")]
    indices = []
    pattern = re.compile(rf".*?(\d+)\.jpg$")
    for f in files:
        match = pattern.match(f)
        if match:
            indices.append(int(match.group(1)))
    return max(indices) + 1 if indices else 1

def download_image_task(url, target_path, photo_id, log_file):
    """Threaded task for downloading a single image"""
    try:
        high_res_url = url.replace('square', 'large').replace('medium', 'large').replace('small', 'large')
        with requests.get(high_res_url, timeout=20, stream=True) as response:
            if response.status_code == 200:
                with Image.open(BytesIO(response.content)) as img:
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                    img.save(target_path, "JPEG", quality=90)
                save_downloaded_id(log_file, photo_id)
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
    
    logger.info(f"\n🚀 Processing: {name} (ID: {taxon_id})")
    
    try:
        first_params = {"taxon_id": taxon_id, "quality_grade": "any", "per_page": 1, "page": 1}
        with requests.get(API_URL, params=first_params, timeout=20) as res:
            if res.status_code == 200:
                total_available = res.json().get('total_results', 0)
                logger.info(f"📊 iNaturalist reports {total_available} total images for this species.")
                current_target = min(TARGET_COUNT, total_available)
            else:
                current_target = TARGET_COUNT
    except Exception:
        current_target = TARGET_COUNT

    if current_total >= current_target:
        logger.info(f"✅ Already reached target ({current_total}/{current_target}). Skipping.")
        return

    logger.info(f"📈 Resuming download: progress {current_total}/{current_target}")
    
    page = (current_total // PER_PAGE) + 1
    
    while current_total < current_target:
        params = {
            "taxon_id": taxon_id,
            "quality_grade": "any", 
            "per_page": PER_PAGE,
            "page": page,
            "photos": "true"
        }
        
        try:
            with requests.get(API_URL, params=params, timeout=30) as response:
                if response.status_code == 429:
                    logger.warning("❌ Rate limited. Sleeping for 2 minutes...")
                    time.sleep(120)
                    continue
                if response.status_code != 200:
                    time.sleep(60)
                    continue
                    
                data = response.json()
                results = data.get('results', [])
                if not results: break
                
                # Setup ThreadPool for this batch of observations
                download_tasks = []
                with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
                    for obs in results:
                        if (current_total + len(download_tasks)) >= current_target: break
                        for photo in obs.get('photos', []):
                            if (current_total + len(download_tasks)) >= current_target: break
                            
                            p_id = str(photo['id'])
                            if p_id in downloaded_ids: continue
                            
                            t_filename = f"{name}_{next_idx:03d}.jpg"
                            t_path = os.path.join(save_dir, t_filename)
                            
                            # Add to thread pool
                            future = executor.submit(download_image_task, photo['url'], t_path, p_id, log_file)
                            download_tasks.append(future)
                            next_idx += 1

                    # Collect results as they finish
                    for future in as_completed(download_tasks):
                        if future.result():
                            current_total += 1
                            if current_total % 25 == 0:
                                logger.info(f"   📸 {name}: {current_total}/{current_target}")

            page += 1
            if current_total >= current_target: break
            time.sleep(DELAY_BETWEEN_PAGES)
            
        except Exception as e:
            logger.error(f"   ⚠️ Error during scrape cycle: {e}")
            time.sleep(10)
            break

def main():
    logger.info("🎬 Initializing BLAZING FAST Master Mushroom Downloader v4...")
    species_to_process = parse_list()
    logger.info(f"📋 Found {len(species_to_process)} mushroom species.")
    
    for species in species_to_process:
        if "almond_mushroom" in species['name'].lower():
            continue
        try:
            scrape_species(species)
            time.sleep(DELAY_BETWEEN_SPECIES)
        except Exception as e:
            logger.error(f"💥 Fatal error: {e}")
            time.sleep(30)

if __name__ == "__main__":
    main()
