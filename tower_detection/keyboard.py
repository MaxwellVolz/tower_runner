from pynput.keyboard import Listener, KeyCode


def create_key_binding(key, func, *args, **kwargs):
    """Create a function to bind a specific key to another function with its arguments."""

    def on_press(key_pressed):
        if key_pressed == KeyCode.from_char(key):
            func(*args, **kwargs)

    return on_press


def create_keyboard_listener(bindings):
    """Create and return a keyboard listener with custom key bindings.

    :param bindings: A list of tuples, each containing (key, function, args, kwargs)
    """

    def on_press(key):
        for binding in bindings:
            bound_key, func, args, kwargs = binding
            if key == KeyCode.from_char(bound_key):
                func(*args, **kwargs)

    return Listener(on_press=on_press)
