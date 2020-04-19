#!/usr/bin/env python

import rospy, time
from std_msgs.msg import Int32MultiArray

class Usonic:
	def __init__(self):
		self.Data = None
	    	rospy.Subscriber('ultrasonic', Int32MultiArray, self.callback)
		self.distance = []

	def callback(self, data):
	    	self.Data = data.data

	def setData(self):
		if (len(self.distance) < 8):
			self.distance.append(self.Data[1])
		elif (len(self.distance) >= 8):
			self.distance = self.distance[1:] + [self.Data[1]]

	def getData(self):
		distance = 0
		distanceLen = 0
		for i in range(len(self.distance)):
			distance    += (i+1) * self.distance[i]
			if distanceLen < 36:			
				distanceLen += (i+1)
		distance /= distanceLen

		return distance
