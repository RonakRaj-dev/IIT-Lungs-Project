import os

# --- CONFIGURATION ---
# Based on your image, the parent folder is 'annotated'
# Adjust the C:\ path to match your exact desktop location
ROOT_DIR = r"C:\Users\gamer\OneDrive\Desktop\IIT Project\Datasets\annotated"


def clean_and_fix_filenames(root):
    print(f"🚀 Starting traversal in: {root}")
    print("-" * 30)

    # count for summary
    renamed_count = 0

    # os.walk traverses 'member 1', 'member 3', and 'member 4' automatically
    for subdir, dirs, files in os.walk(root):
        for filename in files:
            if "_png" in filename:
                # 1. Split at '_png' and keep only the part before it
                clean_name_base = filename.split("_png")[0]

                # 2. Append the correct extension
                new_name = f"{clean_name_base}.png"

                # Construct full paths
                old_file_path = os.path.join(subdir, filename)
                new_file_path = os.path.join(subdir, new_name)

                try:
                    # Perform the rename
                    os.rename(old_file_path, new_file_path)
                    print(f"✅ Subfolder '{os.path.basename(subdir)}': {filename} -> {new_name}")
                    renamed_count += 1
                except FileExistsError:
                    print(f"⚠️ Conflict: {new_name} already exists in {os.path.basename(subdir)}. Skipping.")
                except Exception as e:
                    print(f"❌ Failed to rename {filename}: {e}")

    print("-" * 30)
    print(f"✨ DONE! Total images cleaned: {renamed_count}")


if __name__ == "__main__":
    # Check if the path actually exists before running
    if os.path.exists(ROOT_DIR):
        clean_and_fix_filenames(ROOT_DIR)
    else:
        print(f"❌ Error: The path {ROOT_DIR} was not found. Please check your Windows path.")