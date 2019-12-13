#!/usr/bin/env python

import rospy, rospkg, time, cv2, numpy as np
from cv_bridge       import CvBridge, CvBridgeError
from sensor_msgs.msg import Joy, Image
from std_msgs.msg    import Int32MultiArray

from lineDetector4     import LineDetector
from usonic	       import Usonic

class AutoDrive:


    def __init__(self):
        rospy.init_node('drive')
        self.pub = rospy.Publisher('xycar_motor_msg', Int32MultiArray, queue_size=1)
        self.position = LineDetector()
        self.lPos = -1
        self.rPos = -1
        self.speed = 125
	self.ultrasonic = Usonic()
	self.stop = False

    def exit(self):
        print("finished")

    def auto_drive(self, Angle, Speed):
        drive_info = [Angle, Speed]
        drive_info = Int32MultiArray(data=drive_info)
        self.pub.publish(drive_info)
    
    def stop(self):
	self.lPos, self.rPos = -1, -1

    def trace(self):
        offset = 10
	self.pos = self.position.detect_lines()
	self.lPos, self.rPos = self.pos[0], self.pos[1]
	self.ultrasonic.setData()
	#self.position.show_images(self.lPos, self.rPos)
	
	if self.lPos > 320:
                self.lPos = -1
        if self.rPos < 320:
                self.rPos = -1

	if abs(self.lPos-self.rPos) <= 80:
	    if self.rPos >= 380:
		x_location = 90-(self.rPos-400-offset)*0.6
	   	if x_location < 40:
		    x_location = 40
   	        self.auto_drive(x_location, self.speed)
	    elif self.lPos <= 280:
		x_location = 90+(240-self.lPos-offset)*0.6
		if x_location > 140:
		    x_location = 140
		self.auto_drive(x_location, self.speed)

	if self.lPos == -1:
	    x_location = (self.rPos-320-offset)*0.6
	    if x_location < 40:
		x_location = 40
            self.auto_drive(x_location, self.speed)
        elif self.rPos == -1:
	    x_location = (320-self.lPos-offset)*0.6
	    if x_location < 40:
		x_location = 40
            self.auto_drive(180-x_location, self.speed)

        elif self.lPos != -1 and self.rPos != -1:
            midPos = (self.lPos + self.rPos) // 2

            if (midPos >= 320):
                x_location = 90+(midPos-320)*0.3
            elif (midPos < 320):
                x_location = 90-(320-midPos)*0.3

            if x_location < 40:
                x_location = 40
	    elif x_location > 140:
		x_location = 140
	    print(x_location, " <<<<<<")

	    if (85 < x_location < 95):
		print(self.ultrasonic.getData(), " <<<<<<<<<<<<<<<<<<<<<<<<<<")
		if (self.ultrasonic.getData() < 100):
			self.auto_drive(90, 90)
			time.sleep(0.1)
			self.auto_drive(90, 60)
			time.sleep(0.1)
			self.auto_drive(90, 120)
			time.sleep(0.1)
			return False

            self.auto_drive(x_location, self.speed)
	    	
	elif self.lPos == -1 and self.rPos == -1:
	    self.auto_drive(90, 90)
	return True

	

if __name__ == "__main__":
    car = AutoDrive()
    time.sleep(3)
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        if not car.trace():
		break
        rate.sleep()

    rospy.on_shutdown(car.exit())

