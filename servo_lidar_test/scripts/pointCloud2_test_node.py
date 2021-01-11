#!/usr/bin/env python
import rospy
import math
import sys
import struct

from visualization_msgs.msg import Marker
from visualization_msgs.msg import MarkerArray

from _collections import deque, defaultdict

from sensor_msgs import point_cloud2
from sensor_msgs.msg import PointCloud2, PointField
from std_msgs.msg import Header
import std_msgs.msg
import sensor_msgs.point_cloud2 as pcl2
from servo_lidar_test.msg import pointCloud
import sensor_msgs.point_cloud2 as pc2


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

    pointCloude_publish_rate = 40
    number_of_data_poins = 80000 # Number of data points to be published


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
    points = []
  
    


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
                #cloud_points.append(x[i], y[i], z[i],0) #For When the colors are not included
                pt = [x[i],y[i],z[i],0]
                r = int(200)
                g = int(0)
                b = int(0)
                a = 255
                #print r, g, b, a
                rgb = struct.unpack('I', struct.pack('BBBB', b, g, r, a))[0]
                #print hex(rgb)
                pt[3] = rgb
                points.append(pt)


            if (len(points) > number_of_data_poins):
                #del(cloud_points[0])
                points.pop(0)
        
        fields = [PointField('x', 0, PointField.FLOAT32, 1),
          PointField('y', 4, PointField.FLOAT32, 1),
          PointField('z', 8, PointField.FLOAT32, 1),
          PointField('rgb', 12, PointField.UINT32, 1),
          # PointField('rgba', 12, PointField.UINT32, 1),
          ]

        #scaled_polygon_pcl = pcl2.create_cloud_xyz32(header, cloud_points) #For When the colors are not included
        scaled_polygon_pcl = point_cloud2.create_cloud(header, fields, points)
        pcl_pub.publish(scaled_polygon_pcl)

        rate.sleep()

    rospy.spin()


        

