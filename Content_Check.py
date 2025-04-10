import cv2
import numpy as np
import shutil
import os
import json
from ultralytics import YOLO

# Initialize the YOLOv8 model
model = YOLO("yolov8s.pt")  # You can use a custom-trained model for logos/trademarks

# Load the Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)


def load_config():
    """Load the configuration from JSON."""
    with open("config/info.json") as f:
        return json.load(f)


def detect_faces(image_path):
    """
    Detect faces in the image and return True if faces are found.
    """
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    if len(faces) > 0:
        print(f"Faces detected: {len(faces)}")
        return True
    else:
        print("No faces detected.")
        return False


def detect_objects(image_path):
    """
    Detect objects (logos/trademarks) in the image using YOLOv8.
    """
    results = model(image_path)

    for result in results:
        for obj in result.boxes.data:
            label = obj[5]  # Class label (e.g., logo or trademark)
            confidence = obj[4]  # Confidence score

            if confidence > 0.5:  # Adjust the threshold as necessary
                print(f"Detected object: {label} with confidence {confidence}")
                return True

    print("No logos/trademarks detected.")
    return False


def detect_landmarks(image_path):
    """
    Detect landmarks or event-related objects in the image using YOLOv8.
    """
    results = model(image_path)

    for result in results:
        for obj in result.boxes.data:
            label = obj[5]  # Class label (e.g., 'Eiffel Tower')
            confidence = obj[4]  # Confidence score

            if confidence > 0.5:  # Adjust the threshold as necessary
                print(f"Detected landmark: {label} with confidence {confidence}")
                return True

    print("No landmarks or event-related objects detected.")
    return False


def perform_quality_check(image_path):
    """
    Perform all three checks (face detection, object detection, and landmark detection) on the image.
    Returns True if the image passes all checks.
    """
    is_face_detected = detect_faces(image_path)
    is_logo_detected = detect_objects(image_path)
    is_landmark_detected = detect_landmarks(image_path)

    # Flag the image if any check fails
    if is_face_detected or is_logo_detected or is_landmark_detected:
        print(f"Image {image_path} flagged for review.")
        return False  # Flagged for review due to face/logo/landmark

    print(f"Image {image_path} passed all checks.")
    return True


def process_images_for_checking():
    """
    Process all images in the source folder, perform checks, delete failed photo.
    """
    config = load_config()
    source_folder = config.get("selected_photo_dir")

    if not source_folder:
        print("Folder path is missing in config.json!")
        return

    # List all files in the source folder
    for filename in os.listdir(source_folder):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            image_path = os.path.join(source_folder, filename)

            if perform_quality_check(image_path):
                print(f"{filename} passed the quality check.")
            else:
                os.remove(image_path)  # Remove the image if it fails any of the checks
                print(f"{filename} failed the quality check and was removed.")


# Run the process to check and move images
if __name__ == "__main__":
    process_images_for_checking()
