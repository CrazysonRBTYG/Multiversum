from eventmanager.events import *
from global_consts import *

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
MAIN_MENU_BUTTON_WAIT_AFTER_CLICK = 30
MAIN_MENU_BUTTONS = {"PLAY": {"path": "core/view/assets/main_menu/play_button",
                              "func": None},
                    "COLLECTION": {"path": "core/view/assets/main_menu/collection_button",
                                   "func": None},
                    "SETTINGS": {"path": "core/view/assets/main_menu/settings_button",
                                 "func": StateChangeEvent(STATE_SETTINGS_MENU)},
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


# SETTINGS MENU
_settings_window_width = RESOLUTION[0] // 3.2 # коэффициенты добыты экспериментальным путем
_settings_window_height = RESOLUTION[1] // 1.44 # и эти тоже
SETTINGS_WINDOW_TRANSFORM_RESOLUTION = (_settings_window_width, _settings_window_height)
SETTINGS_WINDOW = {"path": "core/view/assets/settings_menu/settings_window.png",
                   "coords": (RESOLUTION[0]//2, RESOLUTION[1]//2)}
BACK_BUTTON = {"path": "core/view/assets/settings_menu/back_button",
               "func": StateChangeEvent(None),
               "coords": (RESOLUTION[0]//2, RESOLUTION[1]//2 + _settings_window_height * 4 // 10)}