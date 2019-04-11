import cv2
import numpy as np
import TIS
import socket
import time
import sys
import math
import glob

Tis1 = TIS.TIS("41814186", 1280, 960,15, True)

Tis1.Start_pipeline()

Tis1.Snap_image(5)
image1 = Tis1.Get_image()
cv2.imwrite('camera2.png',image1)

print('Press Esc to stop')
lastkey = 0

cv2.namedWindow('Window')  # Create an OpenCV output window

#kernel = np.ones((5, 5), np.uint8)  # Create a Kernel for OpenCV erode function

while lastkey != 27:
        Tis1.Snap_image(1)  # Snap an image with one second timeout
        image = Tis1.Get_image()  # Get the image. It is a numpy array
#image = cv2.erode(image, kernel, iterations=5)  # Example OpenCV image processing
        cv2.imshow('Window', image)  # Display the result

        lastkey = cv2.waitKey(10)

# Stop the pipeline and clean up
#cv2.namedWindow('Window1')  

#cv2.imshow('Window1', image1)
Tis1.Stop_pipeline()
