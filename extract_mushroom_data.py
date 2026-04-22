import docx
import sqlite3
import re
import os
import requests
import urllib.parse
import time

def normalize_name(name):
    return name.replace('🍄', '').strip()

def download_image(title, save_path):
    if os.path.exists(save_path):
        return True
    title = title.split(" (substitute)")[0].split(" (")[0]
    
    print(f"Downloading image for '{title}'...")
    headers = {
        'User-Agent': 'MushroomApp/1.0 (admin@example.com) python-requests/2.33.1'
    }
    search_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(title)}&utf8=&format=json"
    try:
        r = requests.get(search_url, headers=headers, timeout=10)
        data = r.json()
        if not data.get('query', {}).get('search'):
            print(f"  [!] No Wiki page found for '{title}'")
            return False
            
        page_title = data['query']['search'][0]['title']
        img_url = f"https://en.wikipedia.org/w/api.php?action=query&titles={urllib.parse.quote(page_title)}&prop=pageimages&piprop=original&format=json"
        ir = requests.get(img_url, headers=headers, timeout=10)
        idata = ir.json()
        pages = idata.get('query', {}).get('pages', {})
        for k, v in pages.items():
            if 'original' in v:
                image_source = v['original']['source']
                img_data = requests.get(image_source, headers=headers, timeout=10).content
                with open(save_path, 'wb') as f:
                    f.write(img_data)
                print(f"  [✓] Downloaded to {save_path}")
                return True
        print(f"  [!] No original image found on Wiki for '{title}'")
        return False
    except Exception as e:
        print(f"  [!] Error fetching image for '{title}': {e}")
        return False

def main():
    doc = docx.Document("mushroom all description.docx")
    
    mushrooms = {}
    current_mushroom = None
    current_section = None
    
    for p in doc.paragraphs:
        # Split paragraph into lines to handle soft breaks (Shift+Enter) within docx
        lines = p.text.strip().split('\n')
        for text in lines:
            text = text.strip()
            if not text:
                continue
                
            is_title = False
            if text.endswith(":") and len(text) < 40 and " " not in text.split(":")[0][-5:] and "Classification" not in text and "Family" not in text and "Kingdom" not in text and "Type" not in text and "name" not in text.lower():
                is_title = True
            elif "🍄" in text and "Classification" not in text and len(text) < 50:
                is_title = True
                
            if is_title:
                name = text.replace(':', '').replace('🍄', '').strip().lower()
                name = name.replace(' ', '_')
                current_mushroom = name
                mushrooms[current_mushroom] = {
                    'scientific_name': '',
                    'kingdom': '',
                    'family': '',
                    'type': '',
                    'description': '',
                    'frequency': '',
                    'price': '',
                    'recipes': []
                }
                current_section = None
                continue
                
            if not current_mushroom:
                continue

            # Detect sections
            if "Classification" in text:
                current_section = 'classification'
                continue
            elif "Description" in text:
                current_section = 'description'
                continue
            elif "Frequency" in text:
                current_section = 'frequency'
                continue
            elif "Price in Pakistan" in text:
                current_section = 'price'
                continue
            elif "Recipes" in text or "How it is made" in text:
                current_section = 'recipes'
                continue
                
            # Parse data
            if current_section == 'classification':
                if "Scientific name:" in text or "Scientific Name:" in text:
                    mushrooms[current_mushroom]['scientific_name'] = text.split(":", 1)[1].strip()
                elif "Kingdom:" in text:
                    mushrooms[current_mushroom]['kingdom'] = text.split(":", 1)[1].strip()
                elif "Family:" in text:
                    mushrooms[current_mushroom]['family'] = text.split(":", 1)[1].strip()
                elif "Type:" in text:
                    mushrooms[current_mushroom]['type'] = text.split(":", 1)[1].strip()
            elif current_section == 'description':
                mushrooms[current_mushroom]['description'] += text + " "
            elif current_section == 'frequency':
                mushrooms[current_mushroom]['frequency'] += text + "\n"
            elif current_section == 'price':
                mushrooms[current_mushroom]['price'] += text + "\n"
            elif current_section == 'recipes':
                if text[0].isdigit() and (text[1] == '.' or text[1] == ')'):
                    mushrooms[current_mushroom]['recipes'].append(text)
                elif len(mushrooms[current_mushroom]['recipes']) > 0:
                    mushrooms[current_mushroom]['recipes'][-1] += " " + text
                else:
                    mushrooms[current_mushroom]['recipes'].append(text)

    print(f"Found {len(mushrooms)} mushrooms in DOCX.")

    db_path = "frontend/assets/db/mushrooms.db"
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    cur.execute("SELECT sub_class, main_class FROM mushrooms")
    db_mushrooms = {row[0].lower(): row[1] for row in cur.fetchall() if row[0]}
    
    asset_dir = "frontend/assets/mushrooms_dataset"
    os.makedirs(asset_dir, exist_ok=True)
    
    updated_count = 0
    for sub_class, data in mushrooms.items():
        found_key = None
        if sub_class in db_mushrooms:
            found_key = sub_class
        else:
            for db_key in db_mushrooms.keys():
                if sub_class.replace('_', '') == db_key.replace('_', ''):
                    found_key = db_key
                    break
            if not found_key:
                for db_key in db_mushrooms.keys():
                    if sub_class in db_key or db_key in sub_class:
                        found_key = db_key
                        break
        if not found_key:
            continue
            
        sub_class = found_key
        main_class = db_mushrooms[sub_class]
        recipes_joined = " || ".join(data['recipes'])
        
        cur.execute("""
            UPDATE mushrooms 
            SET scientific_name = ?, kingdom = ?, family = ?, type = ?, 
                description = ?, frequency = ?, price_in_pakistan = ?, recipes = ?
            WHERE LOWER(sub_class) = ?
        """, (
            data['scientific_name'], data['kingdom'], data['family'], data['type'],
            data['description'].strip(), data['frequency'].strip(), data['price'].strip(), recipes_joined,
            sub_class
        ))
        updated_count += 1
        
        cat_dir = os.path.join(asset_dir, main_class)
        os.makedirs(cat_dir, exist_ok=True)
        img_path = os.path.join(cat_dir, f"{sub_class}.jpg")
        
        search_term = data['scientific_name'] if data['scientific_name'] else sub_class.replace('_', ' ')
        success = download_image(search_term, img_path)
        if not success and data['scientific_name']:
             download_image(sub_class.replace('_', ' '), img_path)

    conn.commit()
    conn.close()
    print(f"Updated {updated_count} mushrooms in the database.")

if __name__ == "__main__":
    main()
