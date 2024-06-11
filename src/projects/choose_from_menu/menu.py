import pygame
from enum import Enum
import numpy as np

class options_position(Enum):
    center_right = "center_right"
    center_left = "center_left"
    center = "center"


class hand_operation_menu:
    pygame.init()
    
    screen_width = 900
    screen_height = 400
    screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
    # screen = pygame.display.set_mode([screen_width, screen_height])
    pygame.display.set_caption('MENU')

    def __init__(self):
        """
            The menu screen will be full screen
        """
        _screen_info = pygame.display.Info()
        self._screen_width = _screen_info.current_w
        self._screen_hight = _screen_info.current_h
        # print(f"screen simension is : {self._screen_width, self._screen_hight}")

        self.rect_corner_x = 0
        self.rect_corner_y = 0
        self.menu_size = [0, 0]

    def add_menu(self, option_pose=options_position.center, rect_size=[(screen_width/2.5), (screen_height/2.5)], color=(255, 255, 255), text=''):
        font_size = int(rect_size[1]/3)
        self.font = pygame.font.SysFont('Arial', font_size)
        self.menu_size = rect_size
        rect_width, rect_hight = rect_size
        _half_screen_w = (self._screen_width /2)
        _half_screen_h = (self._screen_hight /2)
        distance_from_center = (_half_screen_w-rect_width)/2

        _text_lenght = len(text)
        text_distance_from_rectBorader =  (rect_width - _text_lenght) / 6

        match option_pose.value:
            case "center_left":
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
        _clicked_x, _clicked_y = chosen_coordinate ### Is scaled from 0 to 1

        ### Map all values to range of (0, 1)
        _rect_corner_x_interped = np.interp(self.rect_corner_x, [0, self._screen_width], [0, 1]) 
        _rect_corner_y_interped = np.interp(self.rect_corner_y, [0, self._screen_hight], [0, 1]) 
        _menu_width_interped = np.interp(self.menu_size[0], [0, self._screen_width], [0, 1]) 
        _menu_hight_interped = np.interp(self.menu_size[1], [0, self._screen_width], [0, 1]) 
        # print(_rect_corner_x_interped, _rect_corner_y_interped, _menu_width_interped, _menu_hight_interped)

        if (_clicked_x >  _rect_corner_x_interped and _clicked_x < (_rect_corner_x_interped+_menu_width_interped)) and (
            _clicked_y > _rect_corner_y_interped and _clicked_y < (_rect_corner_y_interped+_menu_hight_interped)
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