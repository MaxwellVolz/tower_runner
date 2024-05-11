import keyboard


def print_keycode(e):
    if e.event_type == "down":  # Ensures we capture the key press event, not release
        print(f"keyboard.add_hotkey('{e.name}', callback_function)")


keyboard.hook(print_keycode)

# Keep the script running
keyboard.wait()
