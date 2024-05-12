import keyboard
import threading
import random
import time

from camera import Camera
from darkroom import scan_for_tower
from navigator import move_mouse

# default areas
light_radius = [960, 400, 240, 130]
minimap_area = [780, 330, 600, 300]

RANDOM_WALK_STEPS = 10
TELEPORT_HOTKEY = "w"


def background_task(stop_event):
    step_count = 0
    directions = ["bottom_left", "bottom_right", "top_left", "top_right"]
    while not stop_event.is_set():
        if step_count < RANDOM_WALK_STEPS:
            # Select a random direction from available directions
            direction = random.choice(directions)
            navigate(direction)
            img = game_camera.take_screenshot(
                area=light_radius, save_image=True, action="adhoc_lightradius"
            )
            tower_coord = scan_for_tower(img)
            if tower_coord:
                print("Tower found at:", tower_coord)
                stop_event.set()
                break
            step_count += 1
        else:
            step_count = 0  # Reset step count after 10 steps
        time.sleep(1)  # Simulate time delay between moves
    print("Navigation stopped")


def background_task2(stop_event):
    print("Task 2 started")
    while not stop_event.is_set():
        # Perform long-running task here
        print("a2o")
        time.sleep(1)

    # TODO: Cleanup
    print("Task2 stopped")


def take_screenshot(area, action):
    img = game_camera.take_screenshot(area=area, save_image=True, action=action)
    print(scan_for_tower(img))


def navigate(direction):
    # Define mouse positions for diagonal movements
    positions = {
        "bottom_left": (500, 1200),
        "bottom_right": (2900, 1200),
        "top_left": (500, 160),
        "top_right": (2900, 160),
    }

    # Get the specified direction's coordinates
    x, y = positions[direction]

    print(f"Navigating to {direction}...")

    # Move mouse to the specified diagonal position
    move_mouse(x, y, duration=0.1)
    keyboard.send(TELEPORT_HOTKEY)


stop_event = threading.Event()

task_thread2 = threading.Thread(target=background_task2, args=(stop_event,))
task_thread2.start()

game_camera = Camera("Diablo II: Resurrected")

keyboard.add_hotkey("esc", lambda: stop_event.set())

keyboard.add_hotkey("1", take_screenshot, args=[light_radius, "adhoc_lightradius"])
keyboard.add_hotkey("2", take_screenshot, args=[minimap_area, "adhoc_minimap"])

# Navigation Controls
navigation_thread = threading.Thread(target=background_task, args=(stop_event,))
keyboard.add_hotkey("3", lambda: navigation_thread.start())

# Keep the main program running, otherwise python exits
keyboard.wait("esc")
