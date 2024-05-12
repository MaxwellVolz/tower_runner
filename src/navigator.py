import win32api as wapi
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
