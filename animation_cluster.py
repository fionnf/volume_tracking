import os
import cv2
import numpy as np
import time
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

CREATE_ANIMATIONS = True

def read_calibration(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        shape = lines[0].split(':')[1].strip()
        min_volume = float(lines[1].split(':')[1].strip())
        max_volume = float(lines[2].split(':')[1].strip())
        instructions = lines[3].split(':')[1].strip()
    return shape, min_volume, max_volume, instructions

def calculate_height(roi, frame, processed_dir, blur_dir, filename):
    roi_frame = frame[int(roi[1]):int(roi[1] + roi[3]), int(roi[0]):int(roi[0] + roi[2])]
    gray_frame = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2GRAY)
    _, binary_frame = cv2.threshold(gray_frame, 30, 255, cv2.THRESH_BINARY)
    blurred_frame = cv2.GaussianBlur(binary_frame, (55, 5), 0)

    blur_image_path = os.path.join(blur_dir, filename)
    cv2.imwrite(blur_image_path, blurred_frame)

    v = np.median(blurred_frame)
    lower = int(max(0, 0.4 * v))
    upper = int(min(255, 1.6 * v))
    edges = cv2.Canny(blurred_frame, lower, upper)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    processed_image = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    cv2.drawContours(processed_image, contours, -1, (0, 255, 0), 2)
    processed_image_path = os.path.join(processed_dir, filename)
    cv2.imwrite(processed_image_path, processed_image)

    if not contours:
        return 0

    contours = sorted(contours, key=lambda c: cv2.boundingRect(c)[1])
    longest_contour = None
    max_length = 0

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = w / float(h)

        if aspect_ratio > 2.0:
            length = cv2.arcLength(contour, True)
            if length > max_length:
                max_length = length
                longest_contour = contour

    if longest_contour is None:
        return 0

    x, y, w, h = cv2.boundingRect(longest_contour)
    height = roi[3] - y
    return height

def remove_outliers_and_interpolate(volumes, threshold=2):
    volumes = np.array(volumes)
    volumes[volumes > 7] = np.nan

    mean_volume = np.nanmean(volumes)
    std_volume = np.nanstd(volumes)
    z_scores = (volumes - mean_volume) / std_volume

    outliers = np.abs(z_scores) > threshold
    clean_volumes = volumes.copy()
    clean_volumes[outliers] = np.nan

    clean_volumes = pd.Series(clean_volumes).interpolate().to_numpy()
    return clean_volumes

def process_images(directory, r1, r2, shape, min_volume, max_volume):
    volumes = []
    timestamps = []
    raw_heights = []
    frames = []

    processed_dir = os.path.join(directory, "processed_images")
    blur_dir = os.path.join(directory, "blur_images")
    container1_processed_dir = os.path.join(processed_dir, "container1")
    container2_processed_dir = os.path.join(processed_dir, "container2")
    container1_blur_dir = os.path.join(blur_dir, "container1")
    container2_blur_dir = os.path.join(blur_dir, "container2")

    for dir_path in [processed_dir, blur_dir, container1_processed_dir, container2_processed_dir, container1_blur_dir,
                     container2_blur_dir]:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    for filename in sorted(os.listdir(directory)):
        if filename.endswith(".jpg"):
            filepath = os.path.join(directory, filename)
            frame = cv2.imread(filepath)
            frames.append(frame)
            timestamp = time.strptime(filename.split('.')[0], "%Y%m%d-%H%M%S")
            timestamps.append(timestamp)

            height1 = calculate_height(r1, frame, container1_processed_dir, container1_blur_dir, filename)
            height2 = calculate_height(r2, frame, container2_processed_dir, container2_blur_dir, filename)

            container_height1 = r1[3]
            container_height2 = r2[3]

            volume1 = calculate_volume(height1, min_volume, max_volume, container_height1, shape)
            volume2 = calculate_volume(height2, min_volume, max_volume, container_height2, shape)

            volumes.append((volume1, volume2))
            raw_heights.append((height1, height2))

    volume1_list = [v[0] for v in volumes]
    volume2_list = [v[1] for v in volumes]

    clean_volume1 = remove_outliers_and_interpolate(volume1_list)
    clean_volume2 = remove_outliers_and_interpolate(volume2_list)

    cleaned_volumes = list(zip(clean_volume1, clean_volume2))
    return timestamps, cleaned_volumes, raw_heights, frames

def calculate_volume(height, min_volume, max_volume, container_height, shape):
    if shape == 'cylindrical':
        return min_volume + (height / container_height) * (max_volume - min_volume)
    else:
        raise ValueError("Unsupported shape")

def save_results(timestamps, volumes, raw_heights, output_file):
    with open(output_file, 'w') as f:
        f.write("Timestamp,Height1,Height2,Volume1,Volume2,TotalVolume\n")
        for timestamp, (volume1, volume2), (height1, height2) in zip(timestamps, volumes, raw_heights):
            total_volume = volume1 + volume2
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S', timestamp)},{height1:.2f},{height2:.2f},{volume1:.2f},{volume2:.2f},{total_volume:.2f}\n")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Process volume tracking images.")
    parser.add_argument('--directory', required=True, help="Directory containing the images")
    parser.add_argument('--calibration', required=True, help="Calibration file path")
    parser.add_argument('--r1', type=int, nargs=4, required=True, help="ROI 1 coordinates: x y width height")
    parser.add_argument('--r2', type=int, nargs=4, required=True, help="ROI 2 coordinates: x y width height")

    args = parser.parse_args()

    shape, min_volume, max_volume, instructions = read_calibration(args.calibration)

    timestamps, volumes, raw_heights, frames = process_images(args.directory, args.r1, args.r2, shape, min_volume, max_volume)
    output_file = os.path.join(args.directory, "volumes.csv")
    save_results(timestamps, volumes, raw_heights, output_file)

    print(f"Results saved to {output_file}")