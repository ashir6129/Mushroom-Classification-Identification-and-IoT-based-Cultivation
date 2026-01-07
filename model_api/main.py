"""
Mushroom Classification REST API
================================
FastAPI endpoint for hierarchical mushroom classification using EfficientNet-B3.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import pandas as pd
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import torchvision.transforms as transforms
from efficientnet_pytorch import EfficientNet
import io

# --------------------------
# DEVICE CONFIGURATION
# --------------------------
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

# --------------------------
# LOAD CLASS STRUCTURE FROM CSV
# (Order matches how training code builds classes from directory structure)
# --------------------------
csv_path = "mushroom_structure.csv"
df = pd.read_csv(csv_path)

# Build MAIN_CLASSES in sorted order (matching training: sorted(os.listdir(root)))
MAIN_CLASSES = sorted(df["main_class"].unique().tolist())

# Build SUB_CLASSES in the order they appear in CSV
# (matching training: iterate through sorted main classes, then sorted sub folders)
SUB_CLASSES = df["sub_class"].tolist()

NUM_MAIN = len(MAIN_CLASSES)
NUM_SUB = len(SUB_CLASSES)

print(f"Main Classes ({NUM_MAIN}): {MAIN_CLASSES}")
print(f"Total Sub Classes: {NUM_SUB}")

# --------------------------
# MODEL DEFINITION (Hierarchical EfficientNet-B3)
# --------------------------
class HierarchicalEffNetB3(nn.Module):
    def __init__(self, num_main, num_sub):
        super().__init__()
        # Using EfficientNet-B3 backbone
        self.backbone = EfficientNet.from_pretrained('efficientnet-b3')
        
        in_features = self.backbone._fc.in_features
        self.backbone._fc = nn.Identity()  # Remove default classifier
        
        # Two separate heads for hierarchical classification
        self.main_head = nn.Linear(in_features, num_main)
        self.sub_head = nn.Linear(in_features, num_sub)
    
    def forward(self, x):
        feat = self.backbone(x)
        return self.main_head(feat), self.sub_head(feat)

# --------------------------
# LOAD MODEL
# --------------------------
model_path = "best_hierarchical_effnet_b3.pth"

print(f"Loading model from {model_path}...")
model = HierarchicalEffNetB3(num_main=NUM_MAIN, num_sub=NUM_SUB).to(device)

# Load trained weights
checkpoint = torch.load(model_path, map_location=device)
model.load_state_dict(checkpoint)
model.eval()

print("✓ Model loaded successfully!")

# --------------------------
# IMAGE TRANSFORMS
# --------------------------
transform = transforms.Compose([
    transforms.Resize(320),
    transforms.CenterCrop(300),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

# --------------------------
# FASTAPI APPLICATION
# --------------------------
app = FastAPI(
    title="Mushroom Classification API",
    description="Hierarchical mushroom classification using EfficientNet-B3",
    version="1.0.0"
)

# Enable CORS for Flutter app integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "message": "Mushroom Classification API is running!",
        "endpoints": {
            "/predict": "POST - Upload an image to classify mushroom",
            "/classes": "GET - Get list of all classes"
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "device": device}

@app.get("/classes")
def get_classes():
    return {
        "main_classes": MAIN_CLASSES,
        "sub_classes": SUB_CLASSES,
        "num_main": NUM_MAIN,
        "num_sub": NUM_SUB
    }

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    Predict mushroom classification from uploaded image.
    
    Returns:
        - main_class: The main category (e.g., Non_Poisnous_Edible, Poisnous_Non_Useable)
        - main_confidence_percent: Confidence score for main class (0-100)
        - species: The specific mushroom species
        - species_confidence_percent: Confidence score for species (0-100)
    """
    # Validate file type
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Read image bytes
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image file: {str(e)}")
    
    # Preprocess image
    tensor = transform(image).unsqueeze(0).to(device)
    
    # Run inference
    with torch.no_grad():
        main_out, sub_out = model(tensor)
        
        # Convert to probabilities
        main_probs = F.softmax(main_out, dim=1)
        sub_probs = F.softmax(sub_out, dim=1)
        
        # Get highest probability class
        main_prob, main_idx = torch.max(main_probs, 1)
        sub_prob, sub_idx = torch.max(sub_probs, 1)
        
        # Convert to percentages
        main_confidence = round(main_prob.item() * 100, 2)
        species_confidence = round(sub_prob.item() * 100, 2)
        
        main_class = MAIN_CLASSES[main_idx.item()]
        species = SUB_CLASSES[sub_idx.item()]
    
    return {
        "Main Class": main_class,
        "Main Confidence (%)": main_confidence,
        "Species": species,
        "Species Confidence (%)": species_confidence,
        "is_poisonous": "Poisnous" in main_class
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
