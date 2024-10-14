

"""
This script captures images at specified intervals using the Picamera2 on a Raspberry Pi, 
saves them to a directory, and uploads them to a Git repository. It also manages disk usage 
by deleting the local images after they have been successfully pushed to GitHub, ensuring 
that the Raspberry Pi's storage does not get full.

Features:
- Captures images at user-defined intervals.
- Saves images and metadata to a specified directory.
- Automatically creates a metadata CSV file and a README file in the output directory.
- Uses the current Git branch to commit and push images and metadata to the repository.
- Deletes local images after successful upload to GitHub to manage disk space.
- Includes a function to check disk usage and delete the oldest files if the usage exceeds a specified threshold.

Dependencies:
- picamera2
- OpenCV
- Git
- shutil
"""

import time
import os
import subprocess
import cv2
from picamera2 import Picamera2
import shutil

# Function to check disk usage and delete oldest files if necessary
def manage_disk_usage(directory, threshold=80):
    total, used, free = shutil.disk_usage("/")
    used_percentage = (used / total) * 100

    if used_percentage > threshold:
        print("Disk usage exceeded threshold. Deleting oldest files...")
        files = sorted(
            (os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".jpg")),
            key=os.path.getctime
        )
        while used_percentage > threshold and files:
            oldest_file = files.pop(0)
            os.remove(oldest_file)
            print(f"Deleted {oldest_file}")
            total, used, free = shutil.disk_usage("/")
            used_percentage = (used / total) * 100

# Ask for the experiment name
experiment_name = input("Enter the experiment name: ")
image_interval = int(input("Enter the image capture interval (in minutes): "))

# Initialize the camera
picam2 = Picamera2()
picam2.start()

# Define the directory to save images
timestamp = time.strftime("%Y%m%d-%H%M%S")
output_dir = f"images/{experiment_name}_{timestamp}"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Create metadata.csv and README.md
metadata_path = os.path.join(output_dir, 'metadata.csv')
readme_path = os.path.join(output_dir, 'README.md')

if not os.path.exists(metadata_path):
    with open(metadata_path, 'w') as f:
        f.write("Timestamp,Image Path\n")

if not os.path.exists(readme_path):
    with open(readme_path, 'w') as f:
        f.write(f"# {experiment_name} Images\n\n")
        f.write("This directory contains images captured during the experiment.\n")
        f.write("Each image is named with a timestamp indicating when it was taken.\n\n")
        f.write("## Metadata\n\n")
        f.write("Additional metadata about the images can be found in `metadata.csv`.\n")

# Use the existing Git repository
repo_path = os.path.dirname(os.path.abspath(__file__))  # Path of the current code

# Ensure the script uses the same branch
current_branch = subprocess.run(['git', 'branch', '--show-current'], cwd=repo_path, capture_output=True, text=True).stdout.strip()
subprocess.run(['git', 'checkout', current_branch], cwd=repo_path)

# Capture images at specified intervals and upload to Git
interval = image_interval * 60
while True:
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    image_path = os.path.join(output_dir, f"{timestamp}.jpg")

    # Capture image
    frame = picam2.capture_array()
    # Optional clockwise rotation
    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    cv2.imwrite(image_path, frame)

    # Update metadata
    with open(metadata_path, 'a') as f:
        f.write(f"{timestamp},{image_path}\n")

    # Add, commit, and push the new image and metadata to the Git repository
    subprocess.run(['git', 'add', image_path, metadata_path], cwd=repo_path)
    subprocess.run(['git', 'commit', '-m', f"Add image and metadata for {timestamp}"], cwd=repo_path)
    subprocess.run(['git', 'push'], cwd=repo_path)

    print(f"Captured and uploaded image at {timestamp}")

    # Delete the image from the local storage after pushing to GitHub
    os.remove(image_path)
    print(f"Deleted local image at {image_path}")

    # Manage disk usage
    manage_disk_usage(output_dir)

    time.sleep(interval)

picam2.stop()
print("Camera stopped.")