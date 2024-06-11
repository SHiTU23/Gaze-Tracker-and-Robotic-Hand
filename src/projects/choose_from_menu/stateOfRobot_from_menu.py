############################################
#   Choose the mode of the robotic hand    #
#     from the menu by gazing at opetions  #
###                                      ###
###  Author: https://github.com/SHiTU23  ###
############################################

import pygame
import numpy as np

from menu import hand_operation_menu, options_position
import sys
import os
### Going to gaze tracker directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from gaze_tracker.gaze_tracker import gaze_data


pygame.init()

menu_open_option = hand_operation_menu()
menu_close_option = hand_operation_menu()

gaze = gaze_data()


running = True
menu_open_option.add_menu(options_position.center_left, color=(10, 150, 10), text='Open Fingers')
menu_close_option.add_menu(options_position.center_right, color=(200, 10, 10), text='Close Fingers')

while running:
    gaze_coordinate = gaze.gaze_coordinate_on_surface()
    print(f"mouse pose: {gaze_coordinate}")

    if menu_open_option.clicked(gaze_coordinate):
        print("open option clicked")
    elif menu_close_option.clicked(gaze_coordinate):
        print("close option clicked")

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
            running = False
pygame.quit()
