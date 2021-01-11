#!/usr/bin/env python


import rospy
from std_msgs.msg import String
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String



def callbackOne(msg):
    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y
    rospy.loginfo('x: {}, y: {}'. format(x, y))

def callbackTwo(msg):
    angle = msg.angle_min  
    rospy.loginfo(angle) 


def main():
    count = 0
    pub = rospy.Publisher('chatter', String, queue_size=10)
    rospy.Subscriber("/odom", Odometry, callbackOne)
    rospy.Subscriber("/scan", LaserScan, callbackTwo)
    rospy.init_node('talker')
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        hello_str = "hello world %s" % rospy.get_time()
        num_int = count +1
        rospy.loginfo(hello_str)
        rospy.loginfo(num_int)
        pub.publish(hello_str)
        pub.publish(num_int)
        rate.sleep()

        
    rospy.spin()
if __name__ == '__main__':
           
        main()
    