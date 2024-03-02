import cv2
import numpy as np
import pyautogui
import time
import os


def capture_area(area):
    """Capture and save an image of the specified screen area with a Unix timestamp."""
    x, y, w, h = area
    capture = pyautogui.screenshot(region=(x, y, w, h))
    capture_np = np.array(capture)

    # Ensure the /images folder exists
    images_folder = "images"
    if not os.path.exists(images_folder):
        os.makedirs(images_folder)

    # Generate a filename with a Unix timestamp
    timestamp = str(int(time.time()))
    filename = f"{images_folder}/capture_{timestamp}.png"

    # Save the screenshot to the /images folder
    cv2.imwrite(filename, cv2.cvtColor(capture_np, cv2.COLOR_RGB2BGR))

    print(f"Saved screenshot to {filename}")

    return cv2.cvtColor(capture_np, cv2.COLOR_BGR2RGB)


def compare_images(img1, img2, threshold=30):
    """Compare two images and return True if their difference exceeds the threshold."""
    diff = cv2.absdiff(img1, img2)
    non_zero_count = np.count_nonzero(diff)
    print(non_zero_count)
    return non_zero_count > threshold
