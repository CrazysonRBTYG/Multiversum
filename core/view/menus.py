import pygame
import gif_pygame
from view.local_consts import *
from view.interface_elements import *
from eventmanager.events import *


# MAIN MENU
MAIN_MENU_BACKGROUND = {"path": "core/view/assets/menu_background.gif",
                        "coords": (0, 0)}
_main_menu_button_width = RESOLUTION[0] * 9 // 32 # коэффициенты добыты экспериментальным путем
_main_menu_button_height = RESOLUTION[1] * 41 // 360 # и эти тоже
MAIN_MENU_BUTTONS_TRANSFORM_RESOLUTION = (_main_menu_button_width, _main_menu_button_height)
MAIN_MENU_BUTTON_CLICK_SPEED = 0.4
MAIN_MENU_BUTTON_WAIT_AFTER_CLICK = 50
MAIN_MENU_BUTTONS = {"PLAY": {"path": "core/view/assets/menu_button",
                              "func": None},
                    "COLLECTION": {"path": "core/view/assets/menu_button",
                                   "func": None},
                    "SETTINGS": {"path": "core/view/assets/menu_button",
                                 "func": None},
                    "EXIT": {"path": "core/view/assets/menu_button",
                             "func": QuitEvent()}}
_buttons_amount = len(MAIN_MENU_BUTTONS)
_first = RESOLUTION[1]//len(MAIN_MENU_BUTTONS)
_last = RESOLUTION[1] - _first
_space_between_buttons = (_last - _first - (_buttons_amount - 1) 
                          * _main_menu_button_height) // (_buttons_amount - 1)
for but in MAIN_MENU_BUTTONS.keys():
    MAIN_MENU_BUTTONS[but]["coords"] = (RESOLUTION[0]//2, _first)
    _first += _space_between_buttons + _main_menu_button_height

class MainMenu:
    """
    Шаблон главного меню и всех его функций
    """

    def __init__(self):
        self._background_image: gif_pygame.GIFPygame = gif_pygame.load(MAIN_MENU_BACKGROUND["path"])
        gif_pygame.transform.scale(self._background_image, RESOLUTION)
        self._background_image_pos: tuple[int, int] = MAIN_MENU_BACKGROUND["coords"]
        self._buttons: list[Button] = [
                Button(MAIN_MENU_BUTTONS[i]["func"],
                *MAIN_MENU_BUTTONS[i]["coords"],
                MAIN_MENU_BUTTONS[i]["path"], MAIN_MENU_BUTTONS_TRANSFORM_RESOLUTION) 
                for i in MAIN_MENU_BUTTONS.keys()]
        self._animations: pygame.sprite.Group = pygame.sprite.Group()
        self._are_all_animations_ended: bool = False
        self._is_any_button_clicked: bool = False
        self._next_event: Event = None # Отслеживание нажатой кнопки
        for but in self._buttons:
            self._animations.add(but)
        
    def draw(self, where):
        """
        Визуальное отображение всех компонентов
        """

        is_cursor_on_button: bool = False
        is_any_button_animating: bool = True
        for but in self._buttons:
            if but.rect.collidepoint(pygame.mouse.get_pos()):
                is_cursor_on_button = True
            if but.is_animating:
                is_any_button_animating = False
        self._are_all_animations_ended = is_any_button_animating
        if is_cursor_on_button:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        self._background_image.render(where, self._background_image_pos)
        self._animations.draw(where)
        self._animations.update(speed=MAIN_MENU_BUTTON_CLICK_SPEED)
        pygame.display.flip()
    
    def button_click(self, click_pos):
        """
        Нажатие на кнопку и получение следующего события после него
        """
        for but in self._buttons:
            if but.rect.collidepoint(click_pos):
                but.click()
                self._next_event = but.func
                self._is_any_button_clicked = True
    
    def do(self) -> Event:
        """
        Возврат события после нажатия на кнопку (если нажата)
        """

        if self._is_any_button_clicked and self._are_all_animations_ended:
            pygame.time.wait(MAIN_MENU_BUTTON_WAIT_AFTER_CLICK) # микро пауза (можно отключить)
            return self._next_event