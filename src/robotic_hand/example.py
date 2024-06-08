from robotic_hand_controlClass import *
from time import sleep

motorID_scanningRange = [10, 35]
hand = hand_control(motorID_scanningRange)
hand.goTo_homePose()

sleep(2)

hand.open_fingers()
sleep(2)
hand.close_fingers()