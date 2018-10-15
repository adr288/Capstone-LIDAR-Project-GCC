#!/user/bin/env python 

import rospy
from nav_msgs.msg import Odometry

def callback(msg):
	
	x = msg.pose.pose.position.x
	y = msg.pose.pose.position.y
	rospy.loginfo('x: {}, y: {}'. format(x, y))


	#angle = msg.angle_min  #Check this in the case of error 
	#rospy.loginfo('The angle is: '. format(angle))

def main():
	rospy.init_node('location_monitor')
	rospy.Subscriber("/odom", Odometry, callback)
	
	#rospy.init_node('pointCloud_test')
	#rospy.Subscriber("/scan", LaserScan, callback)
	rospy.spin()


if __name__ == '__main__':
	main()
