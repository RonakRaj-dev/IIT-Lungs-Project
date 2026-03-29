import pandas as pd
import json
import os

# --- CONFIGURATION ---
ROOT_ANNOTATED_DIR = r"C:\Users\gamer\OneDrive\Desktop\IIT Project\Datasets\annotated"
EXCEL_FILE = r"C:\Users\gamer\OneDrive\Desktop\IIT Project\Datasets\datasets\Pilot\train_final.csv"
OUTPUT_FILE = r"C:\Users\gamer\OneDrive\Desktop\IIT Project\Datasets\datasets\Pilot\train_final_updated.csv"

# Define Clinical Groupings
PATHOLOGIES = [
    'Atelectasis', 'Cardiomegaly', 'Consolidation', 'Edema', 'Effusion',
    'Emphysema', 'Fibrosis', 'Hernia', 'Infiltration', 'Mass',
    'Nodule', 'Pleural_Thickening', 'Pneumonia', 'Pneumothorax'
]

# Minority classes (Rare findings in NIH dataset that require extra weighting)
MINORITY_CLASSES = [
    'Hernia', 'Fibrosis', 'Emphysema', 'Edema', 'Consolidation',
    'Cardiomegaly', 'Pleural_Thickening', 'Pneumothorax'
]


def update_and_encode_coco(excel_path, root_dir, output_path):
    print("📂 Loading Master CSV...")
    df = pd.read_csv(excel_path)
    df['Image Index'] = df['Image Index'].str.strip()

    master_label_mapping = {}
    master_image_meta = {}

    # 1. Gather Annotations from Member Folders
    member_folders = [f for f in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, f))]

    for member in member_folders:
        coco_path = os.path.join(root_dir, member, "annotation.coco")
        if not os.path.exists(coco_path): continue

        print(f"📄 Processing: {member}/annotation.coco")
        with open(coco_path, 'r') as f:
            coco = json.load(f)

        cat_map = {cat['id']: cat['name'] for cat in coco['categories']}

        # Build mapping and clean filenames
        img_id_to_clean_name = {}
        for img in coco['images']:
            raw_name = img['file_name']
            clean_name = raw_name.split("_png")[0] + ".png" if "_png" in raw_name else raw_name
            img_id_to_clean_name[img['id']] = clean_name
            master_image_meta[clean_name] = {'w': img['width'], 'h': img['height']}

        for ann in coco['annotations']:
            clean_name = img_id_to_clean_name.get(ann['image_id'])
            label_name = cat_map.get(ann['category_id'])
            if clean_name:
                if clean_name not in master_label_mapping:
                    master_label_mapping[clean_name] = set()
                master_label_mapping[clean_name].add(label_name)

    # 2. Apply One-Hot Encoding and Minority Check
    print("📝 Performing One-Hot Encoding and Minority Labeling...")

    for idx, row in df.iterrows():
        img_name = row['Image Index']

        # Only update if we have annotations for this image
        if img_name in master_image_meta:
            # A. Update Metadata
            df.at[idx, 'ImageWidth'] = master_image_meta[img_name]['w']
            df.at[idx, 'ImageHeight'] = master_image_meta[img_name]['h']

            # B. Get current labels (Union of all annotations)
            found_labels = master_label_mapping.get(img_name, {"No Finding"})

            # C. One-Hot Encoding
            has_minority = False
            for p in PATHOLOGIES:
                if p in found_labels:
                    df.at[idx, p] = 1
                    # Check if this pathology is in the minority list
                    if p in MINORITY_CLASSES:
                        has_minority = True
                else:
                    df.at[idx, p] = 0

            # D. Handle 'No Finding' and Strip Labels
            df.at[idx, 'No Finding'] = 1 if "No Finding" in found_labels else 0
            df.at[idx, 'Finding Labels'] = "|".join(sorted(list(found_labels)))
            df.at[idx, 'FindingsLabels_Strip'] = str(list(found_labels))

            # E. Minority Count/Flag
            df.at[idx, 'is_minority'] = 1 if has_minority else 0

    # Final Statistics
    minority_count = df['is_minority'].sum()
    print(f"✅ Success! Minority Images identified: {int(minority_count)}")

    df.to_csv(output_path, index=False)
    print(f"✨ Updated file saved to: {output_path}")


if __name__ == "__main__":
    update_and_encode_coco(EXCEL_FILE, ROOT_ANNOTATED_DIR, OUTPUT_FILE)