import docx
doc = docx.Document("mushroom all description.docx")
mush_titles = []
for p in doc.paragraphs:
    text = p.text.strip().split('\n')[0].strip()
    if not text: continue
    is_title = False
    if text.endswith(":") and len(text) < 40 and " " not in text.split(":")[0][-5:] and "Classification" not in text and "Family" not in text and "Kingdom" not in text and "Type" not in text and "name" not in text.lower():
        is_title = True
    elif "🍄" in text and "Classification" not in text and len(text) < 50:
        is_title = True
    if is_title:
        name = text.replace(':', '').replace('🍄', '').strip().lower()
        mush_titles.append(name.replace(' ', '_'))
print(len(mush_titles))
