import os
import pandas as pd

# --- CONFIGURATION ---
BASE_DIR = r"C:\Users\gamer\OneDrive\Desktop\IIT Project\Datasets"
PREPROCESSED_DIR = os.path.join(BASE_DIR, "datasets", "Pilot", "preprocessed_image")
TEST_CSV = os.path.join(BASE_DIR, "datasets", "Pilot", "test_final.csv")


def diagnose_test_mismatch():
    # 1. Load CSV
    df = pd.read_csv(TEST_CSV)
    csv_filenames = set(df['Image Index'].str.strip().unique())

    # 2. Get actual files in the preprocessed folder
    if os.path.exists(PREPROCESSED_DIR):
        folder_files = set(os.listdir(PREPROCESSED_DIR))
    else:
        print(f"❌ Folder not found: {PREPROCESSED_DIR}")
        return

    print(f"📊 CSV expects: {len(csv_filenames)} unique images")
    print(f"📂 Folder contains: {len(folder_files)} total images")

    # 3. Check for direct matches
    matches = csv_filenames.intersection(folder_files)
    print(f"✅ Direct matches found: {len(matches)}")

    if len(matches) == 0:
        print("\n🔍 SEARCHING FOR CLUES...")
        # Check for case sensitivity (e.g., .png vs .PNG)
        lower_folder_files = {f.lower() for f in folder_files}
        case_matches = {f for f in csv_filenames if f.lower() in lower_folder_files}

        if len(case_matches) > 0:
            print(f"💡 Found {len(case_matches)} files with case-sensitivity issues (e.g., .PNG vs .png).")
            print("Action: Rename your files to lowercase .png")
            return

        # Check if files exist ANYWHERE in the Datasets folder
        print("🕵️ Searching entire Datasets directory for the first missing file...")
        sample_file = list(csv_filenames)[0]
        found_path = None
        for root, dirs, files in os.walk(BASE_DIR):
            if sample_file in files:
                found_path = os.path.join(root, sample_file)
                break

        if found_path:
            print(f"📍 Found the missing file here: {found_path}")
            print(f"Action: Move all test images from that folder into: {PREPROCESSED_DIR}")
        else:
            print(f"❌ The file '{sample_file}' does not exist anywhere in {BASE_DIR}.")
            print("Action: Verify if the test images were downloaded or if the filenames in the CSV are correct.")


if __name__ == "__main__":
    diagnose_test_mismatch()