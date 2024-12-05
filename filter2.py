import cv2
from skimage.metrics import structural_similarity as ssim
import numpy as np
import os
import shutil
from time import sleep

# Load the two images
filter = cv2.imread('filter2.jpg', cv2.IMREAD_COLOR)
os.chdir("price_images")
while True:
    files = os.listdir(r"C:\Users\aghil\OneDrive\Desktop\winnig_chance\price_images")
    if not len(files):
        sleep(3)
        continue
    for file in files:
        print(file)
        image = cv2.imread(file, cv2.IMREAD_COLOR)

        # Mean Squared Error (MSE)
        h, w, _ = image.shape

        # Match the template
        result = cv2.matchTemplate(image, filter, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if max_val > 0.8:  # Adjust the threshold (e.g., 0.8) as needed
            top_left = max_loc
            bottom_right = (top_left[0] + w, top_left[1] + h)
            os.remove(file)
            print("found the filteer")
        else:
            print("found the price")
            cv2.imshow('Result', image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            shutil.move(f"C:\\Users\\aghil\\OneDrive\\Desktop\\winnig_chance\\price_images\\{file}", f"C:\\Users\\aghil\\OneDrive\\Desktop\\winnig_chance\\{file}")
            


