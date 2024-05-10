

We are going to be using Python, leveraging OpenCV for map exploration in a top-down view with a limited viewport to analyze and navigate the environment dynamically. 

We have already captured images and post-processed them with:

```py
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.Canny(image, threshold1=119, threshold2=250)
    image = cv2.resize(image, (224, 224))
    # saves image in folder
```

We have a collection of images from a sample"exploration". 

Lets loop through the images we have post-processed in the /map_stitch_practice folder numbered:
- 1.png, 
- 2.png
- ... 
- 40.png 
  
Update a map with new information as a bot explores, we can use techniques such as Kalman filtering. Kalman filtering is a mathematical method that combines prior knowledge with new measurements to estimate the state of a system. 

Implement a stitch_image_to_map() function to stitch the current viewport image onto the existing map. This will require using OpenCV's stitch() function to align and merge the images.

At each step (loop of image directory) lets output the current stitched map and save it. the images are 
lets export to the same folder with the name 1_map.png, 2_map.png, etc.




1. Fine-tune the values of the state vector and covariance matrix, the process and measurement noise matrices, the map boundary, the starting location, and the 
2. 
3. 
4. desired feature to optimize performance and accuracy.



For a school project I am developing an automated player named Jerry for a diablo ii private server. I am using Python with opencv and numpy. I need to define Jerrys role.

When Jerry is activated
1. Determine if location is Black Wood Waypoint
   1. 