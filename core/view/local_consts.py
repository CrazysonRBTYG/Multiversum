RESOLUTION = (1920, 1080)
FPS = 60

# Menus
MAIN_MENU_BACKGROUND = {"file": "core/view/assets/menu_background.gif",
                        "coords": (0, 0)}
MAIN_MENU_BUTTONS_WIDTH = RESOLUTION[0] * 9 // 32 # коэффициенты добыты экспериментальным путем
MAIN_MENU_BUTTONS_HEIGHT = RESOLUTION[1] * 41 // 360 # и эти тоже
MAIN_MENU_BUTTONS = {"PLAY": {"file": "core/view/assets/menu_button.png"},
                    "COLLECTION": {"file": "core/view/assets/menu_button.png"},
                    "SETTINGS": {"file": "core/view/assets/menu_button.png"},
                    "EXIT": {"file": "core/view/assets/menu_button.png"}}
_buttons_amount = len(MAIN_MENU_BUTTONS)
_first = RESOLUTION[1]//len(MAIN_MENU_BUTTONS)
_last = RESOLUTION[1] - _first
_space_between = (_last - _first - (_buttons_amount - 1) * MAIN_MENU_BUTTONS_HEIGHT) // (_buttons_amount - 1)
for but in MAIN_MENU_BUTTONS.keys():
    MAIN_MENU_BUTTONS[but]["coords"] = (RESOLUTION[0]//2, _first)
    _first += _space_between + MAIN_MENU_BUTTONS_HEIGHT
