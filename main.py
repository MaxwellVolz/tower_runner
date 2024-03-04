from pynput.mouse import Button
import cv2
import numpy as np
import pyautogui
import time
import random
import math
import sys


from keyboard import create_keyboard_listener
from mouse import create_mouse_listener
from utils import capture_area, save_image, compare_images
from interval import IntervalThread

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
            tower_check_thread = IntervalThread(interval=2, function=check_for_tower)
            tower_check_thread.start()
    else:
        print("Functionality toggled off")
        # Stop checking for the tower
        if tower_check_thread is not None:
            tower_check_thread.stop()
            tower_check_thread.join()  # Wait for the thread to properly exit


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


def spiral_teleport(iterations=30, angle_of_turn=60, run_duration=1):
    """
    Perform a spiral teleportation movement.

    Args:
    - iterations (int): Number of iterations to perform.
    - angle_of_turn (float): Angle of turn in degrees for each iteration.
    - run_duration (float): Duration to hold the mouse movement in seconds.
    """
    screen_width, screen_height = pyautogui.size()
    # Calculate start position at 80% of screen height from the bottom and centered horizontally
    start_x = screen_width // 2
    start_y = int(
        screen_height * 0.8
    )  # Start from the bottom (90% to be within 80% boundary)

    # Move mouse to start position
    pyautogui.moveTo(start_x, start_y)
    time.sleep(1)  # Pause for the movement to finish

    for _ in range(iterations):
        pyautogui.press("w")  # Simulate teleport
        pyautogui.mouseDown()  # Start holding left click

        # Calculate the end position based on the angle of turn
        angle_radians = math.radians(
            angle_of_turn
        )  # Convert angle to radians for calculation
        end_x = start_x + (
            math.cos(angle_radians) * 100
        )  # Example movement distance is set to 100 pixels
        end_y = start_y - (math.sin(angle_radians) * 100)  # Adjust based on the angle

        # Move mouse in the specified direction for the duration
        pyautogui.moveTo(end_x, end_y, duration=run_duration)

        pyautogui.mouseUp()  # Release left click

        # Update start position for the next iteration
        start_x, start_y = end_x, end_y


def smart_teleport(iterations=10):
    global current_minimap
    global last_minimap

    screen_width, screen_height = pyautogui.size()

    # Define corners with some predefined positions
    mouse_positions = [
        (screen_width * 0.8, screen_height * 0.2),  # Top right
        # Add more corners as needed
    ]
    random.shuffle(mouse_positions)  # Randomize the order of corners

    last_minimap = capture_minimap()

    for _ in range(iterations):
        for corner in mouse_positions:
            if check_for_tower():
                print("Tower found, exiting...")
                return

            # Adding randomness to the mouse position for a "human-like" effect
            target_x = int(corner[0] + random.uniform(-10, 10))
            target_y = int(corner[1] + random.uniform(-10, 10))

            # Simulate the teleportation sequence
            pyautogui.moveTo(target_x, target_y, duration=0.2)
            pyautogui.mouseDown()
            pyautogui.press("w")
            time.sleep(0.5)  # Hold the button for a short duration
            pyautogui.mouseUp()

            current_minimap = capture_minimap()
            print("comparing inc....")

            if compare_images(current_minimap, last_minimap, threshold=30):
                last_minimap = current_minimap
                continue  # If the minimap has changed significantly, continue
            else:
                print("breaking")
                break  # If there's no significant change, break the loop

            # time.sleep(1)  # Wait for a bit before the next iteration


def exit_program():
    print("Spiral search completed without finding the tower.")
    sys.exit("Error message")


# Define key and button bindings
key_bindings = [
    ("f", toggle_functionality, (), {}),
    ("l", exit_program, (), {}),
    # (";", spiral_teleport, (), {}),
    (";", smart_teleport, (), {}),
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
        # Since we're using 'with', no need to manually start the listeners
        # Join the keyboard listener to block the main thread
        # Note: mouse_listener is non-blocking but managed by the 'with' context
        keyboard_listener.join()


if __name__ == "__main__":
    main()
