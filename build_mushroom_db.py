#!/usr/bin/env python3
"""
Parse mushroom_all_description.txt and build a fresh SQLite database.
Reads data directly from the text file - no assumptions.
"""
import sqlite3
import re
import os

TXT_FILE = "mushroom_all_description.txt"
DB_FILE = "frontend/assets/db/mushrooms.db"

# The exact main_class -> sub_class mapping from the ML model
MAIN_CLASS_MAP = {}
with open("mushroom_target_list.csv", "r") as f:
    for line in f:
        line = line.strip()
        if "|" in line:
            mc, sc = line.split("|", 1)
            MAIN_CLASS_MAP[sc] = mc

def title_to_snake(title):
    """Convert 'Almond Mushroom' -> 'almond_mushroom'"""
    return title.strip().lower().replace(" ", "_").replace("'", "").replace("'", "")

def clean_text(text):
    """Clean extracted text: remove bullets, form feeds, emojis, extra whitespace."""
    text = text.replace("\f", "")
    # Remove all emojis
    text = re.sub(r'[\U0001F300-\U0001F9FF\U00002700-\U000027BF\U0001FA00-\U0001FAFF]', '', text)
    text = text.replace("🌿", "").replace("👉", "")
    # Remove bullet dots and circles
    text = text.replace("●", "").replace("○", "").replace("•", "")
    # Remove (4-5 lines) annotations
    text = re.sub(r'\(\d+[–-]\d+\s*lines?\)', '', text)
    # Remove numbering like "1." "2." at start of lines
    lines = []
    for l in text.split("\n"):
        l = l.strip()
        if not l:
            continue
        # Remove leading number+dot like "1. " "2. " "3. "
        l = re.sub(r'^\d+\.\s*', '', l)
        if l:
            lines.append(l)
    return " ".join(lines)

def clean_for_sql(text):
    """Escape single quotes for SQL."""
    return text.replace("'", "''")

