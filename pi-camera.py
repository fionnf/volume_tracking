import time
import os
import git
from picamera2 import Picamera2

# Ask for the experiment name
experiment_name = input("Enter the experiment name: ")

# Initialize the camera
picam2 = Picamera2()
picam2.start()

# Define the directory to save images
output_dir = f"images/{experiment_name}"
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

# Initialize the Git repository
repo = git.Repo.init('.')
origin = repo.remote(name='origin')

# Capture images at specified intervals and upload to Git
interval = 10  # Interval in seconds
while True:
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    image_path = os.path.join(output_dir, f"{timestamp}.jpg")

    # Capture image
    frame = picam2.capture_array()
    #optional clockwise rotation
    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    cv2.imwrite(image_path, frame)

    # Update metadata
    with open(metadata_path, 'a') as f:
        f.write(f"{timestamp},{image_path}\n")

    # Add, commit, and push the new image and metadata to the Git repository
    repo.index.add([image_path, metadata_path])
    repo.index.commit(f"Add image and metadata for {timestamp}")
    origin.push()

    print(f"Captured and uploaded image at {timestamp}")
    time.sleep(interval)

picam2.stop()
print("Camera stopped.")