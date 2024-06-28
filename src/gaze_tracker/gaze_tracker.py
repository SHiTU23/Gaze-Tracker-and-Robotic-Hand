import zmq
import msgpack
from time import sleep


class gaze_data:
    def __init__(self, ip='localhost', port=50020):
        """
            port : The port defaults to 50020. Set in Pupil Capture GUI.
        """
        self.ip_address = ip
        self._ctx = zmq.Context()
        # The REQ talks to Pupil remote and receives the session unique IPC SUB PORT
        _pupil_remote = self._ctx.socket(zmq.REQ)
        _pupil_remote.connect(f'tcp://{self.ip_address}:{port}')

        # Request 'SUB_PORT' for reading data
        _pupil_remote.send_string('SUB_PORT')
        self._sub_port = _pupil_remote.recv_string()

    def gaze_coordinate(self):
        """
            Return Value: gaze 3d coordinate [x, y, z]
        """
        _subscriber = self._ctx.socket(zmq.SUB)
        _subscriber.connect(f'tcp://{self.ip_address}:{self._sub_port}')
        _subscriber.subscribe('gaze.')  # receive all gaze messages

        topic, _payload = _subscriber.recv_multipart()
        message = msgpack.loads(_payload)
        gaze_position = message[b'gaze_point_3d']
        
        # print(f"message: {message}")
        return gaze_position
    
    def worldGaze_norm(self):
        """
            Return Value: gaze 2d coordinate [x, y] from 0-1
            x dir: leftside = 0, right = 1
            y dir: up = 1, down = 0
        """
        _subscriber = self._ctx.socket(zmq.SUB)
        _subscriber.connect(f'tcp://{self.ip_address}:{self._sub_port}')
        _subscriber.subscribe('gaze.')  # receive all gaze messages

        topic, _payload = _subscriber.recv_multipart()
        message = msgpack.loads(_payload)
        gaze_position = message[b'norm_pos']
        
        return gaze_position

    def gaze_coordinate_on_surface(self):
        """
            Return Value: Norm position of gaze on serface [x, y]

            - You need to calibrate a serface in Pupil Software 
        """
        _subscriber = self._ctx.socket(zmq.SUB)
        _subscriber.connect(f'tcp://{self.ip_address}:{self._sub_port}')
        _subscriber.subscribe('surfaces.')

        topic, _payload = _subscriber.recv_multipart()
        message = msgpack.loads(_payload)
        # print(message)
        gaze_position = message[b'gaze_on_surfaces'][0][b'norm_pos'] ### [x, y]
        # print(f"gaze on surface: {gaze_position}") ### The whole data
        return gaze_position



if __name__ == "__main__":
    gaze_data = gaze_data()

    while True:
        # surface_data = gaze_data.gaze_coordinate_on_surface()
        # print(f"surface: {surface_data}") ### norm value of position(from 0 to 1)

        gaze_pose = gaze_data.gaze_coordinate()
        print(f"gaze: {gaze_pose}")

        print("################################### next ###########################################")

        sleep(3)
