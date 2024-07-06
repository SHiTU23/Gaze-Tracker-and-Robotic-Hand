## default path for saving recordings => C:\Users\ASUS\recordings
## changed the path to this => E:\SHiTU\programming\projects\gazeTracker\Gaze-Tracker\src\gaze_tracker\world_camera_capture\world_video_capture

import cv2
import sys
import zmq
from time import sleep 
import os
import shutil
### NOTE If you want to run this code, remove '.gaze_tracker' from import
from gaze_tracker.gaze_tracker import gaze_data 
import time

class capture_world:
    _path_to_project_dir = os.path.abspath(__file__)
    _script_directory = os.path.dirname(_path_to_project_dir)
    _WorldVideo_path = _script_directory+'\world_camera_capture\world_video_capture'
    _World_image_path = _script_directory + '\world_camera_capture\world_frames'
    image_path = _World_image_path + '\world_frame_image.jpg'

    def __init__(self, worldCamera_Fps = 30):
        '''
            worldCamera_Fps: world Fps shown in Pupil core software
            Change the save path in Pupil software to absolute path to 'Gaze-Tracker\src\gaze_tracker\world_camera_capture\world_video_capture' dir
        '''
        self._gaze = gaze_data()
        self._gaze_on_world = [0,0,0]

        self._worldCamera_Fps = worldCamera_Fps
        self._video_lenght = 1 ## second
        self._frame_number = 0

        ## delete previous frames
        self.delete_contents(self._WorldVideo_path)
        self.delete_contents(self._World_image_path)
        print("The folder inside World_capture_path has been deleted.")

        ### Start connecting to Pupil Core software
        _context = zmq.Context()
        self._pupil_remote = zmq.Socket(_context, zmq.REQ)
        ### Local Host and Default IP address for Pupil Core Software
        self._pupil_remote.connect('tcp://127.0.0.1:50020')

    def capture(self, length_of_capture=1):
        '''
         length of capture: length of video in seconds
        '''
        ### number of frames per second for world camerax
        self._video_length = length_of_capture ## second
        _pause_time = self._video_length / 2

        ### Start recording
        self._pupil_remote.send_string('R')
        print(self._pupil_remote.recv_string())

        start_time = time.time()

        ### take the middle frame gaze data
        sleep(_pause_time)
        ### Norm value for gaze on world
        self._gaze_on_world = self._gaze.worldGaze_norm()
        print(f"gaze from class: {self._gaze_on_world}")
        sleep(_pause_time)
        end_time = time.time()
        print(f'time: {end_time-start_time}')

        ### Stop recording
        self._pupil_remote.send_string('r')
        print(self._pupil_remote.recv_string())

        ### time to save the file
        sleep(0.05)

    def gaze_pose_onWorld(self):
        return self._gaze_on_world
    
    def save_frame(self):      
        ### path to the recorded videos --- The sub_folder name changes day by day --- it's based on date
        _sub_folder_name = next(name for name in os.listdir(self._WorldVideo_path))
        _path_to_subFolder = os.path.join(self._WorldVideo_path, _sub_folder_name)
        _record_folder_name = next(name for name in os.listdir(_path_to_subFolder))
        _records_path = os.path.join(_path_to_subFolder, _record_folder_name) 
        _World_captured_video_path = _records_path + '\world.mp4'

        ### the frame middle of the captured video
        self._frame_number = int((self._worldCamera_Fps * self._video_length)/2)

        cap = cv2.VideoCapture(_World_captured_video_path)
        cap.set(cv2.CAP_PROP_POS_FRAMES, self._frame_number)
        if not cap.isOpened():
            print("Error: Could not open video.")
            exit()
        
        _ret, _frame = cap.read()
        if _ret:
            # Save the frame as an image
            cv2.imwrite(self.image_path, _frame)
            sleep(0.05)
            return self.image_path
        else:
            print(f"Error: Could not read frame.")
        cap.release()
        
    def delete_contents(self, folder_path):
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)

            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)


if __name__=='__main__':
    world_view = capture_world()
    world_view.capture()
    print(f"gaze pose: {world_view.gaze_pose_onWorld()}")
    world_view.save_frame()
