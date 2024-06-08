import pypot.dynamixel
from enum import Enum
from time import sleep

class Motor_Name:
    wrist_R = 'wrist_r' ## wrist_R: rotary motor 
    wrist_BF = 'wrist_bf' ## wrist_BF: motor for movement in back and forth
    thumb = 'thumb'
    middle_fingers = 'middle_fingers'

class hand_control:
    ## wrist_R: rotary motor ; wrist_BF: motor for movement in back and forth
    motor_IDs_list = {Motor_Name.wrist_R  : 0,
                      Motor_Name.wrist_BF : 0,
                      Motor_Name.thumb    : 0,
                      Motor_Name.middle_fingers : 0}
    _motor_pose = {}


    def __init__(self, motor_id_scanRange):
        self._get_motor_IDs(motor_id_scanRange)

    def _get_motor_IDs(self, motorID_scanRange):
        global _motor_IDs, _dxl_io 
        self._motor_found = False

        _ports = pypot.dynamixel.get_available_ports()
        print('available ports:', _ports)

        if not _ports:
            raise IOError('No port available.')

        for port in _ports:
            try:
                _dxl_io = pypot.dynamixel.DxlIO(port)
                try:
                    _motor_IDs = _dxl_io.scan(range(motorID_scanRange[0], motorID_scanRange[1]))
                    del _motor_IDs[0] ### motor ID 21 is not connected to a part in hand
                    for motor in _motor_IDs:
                        self._motor_pose[motor] = 0

                    for motor_id, motor_name  in enumerate(self.motor_IDs_list):
                        self.motor_IDs_list[motor_name] = _motor_IDs[motor_id]

                    

                    print(f'Connected to {port}! MotorIDs are: {self.motor_IDs_list}')
                    self._motor_found = True
                    break
                except:
                    self._motor_found = False
                    pass
            except:
                ### THE PORT CANNOT GET OPENED
                self._motor_found = False
                pass
        
        if self._motor_found == False:
            print("XXX NO MOTOR FOUND XXX")
            exit()
        
    def all_motors_goTo_Pose(self, angle=0): # angle between -150, 150
        for motor in _motor_IDs:
            self._motor_pose[motor] = angle ### setting an angle for motor positions

        _dxl_io.set_goal_position(self._motor_pose)
        print("ALL motors Moved to ", angle)

    
    def goTo_single(self, motor_name, angle): 
        ## motor name: wrist_r / wrist_bf / thumb / middle_fingers
        ## angle : -150 to 150 
        motor_name.lower()
        self._motor_pose[self.motor_IDs_list[motor_name]] = angle
        _dxl_io.set_goal_position(self._motor_pose)
        print( f"motor {motor_name} with ID of {self.motor_IDs_list[motor_name]} Moved to ", angle)

    def goTo_multiple(self, motor_names_and_angles):
        ### motor_names_and_angles is a dict contains of motor name and desired pose
        for motor in motor_names_and_angles:
            angle = motor_names_and_angles[motor]
            motor_name = self.motor_IDs_list[motor]
            self._motor_pose[motor_name] = angle

        ## ALL motors move simulataniously
        _dxl_io.set_goal_position(self._motor_pose)

    def goTo_homePose(self):
        self.all_motors_goTo_Pose()

    def open_fingers(self):
        self._finger_poses = {Motor_Name.thumb : -150,
                              Motor_Name.middle_fingers : -150}
        self.goTo_multiple(self._finger_poses)

    def close_fingers(self):
        self._finger_poses = {Motor_Name.thumb : 150,
                              Motor_Name.middle_fingers : 150}
        self.goTo_multiple(self._finger_poses)