def parse_mushrooms(txt_path):
    """Parse the text file into a list of mushroom dicts."""
    with open(txt_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Split into mushroom sections.
    # Each mushroom starts with either:
    #   "Name:" at start of line (first mushroom)
    #   "🌿 snake_case_name" 
    #   "snake_case_name" (without emoji, some entries)
    
    # Find all section boundaries - look for mushroom name headers
    # Pattern: either "Name:" or "🌿 name" where name matches a known sub_class
    
    known_names = set(MAIN_CLASS_MAP.keys())
    
    # Build regex to find section starts
    lines = content.split("\n")
    
    sections = []
    current_name = None
    current_lines = []
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Skip empty lines and form feeds for detection
        if not stripped or stripped == "\f":
            if current_name:
                current_lines.append(line)
            continue
        
        # Check if this line starts a new mushroom section
        detected_name = None
        
        # Pattern 1: "Almond Mushroom:" (first entry, Title Case with colon)
        if i < 5 and stripped.endswith(":") and "Classification" not in stripped and "Description" not in stripped and "Recipes" not in stripped and "Price" not in stripped and "Frequency" not in stripped:
            candidate = title_to_snake(stripped.rstrip(":"))
            if candidate in known_names:
                detected_name = candidate
        
        # Pattern 2: "🌿 snake_case_name" or just "snake_case_name"
        if not detected_name:
            clean = stripped.lstrip("🌿 ").strip()
            # Remove trailing colon if present
            clean_nc = clean.rstrip(":")
            candidate = title_to_snake(clean_nc)
            
            # Direct match check
            if candidate in known_names:
                # Make sure this isn't a section header like "Classification", "Description", etc.
                section_headers = ["classification", "description", "frequency", "frequency_(occurrence)",
                                   "price_in_pakistan", "price_in_pakistan_(per_kg)", "recipes",
                                   "recipes_(how_it_is_made)", "uses", "uses_(no_recipes)"]
                if candidate not in section_headers:
                    # Verify by checking if "Classification" appears within next 10 lines
                    for j in range(i+1, min(i+12, len(lines))):
                        if "Classification" in lines[j]:
                            detected_name = candidate
                            break
        
        # Also check the raw stripped line without emoji
        if not detected_name:
            raw = stripped.replace("🌿", "").strip().rstrip(":")
            raw_snake = raw.lower().replace(" ", "_").replace("'", "").replace("'", "")
            if raw_snake in known_names:
                section_headers = ["classification", "description", "frequency", "frequency_(occurrence)",
                                   "price_in_pakistan", "price_in_pakistan_(per_kg)", "recipes",
                                   "recipes_(how_it_is_made)", "uses", "uses_(no_recipes)"]
                if raw_snake not in section_headers:
                    for j in range(i+1, min(i+12, len(lines))):
                        if "Classification" in lines[j]:
                            detected_name = raw_snake
                            break
        
        if detected_name:
            # Save previous section
            if current_name:
                sections.append((current_name, "\n".join(current_lines)))
            current_name = detected_name
            current_lines = [line]
        else:
            if current_name:
                current_lines.append(line)
    
    # Don't forget the last section
    if current_name:
        sections.append((current_name, "\n".join(current_lines)))
    
    print(f"Found {len(sections)} mushroom sections")
    
    # Now handle the special entries at the end of the file (charcoal_burner, splitgill, spotted_toughshank)
    # These don't have the usual 🌿 header format
    tail_text = "\n".join(lines[5980:])
    
    # charcoal_burner
    if "charcoal_burner" not in [s[0] for s in sections]:
        cb_text = "\n".join(lines[5980:5997])
        sections.append(("charcoal_burner", cb_text))
    
    # splitgill  
    if "splitgill" not in [s[0] for s in sections]:
        sg_text = "\n".join(lines[5997:6015])
        sections.append(("splitgill", sg_text))
    
    # spotted_toughshank
    if "spotted_toughshank" not in [s[0] for s in sections]:
        st_text = "\n".join(lines[6015:6029])
        sections.append(("spotted_toughshank", st_text))
    
    print(f"Total sections after tail processing: {len(sections)}")
    
    # Parse each section into structured data
    mushrooms = []
    for name, text in sections:
        m = extract_fields(name, text)
        mushrooms.append(m)
    
    return mushrooms

def extract_fields(name, text):
    """Extract all fields from a mushroom text section."""
    main_class = MAIN_CLASS_MAP.get(name, "Unknown")
    
    # Determine edibility from text type field or main_class
    edibility = "Unknown"
    if "Non_Poisnous_Edible" in main_class:
        edibility = "Edible"
    elif "Non_Poisnous_Non_Edible" in main_class:
        edibility = "Non-Edible"
    elif "Poisnous_Non_Useable" in main_class:
        edibility = "Poisonous"
    elif "Poisnous_Useable" in main_class:
        edibility = "Poisonous"
    
    # Extract scientific name
    sci_match = re.search(r'Scientific name:\s*(.+)', text)
    scientific_name = sci_match.group(1).strip() if sci_match else ""
    
    # Extract kingdom
    king_match = re.search(r'Kingdom:\s*(.+)', text)
    kingdom = king_match.group(1).strip() if king_match else "Fungi"
    
    # Extract family
    fam_match = re.search(r'Family:\s*(.+)', text)
    family = fam_match.group(1).strip() if fam_match else ""
    
    # Extract description section
    description = extract_section(text, 
        [r'Description(?:\s*\(.*?\))?', r'Description'],
        [r'Frequency', r'Price', r'Recipes', r'Uses'])
    
    # Extract occurrence/frequency section
    occurrence = extract_section(text,
        [r'Frequency\s*\(Occurrence\)', r'Frequency'],
        [r'Price', r'Recipes', r'Uses'])
    
    # Extract price section
    price = extract_section(text,
        [r'Price in Pakistan(?:\s*\(.*?\))?', r'Price'],
        [r'Recipes', r'Uses', r'$'])
    
    # Extract recipes section - only for edible mushrooms
    recipes = ""
    if edibility == "Edible":
        recipes = extract_section(text,
            [r'Recipes(?:\s*\(.*?\))?'],
            [r'____', r'🌿\s+\w'])
    
    # Clean up extracted fields
    description = clean_text(description).strip()
    occurrence = clean_text(occurrence).strip()
    price = clean_text(price).strip()
    recipes = clean_text(recipes).strip()
    
    # Format the display name (Title Case)
    display_name = name.replace("_", " ").title()
    # Fix special cases
    display_name = display_name.replace("Of The", "of the").replace("And ", "and ")
    if display_name.startswith("St "):
        display_name = "St. " + display_name[3:]
    
    return {
        "main_class": main_class,
        "sub_class": name,
        "display_name": display_name,
        "scientific_name": scientific_name,
        "kingdom": kingdom,
        "family": family,
        "edibility": edibility,
        "description": description,
        "occurrence": occurrence,
        "price_pkr": price,
        "recipes": recipes,
    }

def extract_section(text, start_patterns, end_patterns):
    """Extract text between section markers."""
    lines = text.split("\n")
    
    start_idx = None
    for i, line in enumerate(lines):
        stripped = line.strip().replace("🌿", "").strip()
        for pat in start_patterns:
            if re.match(pat, stripped, re.IGNORECASE):
                start_idx = i + 1
                break
        if start_idx is not None:
            break
    
    if start_idx is None:
        return ""
    
    end_idx = len(lines)
    for i in range(start_idx, len(lines)):
        stripped = lines[i].strip().replace("🌿", "").strip()
        if not stripped or stripped == "\f":
            continue
        for pat in end_patterns:
            if pat == "$":
                continue
            if re.match(pat, stripped, re.IGNORECASE):
                end_idx = i
                break
        if end_idx != len(lines):
            break
    
    section_lines = lines[start_idx:end_idx]
    # Filter out form feeds and section markers
    cleaned = []
    for line in section_lines:
        l = line.strip().replace("\f", "")
        if l and not re.match(r'^🌿\s*(Classification|Description|Frequency|Price|Recipes|Uses)', l):
            cleaned.append(l)
    
    return "\n".join(cleaned)

def create_database(mushrooms, db_path):
    """Create a fresh SQLite database with all mushroom data."""
    # Remove old DB
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Removed old {db_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create table with user's preferred schema + main_class for app compatibility
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
            recipes TEXT DEFAULT ''
        )
    """)
    
    inserted = 0
    for m in mushrooms:
        cursor.execute("""
            INSERT INTO mushrooms (main_class, sub_class, scientific_name, kingdom, family,
                                   edibility, description, occurrence, price_pkr, recipes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            m["main_class"],
            m["sub_class"],
            m["scientific_name"],
            m["kingdom"],
            m["family"],
            m["edibility"],
            m["description"],
            m["occurrence"],
            m["price_pkr"],
            m["recipes"],
        ))
        inserted += 1
    
    conn.commit()
    
    # Verify
    cursor.execute("SELECT COUNT(*) FROM mushrooms")
    count = cursor.fetchone()[0]
    print(f"\nInserted {inserted} records. DB contains {count} records.")
    
    # Check for missing mushrooms
    cursor.execute("SELECT sub_class FROM mushrooms")
    in_db = set(row[0] for row in cursor.fetchall())
    missing = set(MAIN_CLASS_MAP.keys()) - in_db
    if missing:
        print(f"\n⚠️  Missing {len(missing)} mushrooms from DB:")
        for m in sorted(missing):
            print(f"  - {m} ({MAIN_CLASS_MAP[m]})")
        
        # Insert missing ones with minimal data
        print("\nInserting missing mushrooms with basic data...")
        for m in sorted(missing):
            mc = MAIN_CLASS_MAP[m]
            edibility = "Edible" if "Edible" in mc else ("Poisonous" if "Poisnous" in mc else "Non-Edible")
            cursor.execute("""
                INSERT INTO mushrooms (main_class, sub_class, scientific_name, kingdom, family,
                                       edibility, description, occurrence, price_pkr, recipes)
                VALUES (?, ?, '', 'Fungi', '', ?, '', '', '', '')
            """, (mc, m, edibility))
        conn.commit()
        
        cursor.execute("SELECT COUNT(*) FROM mushrooms")
        final_count = cursor.fetchone()[0]
        print(f"Final count: {final_count}")
    
    # Print sample entries
    print("\n--- Sample entries ---")
    cursor.execute("SELECT id, sub_class, scientific_name, edibility, description FROM mushrooms LIMIT 5")
    for row in cursor.fetchall():
        print(f"  [{row[0]}] {row[1]} | {row[2]} | {row[3]}")
        print(f"       Desc: {row[4][:80]}...")
    
    # Print category counts
    print("\n--- Category counts ---")
    cursor.execute("SELECT main_class, COUNT(*) FROM mushrooms GROUP BY main_class")
    for row in cursor.fetchall():
        print(f"  {row[0]}: {row[1]}")
    
    conn.close()
    print(f"\n✅ Database saved to: {db_path}")

if __name__ == "__main__":
    mushrooms = parse_mushrooms(TXT_FILE)
    create_database(mushrooms, DB_FILE)
