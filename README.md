# RFB Volume Tracking System

This project is designed to track the volume of liquids in containers using images captured by a Raspberry Pi Zero 2 W with a camera module attached. The system involves two main components:
	1.	Capture Script (pi-camera.py): A script that runs on the Raspberry Pi, responsible for capturing images at regular intervals and uploading them to a Git repository.
	2.	Processing Script (volume_tracker.py): A script that runs on your computer, which processes the captured images to determine the liquid volumes, plot them, make a csv and an animation too!

## Table of Contents

	•	Project Overview
	•	Hardware Requirements
	•	Software Requirements
	•	Capture Script
	•	Processing Script
	•	Camera Tuning Script
	•	Usage Instructions
	•	Troubleshooting

## Hardware Requirements

	•	Raspberry Pi Zero 2 W (or any other Raspberry Pi)
	•	Camera module (e.g., Pi Camera)
	•	Home computer for processing images

## Software Requirements
To run the scripts, you need to install the following dependencies:

	Raspberry Pi (for capture script):
	•	picamera2
	•	opencv-python
	•	git
	•	shutil
	Home Computer (for processing script):
	•	opencv-python
	•	matplotlib
	•	pillow

## pi-camera.py

This script runs on the Raspberry Pi and is responsible for capturing images and managing disk usage. Key features include:

	•	Capturing images at regular, user-defined intervals.
	•	Automatically saving images and metadata to a specified directory.
	•	Uploading captured images to a Git repository.
	•	Managing disk space by automatically deleting local images after successful uploads.
	•	Creating a metadata.csv file and updating a README in the output directory.

Usage Instructions:

	1.	SSH into the Raspberry Pi:

ssh pi@<your_pi_ip> (you can get the ip by running ifconfig on the pi)

	2.	Run the capture script in the background:

nohup python3 pi-camera.py > output.log 2>&1 &

This will run the script even after the SSH session is closed. The log output will be stored in output.log.

	3.	To stop the script, find the process ID (PID) using the command:

ps -ef | grep pi-camera.py

And terminate the process using:

kill <PID>

The script checks disk usage and deletes the oldest images if the disk usage exceeds a specified threshold.

## volume_tracker.py

This script runs on your home computer and processes the captured images to estimate the volumes in the containers. It performs the following tasks:

	•	Loads the images captured by the Raspberry Pi.
	•	Allows the user to select regions of interest (ROIs) for the two containers in the first image.
	•	Analyzes the height of the liquid in the containers using computer vision techniques.
	•	Converts the height data into volume estimates based on calibration data.
	•	Saves the timestamps, volume estimates, and raw height data to a CSV file.
	•	Optionally creates a time-lapse animation showing the container images along with volume annotations.

Steps:

	1.	Copy the images from the Raspberry Pi’s Git repository to your local machine.
	2.	Run the script:

python volume_tracker.py

The script will prompt you to select the directory containing the images and choose a calibration file for volume estimation. It will also allow you to manually select the regions of interest for volume calculation.

	3.	Once the analysis is done, the results (timestamps, volumes, heights) will be saved in a CSV file, and a time-lapse GIF will be generated.

## camera_tune.py

This script allows you to adjust and test the camera settings on the Raspberry Pi. It starts a live feed from the camera and displays it using OpenCV. You can manually tune the settings and see the real-time output.

To run the script:

    1.	SSH into the Raspberry Pi with X11 forwarding enabled: ssh -X pi@<your_pi_ip>
    2.	Run the script: python3 camera_tune.py
    3.	Adjust the camera settings using the trackbars.
    4.  Press q to stop the live feed.

## License

This project is licensed under the MIT License.
