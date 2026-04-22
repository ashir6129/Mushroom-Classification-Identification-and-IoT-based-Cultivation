#!/usr/bin/env python3
"""
Mushroom Image Reviewer - Local Web Server
Run this and open http://localhost:8765 in your browser.
Browse classes, click bad images to select them, hit Delete to remove.
Then run fast_augmentator.py to re-balance to 600.
"""

import os
import json
import http.server
import urllib.parse
import hashlib
from pathlib import Path
from PIL import Image
Image.MAX_IMAGE_PIXELS = None

CATEGORIES = [
    "Class_Zero",
    "Non_Poisnous_Edible",
    "Non_Poisnous_Non_Edible",
    "Poisnous_Non_Useable",
    "Poisnous_Useable"
]

PORT = 8765
THUMB_DIR = "/home/ashirkhan/Updated Data set/.thumbs"
THUMB_SIZE = 150
BASE_DIR = "/home/ashirkhan/Updated Data set/Professional_Mushroom_Dataset"

os.makedirs(THUMB_DIR, exist_ok=True)

def get_thumbnail(filepath):
    """Generate or return cached 150px thumbnail."""
    h = hashlib.md5(filepath.encode()).hexdigest()
    thumb_path = os.path.join(THUMB_DIR, h + ".jpg")
    if os.path.exists(thumb_path):
        with open(thumb_path, 'rb') as f:
            return f.read()
    try:
        img = Image.open(filepath)
        img.thumbnail((THUMB_SIZE, THUMB_SIZE))
        img = img.convert('RGB')
        img.save(thumb_path, 'JPEG', quality=70)
        with open(thumb_path, 'rb') as f:
            return f.read()
    except:
        return None

HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🍄 Mushroom Image Reviewer</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
  
  * { margin: 0; padding: 0; box-sizing: border-box; }
  
  body {
    font-family: 'Inter', sans-serif;
    background: #0f0f1a;
    color: #e0e0e0;
    min-height: 100vh;
  }
  
  .header {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    padding: 20px 30px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 2px solid #2d2d5e;
    position: sticky;
    top: 0;
    z-index: 100;
    backdrop-filter: blur(10px);
  }
  
  .header h1 {
    font-size: 1.5rem;
    background: linear-gradient(90deg, #00d2ff, #7b2ff7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }
  
  .stats {
    display: flex;
    gap: 20px;
    font-size: 0.9rem;
  }
  
  .stat-box {
    background: rgba(255,255,255,0.05);
    padding: 8px 16px;
    border-radius: 8px;
    border: 1px solid rgba(255,255,255,0.1);
  }
  
  .stat-box span { color: #00d2ff; font-weight: 700; }
  
  .controls {
    display: flex;
    gap: 10px;
    align-items: center;
  }
  
  .btn {
    padding: 10px 20px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 600;
    font-size: 0.9rem;
    transition: all 0.2s;
  }
  
  .btn-delete {
    background: linear-gradient(135deg, #ff4444, #cc0000);
    color: white;
  }
  
  .btn-delete:hover { transform: scale(1.05); box-shadow: 0 4px 15px rgba(255,68,68,0.4); }
  
  .btn-delete:disabled { opacity: 0.4; cursor: not-allowed; transform: none; }
  
  .btn-nav {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
  }
  
  .btn-nav:hover { transform: scale(1.05); }
  
  .btn-augment {
    background: linear-gradient(135deg, #11998e, #38ef7d);
    color: #0f0f1a;
  }
  
  .btn-augment:hover { transform: scale(1.05); box-shadow: 0 4px 15px rgba(56,239,125,0.4); }
  
  .sidebar {
    position: fixed;
    left: 0;
    top: 80px;
    bottom: 0;
    width: 280px;
    background: #13132b;
    overflow-y: auto;
    border-right: 1px solid #2d2d5e;
    z-index: 50;
  }
  
  .sidebar-item {
    padding: 10px 16px;
    cursor: pointer;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    transition: all 0.15s;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.85rem;
  }
  
  .sidebar-item:hover { background: rgba(102,126,234,0.15); }
  
  .sidebar-item.active {
    background: linear-gradient(90deg, rgba(102,126,234,0.3), transparent);
    border-left: 3px solid #667eea;
  }
  
  .sidebar-item .count {
    background: rgba(255,255,255,0.1);
    padding: 2px 8px;
    border-radius: 10px;
    font-size: 0.75rem;
    color: #00d2ff;
  }
  
  .main {
    margin-left: 280px;
    padding: 20px;
    padding-top: 100px;
  }
  
  .class-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 16px;
    padding: 16px;
    background: rgba(255,255,255,0.03);
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.08);
  }
  
  .class-header h2 {
    font-size: 1.2rem;
    color: #667eea;
  }
  
  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
    gap: 10px;
  }
  
  .img-card {
    position: relative;
    border-radius: 8px;
    overflow: hidden;
    cursor: pointer;
    border: 3px solid transparent;
    transition: all 0.2s;
    aspect-ratio: 1;
    background: #1a1a2e;
  }
  
  .img-card img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.2s;
  }
  
  .img-card:hover img { transform: scale(1.05); }
  
  .img-card.selected {
    border-color: #ff4444;
    box-shadow: 0 0 15px rgba(255,68,68,0.5);
  }
  
  .img-card.selected::after {
    content: '✕';
    position: absolute;
    top: 6px;
    right: 6px;
    background: #ff4444;
    color: white;
    width: 24px;
    height: 24px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    font-weight: bold;
  }
  
  .img-card .fname {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    background: rgba(0,0,0,0.7);
    padding: 4px 6px;
    font-size: 0.65rem;
    text-overflow: ellipsis;
    overflow: hidden;
    white-space: nowrap;
    opacity: 0;
    transition: opacity 0.2s;
  }
  
  .img-card:hover .fname { opacity: 1; }
  
  .toast {
    position: fixed;
    bottom: 30px;
    right: 30px;
    background: linear-gradient(135deg, #11998e, #38ef7d);
    color: #0f0f1a;
    padding: 14px 24px;
    border-radius: 10px;
    font-weight: 600;
    box-shadow: 0 8px 30px rgba(0,0,0,0.4);
    transform: translateY(100px);
    opacity: 0;
    transition: all 0.3s;
    z-index: 200;
  }
  
  .toast.show { transform: translateY(0); opacity: 1; }
  .toast.error { background: linear-gradient(135deg, #ff4444, #cc0000); color: white; }
  
  .search-box {
    width: 100%;
    padding: 10px 14px;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    color: #e0e0e0;
    border-radius: 8px;
    font-size: 0.85rem;
    margin: 10px;
    width: calc(100% - 20px);
  }
  
  .search-box::placeholder { color: rgba(255,255,255,0.3); }
  .search-box:focus { outline: none; border-color: #667eea; }
  
  .loading {
    text-align: center;
    padding: 60px;
    color: rgba(255,255,255,0.4);
    font-size: 1.2rem;
  }
  
  .select-all-bar {
    display: flex;
    gap: 10px;
    align-items: center;
    margin-bottom: 10px;
    flex-wrap: wrap;
  }
  
  .btn-sm {
    padding: 6px 14px;
    font-size: 0.8rem;
    border-radius: 6px;
  }

  /* Mobile Responsiveness */
  @media (max-width: 768px) {
    .header {
      flex-direction: column;
      gap: 10px;
      padding: 10px;
    }
    .header h1 { font-size: 1.2rem; }
    .stats { flex-wrap: wrap; justify-content: center; gap: 8px; }
    .sidebar {
      width: 100%;
      height: auto;
      max-height: 200px;
      position: relative;
      top: 0;
      border-right: none;
      border-bottom: 1px solid #2d2d5e;
    }
    .main {
      margin-left: 0;
      padding-top: 20px;
    }
    .grid {
      grid-template-columns: repeat(auto-fill, minmax(110px, 1fr));
    }
  }
</style>
</head>
<body>

<div class="header">
  <h1>🍄 Mushroom Image Reviewer</h1>
  <div class="stats">
    <div class="stat-box">Classes: <span id="totalClasses">-</span></div>
    <div class="stat-box">Current: <span id="currentCount">-</span></div>
    <div class="stat-box">Selected: <span id="selectedCount">0</span></div>
  </div>
  <div class="controls">
    <button class="btn btn-delete" id="deleteBtn" disabled onclick="deleteSelected()">🗑️ Delete Selected (0)</button>
    <button class="btn btn-augment" onclick="runAugmentation()">📈 Run Augmentation</button>
  </div>
</div>

<div class="sidebar">
  <input type="text" class="search-box" placeholder="🔍 Search class..." oninput="filterClasses(this.value)">
  <div id="classList"></div>
</div>

<div class="main" id="mainArea">
  <div class="loading">← Select a class from the sidebar to start reviewing</div>
</div>

<div class="toast" id="toast"></div>

<script>
let classes = [];
let currentClass = null;
let currentCategory = null;
let selectedImages = new Set();

async function loadClasses() {
  const res = await fetch('/api/classes');
  classes = await res.json();
  document.getElementById('totalClasses').textContent = classes.length;
  renderClassList(classes);
}

function filterClasses(query) {
  const filtered = classes.filter(c => c.name.toLowerCase().includes(query.toLowerCase()));
  renderClassList(filtered);
}

function renderClassList(list) {
  const el = document.getElementById('classList');
  el.innerHTML = list.map(c => `
    <div class="sidebar-item ${currentClass === c.name ? 'active' : ''}" onclick="loadClass('${c.name}', '${c.category}')">
      <div>
        <div style="font-size: 0.7rem; color: rgba(255,255,255,0.4)">${c.category.replace(/_/g, ' ')}</div>
        <span>${c.name.replace(/_/g, ' ')}</span>
      </div>
      <span class="count">${c.count}</span>
    </div>
  `).join('');
}

async function loadClass(name, category) {
  currentClass = name;
  currentCategory = category;
  selectedImages.clear();
  updateSelectedUI();
  renderClassList(classes);
  
  document.getElementById('mainArea').innerHTML = '<div class="loading">Loading images...</div>';
  
  const res = await fetch(`/api/images?class=${encodeURIComponent(name)}&category=${encodeURIComponent(category)}`);
  const images = await res.json();
  
  document.getElementById('currentCount').textContent = images.length;
  
  let html = `
    <div class="class-header">
      <div>
        <div style="font-size: 0.8rem; color: #667eea; opacity: 0.7">${category.replace(/_/g, ' ')}</div>
        <h2>${name.replace(/_/g, ' ')}</h2>
      </div>
      <span>${images.length} images</span>
    </div>
    <div class="select-all-bar">
      <button class="btn btn-nav btn-sm" onclick="selectAugmented()">Select All AUG</button>
      <button class="btn btn-nav btn-sm" onclick="selectAll()">Select All</button>
      <button class="btn btn-nav btn-sm" onclick="deselectAll()">Deselect All</button>
    </div>
    <div class="grid">
  `;
  
  images.forEach(img => {
    html += `
      <div class="img-card" id="card-${img}" onclick="toggleSelect('${img}')">
        <img src="/img/${encodeURIComponent(category)}/${encodeURIComponent(name)}/${encodeURIComponent(img)}" loading="lazy" alt="${img}">
        <div class="fname">${img}</div>
      </div>
    `;
  });
  
  html += '</div>';
  document.getElementById('mainArea').innerHTML = html;
}

function toggleSelect(img) {
  if (selectedImages.has(img)) {
    selectedImages.delete(img);
    document.getElementById('card-' + img)?.classList.remove('selected');
  } else {
    selectedImages.add(img);
    document.getElementById('card-' + img)?.classList.add('selected');
  }
  updateSelectedUI();
}

function selectAll() {
  document.querySelectorAll('.img-card').forEach(card => {
    const img = card.id.replace('card-', '');
    selectedImages.add(img);
    card.classList.add('selected');
  });
  updateSelectedUI();
}

function selectAugmented() {
  document.querySelectorAll('.img-card').forEach(card => {
    const img = card.id.replace('card-', '');
    if (img.includes('AUG')) {
      selectedImages.add(img);
      card.classList.add('selected');
    }
  });
  updateSelectedUI();
}

function deselectAll() {
  selectedImages.clear();
  document.querySelectorAll('.img-card').forEach(card => card.classList.remove('selected'));
  updateSelectedUI();
}

function updateSelectedUI() {
  const n = selectedImages.size;
  document.getElementById('selectedCount').textContent = n;
  const btn = document.getElementById('deleteBtn');
  btn.textContent = `🗑️ Delete Selected (${n})`;
  btn.disabled = n === 0;
}

async function deleteSelected() {
  if (selectedImages.size === 0) return;
  if (!confirm(`Delete ${selectedImages.size} images from ${currentClass}?`)) return;
  
  const res = await fetch('/api/delete', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ class: currentClass, category: currentCategory, images: Array.from(selectedImages) })
  });
  const data = await res.json();
  
  if (data.success) {
    showToast(`Deleted ${data.deleted} images. Remaining: ${data.remaining}`);
    // Update class count in sidebar
    const cls = classes.find(c => c.name === currentClass && c.category === currentCategory);
    if (cls) cls.count = data.remaining;
    renderClassList(classes);
    loadClass(currentClass, currentCategory);
  } else {
    showToast('Error: ' + data.error, true);
  }
}

async function runAugmentation() {
  if (!confirm('Run augmentation to balance all classes to 600? This may take a few minutes.')) return;
  
  showToast('⏳ Running augmentation...');
  const res = await fetch('/api/augment', { method: 'POST' });
  const data = await res.json();
  
  if (data.success) {
    showToast(`Augmentation complete! ${data.message}`);
    loadClasses();
    if (currentClass) loadClass(currentClass);
  } else {
    showToast('Error: ' + data.error, true);
  }
}

function showToast(msg, isError = false) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.className = 'toast show' + (isError ? ' error' : '');
  setTimeout(() => t.className = 'toast', 3000);
}

// Keyboard shortcut: Delete key
document.addEventListener('keydown', e => {
  if (e.key === 'Delete' && selectedImages.size > 0) deleteSelected();
});

loadClasses();
</script>
</body>
</html>"""


class ReviewHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Suppress logs
    
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        
        if path == '/' or path == '/index.html':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode())
            
        elif path == '/api/classes':
            result = []
            for cat in CATEGORIES:
                cat_path = os.path.join(BASE_DIR, cat)
                if not os.path.exists(cat_path): continue
                folders = sorted([d for d in os.listdir(cat_path) if os.path.isdir(os.path.join(cat_path, d))])
                for f in folders:
                    count = len([i for i in os.listdir(os.path.join(cat_path, f)) 
                               if i.lower().endswith(('.jpg','.jpeg','.png'))])
                    result.append({"name": f, "category": cat, "count": count})
            self.send_json(result)
            
        elif path == '/api/images':
            qs = urllib.parse.parse_qs(parsed.query)
            cls = qs.get('class', [''])[0]
            cat = qs.get('category', [''])[0]
            folder_path = os.path.join(BASE_DIR, cat, cls)
            if os.path.isdir(folder_path):
                images = sorted([f for f in os.listdir(folder_path) 
                               if f.lower().endswith(('.jpg','.jpeg','.png'))])
                self.send_json(images)
            else:
                self.send_json([])
                
        elif path.startswith('/img/'):
            # Path format: /img/category/class/image.jpg
            parts = path[5:].split('/', 2)
            if len(parts) == 3:
                cat = urllib.parse.unquote(parts[0])
                cls = urllib.parse.unquote(parts[1])
                img = urllib.parse.unquote(parts[2])
                filepath = os.path.join(BASE_DIR, cat, cls, img)
                if os.path.isfile(filepath):
                    thumb_data = get_thumbnail(filepath)
                    if thumb_data:
                        self.send_response(200)
                        self.send_header('Content-Type', 'image/jpeg')
                        self.send_header('Cache-Control', 'max-age=86400')
                        self.end_headers()
                        self.wfile.write(thumb_data)
                        return
            self.send_error(404)
            
        elif path.startswith('/full/'):
            parts = path[6:].split('/', 2)
            if len(parts) == 3:
                cat = urllib.parse.unquote(parts[0])
                cls = urllib.parse.unquote(parts[1])
                img = urllib.parse.unquote(parts[2])
                filepath = os.path.join(BASE_DIR, cat, cls, img)
                if os.path.isfile(filepath):
                    self.send_response(200)
                    self.send_header('Content-Type', 'image/jpeg')
                    self.end_headers()
                    with open(filepath, 'rb') as f:
                        self.wfile.write(f.read())
                    return
            self.send_error(404)
        else:
            self.send_error(404)
    
    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        content_len = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_len)
        
        if parsed.path == '/api/delete':
            data = json.loads(body)
            cls = data.get('class', '')
            cat = data.get('category', '')
            images = data.get('images', [])
            folder_path = os.path.join(BASE_DIR, cat, cls)
            
            deleted = 0
            for img in images:
                filepath = os.path.join(folder_path, img)
                if os.path.isfile(filepath):
                    os.remove(filepath)
                    deleted += 1
            
            remaining = len([f for f in os.listdir(folder_path) 
                           if f.lower().endswith(('.jpg','.jpeg','.png'))])
            self.send_json({"success": True, "deleted": deleted, "remaining": remaining})
            
        elif parsed.path == '/api/augment':
            import subprocess
            result = subprocess.run(
                ['python3', '-u', '/home/ashirkhan/Updated Data set/fast_augmentator.py'],
                capture_output=True, text=True, timeout=300
            )
            self.send_json({"success": True, "message": result.stdout.strip()})
        else:
            self.send_error(404)
    
    def send_json(self, data):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())


if __name__ == '__main__':
    server = http.server.HTTPServer(('0.0.0.0', PORT), ReviewHandler)
    print(f"🍄 Mushroom Image Reviewer running at: http://localhost:{PORT}")
    print(f"📂 Dataset: {BASE_DIR}")
    print(f"Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
