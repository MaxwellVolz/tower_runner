import cv2
import numpy as np
import pyautogui
import time
import os


def save_image(image_np, folder="images"):
    """Save an image to a specified folder with a Unix timestamp as the filename."""
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Generate a filename with a Unix timestamp
    timestamp = str(int(time.time()))
    filename = f"{folder}/capture_{timestamp}.png"

    # Save the image to the specified folder
    cv2.imwrite(filename, image_np)

    print(f"Saved screenshot to {filename}")
    return filename


def capture_area(area):
    """Capture an image of the specified screen area and save it using save_image."""
    x, y, w, h = area
    capture = pyautogui.screenshot(region=(x, y, w, h))
    capture_np = np.array(capture)

    # Save the captured area using the new save_image function
    # capture_np_bgr = cv2.cvtColor(capture_np, cv2.COLOR_RGB2BGR)
    # save_image(capture_np_bgr)

    return cv2.cvtColor(capture_np, cv2.COLOR_BGR2RGB)


def compare_images(img1, img2, threshold=30):
    """Compare two images and return True if their difference exceeds the threshold."""
    diff = cv2.absdiff(img1, img2)
    non_zero_count = np.count_nonzero(diff)
    print(non_zero_count)
    return non_zero_count > threshold


def generate_spiral_sequence(length):
    """
    Generate a spiral sequence for a given length X.

    Args:
    - length (int): The total number of steps in the spiral.

    Returns:
    - list: A sequence of steps in the spiral.
    """
    if length < 1:
        return []

    sequence = []
    direction_count = 1  # Initial number of steps in each direction
    total_moves_made = 0  # Keep track of the total moves made

    while total_moves_made < length:
        for _ in range(4):  # Four directions: down, left, up, right
            if total_moves_made + direction_count > length:
                # Adjust the last direction count to not exceed the total length
                direction_count = length - total_moves_made
            sequence.append(direction_count)
            total_moves_made += direction_count
            if total_moves_made == length:
                break  # Stop if the desired length is reached
        direction_count += 1  # Increase the steps for the next cycle

    return sequence


print(generate_spiral_sequence(20))
