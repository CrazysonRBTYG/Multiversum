import gif_pygame
from eventmanager.events import *
from global_consts import *
from model.local_consts import *

RESOLUTION = (1920, 1080)
FULLSCREEN = True
FPS = 60
MATCHES_BREAK_DELAY = 700

FONT = "core/view/assets/PIXY.ttf"

_background = {"path": "core/view/assets/main_menu/background.gif",
               "coords": (0, 0)}
BACKGROUND_IMAGE: gif_pygame.GIFPygame = gif_pygame.load(_background["path"])
gif_pygame.transform.scale(BACKGROUND_IMAGE, RESOLUTION)
BACKGROUND_IMAGE_COORDS: tuple[int, int] = _background["coords"]

# MAIN MENU
_main_menu_button_width = RESOLUTION[0] * 9 // 32 # коэффициенты добыты экспериментальным путем
_main_menu_button_height = RESOLUTION[1] * 41 // 360 # и эти тоже
MAIN_MENU_BUTTONS_TRANSFORM_RESOLUTION = (_main_menu_button_width, _main_menu_button_height)
MAIN_MENU_BUTTON_CLICK_SPEED = 0.4
MAIN_MENU_BUTTONS = {"PLAY": {"path": "core/view/assets/main_menu/play_button",
                              "func": StateChangeEvent(STATE_GAME)},
                    "COLLECTION": {"path": "core/view/assets/main_menu/collection_button",
                                   "func": StateChangeEvent(STATE_COLLECTION)},
                    "SHOP": {"path": "core/view/assets/main_menu/shop_button",
                             "func": StateChangeEvent(STATE_SHOP)},
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

# GAME
_char_cell_width = RESOLUTION[0] * 15 // 64
_char_cell_height = RESOLUTION[1] * 92 // 135
CHAR_CELL_TRANSFORM_RESOLUTION = (_char_cell_width, _char_cell_height)
CHAR_CELL_COORDS = (RESOLUTION[0] * 163 // 1920, RESOLUTION[1] * 49 // 1080)
CHAR_CELL_PATH = "core/view/assets/collection/normis.png"
_stats_cell_width = _char_cell_width
_stats_cell_height = RESOLUTION[1] // 5
STATS_CELL_TRANSFORM_RESOLUTION = (_stats_cell_width, _stats_cell_height)
STATS_CELL_COORDS = (RESOLUTION[0] * 163 // 1920, RESOLUTION[1] * 817 // 1080)
STATS_CELL_PATH = "core/view/assets/game/stats.png"
_board_width = RESOLUTION[0] * 41 // 80
_board_height = RESOLUTION[1] * 41 // 45
_match_cell_width = _board_width // MATCH3_COLS * 140 // 123
_match_cell_height = _board_height // MATCH3_ROWS * 140 // 123
MATCH_CELL_TRANSFORM_RESOLUTION = (_match_cell_width, _match_cell_height)
MATCH_CELL_START_COORDS = (RESOLUTION[0] * 775 // 1920, RESOLUTION[1] * 49 // 1080)
MATCH_CELL_PATH = "core/view/assets/game/cell.png"
MATCH_CELL_W_INC = _match_cell_width * 6 // 7
MATCH_CELL_H_INC = _match_cell_height * 6 // 7

# COLLECTION
COLLECTION_MENU_BUTTON_CLICK_SPEED = 0.25
CHARACTER_IMAGE_COORDS = (RESOLUTION[0] * 735 // 1920, RESOLUTION[1] * 113 // 1080)
CHARACTER_IMAGE_TRANSFORM_RESOLUTION = (RESOLUTION[0] * 450 // 1920, RESOLUTION[1] * 736 // 1080)
CHOOSE_BUTTON_TRANSFORM_RESOLUTION = (RESOLUTION[0] * 360 // 1920, RESOLUTION[1] * 82 // 1080)
CHOOSE_BUTTON_ON_COORDS = (RESOLUTION[0] * 960 // 1920, RESOLUTION[1] * 925 // 1080)
CHOOSE_BUTTON_ON_PATH = "core/view/assets/collection/choose_button"
CHOOSE_BUTTON_FUNC = lambda char, chars: CharacterChangeEvent(chars[char])
CHOOSE_BUTTON_OFF_COORDS = (RESOLUTION[0] * 780 // 1920, RESOLUTION[1] * 885 // 1080)
CHOOSE_BUTTON_OFF_PATH = "core/view/assets/collection/choose_button/3.png"
MOVE_BUTTONS_TRANSFORM_RESOLUTION = (RESOLUTION[0] * 43 // 1920, RESOLUTION[1] * 82 // 1920)
LEFT_BUTTON_FUNC = lambda i: i - 1
LEFT_BUTTON_ON_COORDS = (RESOLUTION[0] * 700 // 1920, RESOLUTION[1] * 480 // 1080)
LEFT_BUTTON_ON_PATH = "core/view/assets/collection/left_button"
LEFT_BUTTON_OFF_COORDS = (RESOLUTION[0] * 680 // 1920, RESOLUTION[1] * 440 // 1080)
LEFT_BUTTON_OFF_PATH = "core/view/assets/collection/left_button/3.png"
RIGHT_BUTTON_FUNC = lambda i: i + 1
RIGHT_BUTTON_ON_COORDS = (RESOLUTION[0] * 1220 // 1920, RESOLUTION[1] * 480 // 1080)
RIGHT_BUTTON_ON_PATH = "core/view/assets/collection/right_button"
RIGHT_BUTTON_OFF_COORDS = (RESOLUTION[0] * 1200 // 1920, RESOLUTION[1] * 440 // 1080)
RIGHT_BUTTON_OFF_PATH = "core/view/assets/collection/right_button/3.png"

# SHOP
SHOP_MENU_BUTTON_CLICK_SPEED = 0.5
SPIN_BUTTON_ON_COORDS = (RESOLUTION[0] // 2, RESOLUTION[1] * 872 // 1080)
SPIN_BUTTON_TRANSFORM_RESOLUTION = (RESOLUTION[0] * 652 // 1920, RESOLUTION[1] * 149 // 1080)
SPIN_BUTTON_ON_PATH = "core/view/assets/shop/spin_button"
SPIN_BUTTON_FUNC = SpinEvent()
SPIN_BUTTON_OFF_COORDS = (RESOLUTION[0] * 637 // 1920, RESOLUTION[1] * 798 // 1080)
SPIN_BUTTON_OFF_PATH = "core/view/assets/shop/spin_button/3.png"

# COLORS
BLACK = (0, 0, 0)
GREEN = (28, 167, 23)
RED = (191, 27, 53)
WHITE = (255, 255, 255)
YELLOW = (180, 169, 25)