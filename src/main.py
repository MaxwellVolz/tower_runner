import keyboard
import threading
import random
import time

from camera import Camera
from darkroom import scan_for_tower, did_we_move, downsample_image
from navigator import move_mouse

# default areas
light_radius = [960, 400, 240, 130]
minimap_area = [780, 330, 600, 300]

RANDOM_WALK_STEPS = 10
TELEPORT_HOTKEY = "w"
# Options: 'random' 'spiral' 'directional'
NAVIGATION_MODE = "directional"

# Define directions for spiral and random movement
directions = {
    "bottom_left": (500, 1300),
    "bottom_right": (2900, 1300),
    "top_left": (500, 10),
    "top_right": (2900, 10),
}
direction_keys = list(directions.keys())

# Spiral Navigation Variables
spiral_step_size = 1
spiral_direction_index = 0
spiral_steps_count = 0

previous_img = None


def spiral_search():
    global spiral_step_size, spiral_direction_index, spiral_steps_count
    direction = direction_keys[spiral_direction_index]

    # Check if it's time to change the direction
    spiral_steps_count += 1
    if spiral_steps_count == spiral_step_size:
        spiral_direction_index = (spiral_direction_index + 1) % 4
        spiral_steps_count = 0
        if spiral_direction_index % 2 == 0:
            spiral_step_size += 1

    return direction


current_direction_index = 0


def directional_search(blocked):
    global current_direction_index
    if blocked:
        # If blocked, choose a nearby direction randomly
        # Calculate adjacent indices assuming circular array behavior
        left_index = (current_direction_index - 1) % 4
        right_index = (current_direction_index + 1) % 4
        # Randomly choose either left or right adjacent direction
        current_direction_index = random.choice([left_index, right_index])
        print(
            f"Blocked, changing direction to {direction_keys[current_direction_index]}"
        )
    else:
        print(f"Continuing in direction {direction_keys[current_direction_index]}")

    return direction_keys[current_direction_index]


def background_task(stop_event):
    global previous_img
    blocked = False  # To track if movement was blocked

    while not stop_event.is_set():
        if NAVIGATION_MODE == "random":
            direction = random.choice(direction_keys)
        elif NAVIGATION_MODE == "spiral":
            direction = spiral_search()
        elif NAVIGATION_MODE == "directional":
            direction = directional_search(blocked)
            blocked = False
        else:
            raise ValueError("Invalid navigation mode")

        navigate(direction)

        time.sleep(0.3)
        current_img = game_camera.take_screenshot(
            area=light_radius, save_image=True, action="adhoc_lightradius"
        )

        # Downsample the current image before comparison
        current_img_downsampled = downsample_image(current_img)

        # Check movement using the downscaled images
        if previous_img is not None and not did_we_move(
            current_img_downsampled, previous_img
        ):
            print("Movement blocked, attempting another direction...")
            blocked = True
            time.sleep(1)
            continue  # Optionally, change direction or handle the blockage

        previous_img = current_img_downsampled

        tower_coord = scan_for_tower(current_img)
        if tower_coord:
            print("Tower found at:", tower_coord)
            stop_event.set()
            break
        time.sleep(1)
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
    x, y = directions[direction]
    print(f"Navigating to {direction}...")
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
