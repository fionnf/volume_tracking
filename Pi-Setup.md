# Raspberry Pi Image Capture and Upload Guide

This guide walks you through setting up a Raspberry Pi to capture images at intervals, store them locally, and upload them to GitHub.

## Table of Contents

	1.	Raspberry Pi OS Installation
	2.	Connecting to Eduroam Wi-Fi
	3.	Initial Setup and Updates
	4.	Enable SSH for Headless Access
	5.	Enable the Camera
	6.	Install Required Packages
	7.	Set Up Git and GitHub SSH
	8.	Running the Script

1. **Raspberry Pi OS Installation**

	1.	Download Raspberry Pi Imager: Visit the Raspberry Pi website and download the Raspberry Pi Imager tool.
	2.	Insert the SD Card into your computer.
	3.	Open Raspberry Pi Imager and:
	•	Choose the OS: Select Raspberry Pi OS (32-bit).
	•	Choose Storage: Select the SD card.
	•	(Optional) Set up SSH, Wi-Fi, and user settings in the “Advanced options” (press Ctrl+Shift+X).
	4.	Write to the SD Card and wait for the process to complete.
	5.	Insert the SD Card into your Raspberry Pi and boot it up.

2. **Connecting to Eduroam Wi-Fi**

	1.	On the first boot, connect the Raspberry Pi to the Eduroam Wi-Fi network. This step is necessary to connect to the network and set up the Pi for headless access afterward.
	2.	Go to the Wi-Fi settings on your Raspberry Pi and select Eduroam.
	3.	Use the following settings:
	•	Anonymous Identity: Leave this field blank.
	•	CA Certificate: Tick No certificate is required.
	•	Domain: Set to rug.nl.
	•	Username: Enter your Eduroam username (usually in the format username@rug.nl).
	•	Password: Enter your Eduroam password.
	4.	Once connected, you can proceed to set up the Raspberry Pi for headless access, allowing you to SSH into it from another device.

3. **Initial Setup and Updates**

	1.	Complete the Raspberry Pi Setup: Follow the on-screen instructions to set up your locale, timezone, and network.
	2.	Open a Terminal (found in the main menu under Accessories).
	3.	Update the system to ensure all packages are up-to-date:

sudo apt update
sudo apt upgrade -y



4. **Enable SSH for Headless Access**

	1.	Enable SSH:
	•	You can enable SSH through the Raspberry Pi Configuration tool:
	•	Open the Raspberry Pi menu, go to Preferences, then Raspberry Pi Configuration.
	•	Go to the Interfaces tab and enable SSH.
	•	Alternatively, you can enable SSH from the terminal:

sudo raspi-config

	•	Select Interface Options.
	•	Select SSH and choose Yes to enable.

	2.	Find the IP Address of the Raspberry Pi:
	•	In the terminal, run:

hostname -I


	•	Note the IP address, which you will use to SSH into the Raspberry Pi from another device.

	3.	Connect via SSH from Another Computer:
	•	On your computer (Mac/Linux), open a terminal. For Windows, use a tool like PuTTY or Windows Terminal.
	•	Enter the following command, replacing <RaspberryPiIP> with the IP address of your Raspberry Pi:

ssh pi@<RaspberryPiIP>


	•	The default username is pi, and the default password is raspberry (if you haven’t changed it).
	•	You should now be connected to your Raspberry Pi via SSH and can operate it headlessly.

5. **Enable the Camera**

	1.	Check if the camera works by trying to capture an image:

raspistill -o test.jpg

If this command returns an error, proceed to the next steps to enable the camera.

	2.	Enable the Legacy Camera:
	•	Open the Raspberry Pi configuration file:

sudo nano /boot/config.txt


	•	Add the following line at the end of the file:

start_x=1
gpu_mem=128


	•	Press Ctrl+X, then Y, and Enter to save and exit.
	•	Reboot the Raspberry Pi:

sudo reboot


	3.	Check the camera again after rebooting:

raspistill -o test.jpg

If the file test.jpg is created without errors, the camera is working.

6. **Install Required Packages**

In your terminal, install the necessary packages using the following commands:

sudo apt install python3-picamera2 -y
sudo apt install python3-opencv -y
sudo apt install git -y
sudo apt install python3-shutil -y

7. **Set Up Git and GitHub SSH**

	1.	Configure Git:
	•	Set up your Git user information:

git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"


	2.	Create an SSH Key:
	•	Generate an SSH key to authenticate with GitHub:

ssh-keygen -t rsa -b 4096 -C "your.email@example.com"


	•	When prompted, press Enter to accept the default location and optionally add a passphrase.

	3.	Add the SSH Key to GitHub:
	•	Display the SSH key:

cat ~/.ssh/id_rsa.pub


	•	Copy the output and go to GitHub SSH settings to add it to your account. Paste the key in the “Key” field and give it a title.

	4.	Verify the SSH Connection:
	•	Test your connection to GitHub:

ssh -T git@github.com


	•	You should see a message welcoming you to GitHub.

8. **Running the Script**

	1.	Transfer the Script to the Raspberry Pi: Save the Python script (pi-camera.py) in a directory on your Raspberry Pi.
	2.	Make the Script Executable:

chmod +x pi-camera.py


	3.	Run the Script:
	•	Start the script in the background to keep it running even if the SSH session is closed:

nohup python3 pi-camera.py <experiment_name> <image_interval> > output.log 2>&1 &

Replace <experiment_name> with your experiment name and <image_interval> with the capture interval in seconds.

	4.	Monitor the Output:
	•	The script output is written to output.log. You can view it with:

tail -f output.log


	5.	Stopping the Script:
	•	Find the process ID (PID) of the script:

ps -ef | grep pi-camera.py


	•	Kill the process with:

kill <PID>


