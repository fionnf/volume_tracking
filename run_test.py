from picamera2 import Picamera2
import time

# Initialize the camera
camera = Picamera2()

# Configure the camera
camera_config = camera.create_still_configuration()
camera.configure(camera_config)

# Start the camera
camera.start()

# Allow the camera to warm up
time.sleep(2)

# Capture an image and save it
image_path = '/home/pi/Desktop/captured_image.jpg'
camera.capture_file(image_path)

# Stop the camera
camera.stop()

print(f"Image captured and saved at {image_path}")

