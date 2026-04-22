import os
import requests
import json
import logging
import sys
from PIL import Image
from io import BytesIO

# specialized_scraper.py

# CONFIG
BASE_DIR = "/home/ashirkhan/Updated Data set/Professional_Mushroom_Dataset"
TARGET_DIR = os.path.join(BASE_DIR, "208)_woodland_inkcap")
SPECIES_NAME = "Woodland_Inkcap"
TAXON_KEYS = {
    "GBIF": "8109355",  # Coprinellus silvaticus
}

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

def get_next_index(directory):
    files = [f for f in os.listdir(directory) if f.startswith(SPECIES_NAME) and f.endswith('.jpg')]
    if not files: return 1
    indices = []
    for f in files:
        try:
            # Format: Woodland_Inkcap_001.jpg
            idx = int(f.split('_')[-1].split('.')[0])
            indices.append(idx)
        except: continue
    return max(indices) + 1 if indices else 1

def download_image(url, path):
    try:
        res = requests.get(url, timeout=15)
        if res.status_code == 200:
            img = Image.open(BytesIO(res.content))
            img = img.convert('RGB')
            img.save(path, 'JPEG')
            return True
    except Exception as e:
        logger.error(f"Failed to download {url}: {e}")
    return False

def scrap_gbif(taxon_key, limit=100):
    logger.info(f"🌐 Searching GBIF for taxon {taxon_key}...")
    url = f"https://api.gbif.org/v1/occurrence/search?taxonKey={taxon_key}&mediaType=StillImage&limit={limit}"
    try:
        res = requests.get(url)
        data = res.json()
        results = data.get('results', [])
        logger.info(f"✅ Found {len(results)} occurrences on GBIF.")
        
        count = 0
        for occ in results:
            media = occ.get('media', [])
            for m in media:
                if m.get('type') == 'StillImage':
                    img_url = m.get('identifier')
                    if not img_url: continue
                    
                    next_idx = get_next_index(TARGET_DIR)
                    filename = f"{SPECIES_NAME}_{next_idx:03d}.jpg"
                    path = os.path.join(TARGET_DIR, filename)
                    
                    if download_image(img_url, path):
                        logger.info(f"💾 Downloaded: {filename}")
                        count += 1
                        break # One image per occurrence
        return count
    except Exception as e:
        logger.error(f"GBIF Error: {e}")
    return 0

def scrap_wikimedia(query, limit=50):
    logger.info(f"🌐 Searching Wikimedia Commons for '{query}'...")
    api_url = "https://commons.wikimedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": query,
        "srnamespace": "6", # Files
        "srlimit": limit
    }
    try:
        res = requests.get(api_url, params=params)
        data = res.json()
        search_results = data.get('query', {}).get('search', [])
        logger.info(f"✅ Found {len(search_results)} files on Wikimedia.")
        
        count = 0
        for item in search_results:
            title = item.get('title')
            # Get image URL
            info_params = {
                "action": "query",
                "format": "json",
                "prop": "imageinfo",
                "titles": title,
                "iiprop": "url"
            }
            info_res = requests.get(api_url, params=info_params)
            info_data = info_res.json()
            pages = info_data.get('query', {}).get('pages', {})
            for page_id in pages:
                info = pages[page_id].get('imageinfo', [])
                if info:
                    img_url = info[0].get('url')
                    next_idx = get_next_index(TARGET_DIR)
                    filename = f"{SPECIES_NAME}_{next_idx:03d}.jpg"
                    path = os.path.join(TARGET_DIR, filename)
                    if download_image(img_url, path):
                        logger.info(f"💾 Downloaded: {filename}")
                        count += 1
        return count
    except Exception as e:
        logger.error(f"Wikimedia Error: {e}")
    return 0

def scrap_mushroom_observer(name, limit=50):
    logger.info(f"🌐 Searching Mushroom Observer for '{name}'...")
    # MO API gives observation IDs first
    api_url = f"https://mushroomobserver.org/api2/images?name={name}&format=json"
    try:
        res = requests.get(api_url)
        data = res.json()
        results = data.get('results', [])
        logger.info(f"✅ Found {len(results)} image records on Mushroom Observer.")
        
        count = 0
        for img_id in results:
            if count >= limit: break
            # Each result is an image ID. We need the actual URL.
            # MO Image IDs have a predictable URL pattern: https://mushroomobserver.org/images/640/{id}.jpg
            img_url = f"https://images.mushroomobserver.org/640/{img_id}.jpg"
            
            next_idx = get_next_index(TARGET_DIR)
            filename = f"{SPECIES_NAME}_{next_idx:03d}.jpg"
            path = os.path.join(TARGET_DIR, filename)
            
            if download_image(img_url, path):
                logger.info(f"💾 Downloaded from MO: {filename}")
                count += 1
        return count
    except Exception as e:
        logger.error(f"Mushroom Observer Error: {e}")
    return 0

if __name__ == "__main__":
    if not os.path.exists(TARGET_DIR): os.makedirs(TARGET_DIR)
    
    gbif_count = scrap_gbif(TAXON_KEYS["GBIF"])
    mo_count = scrap_mushroom_observer("Coprinellus silvaticus")
    mo_count2 = scrap_mushroom_observer("Coprinus silvaticus")
    wiki_count = scrap_wikimedia("Coprinellus silvaticus")
    wiki_count2 = scrap_wikimedia("Coprinus silvaticus")
    
    total = gbif_count + mo_count + mo_count2 + wiki_count + wiki_count2
    logger.info(f"🏁 FINISHED. Total new images: {total}")
