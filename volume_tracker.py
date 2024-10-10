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

# Step 2: Define vertical strip ROIs
print("Please select two vertical strip ROIs in the image for the containers.")
r1 = cv2.selectROI("initial_image.jpg", frame, fromCenter=False, showCrosshair=True)
r2 = cv2.selectROI("initial_image.jpg", frame, fromCenter=False, showCrosshair=True)
print(f"Selected ROI 1: {r1}")
print(f"Selected ROI 2: {r2}")
cv2.destroyAllWindows()

# Step 3: Process the ROIs to calculate the height of the liquid
def calculate_height(roi, frame):
    # Crop the frame to the selected ROI
    roi_frame = frame[int(roi[1]):int(roi[1] + roi[3]), int(roi[0]):int(roi[0] + roi[2])]

    # Convert to grayscale for easier processing
    gray_frame = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred_frame = cv2.GaussianBlur(gray_frame, (3, 3), 0)

    # Apply Canny edge detection with dynamic thresholds
    v = np.median(blurred_frame)
    lower = int(max(0, 0.4 * v))
    upper = int(min(255, 1.6 * v))
    edges = cv2.Canny(blurred_frame, lower, upper)

    # Find contours in the edge-detected image
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        print("No valid meniscus found.")
        return 0

    # Initialize variables to keep track of the most significant horizontal contour
    max_aspect_ratio = 0
    best_contour = None

    # Loop through contours and filter for horizontal lines
    for contour in contours:
        # Get the bounding rectangle of the contour
        x, y, w, h = cv2.boundingRect(contour)

        # Calculate the aspect ratio (width/height)
        aspect_ratio = w / float(h)

        # Get the minimum area rectangle (oriented) to check the angle of the contour
        rect = cv2.minAreaRect(contour)
        angle = rect[2]

        # Condition: Check if the contour is mostly horizontal
        if aspect_ratio > 2.0 and -45 <= angle <= 45:  # Aspect ratio > 5 and angle close to 0 (horizontal)
            if aspect_ratio > max_aspect_ratio:
                max_aspect_ratio = aspect_ratio
                best_contour = contour

    if best_contour is None:
        print("No valid horizontal meniscus found.")
        # Display the edge-detected image even if no contour is found
        cv2.imshow("Processed ROI (No Meniscus Detected)", edges)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return 0

    # Get the bounding box of the best (most significant horizontal) contour
    x, y, w, h = cv2.boundingRect(best_contour)

    # Calculate the height of the liquid
    height = roi[3] - y
    print(f"Height of the liquid: {height} pixels")

    # Draw a line at the meniscus (horizontal contour)
    cv2.line(frame, (roi[0], roi[1] + y), (roi[0] + roi[2], roi[1] + y), (0, 255, 0), 2)

    # Display the processed image (optional)
    cv2.imshow("Processed ROI", edges)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return height

# Calculate the height of the liquid in both containers
print("Processing the first container (ROI 1)...")
height1 = calculate_height(r1, frame)

print("Processing the second container (ROI 2)...")
height2 = calculate_height(r2, frame)

# Step 4: Estimate the volume percentage based on the height
container_height1 = r1[3]  # Total height of the selected ROI
volume_percentage1 = (height1 / container_height1) * 100
print(f"Estimated volume percentage for container 1: {volume_percentage1:.2f}%")

container_height2 = r2[3]  # Total height of the selected ROI
volume_percentage2 = (height2 / container_height2) * 100
print(f"Estimated volume percentage for container 2: {volume_percentage2:.2f}%")

# Save the marked image
cv2.imwrite("training/marked_image.jpg", frame)

# Display the marked image
cv2.imshow("Marked Image", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Stop the camera
picam2.stop()
print("Camera stopped.")