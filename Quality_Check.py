import os
import shutil
import cv2
import numpy as np
from PIL import Image
import json


def load_config():
    """Load the configuration from JSON."""
    with open("config/info.json") as f:
        return json.load(f)


def check_quality(image_path):
    """Check the image quality (e.g., sharpness, noise, exposure)."""

    print("Start quality checking...")
    try:
        img = cv2.imread(image_path)
        # Check if image exists
        if img is None:
            return False

        # Example: Check sharpness using Laplacian variance
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        variance = cv2.Laplacian(gray, cv2.CV_64F).var()
        if variance < 100:  # Adjust this threshold based on your needs
            print(f"Image {image_path} is too blurry.")
            return False

        # Example: Check for noise (using standard deviation of pixel values)
        noise = np.std(gray)
        if noise < 20:  # Adjust this threshold based on your needs
            print(f"Image {image_path} has too little noise (too clean).")
            return False

        # Example: Check exposure using average pixel intensity (a simple method)
        avg_intensity = np.mean(gray)
        if avg_intensity < 50 or avg_intensity > 200:  # Low or high exposure
            print(f"Image {image_path} has poor exposure.")
            return False

        # If no quality issues, return True
        return True

    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return False


def filter_photos():
    """Process and filter out ineligible photos from the stock photo folder."""
    print("Process start...")
    config = load_config()
    stock_photo_dir = config["selected_photo_dir"]
    needs_edit_dir = os.path.join(config["base_photo_dir"], "needs_edit")

    print(stock_photo_dir)

    print(needs_edit_dir)

    # Create "needs_edit" folder if it doesn't exist
    if not os.path.exists(needs_edit_dir):
        os.makedirs(needs_edit_dir)

    # Get list of photos in the stock photo directory
    for photo_name in os.listdir(stock_photo_dir):
        photo_path = os.path.join(stock_photo_dir, photo_name)

        print(photo_path)
        # Skip directories and hidden files
        if os.path.isdir(photo_path) or photo_name.startswith("."):
            continue

        print(f"Checking {photo_name}...")
        if not check_quality(photo_path):
            # If the photo fails the quality check, move it to "needs_edit"
            print(f"Moving {photo_name} to 'needs_edit' folder.")
            shutil.move(photo_path, os.path.join(needs_edit_dir, photo_name))
        else:
            print(f"Photo {photo_name} passed the quality check.")


if __name__ == "__main__":
    filter_photos()
