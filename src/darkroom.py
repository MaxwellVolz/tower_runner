import cv2
import numpy as np
from PIL import Image


def scan_for_tower(image):
    """
    Scans a PIL image object for a specific color cluster (5x5 pixels) and returns the position of the cluster.

    Args:
    image (PIL.Image): A PIL image object.

    Returns:
    tuple: Coordinates (x, y) of the cluster if found, otherwise None.
    """
    if image is None:
        print("No image...")
        return

    if not isinstance(image, Image.Image):
        raise ValueError("The provided image is not a valid PIL Image object")

    image_rgb_pil = image.convert("RGB")

    # Convert PIL image to a numpy array in RGB format
    image_np = np.array(image_rgb_pil)
    if image_np.ndim != 3 or image_np.shape[2] != 3:
        raise ValueError("Image format must be RGB with 3 channels")

    image_rgb = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    # Define the target color and the threshold for matching
    target_color = np.array([120, 22, 110])
    threshold = 30  # Define how close the color match needs to be

    # Create a mask that identifies pixels within the acceptable range
    min_color = np.maximum(0, target_color - threshold)
    max_color = np.minimum(255, target_color + threshold)
    color_mask = cv2.inRange(image_rgb, min_color, max_color)

    # Find non-zero points (where there is a match)
    points = np.argwhere(color_mask == 255)

    # Check if there's a cluster of matching 5x5
    for point in points:
        x, y = point[0], point[1]
        if (
            x + 5 <= image_rgb.shape[0] and y + 5 <= image_rgb.shape[1]
        ):  # Ensure within bounds
            patch = color_mask[x : x + 5, y : y + 5]
            if cv2.countNonZero(patch) == 25:  # Check if all pixels in the patch match
                return (y, x)  # Return as (x, y)

    return None
