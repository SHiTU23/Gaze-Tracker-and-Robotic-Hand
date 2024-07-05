####################################################################
## In this project, all objects that are looked at will be shown by
## drawing a rectangle arounf it
## default path for saving recordings => C:\Users\ASUS\recordings
## changed the path to this => E:\SHiTU\programming\projects\gazeTracker\Gaze-Tracker\src\gaze_tracker\world_camera_capture\world_video_capture
####################################################################
###   Author: https://github.com/SHiTU23                         ###
#################################################################### 

import os
import sys
import pygame
import numpy as np
import cv2
from object_detection_YOLO import object_detection

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from gaze_tracker.world_view import capture_world

pygame.init()
# screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
screen_width=1280
screen_height=720
screen=pygame.display.set_mode([screen_width, screen_height])
font_size = 36
font = pygame.font.SysFont(None, font_size)  

'''
### worldCamera_Fps is set in Pupil Core software
world = capture_world(worldCamera_Fps=30)
capture_length = 1 ## second **min of 0.7**
world.capture(capture_length)
world_image_path = world.save_frame()

### detect objects in the image
img = cv2.imread(world_image_path)
objects = object_detection()
obj_data = objects.detect(img) ### [{'boundry_box':(x, y, w, h), 'name':'laptop'}, ....]

### load the image for its dimension
world_image = pygame.image.load(world_image_path).convert()
world_image_width = world_image.get_width()
world_image_height = world_image.get_height()
print(f"w:{world_image_width}, h:{world_image_height}")

### get gaze position
gaze_point_norm = world.gaze_pose_onWorld() ###[x,y]

### map normal values to image dimension
gaze_point_x = int(np.interp(gaze_point_norm[0], [0, 1], [0, world_image_width]) )
gaze_point_y =int(abs(world_image_height - (np.interp(gaze_point_norm[1], [0,1], [0, world_image_height]))))
gaze_point = (gaze_point_x, gaze_point_y)
print(f"gaze: {gaze_point_norm}, mapped_x: {gaze_point}")
'''

### draw the gaze point on the image
gaze_point_color = (255, 0, 0)  # red color in rgb
bounding_box_color = (0, 255, 0)
gaze_point_thickness = 10
bounding_box_thickness = 5

detected_obj = ''



running = True
while running:
    #######################################################################
    ######             GET THE WORLD IMAGE AND GAZE POSE              #####
    #######################################################################

    ### worldCamera_Fps is set in Pupil Core software
    world = capture_world(worldCamera_Fps=30)
    capture_length = 0.7 ## second **min of 0.7**
    world.capture(capture_length)
    world_image_path = world.save_frame()

    ### detect objects in the image
    img = cv2.imread(world_image_path)
    objects = object_detection()
    obj_data = objects.detect(img) ### [{'boundry_box':(x, y, w, h), 'name':'laptop'}, ....]
    print("objs:", obj_data)

    ### load the image for its dimension
    world_image = pygame.image.load(world_image_path).convert()
    world_image_width = world_image.get_width()
    world_image_height = world_image.get_height()

    ### get gaze position
    gaze_point_norm = world.gaze_pose_onWorld() ###[x,y]

    ### map normal values to image dimension
    gaze_point_x = int(np.interp(gaze_point_norm[0], [0, 1], [0, world_image_width]) )
    gaze_point_y =int(abs(world_image_height - (np.interp(gaze_point_norm[1], [0,1], [0, world_image_height]))))
    gaze_point = (gaze_point_x, gaze_point_y)
    print(f"gaze: {gaze_point_norm}, mapped_x: {gaze_point}")

    #######################################################################
    ######                  SHOW THE IMAGE ON SCREEN                  #####
    #######################################################################

    ### show the world_image on screen
    screen.blit(world_image, (0, 0))

    ### draw the gazed point on the image
    pygame.draw.circle(screen, gaze_point_color, (gaze_point_x, gaze_point_y), gaze_point_thickness)

    for obj in obj_data:
        boundry_box = obj['bounding_box'] ###(x, y, w, h)
        obj_bound_box = pygame.Rect(boundry_box)
        pygame.draw.rect(screen, (100, 100, 100), obj_bound_box, bounding_box_thickness)


    ### check if an object is being looked at
    if objects.is_on_object(gaze_point):
        obj_data = objects.is_on_object(gaze_point)
        obj_name = obj_data['name']
        print(f"Gazed Object is {obj_name}")


        ### draw a bounding box around the gazed obj
        bounding_box = obj_data['bounding_box'] ###(x, y, w, h)
        obj_bounding_box = pygame.Rect(bounding_box)
        pygame.draw.rect(screen, bounding_box_color, obj_bounding_box, bounding_box_thickness)
        ### write object's name
        text_surface = font.render(obj_name, True, bounding_box_color)
        screen.blit(text_surface, (bounding_box[0]+20, bounding_box[1]+10))

    pygame.display.update()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
            running = False
pygame.quit()
