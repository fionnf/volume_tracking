from picamera2 import Picamera2
import cv2
import numpy as np
import time

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

# Step 2: Define vertical strip ROIs for height measurement
print("Please select the first vertical strip ROI in the image for the first container.")
roi1 = cv2.selectROI("initial_image.jpg", frame, fromCenter=False, showCrosshair=True)
roi1 = (roi1[0], roi1[1], 20, roi1[3])
print(f"Selected ROI 1: {roi1}")

print("Please select the second vertical strip ROI in the image for the second container.")
roi2 = cv2.selectROI("initial_image.jpg", frame, fromCenter=False, showCrosshair=True)
roi2 = (roi2[0], roi2[1], 20, roi2[3])
print(f"Selected ROI 2: {roi2}")
cv2.destroyAllWindows()

# Step 3: Process the ROIs to calculate the height of the liquid and mark the threshold
def calculate_height_and_mark(roi, frame):
    # Crop the frame to the selected ROI
    roi_frame = frame[int(roi[1]):int(roi[1] + roi[3]), int(roi[0]):int(roi[0] + roi[2])]

    # Convert to grayscale for easier processing
    gray_frame = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2GRAY)

    # Threshold the image to separate liquid from the background
    _, threshold_frame = cv2.threshold(gray_frame, 127, 255, cv2.THRESH_BINARY)

    # Find the contours of the thresholded image
    contours, _ = cv2.findContours(threshold_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Calculate the height of the liquid based on the contours
    if contours:
        # Assume the largest contour is the liquid
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        cv2.rectangle(frame, (roi[0], roi[1] + y), (roi[0] + w, roi[1] + y + h), (0, 255, 0), 2)
        print(f"Height of the liquid: {h} pixels")
        return h
    else:
        print("No liquid detected.")
        return 0

# Calculate the height of the liquid in both containers
print("Processing the first container...")
liquid_height1 = calculate_height_and_mark(roi1, frame)

print("Processing the second container...")
liquid_height2 = calculate_height_and_mark(roi2, frame)

# Step 4: Estimate the volume percentage based on the height
container_height1 = roi1[3]  # Total height of the selected ROI
volume_percentage1 = (liquid_height1 / container_height1) * 100
print(f"Estimated volume percentage for container 1: {volume_percentage1:.2f}%")

container_height2 = roi2[3]  # Total height of the selected ROI
volume_percentage2 = (liquid_height2 / container_height2) * 100
print(f"Estimated volume percentage for container 2: {volume_percentage2:.2f}%")

# Save the marked image
cv2.imwrite("marked_image.jpg", frame)

# Display the marked image
cv2.imshow("Marked Image", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Stop the camera
picam2.stop()
print("Camera stopped.")