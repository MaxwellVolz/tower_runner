import cv2
import numpy as np

data = np.load("training_data/training_data.npy", allow_pickle=True)
targets = np.load("training_data/target_data.npy", allow_pickle=True)

print(f"Image Data Shape: {data.shape}")
print(f"targets Shape: {targets.shape}")

# Lets see how many of each type of move we have.
unique_elements, counts = np.unique(targets, return_counts=True)
print(np.asarray((unique_elements, counts)))

# Store both data and targets in a list.
# We may want to shuffle down the road.

holder_list = []
for i, image in enumerate(data):
    # holder_list.append([data[i], targets[i]])
    holder_list.append([data[i], ""])

count_NUMPAD7 = 0
count_NUMPAD9 = 0
count_NUMPAD1 = 0
count_NUMPAD3 = 0
count_NUMPAD4 = 0
count_NUMPAD8 = 0
count_NUMPAD6 = 0
count_NUMPAD2 = 0
count_NUMPAD0 = 0
nothing = 0

training_path = "training_data/images/"

for data in holder_list:
    img_data = data[0]
    key_pressed = data[1]

    if key_pressed == "NUMPAD7":
        count_NUMPAD7 += 1
        cv2.imwrite(f"{training_path}NUMPAD7/{count_NUMPAD7}.png", img_data)
    elif key_pressed == "NUMPAD9":
        count_NUMPAD9 += 1
        cv2.imwrite(f"{training_path}NUMPAD9/{count_NUMPAD9}.png", img_data)
    elif key_pressed == "NUMPAD1":
        count_NUMPAD1 += 1
        cv2.imwrite(f"{training_path}NUMPAD1/{count_NUMPAD1}.png", img_data)
    elif key_pressed == "NUMPAD3":
        count_NUMPAD3 += 1
        cv2.imwrite(f"{training_path}NUMPAD3/{count_NUMPAD3}.png", img_data)
    elif key_pressed == "NUMPAD4":
        count_NUMPAD4 += 1
        cv2.imwrite(f"{training_path}NUMPAD4/{count_NUMPAD4}.png", img_data)
    elif key_pressed == "NUMPAD8":
        count_NUMPAD8 += 1
        cv2.imwrite(f"{training_path}NUMPAD8/{count_NUMPAD8}.png", img_data)
    elif key_pressed == "NUMPAD6":
        count_NUMPAD6 += 1
        cv2.imwrite(f"{training_path}NUMPAD6/{count_NUMPAD6}.png", img_data)
    elif key_pressed == "NUMPAD2":
        count_NUMPAD2 += 1
        cv2.imwrite(f"{training_path}NUMPAD2/{count_NUMPAD2}.png", img_data)
    elif key_pressed == "NUMPAD0":
        count_NUMPAD0 += 1
        cv2.imwrite(f"{training_path}NUMPAD0/{count_NUMPAD0}.png", img_data)
    else:
        nothing += 1
        cv2.imwrite(f"{training_path}{nothing}.png", img_data)
