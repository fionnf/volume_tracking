from picamera2 import Picamera2
import cv2
import numpy as np
import time

#Code looks at number of black vs number of white pixels

# Step 1: Initialize the camera and capture an image
picam2 = Picamera2()

print("Starting the camera...")
picam2.start()

# Capture an initial frame
frame = picam2.capture_array()
print("Captured an image from the camera.")

# Rotate the image 90 degrees clockwise
frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
cv2.imwrite("initial_image.jpg", frame)  # Save the image to a file

# Step 2: Define regions of interest (ROIs)
print("Please select two regions of interest (ROI) in the image for the containers.")
r1 = cv2.selectROI("initial_image.jpg", frame, fromCenter=False, showCrosshair=True)
r2 = cv2.selectROI("initial_image.jpg", frame, fromCenter=False, showCrosshair=True)
print(f"Selected ROI 1: {r1}")
print(f"Selected ROI 2: {r2}")
cv2.destroyAllWindows()

# Step 3: Process the ROIs to calculate volume
def calculate_volume(roi, frame):
    # Crop the frame to the selected ROI
    roi_frame = frame[int(roi[1]):int(roi[1] + roi[3]), int(roi[0]):int(roi[0] + roi[2])]

    # Convert to grayscale for easier processing
    gray_frame = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2GRAY)

    # Threshold the image to separate liquid from the background
    _, threshold_frame = cv2.threshold(gray_frame, 127, 255, cv2.THRESH_BINARY)

    # Count the number of non-zero pixels (assuming liquid is darker and fills the region)
    non_zero_pixels = cv2.countNonZero(threshold_frame)
    total_pixels = threshold_frame.size

    # Estimate the volume as a ratio of non-zero pixels to total pixels
    volume_percentage = (non_zero_pixels / total_pixels) * 100
    print(f"Non-zero pixels: {non_zero_pixels}, Total pixels: {total_pixels}")
    print(f"Estimated volume percentage: {volume_percentage:.2f}%")

    return volume_percentage

# Calculate volume for each container
print("Processing the first container (ROI 1)...")
volume1 = calculate_volume(r1, frame)

print("Processing the second container (ROI 2)...")
volume2 = calculate_volume(r2, frame)

# Step 4: Print the estimated volumes
print(f"Estimated volume for container 1: {volume1:.2f}%")
print(f"Estimated volume for container 2: {volume2:.2f}%")

# Stop the camera
picam2.stop()
print("Camera stopped.")