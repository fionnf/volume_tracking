from picamera2 import Picamera2
import time

# Initialize the camera
camera = Picamera2()

# Configure the camera
camera_config = camera.create_still_configuration()
camera.configure(camera_config)

# Start the camera
camera.start()

# Sleep to allow camera adjustment
time.sleep(2)

# Capture the image and save it
camera.capture_file("/home/pi/image.jpg")

# Stop the camera
camera.stop()

print("Picture taken and saved as 'image.jpg'.")