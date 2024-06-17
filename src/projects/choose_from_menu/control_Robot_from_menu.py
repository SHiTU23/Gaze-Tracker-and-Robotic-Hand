####################################################################
#             Choose the mode of the robotic hand                  #
#             from the menu by gazing at opetions                  #
####################################################################
# **** Before using this code, 
#  1. Find the screen dimentions given by gaze tracker:
#       Run gaze_tracker.py and look at each corner of your screen. 
#       Store your numbers as x_min x_max, y_min and y_max. 
#  2. Find motors IDs:
#       Run RoboPlus software to find the range of motor IDs
####################################################################
###   Author: https://github.com/SHiTU23                         ###
####################################################################

import pygame
import numpy as np

from menu import hand_operation_menu, options_position
import sys
import os
from time import sleep
### Going to gaze tracker directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from gaze_tracker.gaze_tracker import gaze_data
from robotic_hand.robotic_hand_controlClass import hand_control


pygame.init()

### Robotic Hand Motor control
motorID_scanningRange = [10, 35]
robotic_hand = hand_control(motorID_scanningRange)
robotic_hand.goTo_homePose()

### Menu options
menu_open_option = hand_operation_menu()
menu_close_option = hand_operation_menu()

### Gaze Tracker data
gaze = gaze_data()

running = True
menu_open_option.add_menu(options_position.center_left, color=(10, 150, 10), text='Open Fingers')
menu_close_option.add_menu(options_position.center_right, color=(200, 10, 10), text='Close Fingers')

gaze_choice = ''
last_gaze_choice = ''

while running:
    gaze_coordinate = gaze.gaze_coordinate_on_surface()
    print(f"gaze pose: {gaze_coordinate}")
    if menu_open_option.clicked(gaze_coordinate):
        gaze_choice = 'open'
    elif menu_close_option.clicked(gaze_coordinate):
        gaze_choice = 'close'
    else:
        gaze_choice = 'out'

    if gaze_choice != last_gaze_choice and gaze_choice == 'open' and gaze_choice!='out':
        last_gaze_choice = gaze_choice
        robotic_hand.open_fingers()
        print("open option clicked")
    elif gaze_choice != last_gaze_choice and  gaze_choice == 'close'and gaze_choice!='out':
        last_gaze_choice = gaze_choice
        robotic_hand.close_fingers()
        print("close option clicked")
    elif gaze_choice == 'out':
        last_gaze_choice = gaze_choice
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
            running = False
pygame.quit()
