#Pose-Estimation-using-OpenCV  
This script helps to detect and track any pose in frame which helps us to track different poses an individual makes while doing an activity. It has many implications in the real world like yoga poses tracker, poster tracker for desk jobs individuals.

#Prerequisites  
Python version 3.0 or more
Working Webcam (**NOTE:** you can also feed a pre-captured video by specifying the path in the cv2.VideoCapture function call)

#Dependencies  
OpenCV, MediaPipe

## Landmark pixel coordinates

For an in-frame normalized landmark `lm` and a frame of width `w` and height `h`, the script converts `(lm.x, lm.y)` to the integer pixel pair `(int(lm.x * w), int(lm.y * h))`. `landmark_to_pixel` isolates this calculation; its output is a two-integer `(x, y)` tuple and it does not mutate the landmark. The focused check compares this bounded non-negative domain against `math.floor` and does not open a camera or import OpenCV/MediaPipe.

Run `python3 work/R29-T043/check.py` for the small result table and regression checks.


