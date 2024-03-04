from pynput.mouse import Button
import cv2
import numpy as np
import sys


from utils.keyboard import create_keyboard_listener
from utils.mouse import create_mouse_listener
from utils.images import capture_area, save_image, compare_images
from utils.interval import IntervalThread

toggle = True
tower_check_thread = None
current_minimap = None
last_minimap = None


def toggle_functionality():
    global toggle, tower_check_thread
    toggle = not toggle
    if toggle:
        print("Functionality toggled on")
        # Start checking for the tower every 2 seconds
        if tower_check_thread is None or not tower_check_thread.is_alive():
            tower_check_thread = IntervalThread(interval=2, function=capture_minimap)
            tower_check_thread.start()
    else:
        print("Functionality toggled off")
        # Stop checking for the tower
        if tower_check_thread is not None:
            tower_check_thread.stop()
            tower_check_thread.join()  # Wait for the thread to properly exit


def capture_minimap():
    print("Capturing minimap...")
    if toggle:
        capture_area([2558, 174, 224, 224], True)


def exit_program():
    print("Spiral search completed without finding the tower.")
    sys.exit("Error message")


# Define key and button bindings
key_bindings = [
    ("f", toggle_functionality, (), {}),
    ("l", exit_program, (), {}),
    (";", capture_minimap, (), {}),
    # (";", check_for_tower, (), {}),
]

button_bindings = [
    # (Button.right, capture_minimap, (), {}),
    # (Button.right, check_for_tower, (), {}),
]


def main():
    # Create listeners
    keyboard_listener = create_keyboard_listener(key_bindings)
    mouse_listener = create_mouse_listener(button_bindings)

    # Use 'with' to manage listener lifecycle
    with keyboard_listener, mouse_listener:
        # Join the keyboard listener to block the main thread
        # Note: mouse_listener is non-blocking but managed by the 'with' context
        keyboard_listener.join()


if __name__ == "__main__":
    main()
