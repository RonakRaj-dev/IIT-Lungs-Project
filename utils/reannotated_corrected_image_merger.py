import os
import re

# Change this to your folder path
folder = r"C:\Users\gamer\OneDrive\Desktop\IIT Project\train"

for fname in os.listdir(folder):
    # Only process files that contain "_png"
    match = re.match(r"^(.*?\d+)_png", fname)
    if match:
        # Build the new filename
        new_name = match.group(1) + ".png"
        old_path = os.path.join(folder, fname)
        new_path = os.path.join(folder, new_name)

        # Rename the file
        os.rename(old_path, new_path)
        print(f"Renamed: {fname} -> {new_name}")
