import argparse
import cv2
import os

def select_two_rois_for_images(folder_path):
    # Get a list of image files in the specified folder (you can customize the image extensions)
    image_files = [f for f in os.listdir(folder_path) if f.endswith(('.png', '.jpg', '.jpeg', '.tif', '.bmp'))]

    if not image_files:
        print("No images found in the folder.")
        return

    # Process only the first image
    image_file = image_files[0]
    image_path = os.path.join(folder_path, image_file)
    img = cv2.imread(image_path)

    if img is None:
        print(f"Error loading image {image_file}.")
        return

    # Display the image and let the user select the first ROI
    print(f"Processing {image_file}. Select the first ROI...")
    roi1 = cv2.selectROI("Select ROI 1", img)

    # If ROI selection was canceled (if all values are 0), return
    if roi1 == (0, 0, 0, 0):
        print(f"First ROI selection for {image_file} was canceled.")
        return

    # Let the user select the second ROI
    print(f"Processing {image_file}. Select the second ROI...")
    roi2 = cv2.selectROI("Select ROI 2", img)

    # If ROI selection was canceled (if all values are 0), return
    if roi2 == (0, 0, 0, 0):
        print(f"Second ROI selection for {image_file} was canceled.")
        return

    # Close the ROI selection windows
    cv2.destroyAllWindows()

    # Print the two ROIs coordinates
    print(f"ROIs for {image_file}:")
    print(f"ROI 1: x={roi1[0]}, y={roi1[1]}, width={roi1[2]}, height={roi1[3]}")
    print(f"ROI 2: x={roi2[0]}, y={roi2[1]}, width={roi2[2]}, height={roi2[3]}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Select two ROIs from the first image in the folder.")
    parser.add_argument('folder_path', type=str, help="Path to the folder containing images")
    args = parser.parse_args()

    select_two_rois_for_images(args.folder_path)