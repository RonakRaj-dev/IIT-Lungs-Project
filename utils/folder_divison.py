import os
import shutil


def divide_files_into_folders(folder_path, num_members=5):
    # Get all files in the folder
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    # Sort files for consistency
    files.sort()

    # Create separate folders for each member
    member_folders = []
    for i in range(num_members):
        member_folder = os.path.join(folder_path, f"member_{i + 1}")
        os.makedirs(member_folder, exist_ok=True)
        member_folders.append(member_folder)

    # Distribute files evenly (round-robin)
    for idx, file in enumerate(files):
        member_index = idx % num_members
        src = os.path.join(folder_path, file)
        dest = os.path.join(member_folders[member_index], file)
        shutil.move(src, dest)

    print(f"✅ Distributed {len(files)} files into {num_members} folders.")


if __name__ == "__main__":
    # Change this path to the folder you want to split
    folder_path = r"C:\Users\gamer\OneDrive\Desktop\IIT Project\Datasets\datasets\Pilot\Sorted_Results\Unidentified"

    divide_files_into_folders(folder_path, num_members=5)
