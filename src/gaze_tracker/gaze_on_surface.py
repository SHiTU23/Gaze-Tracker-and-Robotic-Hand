import zmq
import msgpack
from time import sleep
ctx = zmq.Context()
# The REQ talks to Pupil remote and receives the session unique IPC SUB PORT
pupil_remote = ctx.socket(zmq.REQ)

ip = 'localhost'  # If you talk to a different machine use its IP.
port = 50020  # The port defaults to 50020. Set in Pupil Capture GUI.

pupil_remote.connect(f'tcp://{ip}:{port}')

# Request 'SUB_PORT' for reading data
pupil_remote.send_string('SUB_PORT')
sub_port = pupil_remote.recv_string()

# Request 'PUB_PORT' for writing data
pupil_remote.send_string('PUB_PORT')
pub_port = pupil_remote.recv_string()

while True:
    subscriber = ctx.socket(zmq.SUB)
    subscriber.connect(f'tcp://{ip}:{sub_port}')
    subscriber.subscribe('surfaces.')

    topic, payload = subscriber.recv_multipart()
    message = msgpack.loads(payload)
    
    print(f"{topic}: {message}") ### The whole data
    ### Coordinates of the point that is being looked at:
    print(message[b'gaze_on_surfaces'][0][b'norm_pos']) ### Valur between 0 - 1
    sleep(3)