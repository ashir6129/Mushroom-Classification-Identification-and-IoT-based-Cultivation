import os
import requests
import json
import logging
from PIL import Image
from io import BytesIO

# mushroom_turbo_scraper.py
BASE_DIR = "/home/ashirkhan/Updated Data set/Professional_Mushroom_Dataset"

SHORT_CLASSES = [
    { "id": 208, "name": "woodland_inkcap", "gbif": "8109355", "queries": ["Coprinellus silvaticus", "Coprinus silvaticus"] },
    { "id": 202, "name": "white_false_death_cap", "gbif": "5452083", "queries": ["Amanita citrina alba", "Amanita citrina var. alba"] },
    { "id": 149, "name": "scaly_wood_mushroom", "gbif": "8108291", "queries": ["Agaricus silvaticus", "Agaricus sylvaticus"] },
    { "id": 48, "name": "deadly_fibrecap", "gbif": "10776858", "queries": ["Inosperma erubescens", "Inocybe erubescens"] },
    { "id": 211, "name": "yellow_false_truffle", "gbif": "2524248", "queries": ["Rhizopogon luteolus"] },
    { "id": 98, "name": "jubilee_waxcap", "gbif": "8069214", "queries": ["Gliophorus reginae"] },
    { "id": 212, "name": "yellow_foot_waxcap", "gbif": "2538579", "queries": ["Cuphophyllus flavipes"] },
    { "id": 110, "name": "medusa_mushroom", "gbif": "2535047", "queries": ["Psathyrella caput-medusae"] },
    { "id": 113, "name": "oak_bolete", "gbif": "2524451", "queries": ["Boletus quercicola"] },
    { "id": 169, "name": "splendid_waxcap", "gbif": "2538572", "queries": ["Hygrocybe splendidissima"] }
]

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

def get_next_index(directory, prefix):
    files = [f for f in os.listdir(directory) if f.endswith('.jpg')]
    if not files: return 1
    indices = []
    for f in files:
        try:
            # Look for last number in filename before .jpg
            parts = f.replace('.jpg', '').split('_')
            idx = int(parts[-1])
            indices.append(idx)
        except: continue
    return max(indices) + 1 if indices else 1

def download_image(url, path):
    if os.path.exists(path): return False
    try:
        res = requests.get(url, timeout=10)
        if res.status_code == 200:
            img = Image.open(BytesIO(res.content))
            img = img.convert('RGB')
            img.save(path, 'JPEG')
            return True
    except: pass
    return False

def scrap_gbif(taxon_key, target_dir, prefix, limit=150):
    url = f"https://api.gbif.org/v1/occurrence/search?taxonKey={taxon_key}&mediaType=StillImage&limit={limit}"
    try:
        res = requests.get(url)
        results = res.json().get('results', [])
        count = 0
        for occ in results:
            for m in occ.get('media', []):
                if m.get('type') == 'StillImage':
                    img_url = m.get('identifier')
                    if not img_url: continue
                    idx = get_next_index(target_dir, prefix)
                    filename = f"{prefix}_{idx:03d}.jpg"
                    if download_image(img_url, os.path.join(target_dir, filename)):
                        count += 1
                        break
        logger.info(f"  [GBIF] {prefix}: Collected {count} images.")
        return count
    except: return 0

def scrap_wikimedia(query, target_dir, prefix, limit=50):
    api_url = "https://commons.wikimedia.org/w/api.php"
    params = {"action": "query", "format": "json", "list": "search", "srsearch": query, "srnamespace": "6", "srlimit": limit}
    try:
        res = requests.get(api_url, params=params)
        results = res.json().get('query', {}).get('search', [])
        count = 0
        for item in results:
            title = item.get('title')
            info_params = {"action": "query", "format": "json", "prop": "imageinfo", "titles": title, "iiprop": "url"}
            info_res = requests.get(api_url, params=info_params)
            pages = info_res.json().get('query', {}).get('pages', {})
            for pid in pages:
                info = pages[pid].get('imageinfo', [])
                if info:
                    idx = get_next_index(target_dir, prefix)
                    filename = f"{prefix}_{idx:03d}.jpg"
                    if download_image(info[0]['url'], os.path.join(target_dir, filename)):
                        count += 1
        logger.info(f"  [WIKI] {prefix}: Collected {count} images for '{query}'.")
        return count
    except: return 0

def scrap_mo(name, target_dir, prefix, limit=50):
    api_url = f"https://mushroomobserver.org/api2/images?name={name}&format=json"
    try:
        res = requests.get(api_url)
        results = res.json().get('results', [])
        count = 0
        for img_id in results[:limit]:
            img_url = f"https://images.mushroomobserver.org/640/{img_id}.jpg"
            idx = get_next_index(target_dir, prefix)
            filename = f"{prefix}_{idx:03d}.jpg"
            if download_image(img_url, os.path.join(target_dir, filename)):
                count += 1
        logger.info(f"  [MO] {prefix}: Collected {count} images for '{name}'.")
        return count
    except: return 0

if __name__ == "__main__":
    for item in SHORT_CLASSES:
        folder_name = next(d for d in os.listdir(BASE_DIR) if d.startswith(f"{item['id']})"))
        target_path = os.path.join(BASE_DIR, folder_name)
        prefix = folder_name.split(')_')[1].title().replace('_', '_')
        
        logger.info(f"🚀 Processing {folder_name}...")
        scrap_gbif(item['gbif'], target_path, prefix)
        for q in item['queries']:
            scrap_wikimedia(q, target_path, prefix)
            scrap_mo(q, target_path, prefix)

    logger.info("🏁 ALL SHORT CLASSES PROCESSED.")
