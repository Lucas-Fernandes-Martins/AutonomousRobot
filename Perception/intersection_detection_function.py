import cv2
import math
import numpy as np
from math import atan, pi
from skimage.morphology import skeletonize
from skimage import img_as_ubyte
from collections import defaultdict
def detect_v3(image):
    #########################
    #DRAWING MY CONTOURSSSS##
    #########################
    h, w = image.shape[:2]
    # Convert to HSV color space
    blur = cv2.blur(image,(5,5))
    #ret,thresh1 = cv2.threshold(image,127,255,cv2.THRESH_BINARY)
    ret,thresh1 = cv2.threshold(blur,168,255,cv2.THRESH_BINARY)
    hsv = cv2.cvtColor(thresh1, cv2.COLOR_RGB2HSV)
    # Define range of white color in HSV
    lower_white = np.array([0, 0, 168])
    upper_white = np.array([172, 111, 255])
    # Threshold the HSV image
    mask = cv2.inRange(hsv, lower_white, upper_white)
    # Remove noise
    kernel_erode = np.ones((6,6), np.uint8)
    eroded_mask = cv2.erode(mask, kernel_erode, iterations=1)
    kernel_dilate = np.ones((4,4), np.uint8)
    dilated_mask = cv2.dilate(eroded_mask, kernel_dilate, iterations=1)
    # Find the different contours
    contours, hierarchy = cv2.findContours(dilated_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Sort by area (keep only the biggest one)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    # A.)Draw colored contour, B.)Make black background and draw ALL contours on it
    countoured_image = cv2.drawContours(image, contours, -1, (0, 255, 70), 3)  # draw coloured contour on the image itself
    black_background = np.zeros((h, w, 3), dtype=np.uint8) # define a black background
    contour = cv2.drawContours(black_background, contours, -1, (255, 255, 255), 1)  # image with white contour on black background

    # grayscale, then => erosion before hough lines
    contour_gray = cv2.cvtColor(contour, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((20,20),np.uint8)
    erosion = cv2.erode(contour_gray,kernel,iterations = 1)

    ########################################
    # FINDING HOUGH LINES IN MY contours####
    ########################################
    lines = cv2.HoughLines(contour_gray, 1, np.pi / 180, 150, None, 0, 0)
    # draw lines on a black image:
    blackcanvas = np.zeros_like(contour)
    if lines is not None:
        for i in range(0, len(lines)):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * rho
            y0 = b * rho
            pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
            pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
            cv2.line(blackcanvas, pt1, pt2, (0,0,255), 1, cv2.LINE_AA)

    ##################################
    # detecting 2 groups of lines:####
    ##################################
    hough_angles = [lines[i][0][1] for i in range(0, len(lines))]
    l = len(hough_angles)
    result = ''
    end = False
    for i in range(l):
        if end:
            break
        for j in range(i, l):
            deviation = 0.1
            angle1 = hough_angles[i]
            angle2 = hough_angles[j]
            diff = angle1-angle2
            if (1-deviation)*math.pi/2 <= diff <= (1+deviation)*math.pi/2 or -(1+deviation)*math.pi/2 <= diff <= -(1-deviation)*math.pi/2:
                end = True
                result = 'INTERSECTIONNNN'
                break
    if not end:
        result = 'GO STRAIGHTTT'

    # Outputs (a black image with hough lines drawn, True or Flase depending if intersection is detected or not)
    output = (blackcanvas, end)
    return output
