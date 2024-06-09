#####################################################################
##           Example code for using the Hand_contro class          ##
#####################################################################
### scanning range ###
##      is a range that includes all motorIDs,
##      here, I know that motorIDs are 21, 23, 25, 27 and 29,
##      however, motorID 21 is not connected to any part in RoboticHand.
### goTo_multiple ###
##      takes a dictionary containing motor name and destination angle
##      the dict can have any number of motors, it can be two, or all four motors
### Motor_Name ###
##      Instead of passing a string of the motor name to "goTo" functions, 
##      use "Motor_Name" Enum.
### open_fingers and close_fingers ###
##      These modules have defult values of -150 and 150, respectively,
##      however, it can be changed by passed another angle to their arguments
#####################################################################

from robotic_hand_controlClass import *
from time import sleep

motorID_scanningRange = [10, 35]
hand = hand_control(motorID_scanningRange)
hand.goTo_homePose()

sleep(2)
hand.all_motors_goTo_Pose(100)

sleep(2)
hand.goTo_single(Motor_Name.thumb, 45)

sleep(2)
motors = {Motor_Name.middle_fingers:100, Motor_Name.wrist_BF:150}
hand.goTo_multiple(motors)

sleep(2)
hand.open_fingers()
sleep(2)
hand.close_fingers(-100)