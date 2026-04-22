#!/usr/bin/env python3
"""Runner script for mushroom image downloading."""

import os
import sys
import time
import json
import shutil
import hashlib
import logging
from datetime import datetime

from PIL import Image
from icrawler.builtin import BingImageCrawler, GoogleImageCrawler

# ============================================================
# CONFIGURATION
# ============================================================
DATASET_DIR = "/home/ashirkhan/Updated Data set/raw_images_renamed"
TARGET_IMAGES = 50
EXTRA_DOWNLOAD = 15
MIN_IMAGE_SIZE = (50, 50)
MAX_IMAGE_SIZE_BYTES = 15 * 1024 * 1024
VALID_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.webp', '.tiff'}
DELAY_BETWEEN_CATEGORIES = 3

SEARCH_TEMPLATES = [
    "{name} mushroom",
    "{name} fungus",
    "{name} mushroom identification",
]

# Logging
log_file = os.path.join(os.path.dirname(DATASET_DIR), "download_log.txt")
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


def get_image_count(folder_path):
    count = 0
    for f in os.listdir(folder_path):
        ext = os.path.splitext(f)[1].lower()
        if ext in VALID_EXTENSIONS:
            count += 1
    return count


def get_existing_hashes(folder_path):
    hashes = set()
    for f in os.listdir(folder_path):
        filepath = os.path.join(folder_path, f)
        ext = os.path.splitext(f)[1].lower()
        if ext in VALID_EXTENSIONS and os.path.isfile(filepath):
            try:
                with open(filepath, 'rb') as fh:
                    file_hash = hashlib.md5(fh.read()).hexdigest()
                    hashes.add(file_hash)
            except Exception:
                pass
    return hashes


def validate_image(filepath):
    try:
        with Image.open(filepath) as img:
            img.verify()
        with Image.open(filepath) as img:
            width, height = img.size
            if width < MIN_IMAGE_SIZE[0] or height < MIN_IMAGE_SIZE[1]:
                return False
        file_size = os.path.getsize(filepath)
        if file_size > MAX_IMAGE_SIZE_BYTES or file_size < 1000:
            return False
        return True
    except Exception:
        return False


def clean_name_for_search(folder_name):
    return folder_name.replace('_', ' ').replace('-', ' ').strip()


def get_next_image_number(folder_path):
    max_num = 0
    for f in os.listdir(folder_path):
        name_part = os.path.splitext(f)[0]
        parts = name_part.split('_')
        for part in reversed(parts):
            try:
                num = int(part)
                max_num = max(max_num, num)
                break
            except ValueError:
                continue
    return max_num + 1


def get_all_categories(dataset_dir):
    categories = {}
    for entry in sorted(os.listdir(dataset_dir)):
        full_path = os.path.join(dataset_dir, entry)
        if os.path.isdir(full_path):
            count = get_image_count(full_path)
            categories[entry] = {
                'path': full_path,
                'current_count': count,
                'needed': max(0, TARGET_IMAGES - count)
            }
    return categories


def save_progress(progress_file, completed):
    with open(progress_file, 'w') as f:
        json.dump(completed, f, indent=2)


def load_progress(progress_file):
    if os.path.exists(progress_file):
        with open(progress_file, 'r') as f:
            return json.load(f)
    return {}


def download_images_for_category(category_folder, category_name, num_needed):
    temp_dir = os.path.join(os.path.dirname(DATASET_DIR), "temp_downloads", category_name)
    os.makedirs(temp_dir, exist_ok=True)

    search_name = clean_name_for_search(category_name)
    total_to_download = num_needed + EXTRA_DOWNLOAD

    existing_hashes = get_existing_hashes(category_folder)
    downloaded_count = 0

    for template in SEARCH_TEMPLATES:
        if downloaded_count >= total_to_download:
            break

        query = template.format(name=search_name)
        remaining = total_to_download - downloaded_count

        logger.info(f"  Searching: '{query}' (need {remaining} more)")

        try:
            crawler_logger = logging.getLogger('icrawler')
            crawler_logger.setLevel(logging.WARNING)

            crawler = BingImageCrawler(
                storage={'root_dir': temp_dir},
                downloader_threads=4,
                log_level=logging.WARNING
            )

            crawler.crawl(
                keyword=query,
                max_num=remaining,
                min_size=(100, 100),
                file_idx_offset=downloaded_count
            )

            downloaded_count = len([f for f in os.listdir(temp_dir) if os.path.isfile(os.path.join(temp_dir, f))])

        except Exception as e:
            logger.warning(f"  Bing search failed for '{query}': {e}")

            try:
                logger.info(f"  Trying Google fallback for: '{query}'")
                crawler = GoogleImageCrawler(
                    storage={'root_dir': temp_dir},
                    downloader_threads=4,
                    log_level=logging.WARNING
                )
                crawler.crawl(
                    keyword=query,
                    max_num=remaining,
                    min_size=(100, 100),
                    file_idx_offset=downloaded_count
                )
                downloaded_count = len([f for f in os.listdir(temp_dir) if os.path.isfile(os.path.join(temp_dir, f))])
            except Exception as e2:
                logger.warning(f"  Google fallback also failed: {e2}")

    # Validate, deduplicate, and move good images
    valid_added = 0
    next_num = get_next_image_number(category_folder)

    for filename in sorted(os.listdir(temp_dir)):
        filepath = os.path.join(temp_dir, filename)

        if not os.path.isfile(filepath):
            continue

        if not validate_image(filepath):
            os.remove(filepath)
            continue

        with open(filepath, 'rb') as fh:
            file_hash = hashlib.md5(fh.read()).hexdigest()

        if file_hash in existing_hashes:
            os.remove(filepath)
            continue

        try:
            with Image.open(filepath) as img:
                if img.mode != 'RGB':
                    img = img.convert('RGB')

                new_filename = f"{category_name}_{next_num:04d}.jpg"
                new_filepath = os.path.join(category_folder, new_filename)

                img.save(new_filepath, 'JPEG', quality=90)

                existing_hashes.add(file_hash)
                valid_added += 1
                next_num += 1

        except Exception as e:
            logger.debug(f"  Error processing {filename}: {e}")

        os.remove(filepath)

        if valid_added >= num_needed:
            break

    try:
        shutil.rmtree(temp_dir)
    except Exception:
        pass

    return valid_added


