# Photo_Scan.py

import os
import json
import shutil
from PIL import Image
from datetime import datetime
from tqdm import tqdm  # Progress bar

# Load configuration
print("📥 Loading configuration...")
with open("config/info.json", "r") as f:
    config = json.load(f)

# Resolve absolute paths
base_dir = config["base_photo_dir"]
selected_dir = os.path.join(base_dir, config["selected_photo_dir"])
meta_dir = os.path.join(base_dir, config["meta_dir"])
edit_dir = os.path.join(base_dir, "Needs_Edit")
log_file = os.path.join(meta_dir, config["processed_log_file"])

# Load scan settings
min_width = config["min_width"]
min_height = config["min_height"]
valid_exts = tuple(ext.lower() for ext in config["valid_extensions"])
rescan_all = config.get("rescan_all", False)

# Create necessary folders
print("📁 Ensuring output folders exist...")
os.makedirs(selected_dir, exist_ok=True)
os.makedirs(meta_dir, exist_ok=True)
os.makedirs(edit_dir, exist_ok=True)

# Load previously processed folders
print("📖 Loading processed folder log...")
if os.path.exists(log_file):
    with open(log_file, "r") as f:
        processed = json.load(f)
else:
    processed = {}

# Step 1: Scan all subfolders
print("🔍 Searching for trip folders...")
skip_folders = {
    config["selected_photo_dir"].lower(),
    config["meta_dir"].lower(),
    "needs_edit",
}

trip_folders = [
    name
    for name in os.listdir(base_dir)
    if os.path.isdir(os.path.join(base_dir, name)) and name.lower() not in skip_folders
]
print(f"📂 Found {len(trip_folders)} trip folder(s) to check.")


def is_valid_image(path):
    try:
        with Image.open(path) as img:
            width, height = img.size
            return width >= min_width and height >= min_height
    except Exception:
        return False


now = datetime.now().strftime("%Y-%m-%d")

total_good = 0
total_edit = 0


def print_folder_summary(folder, copied_count, edit_count):
    print(
        f"📈 Folder summary for '{folder}': {copied_count} good, {edit_count} needs edit"
    )


for folder in trip_folders:
    folder_path = os.path.join(base_dir, folder)

    if not rescan_all and folder in processed:
        print(f"⏩ Skipping already processed folder: {folder}")
        continue

    print(f"📁 Processing folder: {folder}")

    files = [
        file for file in os.listdir(folder_path) if file.lower().endswith(valid_exts)
    ]
    copied_count = 0
    edit_count = 0

    for file in tqdm(files, desc=f"   🔄 {folder}", unit="file"):
        src_path = os.path.join(folder_path, file)
        dst_path = (
            os.path.join(selected_dir, file)
            if is_valid_image(src_path)
            else os.path.join(edit_dir, file)
        )

        if os.path.abspath(src_path) == os.path.abspath(dst_path):
            print(f"⚠️ Skipping self-copy: {file}")
            continue

        shutil.copy2(src_path, dst_path)

        if dst_path.startswith(selected_dir):
            copied_count += 1
        else:
            edit_count += 1

    print_folder_summary(folder, copied_count, edit_count)
    total_good += copied_count
    total_edit += edit_count
    processed[folder] = now

# Save updated log
print("💾 Updating processed folder log...")
with open(log_file, "w") as f:
    json.dump(processed, f, indent=4)

print("\n✅ Step 1 complete: Photo scan and copy finished.")
print(f"📊 Total results: {total_good} good photos, {total_edit} need editing")
