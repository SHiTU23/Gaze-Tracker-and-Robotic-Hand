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
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)

### worldCamera_Fps is set in Pupil Core software
# world = capture_world(worldCamera_Fps=30)
# capture_length = 1 ## second **min of 0.7**
# world.capture(capture_length)
# world_image_path = world.save_frame()

world_image_path = './detected_image.jpg'
### detect objects in the image
img = cv2.imread(world_image_path)
objects = object_detection()
obj_data = objects.detect(img) ### [{'boundry_box':[center_x, center_y, w, h], 'name':'laptop'}, ....]

### show the image on screen
world_image = pygame.image.load(world_image_path).convert()

world_image_width = world_image.get_width()
world_image_height = world_image.get_height()
print(f"w:{world_image_width}, h:{world_image_height}")

# gaze_point_norm = world.gaze_pose_onWorld() ###[x,y]
gaze_point_norm = [0.1, 0.1]

### map normal values to image dimension
gaze_point_x = int(np.interp(gaze_point_norm[0], [0, 1], [0, world_image_width]) )
gaze_point_y =int(abs(world_image_height - (np.interp(gaze_point_norm[1], [0,1], [0, world_image_height]))))
gaze_point = (gaze_point_x, gaze_point_y)
print(f"gaze: {gaze_point_norm}, mapped_x: {gaze_point}")

### draw the gaze point on the image
radius = 10
color = (0, 0, 255)  # red color in BGR
thickness = 20
cv2.circle(img, gaze_point, radius, color, thickness)
### draw a bounding box around the gazed obj
if objects.is_on_object(gaze_point):
    print(objects.is_on_object(gaze_point))
    obj_data = objects.is_on_object(gaze_point)
    bounding_box = obj_data['boundry_box'] ###[center_x, center_y, w, h]
    print(bounding_box)

    ### convert tensor int to regular int
    x, y, w, h = bounding_box[0].item(), bounding_box[1].item(), bounding_box[2].item(), bounding_box[3].item()
    start_point = (x-int(w/2), y-int(h/2)) ## top left corner
    end_point = (x+int(w/2), y+int(h/2))
    print(x, y, w, h)
    cv2.rectangle(img, start_point, end_point, color, 2) 
cv2.imwrite('./detected_image3.jpg', img)




'''
running = True
while running:
    screen.blit(world_image, (0, 0))
    pygame.display.update()
    pygame.display.flip()

    pygame.draw.circle(screen, (255, 0, 0), (x, y), 10)
    pygame.display.update()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
            running = False
pygame.quit()
'''