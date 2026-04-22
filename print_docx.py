import docx

try:
    doc = docx.Document("mushroom all description.docx")
    for i, p in enumerate(doc.paragraphs):
        if i > 50:
            break
        print(f"{i}: {p.text}")
except Exception as e:
    print(e)
