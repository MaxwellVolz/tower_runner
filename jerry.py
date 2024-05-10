import time
import keyboard

import pyautogui

from jerry_utils import (
    capture_area,
    check_for_tower,
    move_mouse,
    find_game_window,
    get_window_center,
)


# Enumeration of states for clarity
class State:
    INITIALIZING = 1
    EXPLORING_BLACK_WOODS = 2
    TOWER_DETECTED = 3


# Globals
running = False
current_state = State.INITIALIZING

# Constants
TELEPORT_HOTKEY = "w"
MINIMAP_AREA = [2420, 35, 500, 500]


def teleport():
    print(f"Jerry is teleporting! ({TELEPORT_HOTKEY})")
    keyboard.send(TELEPORT_HOTKEY)


def set_state(new_state):
    global current_state
    current_state = new_state
    print(f"State changed to: {current_state}")


def toggle_running():
    global running
    running = not running
    print(f"Jerry {'started' if running else 'stopped'}")
    capture_area(MINIMAP_AREA)


def check_starting_location():
    print("Checking starting location...")
    # Implement the check here using capture_minimap and other logic
    global current_state
    current_state = State.EXPLORING_BLACK_WOODS  # Example transition


def explore_black_woods():
    print("Exploring Black Woods...")
    # Call check_for_tower and receive tower position
    tower_found, tower_position = check_for_tower()

    if tower_found:
        enter_tower(tower_position)
        time.sleep(0.5)  # Short delay before next action
    else:
        time.sleep(0.5)
        explore_black_woods()


def enter_tower(tower_position, attempts=0):

    jerrys_aggression = 10 // (attempts + 1)  # Increase for more aggression
    print(f"Entering Tower ({jerrys_aggression})...")

    # Recursion base case
    if attempts >= 3:
        print("Maximum attempts to enter the tower reached.")
        return

    # Obtain the screen center
    screen_center_x, screen_center_y = get_window_center()

    # Calculate the target position with aggression scaling
    scaled_tower_position_x = tower_position[0] * jerrys_aggression
    scaled_tower_position_y = tower_position[1] * jerrys_aggression

    target_x = screen_center_x + scaled_tower_position_x
    target_y = screen_center_y + scaled_tower_position_y - 20

    print(f"Jerry's position: ({screen_center_x}, {screen_center_y})")
    print(f"Relative tower position to Jerry: {tower_position}")
    print(f"Absolute screen position to move towards: ({target_x}, {target_y})")

    # Moving Jerry towards the tower
    move_mouse(target_x, target_y)
    print("Jerry is teleporting to the tower...")
    teleport()
    time.sleep(0.3)  # Allow time for the screen to update

    # Check for the tower again after teleporting
    tower_found, new_tower_position = check_for_tower()

    jerrys_aggression = jerrys_aggression // 2

    scaled_tower_position_x = tower_position[0] * jerrys_aggression
    scaled_tower_position_y = tower_position[1] * jerrys_aggression

    click_target_x = screen_center_x + scaled_tower_position_x
    click_target_y = screen_center_y + scaled_tower_position_y

    move_mouse(click_target_x, click_target_y)
    print("Attempting to descend tower entrance...")
    pyautogui.click()
    time.sleep(0.1)
    pyautogui.click()

    time.sleep(1)  # Allow time for the screen to update

    # If a tower is still detected, attempt to enter it again
    if tower_found:
        print("Attempting to enter the tower again...")
        enter_tower(new_tower_position, attempts + 1)
    else:
        print("No tower detected after moving. Ending attempts.")
        toggle_running()


def main():
    print("Jerry is initialized. Press Home to start/stop.")
    # Regular Hotkeys
    keyboard.add_hotkey("home", toggle_running)

    # Debugging Hotkeys
    keyboard.add_hotkey("F1", lambda: set_state(State.INITIALIZING))
    keyboard.add_hotkey("F2", lambda: set_state(State.EXPLORING_BLACK_WOODS))
    keyboard.add_hotkey("F3", lambda: set_state(State.TOWER_DETECTED))

    # Find Game Window - TODO: Implement as check
    find_game_window("Diablo II: Resurrected")

    try:
        while True:
            time.sleep(0.1)  # Reduce CPU usage
            if running:
                if current_state == State.INITIALIZING:
                    check_starting_location()
                elif current_state == State.EXPLORING_BLACK_WOODS:
                    explore_black_woods()
                elif current_state == State.TOWER_DETECTED:
                    enter_tower()
    except KeyboardInterrupt:
        print("Stopping Jerry...")


if __name__ == "__main__":
    main()
