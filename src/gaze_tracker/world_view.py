## default path for saving recordings => C:\Users\ASUS\recordings
## changed the path to this => E:\SHiTU\programming\projects\gazeTracker\Gaze-Tracker\src\gaze_tracker\world_camera_capture\world_video_capture

import cv2
import sys
import zmq
from time import sleep 
import os
import shutil

def delete_contents(folder_path):
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        try: 
            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
        except:
            print(f"Nothing in {item_path} found")
            exit()


path_to_project_dir = os.path.abspath(__file__)
script_directory = os.path.dirname(path_to_project_dir)
WorldVideo_path = script_directory+'\world_camera_capture\world_video_capture'
World_image_path = script_directory + '\world_camera_capture\world_frames'
image_path = World_image_path + '\world_frame_image.jpg'

## delete previous frames
delete_contents(WorldVideo_path)
delete_contents(World_image_path)
print("The folder inside World_capture_path has been deleted.")


### number of frames per second for world camerax
worldCamera_Fps = 30
video_lenght = 3 ## second
frame_number =int((worldCamera_Fps * video_lenght)/2) ### the middle frame to save

context = zmq.Context()
pupil_remote = zmq.Socket(context, zmq.REQ)
### Local Host and Default IP address for Pupil Core Software
pupil_remote.connect('tcp://127.0.0.1:50020')

### Start recording
pupil_remote.send_string('R')
print(pupil_remote.recv_string())

sleep(video_lenght)
### Stop recording
pupil_remote.send_string('r')
print(pupil_remote.recv_string())
### time to save the file
sleep(0.05)


### path to the recorded videos --- The sub_folder name changes day by day --- it's based on date
sub_folder_name = next(name for name in os.listdir(WorldVideo_path))
path_to_subFolder = os.path.join(WorldVideo_path, sub_folder_name)
record_folder_name = next(name for name in os.listdir(path_to_subFolder))
records_path = os.path.join(path_to_subFolder, record_folder_name) 
World_captured_video_path = records_path + '\world.mp4'

cap = cv2.VideoCapture(World_captured_video_path)
# cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()
ret, frame = cap.read()
if ret:
    # Save the frame as an image
    cv2.imwrite(image_path, frame)
    print(f"Frame {frame_number} saved as {image_path}")
    sleep(0.05)
else:
    print(f"Error: Could not read frame {frame_number}.")

# Release the VideoCapture object
cap.release()

