import pygame
from enum import Enum
import numpy as np

class options_position(Enum):
    center_right = "center_right"
    center_left = "center_left"
    center = "center"


class hand_operation_menu:
    pygame.init()
    
    screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
    pygame.display.set_caption('MENU')

    _screen_info = pygame.display.Info()
    _screen_width = _screen_info.current_w
    _screen_height = _screen_info.current_h
    # print(f"screen dimension is : {_screen_width, _screen_height}")
    
    ### Load AprilTag marker
    april_tag_path = "../../../pics/AprilTag/tag25_09_00022-resized.png"
    april_tag = pygame.image.load(april_tag_path).convert()
    _image_width = april_tag.get_width()
    _image_height = april_tag.get_height()
    print(_image_width, _image_height)
    screen.blit(april_tag, (0, _screen_height-_image_height-20))

    def __init__(self):
        """
            The menu screen will be full screen
        """
        self.rect_corner_x = 0
        self.rect_corner_y = 0
        self.menu_size = [0, 0]

    def add_menu(self, option_pose=options_position.center, rect_size=[(_screen_width/5), (_screen_height/5)], color=(255, 255, 255), text=''):
        font_size = int(rect_size[1]/4)
        self.font = pygame.font.SysFont('Arial', font_size)
        self.menu_size = rect_size
        rect_width, rect_hight = rect_size
        _half_screen_w = (self._screen_width /2)
        _half_screen_h = (self._screen_height /2)
        distance_from_center = (_half_screen_w-rect_width)/2

        _text_lenght = len(text)
        text_distance_from_rectBorader =  (rect_width - _text_lenght) / 6

        match option_pose.value:
            case "center_left":
                #### Top left corner of the rectangle
                self.rect_corner_x = _half_screen_w - rect_width - distance_from_center
                self.rect_corner_y = _half_screen_h - (rect_hight/2)
                text_corner_x = abs(self.rect_corner_x + text_distance_from_rectBorader)
                text_corner_y = _half_screen_h - (font_size/2)
            case "center_right":
                self.rect_corner_x = _half_screen_w + distance_from_center
                self.rect_corner_y = _half_screen_h - (rect_hight/2)
                text_corner_x = abs(self.rect_corner_x + text_distance_from_rectBorader)
                text_corner_y = _half_screen_h - (font_size/2)
            case "center":
                self.rect_corner_x = _half_screen_w - (rect_width/2)
                self.rect_corner_y = _half_screen_h - (rect_hight/2)
                text_corner_x = abs(self.rect_corner_x + text_distance_from_rectBorader)
                text_corner_y = _half_screen_h - (font_size/2)

        ### ADD TEXT 
        
        pygame.draw.rect(self.screen, color, pygame.Rect(self.rect_corner_x, self.rect_corner_y, rect_width,rect_hight))
        self.screen.blit(self.font.render(text, True, (255,255,255)), (text_corner_x, text_corner_y))

        pygame.display.update()
        pygame.display.flip()

    def clicked(self, chosen_coordinate):
        _treshold = 0.2
        _clicked_x, _clicked_y = chosen_coordinate ### Is scaled from 0 to 1
        
        ### The other corner of rectangle
        rect_x_2 = self.rect_corner_x + self.menu_size[0]
        rect_y_2 = self.rect_corner_y + self.menu_size[1]

        # ### Map all values to range of (0, 1) 
        rect_x_2 = np.interp(rect_x_2, [0, self._screen_width], [0, 1]) 
        rect_y_2 = np.interp(rect_y_2, [0, self._screen_height], [0, 1])

        _rect_corner_x_interped = np.interp(self.rect_corner_x, [0, self._screen_width], [0, 1]) 
        _rect_corner_y_interped = np.interp(self.rect_corner_y, [0, self._screen_height], [0, 1]) 

        
        print(_rect_corner_x_interped,rect_x_2, _rect_corner_y_interped, rect_y_2)

        if (_clicked_x > (_rect_corner_x_interped-_treshold) and _clicked_x < (rect_x_2+_treshold)) and (
            _clicked_y > _rect_corner_y_interped-_treshold and _clicked_y < (rect_y_2+_treshold)
        ):
            return True
        else:
            return False

if __name__=="__main__":
    right_menu = hand_operation_menu()
    left_menu = hand_operation_menu()
    
    running = True
    while running:
        left_menu.add_menu(options_position.center_left, color=(10, 150, 10), text='Open Fingers')
        right_menu.add_menu(options_position.center_right, color=(200, 10, 10), text='Close Fingers')

        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_x = np.interp(mouse_x, [0, 1600], [0, 1]) 
        mouse_y = np.interp(mouse_y, [0, 900], [0, 1]) 
        mouse_pose = [mouse_x, mouse_y]
        print(f"mouse pose: {mouse_x}, {mouse_y}")
        if right_menu.clicked(mouse_pose):
            print("right menu clicked")
        elif left_menu.clicked(mouse_pose):
            print("left menu clicked")

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
                ):
                running = False
    pygame.quit()
