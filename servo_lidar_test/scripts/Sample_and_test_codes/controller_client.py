#!/usr/bin/env python

import sys
import rospy
from beginner_tutorials.srv import *

def controller_client(start): #(x.y)
    rospy.wait_for_service('controller_service_name')
    try:
        start_servo = rospy.ServiceProxy('controller_service_name', controller_client) #####Understand this portion
        check_start = start_servo(start)# (x,y) #####Understand this portion
        return check_start
    except rospy.ServiceException, e:
    	print "Service call failed"%e 
   

if __name__ == "__main__":
    start=True
    controller_client(start)


