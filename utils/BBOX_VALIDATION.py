import os
import shutil
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.patches as patches

# --- CONFIGURATION ---
BBOX_CSV = r'C:\Users\gamer\OneDrive\Desktop\IIT Project\Datasets\datasets\my_dataset\BBox_Final.csv'
BBOX_512_DIR = r'C:\Users\gamer\OneDrive\Desktop\IIT Project\Datasets\datasets\bbox_resized_512'
AUDIT_OUTPUT = r'C:\Users\gamer\OneDrive\Desktop\IIT Project\Datasets\datasets\bbox_audited'
ORIG_SIZE = 1024
TARGET_SIZE = 512

# --- RESUME SETTING ---
# Provide the name of the LAST image you successfully audited.
# If you leave it as None, it will start from the beginning.
START_AFTER_IMAGE = '00020671_010.png'

# Create Audit Folders
folders = ['Correct', 'Re-annotate', 'Garbage']
for f in folders: os.makedirs(os.path.join(AUDIT_OUTPUT, f), exist_ok=True)

def audit_bbox_dataset():
    df = pd.read_csv(BBOX_CSV)
    unique_images = list(df['Image Index'].unique())

    # --- RESUME LOGIC ---
    if START_AFTER_IMAGE and START_AFTER_IMAGE in unique_images:
        start_idx = unique_images.index(START_AFTER_IMAGE) + 1
        images_to_process = unique_images[start_idx:]
        print(f"⏩ Resuming from index {start_idx}. {len(images_to_process)} images remaining.")
    else:
        images_to_process = unique_images
        print(f"🚀 Starting from the beginning. Total images: {len(images_to_process)}")

    plt.ion()

    for img_name in images_to_process:
        path = os.path.join(BBOX_512_DIR, img_name)
        if not os.path.exists(path):
            continue

        image_data = df[df['Image Index'] == img_name]

        fig, ax = plt.subplots(figsize=(8, 8))
        img = mpimg.imread(path)
        ax.imshow(img, cmap='gray')

        scale_factor = TARGET_SIZE / ORIG_SIZE

        for _, row in image_data.iterrows():
            x, y = row['x'] * scale_factor, row['y'] * scale_factor
            w, h = row['w'] * scale_factor, row['h'] * scale_factor
            label = row['Finding Label']

            rect = patches.Rectangle((x, y), w, h, linewidth=2, edgecolor='lime', facecolor='none')
            ax.add_patch(rect)
            ax.text(x, y - 10, label, color='lime', fontsize=10, fontweight='bold',
                    bbox=dict(facecolor='black', alpha=0.5, pad=2))

        plt.title(f"Reviewing: {img_name}\n[c]=Correct, [r]=Re-annotate, [g]=Garbage, [q]=Quit")
        plt.axis('off')
        plt.draw()
        plt.pause(0.1)

        print(f"\nEvaluating Image: {img_name}")
        val = input("Decision (c/r/g/q): ").lower()

        plt.close(fig)

        if val == 'c':
            shutil.copy(path, os.path.join(AUDIT_OUTPUT, 'Correct', img_name))
        elif val == 'r':
            shutil.copy(path, os.path.join(AUDIT_OUTPUT, 'Re-annotate', img_name))
        elif val == 'g':
            shutil.copy(path, os.path.join(AUDIT_OUTPUT, 'Garbage', img_name))
        elif val == 'q':
            print(f"🛑 Audit paused. Last processed image was: {img_name}")
            break

    print("✅ Audit session complete.")
    plt.ioff()

if __name__ == "__main__":
    audit_bbox_dataset()