import pygame
import gif_pygame
from view.local_consts import *
from view.interface_elements import *


class MainMenu:
    def __init__(self):
        self.background_gif = gif_pygame.load(MAIN_MENU_BACKGROUND["file"])
        gif_pygame.transform.scale(self.background_gif, RESOLUTION)
        self.background_pos = MAIN_MENU_BACKGROUND["coords"]
        self.buttons = [Button(*MAIN_MENU_BUTTONS[i]["coords"], 
                               pygame.transform.scale(pygame.image.load(MAIN_MENU_BUTTONS[i]["file"]), 
                               (MAIN_MENU_BUTTONS_WIDTH, MAIN_MENU_BUTTONS_HEIGHT))) 
                        for i in MAIN_MENU_BUTTONS.keys()]
        
    def draw(self, where):
        self.background_gif.render(where, self.background_pos)
        for button in self.buttons:
            button.draw(where)
        pygame.display.flip()
