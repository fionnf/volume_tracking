import cv2
import os
import gc


# Function to capture a single image and process it
def capture_image_and_process():
    # Open the camera using the V4L2 backend (bypass GStreamer)
    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

    # Set a lower resolution to save memory
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    # Capture a single frame
    ret, frame = cap.read()

    if ret:
        # Convert to grayscale to reduce memory usage
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Optionally resize the frame for further memory optimization
        resized_frame = cv2.resize(gray_frame, (160, 120))

        # Save the captured image to the current directory
        save_path = "captured_image.jpg"
        cv2.imwrite(save_path, resized_frame)
        print(f"Image saved at {save_path}")

    else:
        print("Error: Could not capture image.")

    # Release the camera and clean up
    cap.release()
    gc.collect()  # Force garbage collection to free up memory


# Main function to trigger image capture
if __name__ == "__main__":
    capture_image_and_process()