from picamera2 import Picamera2
import time

camera = Picamera2()

# Lower the resolution to match the one from libcamera-hello
camera_config = camera.create_still_configuration(main={"size": (1296, 972)})
camera.configure(camera_config)

# Start the camera
camera.start()

time.sleep(2)  # Allow time for adjustment

# Capture the image and save it
camera.capture_file("/home/pi/test_image.jpg")

# Stop the camera
camera.stop()

print("Picture taken and saved as 'test_image.jpg'.")