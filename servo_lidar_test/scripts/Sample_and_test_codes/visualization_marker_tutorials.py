#!/usr/bin/env python

import roslib; roslib.load_manifest('visualization_marker_tutorials')
from visualization_msgs.msg import Marker
from visualization_msgs.msg import MarkerArray
import rospy
import math
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


#--------------------------------------------------
# Subscriber Setup
#---------------------------------------------------
rospy.Subscriber('pointCloud', pointCloud, get_pointCloud_coordinates) 




topic = 'visualization_marker_array'
publisher = rospy.Publisher(topic, MarkerArray, queue_size=100)

rospy.init_node('register')

markerArray = MarkerArray()

count = 0
MARKERS_MAX = 1000



while not rospy.is_shutdown():

  marker = Marker()
  marker.header.frame_id = "/neck"
  marker.type = marker.SPHERE
  marker.action = marker.ADD
  marker.scale.x = 0.05
  marker.scale.y = 0.05
  marker.scale.z = 0.05
  marker.color.a = 5.0
  marker.color.r = 1.0
  marker.color.g = 1.0
  marker.color.b = 0.0
  marker.pose.orientation.w = 1.0

  for i in range(len(x)): 
  
   if(x[i] != 0 or y[i]!=0 or z[i]!=0):

     marker.pose.position.x = x[i]
     marker.pose.position.y = y[i] 
     marker.pose.position.z = z[i]

     #if(count > MARKERS_MAX):
       #markerArray.markers.pop(0)
  
     markerArray.markers.append(marker)
  
     id = 0
     for m in markerArray.markers:
       m.id = id
       id += 1

      # Publish the MarkerArray
     publisher.publish(markerArray)

     count += 1

  rospy.sleep(0.01)