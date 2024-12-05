# this file takes the images from images folder 
# andfilters the images baise on simularety with the "price_image.jpg"
# then delete the images that are not similar

import cv2
from skimage.metrics import structural_similarity as ssim
import numpy as np
import os
import shutil
from time import sleep

# remember this image sould be at the same scail of those you are going to search for 
# so you sould download them from the product page of the price
# aslo do not try to resize an image to search for it , it do not work
price_image = cv2.imread("price_image.jpg", cv2.IMREAD_GRAYSCALE)

os.chdir("images")
while True:
    files = os.listdir(r"C:\Users\aghil\OneDrive\Desktop\winnig_chance\images")
    if not len(files) :
        sleep(3)
        continue
    for file in files:
        try:
            image2 = cv2.imread(file, cv2.IMREAD_GRAYSCALE)

            
            if price_image.shape != image2.shape:
                os.remove(file)
                continue
            mse = np.mean((price_image - image2) ** 2)

            # Structural Similarity Index (SSIM)
            similarity, _ = ssim(price_image, image2, full=True)
            if similarity < 0.8:
                os.remove(file)
                continue

            print(f"MSE: {mse}")
            print(f"SSIM: {similarity}")
            shutil.move(f"C:\\Users\\aghil\\OneDrive\\Desktop\\winnig_chance\\images\\{file}", f"C:\\Users\\aghil\\OneDrive\\Desktop\\winnig_chance\\price_images\\{file}")
        except Exception as e:
            print(file)
            print(f"ERROR{e}")

