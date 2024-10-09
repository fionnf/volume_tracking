# Volume Tracking in Two Containers - Strategy

This document outlines the steps to implement a basic volume tracking system using a camera. The objective is to capture images of two containers, define regions of interest (ROIs), and calculate the estimated volume of liquid in each container based on image processing.

## 1. Setting Up `picamera2` for Image Capture

We will use the `picamera2` library to capture images from the Raspberry Pi camera. The following steps will guide you through initializing the camera and capturing images for further processing.

### Steps:
1. Initialize the `picamera2` camera.
2. Capture a frame and display it to the user.

## 2. Defining Regions of Interest (ROIs)

The user will manually select two regions of interest (ROIs) in the captured image, corresponding to the areas of the containers whose volume we want to track. This will be done using OpenCV's `selectROI()` function.

### Steps:
1. Display the captured frame to the user.
2. Use `cv2.selectROI()` to let the user select two regions: one for each container.
3. Print the coordinates of the selected ROIs for debugging purposes.

## 3. Calculating the Volume Based on Pixel Count

The volume in each container will be estimated based on the number of non-zero (filled) pixels in the defined ROIs. This method assumes that the liquid is darker than the background, and thresholding can separate the liquid from the rest of the image.

### Steps:
1. Convert the ROI to grayscale to simplify image processing.
2. Apply thresholding to create a binary image, where the liquid is represented by non-zero pixels.
3. Count the number of non-zero pixels and calculate the ratio of non-zero pixels to the total pixels in the ROI. This will provide an estimate of the volume percentage.

