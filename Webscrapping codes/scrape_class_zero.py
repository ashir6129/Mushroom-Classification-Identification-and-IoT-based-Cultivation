
import os
import time
import requests
import logging
import sys
from PIL import Image
from io import BytesIO
import concurrent.futures
import threading

# ============================================================
# CONFIGURATION
# ============================================================
TARGET_DIR = "/home/ashirkhan/Updated Data set/Professional_Mushroom_Dataset/Class_Zero/Background"
TARGET_COUNT = 600
API_URL = "https://api.inaturalist.org/v1/observations"
PER_PAGE = 200

# Queries for Class Zero (Background/Other)
QUERIES = [
    {"q": "forest floor"}, {"q": "mossy ground"}, {"q": "pine needles"},
    {"q": "tree bark"}, {"q": "grass"}, {"q": "dirt ground"},
    {"q": "leaves"}, {"taxon_id": 47126}, {"taxon_id": 311249},
    {"taxon_id": 1}, {"q": "basket"}, {"q": "shoes on grass"},
    {"q": "forest floor texture"}, {"q": "dry sticks"}, {"q": "fallen logs"},
    {"q": "green moss"}, {"q": "wildflowers"}, {"q": "fern leaves"},
    {"q": "clover patch"}, {"q": "soil ground"}, {"q": "human hands"},
    {"q": "outdoors basket"}, {"q": "wood chips"}, {"q": "pine cones"},
    {"q": "nature background"}, {"taxon_id": 47170}, {"taxon_id": 47169},
    {"taxon_id": 48225}, {"q": "unknown mushroom"}, {"q": "generic mushroom"}
]

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("/home/ashirkhan/Updated Data set/class_zero_download.log")
    ]
)
logger = logging.getLogger(__name__)

# Global lock for thread-safe file operations
file_lock = threading.Lock()

def get_next_index(directory):
    files = [f for f in os.listdir(directory) if f.startswith("Class_Zero_") and f.endswith(".jpg")]
    if not files: return 1
    indices = set()
    for f in files:
        try:
            indices.add(int(f.split('_')[-1].split('.')[0]))
        except: continue
    i = 1
    while i in indices:
        i += 1
    return i

def get_file_count(directory):
    return len([f for f in os.listdir(directory) if f.lower().endswith('.jpg')])

def download_image(url, path):
    try:
        high_res_url = url.replace('square', 'large').replace('medium', 'large')
        res = requests.get(high_res_url, timeout=15)
        if res.status_code == 200:
            img = Image.open(BytesIO(res.content))
            img = img.convert('RGB')
            if max(img.size) > 1024:
                img.thumbnail((1024, 1024), Image.Resampling.LANCZOS)
            img.save(path, 'JPEG', quality=85)
            return True
    except: pass
    return False

def scrape_query(query_params):
    if get_file_count(TARGET_DIR) >= TARGET_COUNT: return False
    page = 1
    params = {"per_page": PER_PAGE, "photos": "true", "quality_grade": "research"}
    params.update(query_params)
    label = query_params.get('q') or f"Taxon_{query_params.get('taxon_id')}"
    logger.info(f"🔍 Searching: {label}")

    while True:
        try:
            params['page'] = page
            res = requests.get(API_URL, params=params, timeout=20)
            if res.status_code != 200: break
            results = res.json().get('results', [])
            if not results: break
            
            download_urls = []
            for obs in results:
                for photo in obs.get('photos', []):
                    download_urls.append(photo['url'])
                    break
            
            def thread_download(url):
                with file_lock:
                    if get_file_count(TARGET_DIR) >= TARGET_COUNT:
                        return
                    idx = get_next_index(TARGET_DIR)
                    filename = f"Class_Zero_{idx:03d}.jpg"
                    path = os.path.join(TARGET_DIR, filename)
                    # Touch the file to "reserve" it for other threads
                    open(path, 'a').close()
                
                # Now download (overwrite the placeholder)
                if download_image(url, path):
                    logger.info(f"   💾 Parallel Download: {filename}")
                else:
                    # If download fails, remove placeholder so it can be reused
                    try: os.remove(path)
                    except: pass

            with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
                executor.map(thread_download, download_urls)
            
            if get_file_count(TARGET_DIR) >= TARGET_COUNT: return False
            page += 1
            time.sleep(0.1)
        except Exception as e:
            logger.error(f"Error: {e}")
            break
    return True

def main():
    if not os.path.exists(TARGET_DIR): os.makedirs(TARGET_DIR)
    logger.info("🚀 Starting FAST Class Zero Scraping (20 workers)...")
    for q in QUERIES:
        if not scrape_query(q): break
    logger.info("✨ Speed Scrape Finished!")

if __name__ == "__main__":
    main()
