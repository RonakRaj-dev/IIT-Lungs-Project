import json
import os
import pandas as pd

# --- CONFIGURATION (EDIT THESE PATHS) ---
CSV_FILE_PATH = r'C:\Users\gamer\OneDrive\Desktop\IIT Project\Datasets\datasets\my_dataset\BBox_Final.csv'  # Your existing CSV file
JSON_FILE_PATH = r'C:\Users\gamer\OneDrive\Desktop\IIT Project\train\_annotations.coco.json'  # Roboflow JSON export
IMAGE_FOLDER_PATH = r'C:\Users\gamer\OneDrive\Desktop\IIT Project\Datasets\datasets\bbox_audited\Correct'  # Folder containing the images to update

# Define your CSV column names here to match your file
COL_FILENAME = 'filename'  # Column containing image file names
COL_X = 'x'  # Column for X coordinate (Top-Left)
COL_Y = 'y'  # Column for Y coordinate (Top-Left)
COL_W = 'w'  # Column for Width
COL_H = 'h'  # Column for Height
COL_AREA = 'area'  # Column for Area


# ----------------------------------------

def update_csv_from_roboflow():
    print("🚀 Loading files...")
    df = pd.read_csv(CSV_FILE_PATH)

    with open(JSON_FILE_PATH, 'r') as f:
        coco_data = json.load(f)

    # 1. Create a "Clean" mapping for Roboflow filenames
    # Roboflow: '000...018_png.rf.xyz.png' -> CSV: '000...018.png'
    filename_to_ann = {}
    id_to_name = {img['id']: img['file_name'] for img in coco_data['images']}

    for ann in coco_data['annotations']:
        rf_name = id_to_name.get(ann['image_id'])
        if rf_name:
            # Extract original name: remove the '.rf.xxxxx' part
            # This looks for the part before '_png' or '.rf' to match your CSV
            clean_name = rf_name.split('.rf.')[0].replace('_png', '.png')

            filename_to_ann[clean_name] = {
                'bbox': ann['bbox'],  # [x, y, width, height]
                'area': ann['area']
            }

    # 2. Get list of images actually present in the folder
    folder_images = set(os.listdir(IMAGE_FOLDER_PATH))

    # 3. Update the CSV
    updates = 0
    for index, row in df.iterrows():
        img_name = str(row['Image Index'])

        # Check if this image is in our folder AND has new data
        if img_name in folder_images and img_name in filename_to_ann:
            new_data = filename_to_ann[img_name]
            bbox = new_data['bbox']  # [x, y, w, h]

            # Update the specific columns from your sample
            df.at[index, 'x'] = bbox[0]
            df.at[index, 'y'] = bbox[1]
            df.at[index, 'w'] = bbox[2]
            df.at[index, 'h'] = bbox[3]
            df.at[index, 'area'] = new_data['area']
            updates += 1

    # 4. Save result
    output_path = "updated_annotations.csv"
    df.to_csv(output_path, index=False)
    print(f"✅ Done! Updated {updates} images. Saved to {output_path}")


if __name__ == "__main__":
    update_csv_from_roboflow()
