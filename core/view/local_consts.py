from eventmanager.events import *

RESOLUTION = (1920, 1080)
FULLSCREEN = True
FPS = 60

# MAIN MENU
MAIN_MENU_BACKGROUND = {"path": "core/view/assets/main_menu/background.gif",
                        "coords": (0, 0)}
_main_menu_button_width = RESOLUTION[0] * 9 // 32 # коэффициенты добыты экспериментальным путем
_main_menu_button_height = RESOLUTION[1] * 41 // 360 # и эти тоже
MAIN_MENU_BUTTONS_TRANSFORM_RESOLUTION = (_main_menu_button_width, _main_menu_button_height)
MAIN_MENU_BUTTON_CLICK_SPEED = 0.4
MAIN_MENU_BUTTON_WAIT_AFTER_CLICK = 50
MAIN_MENU_BUTTONS = {"PLAY": {"path": "core/view/assets/main_menu/play_button",
                              "func": None},
                    "COLLECTION": {"path": "core/view/assets/main_menu/collection_button",
                                   "func": None},
                    "SETTINGS": {"path": "core/view/assets/main_menu/settings_button",
                                 "func": None},
                    "EXIT": {"path": "core/view/assets/main_menu/exit_button",
                             "func": QuitEvent()}}
_buttons_amount = len(MAIN_MENU_BUTTONS)
_first = RESOLUTION[1]//len(MAIN_MENU_BUTTONS)
_last = RESOLUTION[1] - _first
_space_between_buttons = (_last - _first - (_buttons_amount - 1) 
                          * _main_menu_button_height) // (_buttons_amount - 1)
for but in MAIN_MENU_BUTTONS.keys():
    MAIN_MENU_BUTTONS[but]["coords"] = (RESOLUTION[0]//2, _first)
    _first += _space_between_buttons + _main_menu_button_height