# ============================================================
# MAIN EXECUTION
# ============================================================
if __name__ == '__main__':
    categories = get_all_categories(DATASET_DIR)
    needs_download = {k: v for k, v in categories.items() if v['needed'] > 0}

    progress_file = os.path.join(os.path.dirname(DATASET_DIR), "download_progress.json")
    progress = load_progress(progress_file)

    temp_base = os.path.join(os.path.dirname(DATASET_DIR), "temp_downloads")
    os.makedirs(temp_base, exist_ok=True)

    successful = 0
    failed = 0
    skipped = 0

    logger.info("=" * 70)
    logger.info("🍄 MUSHROOM IMAGE DATASET EXPANDER")
    logger.info(f"   Categories to process: {len(needs_download)}")
    logger.info(f"   Target: {TARGET_IMAGES} images per category")
    logger.info(f"   Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 70)

    for idx, (name, info) in enumerate(sorted(needs_download.items()), 1):
        if name in progress and progress[name].get('completed', False):
            current = get_image_count(info['path'])
            if current >= TARGET_IMAGES:
                logger.info(f"[{idx}/{len(needs_download)}] ⏭️  {name} - Already completed (has {current})")
                skipped += 1
                continue

        logger.info(f"\n[{idx}/{len(needs_download)}] 🍄 Processing: {name}")
        logger.info(f"   Current: {info['current_count']} images | Need: {info['needed']} more")

        try:
            added = download_images_for_category(
                category_folder=info['path'],
                category_name=name,
                num_needed=info['needed']
            )

            new_total = get_image_count(info['path'])

            if added > 0:
                logger.info(f"   ✅ Added {added} images → Total now: {new_total}")
                successful += 1
            else:
                logger.warning(f"   ⚠️  No valid images downloaded")
                failed += 1

            progress[name] = {
                'completed': new_total >= TARGET_IMAGES,
                'images_added': added,
                'total_images': new_total,
                'timestamp': datetime.now().isoformat()
            }
            save_progress(progress_file, progress)

        except Exception as e:
            logger.error(f"   ❌ Error processing {name}: {e}")
            failed += 1
            progress[name] = {
                'completed': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
            save_progress(progress_file, progress)

        if idx < len(needs_download):
            time.sleep(DELAY_BETWEEN_CATEGORIES)

    try:
        shutil.rmtree(temp_base)
    except Exception:
        pass

    # Final report
    logger.info("\n" + "=" * 70)
    logger.info("📋 DOWNLOAD COMPLETE!")
    logger.info("=" * 70)
    logger.info(f"   ✅ Successful: {successful} categories")
    logger.info(f"   ⏭️  Skipped: {skipped} categories")
    logger.info(f"   ❌ Failed: {failed} categories")

    categories_final = get_all_categories(DATASET_DIR)
    below_target = [(n, i['current_count']) for n, i in categories_final.items() if i['current_count'] < TARGET_IMAGES]

    if below_target:
        logger.info(f"\n   ⚠️  {len(below_target)} categories still below target:")
        for name, count in sorted(below_target, key=lambda x: x[1]):
            logger.info(f"      {name}: {count}/{TARGET_IMAGES}")
    else:
        logger.info(f"\n   🎉 All categories have reached {TARGET_IMAGES}+ images!")

    logger.info(f"\n   Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 70)
