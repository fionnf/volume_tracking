import cv2
import numpy as np

# Load the image from a file
image_path = "training_1.png"
frame = cv2.imread(image_path)

# Rotate the image 90 degrees clockwise if needed
# frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

# Define vertical strip ROIs for two containers
print("Please select the first vertical strip ROI in the image for the first container.")
roi1 = cv2.selectROI("Select ROI 1", frame, fromCenter=False, showCrosshair=True)
print(f"Selected ROI 1: {roi1}")
cv2.destroyAllWindows()

print("Please select the second vertical strip ROI in the image for the second container.")
roi2 = cv2.selectROI("Select ROI 2", frame, fromCenter=False, showCrosshair=True)
print(f"Selected ROI 2: {roi2}")
cv2.destroyAllWindows()

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
    max_aspect_ratio = -20
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
height1 = calculate_height(roi1, frame)

print("Processing the second container (ROI 2)...")
height2 = calculate_height(roi2, frame)

# Save the marked image
cv2.imwrite("marked_image.jpg", frame)

# Display the marked image
cv2.imshow("Marked Image", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()