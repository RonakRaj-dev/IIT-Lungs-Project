import pandas as pd
import cv2
import os

# --- CONFIGURATION ---
ROOT = r'C:\Users\gamer\OneDrive\Desktop\IIT Project\Datasets\datasets'
BBOX_CSV_PATH = r'C:\Users\gamer\OneDrive\Desktop\IIT Project\Datasets\datasets\nih-chest-xrays\data\versions\3\BBox_List_2017.csv'
BASE_DATA_DIR = r'C:\Users\gamer\OneDrive\Desktop\IIT Project\Datasets\datasets\nih-chest-xrays\data\versions\3'
BBOX_OUTPUT_DIR = os.path.join(ROOT, 'bbox_resized_512')
IMG_SIZE = 512

# Create output folder
os.makedirs(BBOX_OUTPUT_DIR, exist_ok=True)

# 1. Load the BBox Metadata
bbox_df = pd.read_csv(BBOX_CSV_PATH)
unique_images = bbox_df['Image Index'].unique()

print(f"🔍 Found {len(unique_images)} unique images in the BBox file.")

# 2. Map all filenames to their specific subfolder for fast lookup
print("📂 Scanning subfolders to locate images...")
image_path_map = {}
for root, dirs, files in os.walk(BASE_DATA_DIR):
    for file in files:
        if file.endswith('.png'):
            image_path_map[file] = os.path.join(root, file)

# 3. Extract and Resize Loop
count = 0
not_found = 0

for img_name in unique_images:
    target_path = os.path.join(BBOX_OUTPUT_DIR, img_name)

    # Check if we found the image path during the scan
    if img_name in image_path_map:
        source_path = image_path_map[img_name]

        # Read image
        img = cv2.imread(source_path)

        if img is not None:
            # Resize to 512x512
            img_resized = cv2.resize(img, (IMG_SIZE, IMG_SIZE), interpolation=cv2.INTER_AREA)

            # Save to new folder
            cv2.imwrite(target_path, img_resized)
            count += 1

            if count % 100 == 0:
                print(f"✅ Processed {count}/{len(unique_images)} images...")
        else:
            print(f"❌ Error: Could not decode {img_name}")
    else:
        not_found += 1

print(f"\n--- Processing Summary ---")
print(f"✨ Success: {count} images resized and saved in '{BBOX_OUTPUT_DIR}'")
if not_found > 0:
    print(f"⚠️ Warning: {not_found} images from BBox list were not found in the subfolders.")