import cv2
import numpy as np
import time
import csv
from picamera2 import Picamera2

# Initialize the camera
picam2 = Picamera2()
picam2.start()

# Define the directory to save images and log file
output_dir = "output_images"
log_file = f"{output_dir}/log.csv"

# Create the output directory if it doesn't exist
import os
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Capture an initial frame to define ROIs
frame = picam2.capture_array()
frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
cv2.imwrite(f"{output_dir}/initial_image.jpg", frame)

# Define vertical strip ROIs for two containers
print("Please select the first vertical strip ROI in the image for the first container.")
r1 = cv2.selectROI("initial_image.jpg", frame, fromCenter=False, showCrosshair=True)
print(f"Selected ROI 1: {r1}")
cv2.destroyAllWindows()

print("Please select the second vertical strip ROI in the image for the second container.")
r2 = cv2.selectROI("initial_image.jpg", frame, fromCenter=False, showCrosshair=True)
print(f"Selected ROI 2: {r2}")
cv2.destroyAllWindows()

def calculate_height(roi, frame):
    roi_frame = frame[int(roi[1]):int(roi[1] + roi[3]), int(roi[0]):int(roi[0] + roi[2])]
    gray_frame = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2GRAY)
    blurred_frame = cv2.GaussianBlur(gray_frame, (3, 3), 0)
    v = np.median(blurred_frame)
    lower = int(max(0, 0.4 * v))
    upper = int(min(255, 1.6 * v))
    edges = cv2.Canny(blurred_frame, lower, upper)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        print("No valid meniscus found.")
        return 0

    max_aspect_ratio = 0
    best_contour = None

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = w / float(h)
        rect = cv2.minAreaRect(contour)
        angle = rect[2]

        if aspect_ratio > 2.0 and -45 <= angle <= 45:
            if aspect_ratio > max_aspect_ratio:
                max_aspect_ratio = aspect_ratio
                best_contour = contour

    if best_contour is None:
        print("No valid horizontal meniscus found.")
        return 0

    x, y, w, h = cv2.boundingRect(best_contour)
    height = roi[3] - y
    return height

# Open the CSV log file
with open(log_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Timestamp", "Height1", "Height2"])

    # Capture images at specified intervals and perform analysis
    interval = 10  # Interval in seconds
    while True:
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        frame = picam2.capture_array()
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        image_path = f"{output_dir}/{timestamp}.jpg"
        cv2.imwrite(image_path, frame)

        height1 = calculate_height(r1, frame)
        height2 = calculate_height(r2, frame)

        writer.writerow([timestamp, height1, height2])
        print(f"Captured and processed image at {timestamp}")

        time.sleep(interval)

picam2.stop()
print("Camera stopped.")