# tower_runner

d2 bot for sorc tower runs

## Description

This project image processing techniques and executes actions based on these detections. The project leverages multithreading to perform periodic checks without blocking the main execution flow.

Currently, developing an autonomous navigation system using Python, threading, and potentially OpenCV for image processing. The goal is to explore an environment, initially with no predefined map, by randomly walking and using cameras to scan for specific goals like towers.

## TODO

1. Implement snake-movement
   - pick direction
     - move +/- 15 degrees until stuck.
     - pick direction +/- 130-270

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

### Pathfinding

Radial with rollback

"radial pathfinding strategy with rollback, as you've described, can be an effective way to explore an environment from a central point outward, similar to a depth-first search that branches out in all directions. This approach is useful when the environment is relatively open or when the goal is to systematically explore every accessible area. "

Pros:

Comprehensive: Ensures thorough exploration of the area.
Adaptable: Can dynamically adjust to obstacles and explore alternative paths.
Cons:

Inefficient in large or complex environments due to repeated backtracking.
May not be the fastest method to reach a specific distant goal if known in advance.

example
1. move north until blocked
   2. move northeast until blocked
      1. move north until blocked
      2. move northeast until blocked
   3. move east until blocked
      1. move northeast until blocked
      2. move east until blocked
   3. move southeast until blocked
      1. move east until blocked
      2. move southeast until blocked
   4. etc.

continue until circle is completed

```py
def explore(x, y, visited, directions):
    """Explore using a radial and rollback strategy."""
    if (x, y) in visited:
        return
    visited.add((x, y))

    for dx, dy in directions:
        next_x, next_y = x + dx, y + dy
        if is_passable(next_x, next_y):
            explore(next_x, next_y, visited, directions)
        else:
            # If blocked, try next direction from current position
            continue

def is_passable(x, y):
    """Check if the new position is passable or blocked."""
    # Implement logic to check if the position is passable
    pass

# Directions represent N, NE, E, SE, S, SW, W, NW
directions = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
visited = set()
start_x, start_y = 0, 0  # Starting coordinates

explore(start_x, start_y, visited, directions)
```
Tuning
Direction Priority: Change the order of directions based on the environment or known goals to optimize the path.
Step Size: Adjust the step size (how far you move in each direction) to explore more quickly or more carefully.
Recursion Limits: Set limits on recursion depth to prevent excessive backtracking in very dense areas.
Memory Management: Use iterative approaches with explicit stacks if recursion depth becomes an issue due to large exploration areas.

Enhancements
Graph-based Pathfinding: Consider converting the environment into a graph and using algorithms like A* or Dijkstra’s for more efficient goal-directed movement.
Dynamic Path Adjustment: Implement real-time adjustments based on newly discovered obstacles or cleared paths.
Heuristics: Introduce heuristics to prioritize directions that are more likely to lead to open areas or specific goals.


