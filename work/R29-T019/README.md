# R29 T019 HeartRate scaling checks

HeartRate detection is in HeartRate Detection OpenC py HeartRate.py.

## Preconditions and Source Anchors
Precondition anchors at lines 21 and 22:
x, y, w, h = 800, 500, 100, 100
x, y, w, h = 950, 300, 100, 100
Heartbeat buffer length is 128 defined at line 23.
Crop extraction and averaging at lines 35 and 36:
crop_img = img[y:y + h, x:x + w]
heartbeat_values = heartbeat_values[1:] + [np.average(crop_img)]

## Complexity Scaling Analysis
Input size variable: N = w * h, the number of cropped pixels.
Operation: np.average(crop_img) visits each of the N pixels once to compute the mean value.
Complexity class: Linear time O(N) for pixel averaging, plus O(K) list slicing where K = 128.
Worst case per frame complexity is O(N + K).

## Verification Results
1. Smallest valid input: w=1 and h=1 (N=1 pixel) returns exact pixel value and maintains buffer length of 128.
2. Ordinary input: w=100 and h=100 (N=10000 pixels) computes average and updates buffer.
3. Scaling measurements saved in work/R29-T019/timings.txt demonstrate scaling across multiple pixel dimensions.
