Hardware models used:

Hokuyo URG-04LX-UG01 
Dynamixel MX-28 Servo Motor
USB2Dynamixel and the USB to Dynamixel adapter
NUC


Setting up the hardware:

1) Plug in the USB port into the USB2Dynamixel and the NUC

2) Plug in the power cable into to the USB to Dynamixel adapter and an outlet 

3) Plug the LIDAR to USB cable into the LIDAR and the NUC

4) Connect the 3 pin cable to the servo motor and the USB to Dynamixel adapter


Required softwares to run this project:

Ubuntu 14.04

ROS indigo

Python 2.7

Hokuyo ROS package
(http://wiki.ros.org/hokuyo_node/Tutorials/UsingTheHokuyoNode)

Use the servo_lidar_test package to run the main code (“https://github.com/adr288/Capstone-LIDAR-Project-GCC”)

Setting up the software:

To start:

1) First we need to have open 3 terminal windows in ubuntu. (Ctrl + shift  + T adds a new terminal tab)

2) In the first terminal enter " roscore" command (type “roscore” + press enter)


3) 

   3.1) If running the ubuntu on a virtual machine, in terminal two first type “sudo chmod 777 /dev/ttyACM0”. Then enter the system password (Skip this section if not using virtual machine) If an error occurs, wait 10 seconds and unplug the lidar cable. Then plug it back in.

   3.2)After that, while still in the second terminal, enter “rosrun hokuyo_node hokuyo_node”. If a red error text appears, wait 5 minutes for the code to self troubleshoot. If the LIDAR doesn’t start scanning, press ctrl + c. and do this step again.

4) In terminal three, enter “roslaunch servo_lidar_test servo_lidar_test.launch” then press Enter, it should start working/scanning. If we want to save the scanned image, we can do that in rviz by pressing File→ Save Image
To stop running, terminate terminal 3 (ctrl + c) ,
If we want it to run again, do step 4.
Once finished for the day, terminate the lidar, then
 terminate roscore and close all the terminals.

Ctrl+ C to terminate code/program
When writing command in the terminal, hitting tab midway through a word will auto fill the remaining word


