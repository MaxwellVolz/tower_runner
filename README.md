# tower_runner

d2 bot for sorc tower runs

## Description

This project image processing techniques and executes actions based on these detections. The project leverages multithreading to perform periodic checks without blocking the main execution flow.

## Features

- **Screen Capture**: Captures specified screen areas for processing.
- **Image Processing**: Searches for predefined color patterns to detect specific features.
- **Periodic Checks**: Uses a custom `IntervalThread` class for non-blocking, periodic execution of tasks.
- **Toggle Functionality**: Allows enabling/disabling the periodic checks dynamically.

## Getting Started

### Dependencies

- Python 3.6+
- OpenCV
- PyAutoGUI
- NumPy
- pynput

### Installing

1. Clone the repository to your local machine.
2. Ensure Python 3.6+ is installed.
3. Install the required Python packages:

```bash
pip install opencv-python numpy PyAutoGUI pynput
```

### Executing Program

1. Navigate to the project directory.
2. Run `main.py` to start the program:

```bash
python main.py
```

3. Use the specified toggle key (e.g., "f") to enable/disable the periodic checks.

## File Descriptions

- `main.py`: The main script that initializes the application, handles user inputs, and manages the toggle functionality.
- `interval.py`: Contains the `IntervalThread` class used for scheduling periodic tasks without blocking the main thread.
- `utils.py`: Includes utility functions for screen capture and image processing, such as `capture_area` and `compare_images`.


## Spiral Explanation

Spiral Pattern: The function creates a square spiral pattern starting from the center of the screen. It moves in a direction (up, right, down, left), changes direction after completing part of the square, and gradually increases the length of each leg of the spiral to expand outward.

Control Parameters:


## Fast AI Integration

### Notes

- [youtube](https://www.youtube.com/watch?v=GS_0ZKzrvk0)
- image for neural net should be 224 224
  - [capture training code](https://github.com/ClarityCoders/Fall-Guys-AI/blob/master/training.py)


### Goal

1. Find Tower Entrance
   1. Search **Black Marsh** with FastAI
   2. Enter **Tower** with Image Detection 
2. Level 1
   1. Select **Level Exit** with Image Detection 
3. Level 2 - 5
   1. Search Level with FastAI
   2. Select **Level Exit** with Image Detection 

### Training SOP

1. Capturing Images - whole minimap
   1. Capture #1 at *Black Wood Waypoint*
   2. Teleport in a direction
      1. Record Mouse location
      2. Capture
2. Process Images
   1. Convert to B/W line art
   2. Record Mouse location with filename
   3. Save to numpy array for neural network training



### CLI

1. Setup
   1. Check for Game Window
   2. Get Minimap location
   3. Open Map, Screenshot, Paint
   4. Enter **X Y** of center of **Blue X**
2. Run

### 