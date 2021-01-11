#!/usr/bin/env python

import rospy
import math
from std_msgs.msg import String
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from servo_lidar_test.msg import Num
from servo_lidar_test.msg import pointCloud
from servo_lidar_test.msg import servo
from servo_lidar_test.srv import controller_client

#Lidar And servo variables used in the controller node
myRanges= []
angleOfIncrement = 0
startAngle = 0
lidarAngleOffset = math.pi / 2.0 # Offseting lidar rays' angles by 90 degrees 


servoAngle = 0
servoOffset = 0.3316 # Offseting servo
start_scan = 1
arrayOfServoAngles = []



#Lidar callback function
def get_lidar_data(msg):
    global myRanges    # Needs to be global to be used in the main
    global angleOfIncrement
    global startAngle
    global rangeTime

    myRanges = msg.ranges[:]
    angleOfIncrement = msg.angle_increment
    startAngle = msg.angle_min
    rangeTime = msg.header
    #rospy.loginfo(myRanges)
     
#servo callback function
def get_servo_data(msg):
    global servoAngle
    global servoTime
    global arrayOfServoAngles

    servoTime = msg.header
    servoAngle = msg.servoAngle + servoOffset
    arrayOfServoAngles = msg.arrayOfServoAngles[:]

    #print(servoTime)
     
# server callback funtion (To be developed)
def handle_start(req):
    start_scan = req.start 
    print  (req.start)
    return (req.start)


def main():

    rospy.init_node('controller_test')  #Node name in ROS
    s = rospy.Service('controller_service_name', controller_client, handle_start) # Service setup (to be developed)
    controller_publish_rate = 40 #  contrller node Publish Rate Hz
   
    #t = input('hi, should I start Scanning?') #input from user node(to be developed)
    print("Starting the controller node.....")
   
    #coordinates = []  # Can be used if publishing one point at a time
    x = []
    y = []
    z = []

    #Max and Min range to be pubblished by the controller node
    RangeMax = 2 
    RangeMin = 0.1


    
   
    #--------------------------------------------------
    # Publisher Setup
    #--------------------------------------------------
    pub = rospy.Publisher('pointCloud', pointCloud, queue_size=10)
   

    #--------------------------------------------------
    # Subscriber Setup
    #--------------------------------------------------
    rospy.Subscriber("/scan", LaserScan, get_lidar_data)
    rospy.Subscriber("servo_cmd", servo, get_servo_data)
    
    
    rospy.sleep(2.)
    rate = rospy.Rate(controller_publish_rate) 
    print("controller node started!")
    
    msg = pointCloud()          #Copying poindCloud message into msg variable
    #msg.pointCloudRanges = []  #Can be used if publishing one point at a time

    #Defining the node header 
    msg.header.stamp = rospy.Time.now()
    msg.header.frame_id = 'controller'

    

    #--------------------------------------------------
    # Loop
    #--------------------------------------------------
    
    while not rospy.is_shutdown():
        
        rayAngle = startAngle  #Assinging the initial angle of the publishing array
        index = 0              #counter

        for r in myRanges:

            rayAngle = startAngle + index * angleOfIncrement + lidarAngleOffset 
            #incrementedServoAngle = servoAngle + index * 0.000117 # interpolating the servo angle 

            
            
             
            if(r > RangeMax or r < RangeMin):     #If the lidar range is out of desired range assign zero to it
                r = 0 

            #------------Changing from polar to cartesian coordinates----------

            #------------To publish single coordinates of x,y,z------------
            # y.append(r * math.cos(servoAngle) * math.sin(rayAngle))
            # z.append (r * math.sin(servoAngle) * math.sin(rayAngle))
            # x.append(r * math.cos(rayAngle))

            #y.append(r * math.cos(incrementedServoAngle) * math.sin(rayAngle))
            #z.append (r * math.sin(incrementedServoAngle) * math.sin(rayAngle))
            #x.append(r * math.cos(rayAngle))
            #--------------------------------------------------------------
            
            #-------------------Using Servo Array--------------------------
            #rospy.loginfo(arrayOfServoAngles[index])
            x.append(r * math.cos(arrayOfServoAngles[index]) * math.sin(rayAngle)) #
            y.append (r * math.sin(arrayOfServoAngles[index]) * math.sin(rayAngle))
            z.append(r * math.cos(rayAngle))
            index = index + 1
            #rospy.loginfo(index)
            #rospy.loginfo(len(myRanges))
            


        msg.x = x[:]
        msg.y = y[:]
        msg.z = z[:]
            
        #Publishing the coordinates
        pub.publish(msg)
        del x[:]
        del y[:]
        del z[:]

        

    
        rate.sleep()

         
        
    rospy.spin()

if __name__ == '__main__':
           
        main()