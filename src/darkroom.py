import cv2
import numpy as np
from PIL import Image

import os

debug_dir = "screenshots_debug"


def downsample_image(image, scale_percent=40):
    if isinstance(image, Image.Image):
        image = np.array(image)  # Convert PIL Image to NumPy array

    image = cv2.GaussianBlur(image, (5, 5), 0)
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    return resized


def did_we_move(
    current_image_downsampled, previous_image_downsampled, debug_dir="debug_images"
):
    if previous_image_downsampled is None:
        return True

    if not os.path.exists(debug_dir):
        os.makedirs(debug_dir)

    difference_threshold = 50
    # Calculate the total number of pixels in one of the images
    total_pixels = current_image_downsampled.size

    # Calculate the difference and apply a binary threshold
    difference = cv2.absdiff(current_image_downsampled, previous_image_downsampled)
    _, threshold = cv2.threshold(
        difference, difference_threshold, 255, cv2.THRESH_BINARY
    )
    non_zero_count = np.count_nonzero(threshold)

    # Calculate the percentage of changed pixels
    changed_percentage = (non_zero_count / total_pixels) * 100
    similarity_threshold = (
        1.0  # Adjust this to fine-tune when images are considered 'the same'
    )

    # Save the difference images for debugging without annotations
    cv2.imwrite(
        os.path.join(debug_dir, "current_downsampled.jpg"), current_image_downsampled
    )
    cv2.imwrite(
        os.path.join(debug_dir, "previous_downsampled.jpg"), previous_image_downsampled
    )
    cv2.imwrite(os.path.join(debug_dir, "difference.jpg"), difference)
    cv2.imwrite(os.path.join(debug_dir, "threshold.jpg"), threshold)

    print(f"Changed pixels percentage: {changed_percentage}%")
    print(
        f"Changed pixels percentage ({changed_percentage}%) > Similarity threshold ({similarity_threshold}%): {changed_percentage < similarity_threshold}"
    )

    # Only return False if the changed pixels are less than the similarity threshold (images are very similar)
    return changed_percentage > similarity_threshold


def calculate_minimap_offset(destination_on_minimap):
    # screen = (1720, 720)
    minimap_area = (260, 150)  # width, height
    screen_width_offset = 1720 - 900
    screen_height_offset = 1200

    # Calculate the center of the minimap

    # Calculate the vector from the center of the minimap to the destination
    vector_to_destination = (
        (destination_on_minimap[0] / minimap_area[0]) * 1800,
        (destination_on_minimap[1] / minimap_area[1]) * screen_height_offset,
    )

    # Calculate the new screen position by applying the vector to the screen center
    new_screen_position = (
        screen_width_offset + vector_to_destination[0],
        vector_to_destination[1],
    )

    print(f"Move mouse to screen coordinates: {new_screen_position}")

    return new_screen_position


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

                return calculate_minimap_offset((y, x))

    return None
