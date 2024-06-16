import pygame
import gif_pygame
from view.local_consts import *
from view.interface_elements import *
from eventmanager.events import *
import time

# MAIN MENU
MAIN_MENU_BACKGROUND = {"file": "core/view/assets/menu_background.gif",
                        "coords": (0, 0)}
MAIN_MENU_BUTTONS_WIDTH = RESOLUTION[0] * 9 // 32 # коэффициенты добыты экспериментальным путем
MAIN_MENU_BUTTONS_HEIGHT = RESOLUTION[1] * 41 // 360 # и эти тоже
MAIN_MENU_BUTTONS = {"PLAY": {"file": "core/view/assets/menu_button",
                              "func": None},
                    "COLLECTION": {"file": "core/view/assets/menu_button",
                                   "func": None},
                    "SETTINGS": {"file": "core/view/assets/menu_button",
                                 "func": None},
                    "EXIT": {"file": "core/view/assets/menu_button",
                             "func": QuitEvent()}}
_buttons_amount = len(MAIN_MENU_BUTTONS)
_first = RESOLUTION[1]//len(MAIN_MENU_BUTTONS)
_last = RESOLUTION[1] - _first
_space_between = (_last - _first - (_buttons_amount - 1) * MAIN_MENU_BUTTONS_HEIGHT) // (_buttons_amount - 1)
for but in MAIN_MENU_BUTTONS.keys():
    MAIN_MENU_BUTTONS[but]["coords"] = (RESOLUTION[0]//2, _first)
    _first += _space_between + MAIN_MENU_BUTTONS_HEIGHT


class MainMenu:
    def __init__(self):
        self.background_gif = gif_pygame.load(MAIN_MENU_BACKGROUND["file"])
        gif_pygame.transform.scale(self.background_gif, RESOLUTION)
        self.background_pos = MAIN_MENU_BACKGROUND["coords"]
        self.buttons = [Button(MAIN_MENU_BUTTONS[i]["func"],
                               *MAIN_MENU_BUTTONS[i]["coords"],
                               MAIN_MENU_BUTTONS[i]["file"],
                               MAIN_MENU_BUTTONS_WIDTH, MAIN_MENU_BUTTONS_HEIGHT) 
                        for i in MAIN_MENU_BUTTONS.keys()]
        self.moving_sprites = pygame.sprite.Group()
        self._is_animation_ended: bool = False
        self.clicked: bool = False
        self.next_event: Event = None
        for but in self.buttons:
            self.moving_sprites.add(but)
        
    def draw(self, where):
        is_cursor_on_button: bool = False
        is_any_button_animating: bool = True
        for but in self.buttons:
            if but.rect.collidepoint(pygame.mouse.get_pos()):
                is_cursor_on_button = True
            if but.is_animating:
                is_any_button_animating = False
        self._is_animation_ended = is_any_button_animating
        if is_cursor_on_button:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        self.background_gif.render(where, self.background_pos)
        self.moving_sprites.draw(where)
        self.moving_sprites.update()
        pygame.display.flip()
    
    def button_click(self, where, click_pos):
        for but in self.buttons:
            if but.rect.collidepoint(click_pos):
                but.click()
                self.next_event = but.func
                self.clicked = True
        self.draw(where)
    
    def do(self):
        if self.clicked and self._is_animation_ended:
            pygame.time.wait(75)
            return self.next_event
