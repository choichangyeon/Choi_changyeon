#!/usr/bin/env python

import time
import cv2
import numpy as np
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

class YellowLineDetector:

    def __init__(self):
        self.image_width = 640
 	self.scanPoint = (260, 320)
        self.area_width, self.area_height = 20, 10
        area = self.area_width * self.area_height
        self.pixel_cnt_threshold = area * 0.6
        self.roi_vertical_pos = 300
	self.mask = np.empty(shape=[0])
	self.view = np.empty(shape=[0])
	self.detected = False
	

        self.cam_img = np.zeros(shape=(480, 640, 3), dtype=np.uint8)
        self.bridge = CvBridge()
        rospy.Subscriber('/usb_cam/image_raw', Image, self.conv_image)

    def conv_image(self, data):
        self.cam_img = self.bridge.imgmsg_to_cv2(data, "bgr8")

        v = self.roi_vertical_pos
        self.roi = self.cam_img[v:v + 40, :]

        lbound = np.array([20, 100, 100], dtype=np.uint8)
        ubound = np.array([30, 250, 255], dtype=np.uint8)
        
	self.mask = cv2.inRange(self.roi, lbound, ubound)
        self.view = cv2.cvtColor(self.mask, cv2.COLOR_GRAY2BGR)

    def detect_lines(self):
	    
        area = self.mask[self.roi_vertical_pos:self.roi_vertical_pos + 20, 315:325]
        if cv2.countNonZero(area) > self.pixel_cnt_threshold:
		self.detected = True
		print(self.detected)
        # Return positions of left and right lines detected.
        return self.detected

    def show_images(self):
        if self.detected:
                lsquare = cv2.rectangle(self.view,
                                        (self.roi_vertical_pos, 315),
                                        (self.roi_vertical_pos+20, 325),
                                        (0, 255, 0), 3)

        cv2.imshow("origin", self.roi)
	cv2.imshow("yellow", self.view)
        cv2.waitKey(1)


if __name__ == '__main__':
	test = LineDetector()
	time.sleep(3)
       	while not rospy.is_shutdown():
        	test.detect_lines()
	cv2.destroyAllWindows()

        # Display images for debugging purposes;
        # do not forget to call cv2.waitKey().
