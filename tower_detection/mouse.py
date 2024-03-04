from pynput.mouse import Listener, Button


def create_button_binding(button, func, *args, **kwargs):
    """Create a function to bind a specific mouse button to another function with its arguments."""

    def on_click(x, y, button_pressed, pressed):
        if button_pressed == button and pressed:
            func(*args, **kwargs)

    return on_click


def create_mouse_listener(bindings):
    """Create and return a mouse listener with custom button bindings.

    :param bindings: A list of tuples, each containing (button, function, args, kwargs)
    """

    def on_click(x, y, button, pressed):
        for binding in bindings:
            bound_button, func, args, kwargs = binding
            if button == bound_button and pressed:
                func(*args, **kwargs)

    return Listener(on_click=on_click)
