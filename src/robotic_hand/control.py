import pypot.dynamixel

from enum import Enum
from time import sleep

ports = pypot.dynamixel.get_available_ports()
print('available ports:', ports)

if not ports:
    raise IOError('No port available.')

port = ports[-1] ### COM6 : The port that hand is connetd to
dxl_io = pypot.dynamixel.DxlIO(port)
print('Connected!')

### I know that motor Ids are from 21 to 29
### So the range for scannign would close to these number 
motor_IDs = dxl_io.scan(range(10, 35))
del motor_IDs[0] ### motor is 21 is not connected to a motor on hand
motor_pose = {}
for motor in motor_IDs:
    motor_pose[motor] = 0 ### setting the default value for motor positions

print(motor_pose)
class Motor(Enum):
    wrist_R = 23 ### Wrist rotary movement
    wrist_BF = 25 ### Wrist back forth movement
    thumb = 27
    fingers = 29

# motor_pose[Motor.thumb.value] = 90
dxl_io.set_goal_position(motor_pose)
for motor in motor_IDs:
    print(Motor(motor).name)
    for i in range (-150, 150, 25):
        motor_pose[motor] = i
        dxl_io.set_goal_position(motor_pose)
        sleep(0.5)

