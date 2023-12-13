import cv2
import numpy as np
import math

class CornerDetection:

  def __init__(self):
      pass

  def get_coner_detected(self, image):
    ########################
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
    kernel_erode = np.ones((5,5), np.uint8)
    eroded_mask = cv2.erode(mask, kernel_erode, iterations=1)
    kernel_dilate = np.ones((2,2), np.uint8)
    dilated_mask = cv2.dilate(eroded_mask, kernel_dilate, iterations=2)
    # Find the different contours
    major = cv2.__version__.split('.')[0]
    if major == '3':
        im2, contours, hierarchy = cv2.findContours(dilated_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    else:
        contours, hierarchy = cv2.findContours(dilated_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Sort by area (keep only the biggest one)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    # A.)Draw colored contour, B.)Make black background and draw ALL contours on it
    black_background = np.zeros((h, w, 3), dtype=np.uint8) #define a black background
    contour = cv2.drawContours(black_background, contours, -1, (255,255,255), 1) #image with white contour on black background
    contour = cv2.dilate(contour, kernel_dilate, iterations=5)

    ################################
    # APPLYING MASKS ON THE BORDER##
    ################################
    contour_open = contour.copy()
    percentage = 0.07
    # Create masks for the regions to keep
    top_mask = np.ones_like(contour_open)*255
    top_mask[:int(h * percentage), :, :] = 0
    bottom_mask = np.ones_like(contour_open)*255
    bottom_mask[-int(h * percentage):, :, :] = 0
    left_mask = np.ones_like(contour_open)*255
    left_mask[:, :int(w * percentage), :] = 0
    right_mask = np.ones_like(contour_open)*255
    right_mask[:, -int(w * percentage):, :] = 0
    # Apply the masks to set the corresponding regions to zero
    contour_open = cv2.bitwise_and(contour_open, top_mask)
    contour_open = cv2.bitwise_and(contour_open, bottom_mask)
    contour_open = cv2.bitwise_and(contour_open, left_mask)
    contour_open = cv2.bitwise_and(contour_open, right_mask)

    #grayscale, then => erosion before hough lines
    contour_gray = cv2.cvtColor(contour_open, cv2.COLOR_BGR2GRAY)

    ########################################
    #FINDING HOUGH LINES IN MY contours#####
    ########################################
    lines = cv2.HoughLines(contour_gray, 1, np.pi / 180, 150, None, 0, 0)
    #draw lines on a black image:
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
            # cv2.line(blackcanvas, pt1, pt2, (0,0,255), 1, cv2.LINE_AA)
    else:
        return False

    ##################################
    #detecting 2 groups of lines:#####
    ##################################
    hough_angles = [lines[i][0][1] for i in range(0, len(lines))]
    l = len(hough_angles)
    result = ''
    end = False
    for i in range(l):
        if end:
            break
        for j in range(i, l):
            deviation = 0.03
            angle1 = hough_angles[i]
            angle2 = hough_angles[j]
            diff = angle1-angle2
            if (1-deviation)*math.pi/2 <= diff <= (1+deviation)*math.pi/2 or -(1+deviation)*math.pi/2 <= diff <= -(1-deviation)*math.pi/2:
                end = True
                result = 'INTERSECTIONNNN'
                break
    if not end:
        result = 'GO STRAIGHTTT'

    #Outputs (a black image with hough lines drawn, True or Flase depending if intersection is detected or not)
    output = (blackcanvas, end, lines, contour_gray, hough_angles)

    return end
