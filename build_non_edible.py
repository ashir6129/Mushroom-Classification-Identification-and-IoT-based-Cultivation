import sqlite3
import re
import os

# Paths
TXT_FILE = "mushroom_all_description.txt"
CSV_FILE = "mushroom_target_list.csv"
DB_FILE = "frontend/assets/db/mushrooms.db"

TARGET_CLASS = "Non_Poisnous_Non_Edible"
TARGET_MUSHROOMS = []
with open(CSV_FILE, "r") as f:
    for line in f:
        if "|" in line:
            parts = line.strip().split("|")
            if parts[0] == TARGET_CLASS:
                TARGET_MUSHROOMS.append(parts[1])

print(f"Targeting {len(TARGET_MUSHROOMS)} mushrooms for {TARGET_CLASS}")

# Manual extraction for the 4 problematic mushrooms at the end
# (Found by searching scientific names in the file)
MANUAL_DATA = {
    "yellow_false_truffle": {
        "scientific_name": "Rhizopogon luteolus",
        "description": "Yellow false truffle is an underground fungus with yellowish skin and round shape. It grows near pine tree roots. It has a mild earthy smell. The texture is firm inside and spongy outside.",
        "occurrence": "Found in Europe and Asia. Grows underground in forests. Found in Pakistan."
    },
    "charcoal_burner": {
        "scientific_name": "Russula cyanoxantha",
        "description": "Charcoal burner is a common forest mushroom with mixed green-purple cap colors. It has soft, flexible gills compared to other brittlegills. It is edible and considered good for cooking. It grows in deciduous forests.",
        "occurrence": "Found in Europe and Asia. Forest mushroom. Found in Pakistan."
    },
    "splitgill": {
        "scientific_name": "Schizophyllum commune",
        "description": "Splitgill is a small fan-shaped fungus with split gills. It grows on dead wood in clusters. It becomes chewy when cooked. It is edible in some cultures after proper cooking.",
        "occurrence": "Found in Asia, Europe, and Pakistan. Wood fungus. Found in Pakistan."
    },
    "spotted_toughshank": {
        "scientific_name": "Collybia maculata",
        "description": "Spotted toughshank is a white mushroom with brown spotting. It has very hard and tough flesh. It is not used for food. It grows in forest soil and leaf litter.",
        "occurrence": "Found in Europe and Asia. Forest mushroom. Found in Pakistan."
    }
}

def clean_text(text):
    if not text: return ""
    text = re.sub(r'[^\x00-\x7F]+', '', text) 
    for char in ["●", "○", "•", "👉", "🌿"]:
        text = text.replace(char, "")
    text = re.sub(r'\(.*lines?\)', '', text)
    text = re.sub(r'^\d+\.\s*', '', text, flags=re.MULTILINE)
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    return " ".join(lines)

with open(TXT_FILE, "r", encoding="utf-8") as f:
    full_text = f.read()

full_text = full_text.replace('\f', '\n').replace('\r', '\n')

headers = []
for m_name in TARGET_MUSHROOMS:
    if m_name in MANUAL_DATA: continue # Handle later
    
    disp = m_name.replace("_", " ")
    patterns = [
        rf"🌿\s*{re.escape(m_name)}", 
        rf"🌿\s*{re.escape(disp)}", 
        rf"^\s*{re.escape(m_name)}\s*$",
        rf"^\s*{re.escape(disp)}\s*$"
    ]
    for p in patterns:
        for match in re.finditer(p, full_text, re.IGNORECASE | re.MULTILINE):
            headers.append((match.start(), m_name))
            break

headers.sort()

mushrooms_to_insert = []
seen = set()

# Process standard ones
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
        "edibility": "Non-Edible",
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
        elif any(h in line for h in ["Classification", "Description", "Frequency", "Price", "Recipes", "Uses"]):
            continue
        elif current_section:
            data[current_section] += " " + line

    for key in ["description", "occurrence"]:
        data[key] = clean_text(data[key])
    
    mushrooms_to_insert.append(data)
    seen.add(m_name)

# Process manual ones
for m_name, info in MANUAL_DATA.items():
    if m_name in TARGET_MUSHROOMS and m_name not in seen:
        data = {
            "sub_class": m_name,
            "scientific_name": info["scientific_name"],
            "kingdom": "Fungi",
            "family": "Russulaceae" if "Russula" in info["scientific_name"] else ("Schizophyllaceae" if "Schizophyllum" in info["scientific_name"] else "Marasmiaceae"),
            "edibility": "Non-Edible",
            "description": info["description"],
            "occurrence": info["occurrence"],
            "price_pkr": "",
            "recipes": ""
        }
        mushrooms_to_insert.append(data)
        seen.add(m_name)

# 2. Update Database
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()
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
