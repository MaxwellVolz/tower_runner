import cv2
import numpy as np
import pyautogui
from pynput import mouse, keyboard
import time
import pygetwindow as gw

import os

# Initialize the mouse controller for direct input
from pynput.mouse import Controller, Button
import pydirectinput

# Window to focus on
window_title = "Diablo II: Resurrected"
# Attempt to get and activate the window with the specified title
try:
    win = gw.getWindowsWithTitle(window_title)[0]
    win.activate()
    time.sleep(1)  # Wait for the window to come to the front
except IndexError:
    print(f"No window titled '{window_title}' found.")

# Toggle for enabling/disabling the functionality
toggle = True
# Flag for right-click detection
right_click_detected = False


def on_press(key):
    """Handle keyboard press events."""
    global toggle
    try:
        # Toggle functionality with 'f' key
        if key.char == "f":
            toggle = not toggle
            print(f"Functionality toggled {'on' if toggle else 'off'}")
            # TODO: do something when toggles

    except AttributeError:
        pass  # Ignore special keys


def on_click(x, y, button, pressed):
    """Handle mouse click events."""
    print(f"[{button}] [{pressed}] while toggle: [{toggle}]")

    global right_click_detected
    if button == mouse.Button.right and pressed and toggle:

        # Set flag if right-click is detected while toggled on
        capture_area([2580, 220, 180, 110])  # ultrawide - minimap
        # capture_area([0, 0, 3440, 1440]) # fullscreen
        right_click_detected = True


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


def main():
    """Main function to initialize listeners and handle the main loop."""
    global right_click_detected

    # Initialize keyboard and mouse listeners
    keyboard_listener = keyboard.Listener(on_press=on_press)
    mouse_listener = mouse.Listener(on_click=on_click)

    keyboard_listener.start()
    mouse_listener.start()

    try:
        while True:
            # Main loop placeholder for processing logic
            if toggle and right_click_detected:
                # Reset the right-click detection flag after processing
                right_click_detected = False
            time.sleep(1)  # Loop delay for responsiveness and performance balance
    except KeyboardInterrupt:
        # Graceful exit on keyboard interrupt (Ctrl+C)
        print("Program terminated by user.")


if __name__ == "__main__":
    main()
