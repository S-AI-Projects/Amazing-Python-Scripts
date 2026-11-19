import numpy as np
from matplotlib import pyplot as plt
import cv2
import io
import time

# Complexity analysis:
# Input size variable is N = w * h, representing the number of pixels in crop_img.
# Computing np.average(crop_img) visits each pixel once, which requires O(N) operations.
# List slicing heartbeat_values[1:] + [avg] requires O(K) where K = heartbeat_count = 128.
# Worst case complexity per frame is O(N + K).


def process_heartrate_frame(crop_img, heartbeat_values, heartbeat_times, current_time=None):
    # Core frame update function
    # Complexity is O(N) where N is crop_img.size
    if current_time is None:
        current_time = time.time()
    avg_val = float(np.average(crop_img))
    new_values = heartbeat_values[1:] + [avg_val]
    new_times = heartbeat_times[1:] + [current_time]
    return new_values, new_times, avg_val


if __name__ == '__main__':
    # Camera stream
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1280)
    cap.set(cv2.CAP_PROP_FPS, 30)
    # Video stream (optional, not tested)
    # cap = cv2.VideoCapture("video.mp4")
    # Image crop
    x, y, w, h = 800, 500, 100, 100
    x, y, w, h = 950, 300, 100, 100
    heartbeat_count = 128
    heartbeat_values = [0]*heartbeat_count
    heartbeat_times = [time.time()]*heartbeat_count
    # Matplotlib graph surface
    fig = plt.figure()
    ax = fig.add_subplot(111)
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        crop_img = img[y:y + h, x:x + w]
        # Update the data
        heartbeat_values, heartbeat_times, _ = process_heartrate_frame(
            crop_img, heartbeat_values, heartbeat_times
        )
        # Draw matplotlib graph to numpy array
        ax.plot(heartbeat_times, heartbeat_values)
        fig.canvas.draw()
        plot_img_np = np.fromstring(fig.canvas.tostring_rgb(),
                                    dtype=np.uint8, sep='')
        plot_img_np = plot_img_np.reshape(
            fig.canvas.get_width_height()[::-1] + (3,))
        plt.cla()
        # Display the frames
        cv2.imshow('Crop', crop_img)
        cv2.imshow('Graph', plot_img_np)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
