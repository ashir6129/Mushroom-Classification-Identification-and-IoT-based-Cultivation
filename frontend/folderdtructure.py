import os

# --- CHANGE THIS TO YOUR PROJECT PATH ---
base_path = "/home/ashirkhan/Final Year Project/mushroom_fyp/frontend/lib"

folders = [
    "themes",
    "screens/splash",
    "screens/home",
    "screens/camera",
    "screens/explore",
    "screens/details",
    "widgets/buttons",
    "widgets/cards",
    "widgets/tags",
    "widgets/search",
    "services",
    "models",
    "utils",
]

files = {
    "main.dart": "",
    "themes/app_colors.dart": "",
    "themes/app_theme.dart": "",
    "themes/app_text_styles.dart": "",
    
    "screens/splash/splash_screen.dart": "",
    "screens/home/home_screen.dart": "",
    "screens/camera/camera_detector_screen.dart": "",
    "screens/explore/explore_mushrooms_screen.dart": "",
    "screens/details/mushroom_details_screen.dart": "",
    
    "widgets/buttons/app_button.dart": "",
    "widgets/cards/mushroom_card.dart": "",
    "widgets/tags/tag_badge.dart": "",
    "widgets/search/search_bar.dart": "",
    
    "services/ai_service.dart": "",
    "models/mushroom_model.dart": "",
    "utils/constants.dart": "",
    "utils/dummy_data.dart": "",
}

# ---- CREATE FOLDERS ----
for folder in folders:
    folder_path = os.path.join(base_path, folder)
    os.makedirs(folder_path, exist_ok=True)
    print(f"Created folder: {folder_path}")

# ---- CREATE FILES ----
for file_path, content in files.items():
    full_path = os.path.join(base_path, file_path)
    with open(full_path, "w") as f:
        f.write(content)
    print(f"Created file: {full_path}")

print("\n🎉 Flutter frontend base structure created successfully!")

