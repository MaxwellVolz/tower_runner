import win32api as wapi
import win32con
import win32gui
import time
import random


# Find the Diablo II: Resurrected window and confirm
def find_game_window(title):
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


# Calculate movement offsets
def calculate_offsets(width, height, offset=200):
    center_h = (height // 2) - 100
    center_w = width // 2
    return {
        "Top-Left": (offset, offset),
        "Bottom-Left": (offset, height - offset),
        "Top-Right": (width - offset, offset),
        "Bottom-Right": (width - offset, height - offset),
        "Top": (center_w, center_h - 400),
        "Bottom": (center_w, center_h + 300),
        "Right": (center_w + 600, center_h),
        "Left": (center_w - 600, center_h),
    }


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


# Press key
def press_key(key="W"):
    wapi.keybd_event(ord(key), 0, 0, 0)
    time.sleep(0.05)
    wapi.keybd_event(ord(key), 0, win32con.KEYEVENTF_KEYUP, 0)


def listen_for_numpad_and_move(offsets):
    running = True
    while running:
        # Numpad 7: Top-Left
        if wapi.GetAsyncKeyState(win32con.VK_NUMPAD7) < 0:
            move_mouse(*offsets["Top-Left"])
            press_key("W")

        # Numpad 9: Top-Right
        elif wapi.GetAsyncKeyState(win32con.VK_NUMPAD9) < 0:
            move_mouse(*offsets["Top-Right"])
            press_key("W")

        # Numpad 1: Bottom-Left
        elif wapi.GetAsyncKeyState(win32con.VK_NUMPAD1) < 0:
            move_mouse(*offsets["Bottom-Left"])
            press_key("W")

        # Numpad 3: Bottom-Right
        elif wapi.GetAsyncKeyState(win32con.VK_NUMPAD3) < 0:
            move_mouse(*offsets["Bottom-Right"])
            press_key("W")

        # Numpad 4: Left
        elif wapi.GetAsyncKeyState(win32con.VK_NUMPAD4) < 0:
            move_mouse(*offsets["Left"])
            press_key("W")

        # Numpad 8: Top
        elif wapi.GetAsyncKeyState(win32con.VK_NUMPAD8) < 0:
            move_mouse(*offsets["Top"])
            press_key("W")

        # Numpad 6: Right
        elif wapi.GetAsyncKeyState(win32con.VK_NUMPAD6) < 0:
            move_mouse(*offsets["Right"])
            press_key("W")

        # Numpad 2: Bottom
        elif wapi.GetAsyncKeyState(win32con.VK_NUMPAD2) < 0:
            move_mouse(*offsets["Bottom"])
            press_key("W")

        # Numpad 0: Toggle running state
        elif wapi.GetAsyncKeyState(win32con.VK_NUMPAD0) < 0:
            running = False

        time.sleep(0.1)  # Short delay to prevent high CPU usage


# Assuming your existing code setup here
game_window = find_game_window("Diablo II: Resurrected")
if game_window:
    width, height = get_window_size(game_window)
    offsets = calculate_offsets(width, height)
    listen_for_numpad_and_move(offsets)
