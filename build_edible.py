import sqlite3
import re
import os

# Paths
TXT_FILE = "mushroom_all_description.txt"
CSV_FILE = "mushroom_target_list.csv"
DB_FILE = "frontend/assets/db/mushrooms.db"

# 1. Identify Target Mushrooms for this Class
TARGET_CLASS = "Non_Poisnous_Edible"
TARGET_MUSHROOMS = []

with open(CSV_FILE, "r") as f:
    for line in f:
        if "|" in line:
            parts = line.strip().split("|")
            if len(parts) >= 2:
                main_c, sub_c = parts[0], parts[1]
                if main_c == TARGET_CLASS:
                    TARGET_MUSHROOMS.append(sub_c)

print(f"Targeting {len(TARGET_MUSHROOMS)} mushrooms for {TARGET_CLASS}")

def clean_text(text):
    if not text: return ""
    # Remove Emojis and non-ASCII
    text = re.sub(r'[^\x00-\x7F]+', '', text) 
    # Remove specific bullet characters
    for char in ["●", "○", "•", "👉", "🌿"]:
        text = text.replace(char, "")
    # Remove (4–5 lines)
    text = re.sub(r'\(.*lines?\)', '', text)
    # Remove numbering like 1. 2. at start of lines
    text = re.sub(r'^\d+\.\s*', '', text, flags=re.MULTILINE)
    # Standardize whitespace
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    return " ".join(lines)

with open(TXT_FILE, "r", encoding="utf-8") as f:
    full_text = f.read()

# Normalize line endings and form feeds
full_text = full_text.replace('\f', '\n').replace('\r', '\n')

# Find all headers in the text and split accordingly
headers = []
for m_name in TARGET_MUSHROOMS:
    disp = m_name.replace("_", " ")
    # Search for common header patterns in the text
    patterns = [
        rf"🌿\s*{re.escape(m_name)}", 
        rf"🌿\s*{re.escape(disp)}", 
        rf"^{re.escape(disp)}:", 
        rf"^{re.escape(disp)}$"
    ]
    for p in patterns:
        for match in re.finditer(p, full_text, re.IGNORECASE | re.MULTILINE):
            headers.append((match.start(), m_name))

headers.sort()

mushrooms_to_insert = []
seen = set()

for i in range(len(headers)):
    start_pos, m_name = headers[i]
    if m_name in seen: continue
    
    end_pos = headers[i+1][0] if i+1 < len(headers) else len(full_text)
    block = full_text[start_pos:end_pos]
    
    lines = [l.strip() for l in block.split('\n') if l.strip()]
    
    data = {
        "sub_class": m_name,
        "scientific_name": "",
        "kingdom": "Fungi",
        "family": "",
        "edibility": "Edible",
        "description": "",
        "occurrence": "",
        "price_pkr": "",
        "recipes": ""
    }
    
    current_section = None
    for line in lines:
        l_low = line.lower()
        if "scientific name:" in l_low:
            data["scientific_name"] = line.split(":", 1)[1].strip()
        elif "kingdom:" in l_low:
            data["kingdom"] = line.split(":", 1)[1].strip()
        elif "family:" in l_low:
            data["family"] = line.split(":", 1)[1].strip()
        elif "description" in l_low: current_section = "description"
        elif "frequency" in l_low or "occurrence" in l_low: current_section = "occurrence"
        elif "price in pakistan" in l_low: current_section = "price_pkr"
        elif "recipes" in l_low: current_section = "recipes"
        elif any(h in line for h in ["Classification", "Description", "Frequency", "Price", "Recipes"]):
            continue
        elif current_section:
            data[current_section] += " " + line

    for key in ["description", "occurrence", "price_pkr", "recipes"]:
        data[key] = clean_text(data[key])
    
    mushrooms_to_insert.append(data)
    seen.add(m_name)

# 2. Update Database
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS mushrooms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    main_class TEXT NOT NULL,
    sub_class TEXT NOT NULL,
    scientific_name TEXT DEFAULT '',
    kingdom TEXT DEFAULT 'Fungi',
    family TEXT DEFAULT '',
    edibility TEXT DEFAULT '',
    description TEXT DEFAULT '',
    occurrence TEXT DEFAULT '',
    price_pkr TEXT DEFAULT '',
    recipes TEXT DEFAULT '',
    images TEXT DEFAULT ''
)
""")
cursor.execute("DELETE FROM mushrooms WHERE main_class = ?", (TARGET_CLASS,))

# Images are in the flattened gallery folder
GALLERY_DIR = "frontend/assets/mushrooms_gallery"

for m in mushrooms_to_insert:
    folder_name = m['sub_class'].lower().replace(' ', '_')
    
    image_list = []
    # Check for up to 4 images in the gallery
    for i in range(1, 5):
        img_filename = f"{folder_name}_{i}.jpg"
        if os.path.exists(os.path.join(GALLERY_DIR, img_filename)):
            image_list.append(img_filename)
        elif os.path.exists(os.path.join(GALLERY_DIR, f"{folder_name}_{i}.png")):
             image_list.append(f"{folder_name}_{i}.png")
    
    images_str = ";".join(image_list)

    cursor.execute("""
    INSERT INTO mushrooms (main_class, sub_class, scientific_name, kingdom, family, edibility, description, occurrence, price_pkr, recipes, images)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (TARGET_CLASS, m["sub_class"], m["scientific_name"], m["kingdom"], m["family"], m["edibility"], m["description"], m["occurrence"], m["price_pkr"], m["recipes"], images_str))

conn.commit()
final_count = cursor.execute("SELECT COUNT(*) FROM mushrooms WHERE main_class = ?", (TARGET_CLASS,)).fetchone()[0]
conn.close()

print(f"Processed {len(seen)} unique mushrooms out of {len(TARGET_MUSHROOMS)}")
print(f"Final Count in Database: {final_count}")
if len(seen) < len(TARGET_MUSHROOMS):
    print(f"STILL MISSING ({len(TARGET_MUSHROOMS) - len(seen)}): {sorted(list(set(TARGET_MUSHROOMS) - seen))}")
