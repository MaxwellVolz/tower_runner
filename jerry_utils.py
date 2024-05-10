import time
import os
import random

import cv2
import numpy as np
import pyautogui

import win32api as wapi

# import win32con
import win32gui


# Find the Diablo II: Resurrected window and confirm
def find_game_window(title="Diablo II: Resurrected"):
    hwnd = win32gui.FindWindow(None, title)
    if hwnd:
        print(f"Window '{title}' found, handle {hwnd}")
        return hwnd
    else:
        print(f"Window '{title}' not found.")
        return None


# Get window size
def get_window_size(hwnd):
    rect = win32gui.GetWindowRect(hwnd)
    width = rect[2] - rect[0]
    height = rect[3] - rect[1]
    return width, height


def get_window_center(hwnd=find_game_window()):
    # Use the existing function to get window size
    width, height = get_window_size(hwnd)

    # Get the window's position
    rect = win32gui.GetWindowRect(hwnd)
    top_left_x = rect[0]
    top_left_y = rect[1]

    # Calculate the center
    center_x = top_left_x + width // 2
    center_y = top_left_y + height // 2

    return center_x, center_y


# Move mouse with randomness
def move_mouse(x, y, duration=0.2):
    start_x, start_y = wapi.GetCursorPos()
    end_x, end_y = x, y
    steps = int(duration / 0.01)
    for i in range(steps):
        step_x = start_x + (end_x - start_x) * i // steps
        step_y = start_y + (end_y - start_y) * i // steps
        wapi.SetCursorPos(
            (step_x + random.randint(-5, 5), step_y + random.randint(-5, 5))
        )
        time.sleep(0.01)
    wapi.SetCursorPos((end_x, end_y))


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


def capture_area(area, plz_save=True, convert_bw=False):
    """
    Capture an image of the specified screen area and save it using save_image.

    Parameters:
    - area: Tuple of (x, y, width, height) for the capture region.
    - plz_save: Boolean indicating whether to save the captured image.
    - convert_bw: Boolean indicating whether to convert the image to black and white.
    """
    x, y, w, h = area
    capture = pyautogui.screenshot(region=(x, y, w, h))
    capture_np = np.array(capture)

    # Optionally save the captured area
    if plz_save:
        capture_np_bgr = cv2.cvtColor(capture_np, cv2.COLOR_RGB2BGR)
        save_image(capture_np_bgr)

    # Convert to grayscale if requested
    if convert_bw:
        capture_np = cv2.cvtColor(capture_np, cv2.COLOR_BGR2GRAY)

    # If not converting to BW, ensure the image is in RGB format
    else:
        capture_np = cv2.cvtColor(capture_np, cv2.COLOR_BGR2RGB)

    return capture_np


def check_for_tower(min_area_size=20):
    # Example area to capture, replace with the actual area you want to monitor
    captured_area = capture_area([2580, 220, 180, 120], False, False)
    area_height, area_width, _ = captured_area.shape

    tolerance = 40
    # rgb = [170, 70, 180]
    rgb = [170, 70, 140]

    # Define the color range for the tower
    lower = np.array([x - tolerance for x in rgb])
    upper = np.array([x + tolerance for x in rgb])

    # Create a mask to find areas within the specified color range
    mask = cv2.inRange(captured_area, lower, upper)
    kernel = np.ones((5, 5), np.uint8)

    # Process mask to improve contour detection
    mask_processed = cv2.dilate(mask, kernel, iterations=1)
    mask_processed = cv2.erode(mask_processed, kernel, iterations=1)

    # Find contours in the processed mask
    contours, _ = cv2.findContours(
        mask_processed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    center_of_area = (area_width // 2, area_height // 2)

    found_contours = False
    tower_position_relative_to_jerry = None
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > min_area_size:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(captured_area, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Calculate the center of the detected tower
            tower_center = (x + w // 2, y + h // 2)

            # Calculate the tower's position relative to Jerry
            tower_position_relative_to_jerry = (
                tower_center[0] - center_of_area[0],
                tower_center[1] - center_of_area[1],
            )

            found_contours = True
            break  # Assuming you only need the first detected tower

    if not found_contours:
        print("No tower found or towers are smaller than the minimum area size.")
        return False, None

    # Save the processed image with rectangles around detected towers larger than min_area_size
    save_image(cv2.cvtColor(captured_area, cv2.COLOR_RGB2BGR))
    print("Processed image saved with detected areas larger than minimum area size.")

    # Return True and the tower's relative position if a tower was found
    return True, tower_position_relative_to_jerry


def stitch_to_map(minimap_image):
    """Stitch the minimap image to the overall map."""
    # Placeholder for stitching code
    pass


def find_fog(map_image):
    """Find unexplored areas in the map."""
    # Placeholder for fog finding code
    pass


def move_jerry(direction):
    """Move Jerry in a given direction."""
    # Placeholder for movement code
    pass


def image_match(image, template):
    """Match a template image within another image."""
    # Placeholder for image matching code
    pass
