import zmq
from time import sleep 

context = zmq.Context()
pupil_remote = zmq.Socket(context, zmq.REQ)
### Local Host and Default IP address for Pupil Core Software
pupil_remote.connect('tcp://127.0.0.1:50020')

### Start recording
pupil_remote.send_string('R')
print(pupil_remote.recv_string())

sleep(5)
### Stop recording
pupil_remote.send_string('r')
print(pupil_remote.recv_string())