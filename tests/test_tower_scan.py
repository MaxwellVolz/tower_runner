# tests/test_tower_scan.py
import pytest
from pathlib import Path
import sys
import os
from PIL import Image

# path shim for imports
project_root = Path(__file__).resolve().parents[1]
sys.path.append(str(project_root / "src"))

from darkroom import scan_for_tower

# Directly specify the path to the screenshot_samples directory
base_dir = project_root / "screenshot_samples"

has_cluster = "20240510_175549_adhoc_minimap.png"


# 20240510_175549_adhoc_minimap.png - has cluster, center right
# 20240510_175557_adhoc_minimap - has cluster, far right
# 20240510_175601_adhoc_minimap.png - no cluster, distraction


def load_image(file_path):

    print(f"Loading image: {file_path}")
    try:
        # Open an image file
        with Image.open(file_path) as img:
            return img
    except IOError:
        print("Error opening image. Please check the file path.")
        return None


def test_scan_for_tower_finds_cluster():
    # Path to the image with a specific cluster
    image_path = base_dir / "20240510_175549_adhoc_minimap.png"
    img = load_image(image_path)

    assert img is not None, "Failed to load image."

    result = scan_for_tower(img)

    assert result == (420, 300)  # Replace with expected coordinates


def test_scan_for_tower_no_cluster():
    # Path to the image without a cluster
    image_path = base_dir / "20240510_175601_adhoc_minimap.png"
    img = load_image(image_path)

    assert img is not None, "Failed to load image."

    result = scan_for_tower(img)

    assert result is None


def test_truth():
    assert True is not None
