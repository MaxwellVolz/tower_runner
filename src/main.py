import keyboard
import threading
import random
import time

from camera import Camera
from darkroom import (
    scan_for_tower,
    load_image,
    find_image_on_screen,
    did_we_move,
    downsample_image,
)
from navigator import move_mouse, click_mouse

# default areas
light_radius = [950, 390, 260, 150]
minimap_area = [780, 330, 600, 300]
tower_1_area = [1100, 240, 1000, 800]
fullscreen = [0, 0, 3440, 1440]

RANDOM_WALK_STEPS = 10
TELEPORT_HOTKEY = "w"
# Options: 'random' 'spiral' 'directional'
NAVIGATION_MODE = "directional"

# Define directions for spiral and random movement
directions = {
    "bottom_left": (500, 1300),
    # "bottom": (500, 1300),
    "bottom_right": (2900, 1300),
    "right": (2900, 666),
    "top_right": (2900, 10),
    # "top": (500, 1300),
    "top_left": (500, 10),
    "left": (500, 666),
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
    num_directions = len(direction_keys)

    if blocked:
        # If blocked, choose a nearby direction randomly
        # Calculate adjacent indices assuming circular array behavior
        left_index = (current_direction_index - 1) % num_directions
        right_index = (current_direction_index + 1) % num_directions
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
            time.sleep(0.2)
            continue  # Optionally, change direction or handle the blockage

        previous_img = current_img_downsampled

        tower_coord = scan_for_tower(current_img)
        if tower_coord:
            print("Tower found, move:", tower_coord)
            stop_event.set()
            move_to_tower(tower_coord)

            time.sleep(0.5)
            tower_coord = scan_for_tower(current_img)
            move_to_tower(tower_coord)

            #  TODO: scan_for_tower is now return the coords for our next mouse move...lets handle triggering the next "phase" of our bot

            break
        time.sleep(0.4)
    print("Navigation stopped")


def background_task2(stop_event):
    print("Task 2 started")
    while not stop_event.is_set():
        # Perform long-running task here
        print("a2o")
        time.sleep(1)

    print("Task2 stopped")


def take_screenshot(area, action):
    img = game_camera.take_screenshot(area=area, save_image=True, action=action)
    print(scan_for_tower(img))


def move_to_tower(tower_coords):
    print(f"Moving towards: {tower_coords}")
    move_mouse(*tower_coords, duration=0.1)
    keyboard.send(TELEPORT_HOTKEY)


def navigate(direction):
    x, y = directions[direction]
    print(f"Navigating to {direction}...")
    move_mouse(x, y, duration=0.1)
    keyboard.send(TELEPORT_HOTKEY)


def enter_level_1():
    search_area = (800, 200, 1200, 600)
    step = 200
    x_start, y_start, width, height = search_area

    template_image = load_image("level_1.png")

    for x in range(x_start, x_start + width, step):
        for y in range(y_start, y_start + height, step):
            move_mouse(x, y, duration=0.1)
            print(f"Mouse moved to ({x}, {y})")
            time.sleep(0.1)  # Wait for the screen to stabilize if necessary
            img = game_camera.take_screenshot(
                area=tower_1_area, save_image=True, action="tower1", output_bgr=True
            )

            if find_image_on_screen(img, template_image):
                print(f"Image found near ({x}, {y})")
                # move_mouse(x, y)  # Move the mouse to the found location
                click_mouse()  # Perform the click
                return (x, y)  # Exit the function after action is taken

    print("Level 1 entrance not found. Exiting search.")
    return None


stop_event = threading.Event()

task_thread2 = threading.Thread(target=background_task2, args=(stop_event,))
task_thread2.start()

game_camera = Camera("Diablo II: Resurrected")

keyboard.add_hotkey("esc", lambda: stop_event.set())

keyboard.add_hotkey("1", take_screenshot, args=[light_radius, "adhoc_lightradius"])
keyboard.add_hotkey("2", take_screenshot, args=[minimap_area, "adhoc_minimap"])

keyboard.add_hotkey("3", take_screenshot, args=[fullscreen, "adhoc_fullscreen"])

# Navigation Controls
navigation_thread = threading.Thread(target=background_task, args=(stop_event,))

keyboard.add_hotkey("4", lambda: navigation_thread.start())
keyboard.add_hotkey("5", enter_level_1)


# Keep the main program running, otherwise python exits
keyboard.wait("esc")
