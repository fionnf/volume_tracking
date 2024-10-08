import cv2

# Initialize the camera
vc = cv2.VideoCapture(0)

# Check if the camera is opened correctly
if not vc.isOpened():
    print("Error: Could not open camera.")
    exit()

# Main loop to capture and display the video feed
while True:
    rval, frame = vc.read()  # Capture frame-by-frame
    if not rval:
        print("Error: Could not read frame.")
        break

    # Display the resulting frame
    cv2.imshow("Camera Feed", frame)

    # Exit on ESC key
    key = cv2.waitKey(20)
    if key == 27:  # ESC key
        break

# Clean up
vc.release()
cv2.destroyAllWindows()