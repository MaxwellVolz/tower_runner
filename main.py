from pynput.mouse import Button
import cv2
import numpy as np

from keyboard import create_keyboard_listener
from mouse import create_mouse_listener
from utils import capture_area, save_image

toggle = True


def toggle_functionality():
    global toggle
    toggle = not toggle
    print(f"Functionality toggled {'on' if toggle else 'off'}")


def capture_minimap():
    if toggle:
        capture_area([2580, 220, 180, 120])


def check_for_tower(min_area_size=20):
    # Example area to capture, replace with the actual area you want to monitor
    captured_area = capture_area([2580, 220, 180, 120])

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

    found_contours = False
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > min_area_size:  # Only consider contours larger than min_area_size
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(captured_area, (x, y), (x + w, y + h), (0, 255, 0), 2)
            found_contours = True

    if not found_contours:
        print("No tower found or towers are smaller than the minimum area size.")
        return False

    # Save the processed image with rectangles around detected towers larger than min_area_size
    save_image(cv2.cvtColor(captured_area, cv2.COLOR_RGB2BGR))

    print("Processed image saved with detected areas larger than minimum area size.")
    return True


# Define key and button bindings
key_bindings = [
    ("f", toggle_functionality, (), {}),
]

button_bindings = [
    # (Button.right, capture_minimap, (), {}),
    (Button.right, check_for_tower, (), {}),
]


def main():
    # Create listeners
    keyboard_listener = create_keyboard_listener(key_bindings)
    mouse_listener = create_mouse_listener(button_bindings)

    # Use 'with' to manage listener lifecycle
    with keyboard_listener, mouse_listener:
        # Since we're using 'with', no need to manually start the listeners
        # Join the keyboard listener to block the main thread
        # Note: mouse_listener is non-blocking but managed by the 'with' context
        keyboard_listener.join()


if __name__ == "__main__":
    main()
