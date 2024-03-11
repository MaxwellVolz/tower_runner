import cv2
import numpy as np
import pyautogui
import time
import os


def save_image(image_np, folder="./images"):
    # Save an image with timestamp filename
    abs_folder_path = os.path.abspath(folder)

    if not os.path.exists(abs_folder_path):
        os.makedirs(abs_folder_path)

    # Generate a filename with a Unix timestamp
    timestamp = str(int(time.time()))
    filename = f"{abs_folder_path}/capture_{timestamp}.png"

    # Save the image to the specified folder
    cv2.imwrite(filename, image_np)

    print(f"Saved screenshot: {filename}")
    return filename


def capture_area(area, plz_save=True):
    """Capture an image of the specified screen area and save it using save_image."""
    x, y, w, h = area
    capture = pyautogui.screenshot(region=(x, y, w, h))
    capture_np = np.array(capture)

    # Save the captured area using the new save_image function
    if plz_save:
        capture_np_bgr = cv2.cvtColor(capture_np, cv2.COLOR_RGB2BGR)
        save_image(capture_np_bgr)

    return cv2.cvtColor(capture_np, cv2.COLOR_BGR2RGB)


def compare_images(img1, img2, threshold=30):
    """Compare two images and return True if their difference exceeds the threshold."""
    diff = cv2.absdiff(img1, img2)
    non_zero_count = np.count_nonzero(diff)
    print(non_zero_count)
    return non_zero_count > threshold
