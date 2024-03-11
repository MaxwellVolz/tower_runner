import win32api as wapi
import win32con

keyList = ["\b"]
for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ 123456789,.'APS$/\\":
    keyList.append(char)


def key_check():
    keys = []
    for key in keyList:
        if wapi.GetAsyncKeyState(ord(key)):
            keys.append(key)
    if "H" in keys:
        return "H"
    elif "B" in keys:
        return "B"
    elif "D" in keys:
        return "D"
    elif "W" in keys:
        return "W"
    else:
        return "W"


def numpad_check():
    numpad_keys = {
        win32con.VK_NUMPAD7: "NUMPAD7",
        win32con.VK_NUMPAD9: "NUMPAD9",
        win32con.VK_NUMPAD1: "NUMPAD1",
        win32con.VK_NUMPAD3: "NUMPAD3",
        win32con.VK_NUMPAD4: "NUMPAD4",
        win32con.VK_NUMPAD8: "NUMPAD8",
        win32con.VK_NUMPAD6: "NUMPAD6",
        win32con.VK_NUMPAD2: "NUMPAD2",
        win32con.VK_NUMPAD0: "NUMPAD0",
    }
    for key, value in numpad_keys.items():
        if wapi.GetAsyncKeyState(key) & 0x8000:
            return value
    return None  # No relevant numpad key was pressed


def mouse_status():
    # Get the current position of the mouse
    x, y = wapi.GetCursorPos()

    # Check the state of the mouse buttons
    left_click = wapi.GetKeyState(
        0x01
    )  # Left button down = 0 or 1. Button up = -127 or -128
    right_click = wapi.GetKeyState(
        0x02
    )  # Right button down = 0 or 1. Button up = -127 or -128

    # Format the mouse status
    status = {
        "Position": (x, y),
        "Left Click": "Pressed" if left_click < 0 else "Released",
        "Right Click": "Pressed" if right_click < 0 else "Released",
    }

    return status
