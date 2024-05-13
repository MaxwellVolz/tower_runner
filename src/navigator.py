import win32api as wapi
import win32con
import random
import time


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


def click_mouse():
    x, y = wapi.GetCursorPos()

    # Random delay before the click
    time_before_click = random.uniform(0.05, 0.15)
    time.sleep(time_before_click)

    # Simulate mouse down and up to perform a click
    wapi.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    time_during_click = random.uniform(
        0.05, 0.1
    )  # Short delay to simulate real click speed
    time.sleep(time_during_click)
    wapi.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

    # Random delay after the click
    time_after_click = random.uniform(0.05, 0.15)
    time.sleep(time_after_click)

    print(
        f"Clicked at position: ({x}, {y}), with pre-delay {time_before_click:.2f}s, click-delay {time_during_click:.2f}s, and post-delay {time_after_click:.2f}s"
    )
