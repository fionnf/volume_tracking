# RFB Volume Tracking System

This project is designed to track the volume of liquids in containers using images captured by a Raspberry Pi Zero 2 W with a camera module attached. The system involves two main components:
1. **Capture Script** (`pi-camera.py`): A script that runs on the Raspberry Pi, responsible for capturing images at regular intervals and uploading them to a Git repository.
2. **Processing Script** (`volume_tracker.py`): A script that runs on your computer, which processes the captured images to determine the liquid volumes, plot them, create a CSV, and an animation too!

## Table of Contents

- Project Overview
- Hardware Requirements
- Software Requirements
- Capture Script
- Processing Script
- Camera Tuning Script
- Usage Instructions
- Troubleshooting

## Hardware Requirements

- Raspberry Pi Zero 2 W (or any other Raspberry Pi)
- Camera module (e.g., Pi Camera)
- Home computer for processing images

## Software Requirements

To run the scripts, you need to install the following dependencies:

**Raspberry Pi (for capture script):**
- `picamera2`
- `opencv-python`
- `git`
- `shutil`

**Home Computer (for processing script):**
- `opencv-python`
- `matplotlib`
- `pillow`

## `pi-camera.py`

This script runs on the Raspberry Pi and is responsible for capturing images and managing disk usage. Key features include:

- Capturing images at regular, user-defined intervals.
- Automatically saving images and metadata to a specified directory.
- Uploading captured images to a Git repository.
- Managing disk space by automatically deleting local images after successful uploads.
- Creating a `metadata.csv` file and updating a `README` in the output directory.

### Usage Instructions:

1. SSH into the Raspberry Pi:

   ```bash
   ssh pi@<your_pi_ip>  # You can get the IP by running ifconfig on the Pi