#!/usr/bin/env python
import os 
from lib_robotis import * 
import os.path 
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from sensor_msgs.msg import LaserScan
import numpy as np

import rospy
from std_msgs.msg import String
from servo_lidar_test.msg import Num
from servo_lidar_test.msg import servo
 
 #-----------------------------------------------------------------
 #Need this part to be able to run the servo
dyn = USB2Dynamixel_Device('/dev/ttyUSB0')
servo_offset= math.radians(-20)
p = Robotis_Servo( dyn, 1, series = "MX" )
myRanges= []

#Lidar callback function
def get_lidar_data(msg):
  global myRanges    # Needs to be global to be used in the main
  myRanges = msg.ranges[:]
  
  




#-------------------------------------------------------------------
#--------------------Our main is defined here----------------------- 
def main():


#-------------------------------------------------------------------
#---------------------------Variables-------------------------------
  define_rate = 20
  #amount that servo reads is not the same as the amount the servo moves
  #to make sure servo moves to our desired ranges, we have added this offset
  upperBound= 4000 #2700 in bits
  lowerBound= 1000 #1900 in bits
  boundOffset= 500 #amount that servo reads is not the same as the amount the servo moves so 
  #to make sure servo moves to our desired ranges, we have added this offset
  home=0 #in radians
  servo_speed = 0.5 # radians/sec
  nuberOfDataPoints = 501




  arrayOfServoPositions = [0]
  interpolatedAnarrayOfServoPositions = []



#--------------------------------------------------
# Subscriber Setup
#--------------------------------------------------
  rospy.Subscriber("/scan", LaserScan, get_lidar_data)


#--------------------------------------------------------------------
#--------------------------Publisher node----------------------------
  servo_pub = rospy.Publisher('servo_cmd', servo, queue_size=10)
#(topic name, message file(.srv) name, and queue size)

#---------------------------------------------------------------------
#If you want to recieve what position the servo should go to create the rest of this part 
#rospy.Subscriber("controller", controller, callbackThree) #what position to go


#--------------------------------------------------------------------
#--------------------------Node Name---------------------------------
  rospy.init_node('servo_test')


#--------------------------------------------------------------------
#----------------------Setting the rate---------------------------
  rate = rospy.Rate(define_rate)


#------------------------Code starts running here--------------------
  msg3 = servo() #accessing the variable names in the servo message file 
    
  count = 0

  p.move_angle(home + servo_offset) #offset because of the shaft 
  print(math.degrees(p.read_angle())) 
  p.set_angvel(servo_speed) #speed of the servo motor

  while not rospy.is_shutdown(): 
      
   nuberOfDataPoints = len(myRanges)
   #print(len(myRanges))
   while count < upperBound and not rospy.is_shutdown(): #Going from encoder position 0 to 2500
     
     p.move_to_encoder(upperBound + boundOffset) #Making sure servo moves to the max encoder position 2500
     msg3.servoAngle = p.read_angle() + servo_offset #assigns the angle read to the variable servoAngle
     
     #-------------Interpolating Array---------------#
     index = np.linspace(0, 1,num = 2, endpoint=True)
     arrayOfServoPositions.append(p.read_angle() + servo_offset)
     #rospy.loginfo(arrayOfServoPositions)
     f = interp1d(index, arrayOfServoPositions)
     indexNew = np.linspace(0, 1, num = nuberOfDataPoints, endpoint=True)
     interpolatedAnarrayOfServoPositions = f(indexNew)
     #rospy.loginfo(interpolatedAnarrayOfServoPositions)
     

    
     #-------------Publishing Array---------------#
     msg3.arrayOfServoAngles = interpolatedAnarrayOfServoPositions[:]
     count = p.read_encoder() #Count changes as servo is going to 4000 
     servo_pub.publish(msg3)
     #rospy.loginfo(len(interpolatedAnarrayOfServoPositions))
     arrayOfServoPositions.pop(0)
     #arrayOfServoPositions.append(p.read_angle() + servo_offset)
     rate.sleep()
    

   #servo_pub.publish(msg3)
   #rospy.loginfo(len(arrayOfServoPositions))

   while count > lowerBound and not rospy.is_shutdown(): #Going back down from encoder position 2500
      p.move_to_encoder(boundOffset - upperBound) #making sure servo goes down by addign the offset
      msg3.servoAngle = p.read_angle() + servo_offset

      #-------------Interpolating Array---------------#
      index = np.linspace(0, 1,num = 2, endpoint=True)
      arrayOfServoPositions.append(p.read_angle() + servo_offset)
      #rospy.loginfo(arrayOfServoPositions)
      f = interp1d(index, arrayOfServoPositions)
      indexNew = np.linspace(0, 1, num = nuberOfDataPoints, endpoint=True)
      interpolatedAnarrayOfServoPositions = f(indexNew)
      #rospy.loginfo(interpolatedAnarrayOfServoPositions)

      #-------------Publishing Array---------------#
      msg3.arrayOfServoAngles = interpolatedAnarrayOfServoPositions[:]
      count = p.read_encoder() 
      servo_pub.publish(msg3)
      #rospy.loginfo(len(interpolatedAnarrayOfServoPositions))
      arrayOfServoPositions.pop(0)
      #arrayOfServoPositions.append(p.read_angle() + servo_offset)
      rate.sleep()


   #plt.show()  
   
  rospy.spin()
  
if __name__ == '__main__':
        try:  
          main()
            
        finally:
          #Homing After Cancelation of code
          p.move_to_encoder(2300)


      