
import os
from pathlib import Path

DATASET_DIR = "/home/ashirkhan/Updated Data set/raw_images_renamed"
OUTPUT_FILE = "/home/ashirkhan/Updated Data set/dataset_review.html"

def generate_html():
    categories = sorted([d for d in os.listdir(DATASET_DIR) if os.path.isdir(os.path.join(DATASET_DIR, d))])
    
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Mushroom Dataset Review & Clean</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0f172a; color: #f8fafc; padding: 20px; margin: 0; }
            .sidebar { position: fixed; right: 20px; top: 20px; width: 300px; background: #1e293b; padding: 20px; border-radius: 12px; border: 1px solid #334155; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5); z-index: 1000; max-height: 80vh; overflow-y: auto; }
            .main { margin-right: 340px; }
            .category { margin-bottom: 40px; background: #1e293b; padding: 20px; border-radius: 12px; border: 1px solid #334155; }
            .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 12px; }
            .img-container { position: relative; border-radius: 8px; overflow: hidden; border: 3px solid transparent; transition: all 0.2s; cursor: pointer; background: #0f172a; }
            .img-container.selected { border-color: #ef4444; transform: scale(0.95); opacity: 0.6; }
            .img-container.selected::after { content: "✕"; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); color: #ef4444; font-size: 40px; font-weight: bold; text-shadow: 0 0 10px black; }
            img { width: 100%; height: 140px; object-fit: cover; }
            .filename { font-size: 9px; padding: 4px; color: #94a3b8; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
            h2 { color: #10b981; margin-top: 0; border-bottom: 1px solid #334155; padding-bottom: 10px; }
            button { background: #ef4444; color: white; border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer; font-weight: bold; width: 100%; margin-top: 10px; }
            button:hover { background: #dc2626; }
            textarea { width: 100%; height: 100px; margin-top: 10px; background: #0f172a; color: #10b981; border: 1px solid #334155; border-radius: 4px; font-family: monospace; font-size: 11px; }
            .stats { color: #94a3b8; font-size: 14px; margin-bottom: 10px; }
            .sticky-header { background: #0f172a; padding: 20px; border-bottom: 1px solid #334155; margin-bottom: 20px; }
        </style>
    </head>
    <body>
        <div class="sidebar">
            <h3>🗑️ Deletion Tools</h3>
            <div class="stats">Selected: <span id="select-count">0</span> images</div>
            <p style="font-size: 12px; color: #94a3b8;">Click images to mark them for deletion. Then copy the list below.</p>
            <textarea id="delete-list" readonly placeholder="List will appear here..."></textarea>
            <button onclick="copyList()">📋 Copy Deletion List</button>
            <hr style="border: 0; border-top: 1px solid #334155; margin: 20px 0;">
            <p style="font-size: 11px; color: #94a3b8;">After copying, run the <code>bulk_delete.py</code> script with this list.</p>
        </div>

        <div class="main">
            <div class="sticky-header">
                <h1>🍄 Mushroom Dataset Quality Control</h1>
                <p>Scroll through and click on any images that are <b>NOT</b> mushrooms (logos, maps, people, etc.)</p>
            </div>
    """

    for cat in categories:
        cat_path = os.path.join(DATASET_DIR, cat)
        images = sorted([f for f in os.listdir(cat_path) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))])
        
        if not images: continue
        
        html_content += f'<div class="category"><h2>{cat} <span style="font-size: 12px; color: #64748b;">({len(images)} images)</span></h2><div class="grid">'
        
        for img_name in images:
            # We use absolute paths to ensure it works wherever the user opens it
            # But relative is safer for shared environments.
            rel_path = f"raw_images_renamed/{cat}/{img_name}"
            full_path = f"{cat}/{img_name}"
            html_content += f"""
                <div class="img-container" onclick="toggleSelect(this, '{full_path}')">
                    <img src="{rel_path}" loading="lazy">
                    <div class="filename">{img_name}</div>
                </div>
            """
        html_content += '</div></div>'

    html_content += """
        </div>
        <script>
            let selectedFiles = new Set();
            
            function toggleSelect(el, path) {
                if (selectedFiles.has(path)) {
                    selectedFiles.delete(path);
                    el.classList.remove('selected');
                } else {
                    selectedFiles.add(path);
                    el.classList.add('selected');
                }
                updateList();
            }
            
            function updateList() {
                const textarea = document.getElementById('delete-list');
                const countSpan = document.getElementById('select-count');
                textarea.value = Array.from(selectedFiles).join('\\n');
                countSpan.innerText = selectedFiles.size;
            }
            
            function copyList() {
                const textarea = document.getElementById('delete-list');
                textarea.select();
                document.execCommand('copy');
                alert('List copied to clipboard!');
            }
        </script>
    </body>
    </html>
    """
    
    with open(OUTPUT_FILE, "w") as f:
        f.write(html_content)
    
    print(f"✅ Enhanced Review Gallery generated: {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_html()
