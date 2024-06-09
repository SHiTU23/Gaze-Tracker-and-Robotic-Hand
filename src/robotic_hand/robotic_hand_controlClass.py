import pypot.dynamixel
from enum import Enum
from time import sleep

class Motor_Name:
    wrist_R = 'wrist_r' ## wrist_R: rotary motor 
    wrist_BF = 'wrist_bf' ## wrist_BF: motor for movement in back and forth
    thumb = 'thumb'
    middle_fingers = 'middle_fingers'

class hand_control:
    def __init__(self, motor_id_scanRange):
        ###### Defining Variables ######
        self.motor_IDs_list = { Motor_Name.wrist_R  : 0, ## wrist_R : rotary motor 
                                Motor_Name.wrist_BF : 0, ## wrist_BF: motor for movement in back and forth
                                Motor_Name.thumb    : 0,
                                Motor_Name.middle_fingers : 0}
        self._motor_pose = {}
        self._motor_IDs = []
        self._dxl_io = []
        ################################
        self._get_motor_IDs(motor_id_scanRange)

    def _get_motor_IDs(self, motorID_scanRange):
        _motor_found = False

        _ports = pypot.dynamixel.get_available_ports()
        print('available ports:', _ports)

        if not _ports:
            raise IOError('No port available.')

        for port in _ports:
            try:
                self._dxl_io = pypot.dynamixel.DxlIO(port)
                try:
                    self._motor_IDs = self._dxl_io.scan(range(motorID_scanRange[0], motorID_scanRange[1]))
                    del self._motor_IDs[0] ### motor ID 21 is not connected to a part in hand
                    for motor in self._motor_IDs:
                        self._motor_pose[motor] = 0

                    for motor_id, motor_name  in enumerate(self.motor_IDs_list):
                        self.motor_IDs_list[motor_name] = self._motor_IDs[motor_id]

                    

                    print(f'Connected to {port}! MotorIDs are: {self.motor_IDs_list}')
                    _motor_found = True
                    break
                except:
                    _motor_found = False
                    pass
            except:
                ### THE PORT CANNOT GET OPENED
                _motor_found = False
                pass
        
        if _motor_found == False:
            print("XXX NO MOTOR FOUND XXX")
            exit()
        
    def all_motors_goTo_Pose(self, angle=0): 
        """
        angle range between -150, 150 , 
        defualt value is 0
        """

        for motor in self._motor_IDs:
            self._motor_pose[motor] = angle ### setting an angle for motor positions

        self._dxl_io.set_goal_position(self._motor_pose)
        print("ALL motors Moved to ", angle)

    
    def goTo_single(self, motor_name, angle): 
        """
         motor name: wrist_r / wrist_bf / thumb / middle_fingers
         angle range : -150 to 150 
        """
        motor_name.lower()
        self._motor_pose[self.motor_IDs_list[motor_name]] = angle
        self._dxl_io.set_goal_position(self._motor_pose)
        print( f"motor {motor_name} with ID of {self.motor_IDs_list[motor_name]} Moved to {angle} degree")

    def goTo_multiple(self, motor_names_and_angles):
        """
         motor_names_and_angles is a dict contains of motor name and desired pose

         Ex: motors= {"thumb": 45, "middle_fingers": 100}
        """
        for motor in motor_names_and_angles:
            angle = motor_names_and_angles[motor]
            motor_name = self.motor_IDs_list[motor]
            self._motor_pose[motor_name] = angle

        ## ALL motors move simulataniously
        self._dxl_io.set_goal_position(self._motor_pose)

    def goTo_homePose(self):
        """
         All motors go to 0 degree
        """
        self.all_motors_goTo_Pose()

    def open_fingers(self, open_angle=-150):
        """
         Default value is -150
         open_angle range: -150 to 150
         150 is close angle
        """
        _finger_poses = {Motor_Name.thumb : open_angle,
                         Motor_Name.middle_fingers : open_angle}
        self.goTo_multiple(_finger_poses)
        print("Hand Opened!")

    def close_fingers(self, close_angle=150):
        """
         Default value is 150
         close_angle range: 150 to -150
         -150 is open angle
        """
        _finger_poses = {Motor_Name.thumb : close_angle,
                         Motor_Name.middle_fingers : close_angle}
        self.goTo_multiple(_finger_poses)
        print("Hand Closed!")

