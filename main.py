from keyboard import create_keyboard_listener
from mouse import create_mouse_listener
from utils import capture_area
from pynput.mouse import Button

toggle = True


def toggle_functionality():
    global toggle
    toggle = not toggle
    print(f"Functionality toggled {'on' if toggle else 'off'}")


def capture_minimap():
    if toggle:
        capture_area([2580, 220, 180, 120])


# Define key and button bindings
key_bindings = [
    ("f", toggle_functionality, (), {}),
]

button_bindings = [
    (Button.right, capture_minimap, (), {}),
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
