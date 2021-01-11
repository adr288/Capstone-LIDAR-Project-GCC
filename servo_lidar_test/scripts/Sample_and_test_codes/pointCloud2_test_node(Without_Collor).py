#!/usr/bin/env python
import rospy
import math
import sys

from visualization_msgs.msg import Marker
from visualization_msgs.msg import MarkerArray

from _collections import deque, defaultdict

from sensor_msgs.msg import PointCloud2
import std_msgs.msg
import sensor_msgs.point_cloud2 as pcl2
from servo_lidar_test.msg import pointCloud


x = []
y = []
z = []

#pointCloud callback function
def get_pointCloud_coordinates(msg):

    global x
    global y
    global z
    global coordinatesArray

    x = msg.x[:]
    y = msg.y[:]
    z = msg.z[:]
    #coordinatesArray = msg.pointCloudCoordinates[:]
    


if __name__ == '__main__':

    pointCloude_publish_rate = 30
    number_of_data_poins = 30000 # Number of data points to be published


    rospy.init_node('pointCloud2_test')
    rate = rospy.Rate(pointCloude_publish_rate)  #Publishing Rate

    #--------------------------------------------------
    # Subscriber Setup
    #---------------------------------------------------
    rospy.Subscriber('pointCloud', pointCloud, get_pointCloud_coordinates) # Subscribes to Adrik's node


    #--------------------------------------------------
    # Publisher Setup
    #--------------------------------------------------
    pcl_pub = rospy.Publisher("/my_pcl_topic", PointCloud2, queue_size=10)



    rospy.loginfo("Initializing sample pcl2 publisher node...")
    
    #give time to roscore to make the connections
    rospy.sleep(1.)
    
    
    #header
    header = std_msgs.msg.Header()
    header.stamp = rospy.Time.now()
    header.frame_id = 'laser'
    
    
    #Initialization 
    rospy.loginfo("happily publishing sample pointcloud.. !")
    count = 0
    cloud_points = []
    coordinatesArray = []
    marker = Marker()
    marker.type = marker.SPHERE
    marker.action = marker.ADD
    marker.scale.x = 0.2
    marker.scale.y = 0.2
    marker.scale.z = 0.2
    marker.color.a = 1.0
    marker.color.r = 1.0
    marker.color.g = 1.0
    marker.color.b = 0.0
    marker.pose.orientation.w = 1.0
    


    while not rospy.is_shutdown():
       
       
        #----------------- For When getting x,y and z single points from controller node-------------------
        # if(x != 0 or y!=0 or z!=0):

        #     cloud_points.append([x, y, z])

        
        # if (len(cloud_points) > number_of_data_poins):

        #     del(cloud_points[0])


        # #create pcl from points
        # scaled_polygon_pcl = pcl2.create_cloud_xyz32(header, cloud_points)

        # pcl_pub.publish(scaled_polygon_pcl)
        #--------------------------------------------------------------------------------------


        #create pcl from points
        for i in range(len(x)):

            if(x[i] != 0 or y[i]!=0 or z[i]!=0):
                cloud_points.append([x[i], y[i], z[i]])

            if (len(cloud_points) > number_of_data_poins):
                #del(cloud_points[0])
                cloud_points.pop(0)

        scaled_polygon_pcl = pcl2.create_cloud_xyz32(header, cloud_points)
        pcl_pub.publish(scaled_polygon_pcl)

     rate.sleep()

    rospy.spin()


        

