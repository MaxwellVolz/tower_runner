spiral teleport (iterations, run_duration)

- use screen size at 80% for mouse positions
- 
start with mouse at bottom of screen
  
for iterations
    press W
    hold left click
    for run_duration
    move mouse left by angle_of_turn(example 60 degrees)
    release mouse



lets define a function called smart_teleport(iterations)

need to store global current_minimap

1. get screen size
2. determine corners for mouse_positions[]
   1. top_right = (screen-width * 0.8, screen_height * 0.2)

randomize the order of the corners

set direction to first corner

for iterations

    if time_to_exit: exit loop
    set mouse to first corner with some randomness "human"
    hold left mouse
    press W
    release left mouse

    if check_for_tower is True
        exit loop
    
    compare current_minimap to last_minimap using compare_images(img1, img2, threshold=30)

    if compare_images returns True, set direction to next corner
    and continue with iterations



