import numpy as np
import cv2
import time
import os
import win32api as wapi

from utils.getkeys import key_check, numpad_check
from utils.images import capture_area


file_name = "training_data/training_data.npy"
file_name2 = "training_data/target_data.npy"


def get_data():
    if os.path.isfile(file_name):
        print("File exists, loading previous data!")
        image_data = list(np.load(file_name, allow_pickle=True))
        targets = list(np.load(file_name2, allow_pickle=True))
    else:
        print("File does not exist, starting fresh!")
        image_data = []
        targets = []
    return image_data, targets


def save_data(image_data, targets):
    np.save(file_name, image_data)
    np.save(file_name2, targets)


image_data, targets = get_data()
while True:
    keys = key_check()
    print("waiting press D to start")
    if keys == "D":
        print("Starting")
        break


count = 0
while True:
    count += 1
    last_time = time.time()

    # Every time loop -------------------------------------------=
    image = capture_area([2420, 35, 500, 500])
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.Canny(image, threshold1=119, threshold2=250)
    image = cv2.resize(image, (224, 224))

    # Convert to numpy array and append to image_data
    image = np.array(image)
    image_data.append(image)
    # Every time loop -------------------------------------------=

    # Check for numpad key press
    # numpad_key = numpad_check()
    # if numpad_key:
    #     # Only proceed with capturing and processing the image if a specified numpad key is pressed
    #     image = capture_area([2420, 35, 500, 500])
    #     image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #     image = cv2.Canny(image, threshold1=119, threshold2=250)
    #     image = cv2.resize(image, (224, 224))

    #     # Convert to numpy array and append to image_data
    #     image = np.array(image)
    #     image_data.append(image)

    #     # Append the pressed numpad key to targets
    #     targets.append(numpad_key)

    # Break the loop if "H" key is pressed
    if wapi.GetAsyncKeyState(ord("H")) & 0x8000:
        break

    time.sleep(0.5)

    print("loop took {} seconds".format(time.time() - last_time))

save_data(image_data, targets)
