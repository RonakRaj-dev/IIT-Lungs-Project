import os
import shutil
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array

# --- CONFIGURATION ---
MODEL_PATH = r'C:\Users\gamer\OneDrive\Desktop\IIT Project\utils\heavy_teacher_final.h5'
TRAIN_CSV_PATH = r'C:\Users\gamer\OneDrive\Desktop\IIT Project\Datasets\datasets\Pilot\train_final.csv'
BBOX_REF_CSV = r'C:\Users\gamer\OneDrive\Desktop\IIT Project\utils\updated_annotations.csv'
PILOT_IMG_DIR = r'C:\Users\gamer\OneDrive\Desktop\IIT Project\Datasets\datasets\Pilot\Image_512'
SORT_OUTPUT_ROOT = r'C:\Users\gamer\OneDrive\Desktop\IIT Project\Datasets\datasets\Pilot\Sorted_Results'

TARGET_SIZE = (512, 512)
IOU_THRESHOLD = 0.50
CONF_THRESHOLD = 0.70

# 1. Setup Folders
id_dir = os.path.join(SORT_OUTPUT_ROOT, 'Identified')
un_dir = os.path.join(SORT_OUTPUT_ROOT, 'Unidentified')
os.makedirs(id_dir, exist_ok=True)
os.makedirs(un_dir, exist_ok=True)


# 2. Helper: Calculate Intersection over Union (IoU)
def calculate_iou(boxA, boxB):
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[0] + boxA[2], boxB[0] + boxB[2])
    yB = min(boxA[1] + boxA[3], boxB[1] + boxB[3])

    interArea = max(0, xB - xA) * max(0, yB - yA)
    boxAArea = boxA[2] * boxA[3]
    boxBArea = boxB[2] * boxB[3]

    iou = interArea / float(boxAArea + boxBArea - interArea + 1e-6)
    return iou


# 3. Load Model and Data
print("🧠 Loading Teacher and Reference Data...")
model = tf.keras.models.load_model(MODEL_PATH, compile=False)
train_df = pd.read_csv(TRAIN_CSV_PATH)
bbox_ref = pd.read_csv(BBOX_REF_CSV)


def run_verified_sorting_with_logging():
    count = 0
    total = len(train_df)

    # --- LOGGING LIST ---
    log_data = []

    for idx, row in train_df.iterrows():
        img_name = row['Image Index']
        img_path = os.path.join(PILOT_IMG_DIR, img_name)

        if not os.path.exists(img_path): continue

        # A. Get Ground Truth
        ref_row = bbox_ref[bbox_ref['Image Index'] == img_name]
        if ref_row.empty:
            log_data.append({'Image Index': img_name, 'Confidence': 0, 'IoU': 0, 'Status': 'Unidentified (No Ref)'})
            shutil.copy(img_path, os.path.join(un_dir, img_name))
            continue

        gt_box = [ref_row.iloc[0]['x'] / 1024, ref_row.iloc[0]['y'] / 1024,
                  ref_row.iloc[0]['w'] / 1024, ref_row.iloc[0]['h'] / 1024]

        # B. Model Prediction
        img = load_img(img_path, target_size=TARGET_SIZE)
        img_arr = np.expand_dims(img_to_array(img) / 255.0, axis=0)
        preds = model.predict(img_arr, verbose=0)

        pred_conf = np.max(preds[0][0])
        pred_box = preds[1][0]

        # C. Verification Step (IoU)
        iou_score = calculate_iou(gt_box, pred_box)

        # D. Verified Segregation
        status = "Unidentified"
        if pred_conf >= CONF_THRESHOLD and iou_score >= IOU_THRESHOLD:
            shutil.copy(img_path, os.path.join(id_dir, img_name))
            status = "Identified"
        else:
            shutil.copy(img_path, os.path.join(un_dir, img_name))

        # E. Record to Log
        log_data.append({
            'Image Index': img_name,
            'Confidence': round(float(pred_conf), 4),
            'IoU': round(float(iou_score), 4),
            'Status': status
        })

        count += 1
        if count % 100 == 0:
            print(f"✅ Verified & Logged {count}/{total} images...")

    # --- SAVE LOG FILE ---
    log_df = pd.DataFrame(log_data)
    log_csv_path = os.path.join(SORT_OUTPUT_ROOT, 'verification_log.csv')
    log_df.to_csv(log_csv_path, index=False)
    print(f"\n✨ DONE! Verification log saved to: {log_csv_path}")


if __name__ == "__main__":
    run_verified_sorting_with_logging()