import cv2
import numpy as np


class LineDetection:

    def __init__(self):
        pass

    def get_line_detected(self, image):
        h, w = image.shape[:2]
        blur = cv2.blur(image, (20, 20))
        # ret,thresh1 = cv2.threshold(image,127,255,cv2.THRESH_BINARY)
        ret, thresh1 = cv2.threshold(blur, 168, 255, cv2.THRESH_BINARY)
        hsv = cv2.cvtColor(thresh1, cv2.COLOR_RGB2HSV)

        # Define range of white color in HSV
        lower_white = np.array([0, 0, 168])
        upper_white = np.array([172, 111, 255])
        # Threshold the HSV image
        mask = cv2.inRange(hsv, lower_white, upper_white)
        # cv2.imwrite('out_test.png', mask)
        # Remove noise
        kernel_erode = np.ones((10, 6), np.uint8)

        eroded_mask = cv2.erode(mask, kernel_erode, iterations=4)
        kernel_dilate = np.ones((5, 2), np.uint8)
        dilated_mask = cv2.dilate(eroded_mask, kernel_dilate, iterations=2)
        im2, contours, hierarchy = cv2.findContours(dilated_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:1]
        if len(contours) > 0:
            M = cv2.moments(contours[0])
            # print(M)
            # Centroid
            try:
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                return [cx - w/2, h-cy]
            except:
                return [0, 10]
        else:
            return [0, 10]



