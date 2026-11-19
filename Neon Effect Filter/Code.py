import numpy as np
import cv2
import os.path
from matplotlib import pyplot as plt


def apply_neon_effect(img_path):
    # Failure path: Check if image reading fails at line 9
    img = cv2.imread(img_path)
    if img is None:
        print(f"Error: Unable to load image at {img_path}")
        return None

    image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    img_small = cv2.pyrDown(image)
    num_iter = 5
    for _ in range(num_iter):
        img_small = cv2.bilateralFilter(img_small, d=9, sigmaColor=9, sigmaSpace=7)

    img_rgb = cv2.pyrUp(img_small)

    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
    img_blur = cv2.medianBlur(img_gray, 7)
    img_edge = cv2.adaptiveThreshold(
        img_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 7, 2)

    img_edge = cv2.cvtColor(img_edge, cv2.COLOR_GRAY2RGB)
    array = cv2.bitwise_and(image, img_edge)
    array1 = cv2.bitwise_xor(array, image)
    return array1


if __name__ == '__main__':
    # example -> C:\Users\xyz\OneDrive\Desktop\project\image.jpg
    img_path = input("Enter the path of image: ")
    result = apply_neon_effect(img_path)
    if result is not None:
        plt.figure(figsize=(10, 10))
        plt.imshow(result, cmap='gray')
        plt.title("Neon Effect Filtered Photo")
        plt.axis('off')
        filename = os.path.basename(img_path)
        # saved file name as (Filtered)image_name.jpg
        plt.savefig("./Neon Effect Filter/Neon Effect Filter" + filename)
        plt.show()
