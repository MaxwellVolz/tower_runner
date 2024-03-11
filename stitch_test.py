import cv2
import numpy as np
import os


def align_images(image1, image2):
    """Align image2 to image1 using feature matching and homography."""
    # Convert images to grayscale
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    # Initialize ORB detector
    orb = cv2.ORB_create()

    # Detect keypoints and descriptors
    keypoints1, descriptors1 = orb.detectAndCompute(gray1, None)
    keypoints2, descriptors2 = orb.detectAndCompute(gray2, None)

    # Match descriptors using KNN
    matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
    matches = matcher.knnMatch(descriptors1, descriptors2, 2)

    # Filter matches using the Lowe's ratio test
    good_matches = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good_matches.append(m)

    if len(good_matches) > 4:
        # Extract location of good matches
        points1 = np.float32([keypoints1[m.queryIdx].pt for m in good_matches]).reshape(
            -1, 1, 2
        )
        points2 = np.float32([keypoints2[m.trainIdx].pt for m in good_matches]).reshape(
            -1, 1, 2
        )

        # Find homography
        H, _ = cv2.findHomography(points2, points1, cv2.RANSAC)

        # Use homography to warp image
        height, width, channels = image1.shape
        aligned_image = cv2.warpPerspective(image2, H, (width, height))

        return aligned_image
    else:
        print("Not enough matches are found - {}/{}".format(len(good_matches), 4))
        return image2  # Return the original image if we can't align


def process_and_stitch_images(images_folder, output_folder):
    """Process and stitch images from a folder."""
    images = sorted(
        [img for img in os.listdir(images_folder) if img.endswith(".png")],
        key=lambda x: int(x.split(".")[0]),
    )

    base_image = None
    for i, img_name in enumerate(images, 1):
        img_path = os.path.join(images_folder, img_name)
        current_image = cv2.imread(img_path)

        if base_image is None:
            base_image = current_image
        else:
            aligned_image = align_images(base_image, current_image)
            # Attempt to stitch the aligned image with the base
            base_image = (
                aligned_image  # For simplicity, we just update the base image here
            )

        output_path = os.path.join(output_folder, f"{i}_map.png")
        cv2.imwrite(output_path, base_image)
        print(f"Image {img_name} processed and map updated at {output_path}.")


# Specify the paths to your image and output directories
images_folder = "map_stitch_practice"
output_folder = "map_stitch_practice"

process_and_stitch_images(images_folder, output_folder)
