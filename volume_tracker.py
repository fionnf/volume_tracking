import os
import cv2
import numpy as np
import time
import matplotlib.pyplot as plt

def read_calibration(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        shape = lines[0].split(':')[1].strip()
        min_volume = float(lines[1].split(':')[1].strip())
        max_volume = float(lines[2].split(':')[1].strip())
        instructions = lines[3].split(':')[1].strip()
    return shape, min_volume, max_volume, instructions

def calculate_height(roi, frame, processed_dir, filename):
    roi_frame = frame[int(roi[1]):int(roi[1] + roi[3]), int(roi[0]):int(roi[0] + roi[2])]
    gray_frame = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2GRAY)
    blurred_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0)
    v = np.median(blurred_frame)
    lower = int(max(0, 0.4 * v))
    upper = int(min(255, 1.6 * v))
    edges = cv2.Canny(blurred_frame, lower, upper)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Save the processed image with edge detection lines
    processed_image = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    cv2.drawContours(processed_image, contours, -1, (0, 255, 0), 2)
    processed_image_path = os.path.join(processed_dir, filename)
    cv2.imwrite(processed_image_path, processed_image)

    if not contours:
        return 0

    max_aspect_ratio = 0
    best_contour = None

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = w / float(h)
        rect = cv2.minAreaRect(contour)
        angle = rect[2]

        if aspect_ratio > 2.0 and -45 <= angle <= 45:
            if aspect_ratio > max_aspect_ratio:
                max_aspect_ratio = aspect_ratio
                best_contour = contour

    if best_contour is None:
        return 0

    x, y, w, h = cv2.boundingRect(best_contour)
    height = roi[3] - y
    return height

def calculate_volume(height, min_volume, max_volume, container_height, shape):
    if shape == 'cylindrical':
        return min_volume + (height / container_height) * (max_volume - min_volume)
    else:
        raise ValueError("Unsupported shape")

def process_images(directory, r1, r2, shape, min_volume, max_volume):
    volumes = []
    timestamps = []
    raw_heights = []

    # Create a subdirectory for processed images
    processed_dir = os.path.join(directory, "processed_images")
    if not os.path.exists(processed_dir):
        os.makedirs(processed_dir)

    for filename in sorted(os.listdir(directory)):
        if filename.endswith(".jpg"):
            filepath = os.path.join(directory, filename)
            frame = cv2.imread(filepath)
            timestamp = time.strptime(filename.split('.')[0], "%Y%m%d-%H%M%S")
            timestamps.append(timestamp)

            height1 = calculate_height(r1, frame, processed_dir, filename)
            height2 = calculate_height(r2, frame, processed_dir, filename)

            container_height1 = r1[3]
            volume1 = calculate_volume(height1, min_volume, max_volume, container_height1, shape)

            container_height2 = r2[3]
            volume2 = calculate_volume(height2, min_volume, max_volume, container_height2, shape)

            volumes.append((volume1, volume2))
            raw_heights.append((height1, height2))

    return timestamps, volumes, raw_heights

def save_results(timestamps, volumes, raw_heights, output_file):
    with open(output_file, 'w') as f:
        f.write("Timestamp,Height1,Height2,Volume1,Volume2,TotalVolume\n")
        for timestamp, (volume1, volume2), (height1, height2) in zip(timestamps, volumes, raw_heights):
            total_volume = volume1 + volume2
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S', timestamp)},{height1:.2f},{height2:.2f},{volume1:.2f},{volume2:.2f},{total_volume:.2f}\n")

def plot_volumes(timestamps, volumes):
    times = [time.mktime(ts) for ts in timestamps]
    volume1 = [v[0] for v in volumes]
    volume2 = [v[1] for v in volumes]
    total_volume = [v[0] + v[1] for v in volumes]

    plt.plot(times, volume1, label='Container 1')
    plt.plot(times, volume2, label='Container 2')
    plt.plot(times, total_volume, label='Total Volume')
    plt.xlabel('Time')
    plt.ylabel('Volume (mL)')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    directory = input("Enter the directory containing the images: ")
    calibration_dir = 'calibration'
    calibration_files = [f for f in os.listdir(calibration_dir) if f.endswith('.txt')]

    print("Available calibration files:")
    for i, file in enumerate(calibration_files):
        print(f"{i + 1}: {file}")

    file_index = int(input("Select the calibration file by number: ")) - 1
    calibration_file = os.path.join(calibration_dir, calibration_files[file_index])
    output_file = os.path.join(directory, "volumes.csv")

    shape, min_volume, max_volume, instructions = read_calibration(calibration_file)

    print(f"Instructions: {instructions}")

    # Select ROIs once
    sample_image = cv2.imread(os.path.join(directory, sorted(os.listdir(directory))[0]))
    r1 = cv2.selectROI("Select ROI 1", sample_image, fromCenter=False, showCrosshair=True)
    r2 = cv2.selectROI("Select ROI 2", sample_image, fromCenter=False, showCrosshair=True)
    cv2.destroyAllWindows()

    timestamps, volumes, raw_heights = process_images(directory, r1, r2, shape, min_volume, max_volume)
    save_results(timestamps, volumes, raw_heights, output_file)
    plot_volumes(timestamps, volumes)