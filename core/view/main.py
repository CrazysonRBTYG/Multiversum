import pygame
import view.menus
from model.main import GameLogic
from eventmanager.main import *
from global_consts import *
from view.local_consts import *


class Drawer:
    """
    Отображает текущее игровое состояние на экране
    """

    def __init__(self, event_handler: EventHandler, game_model: GameLogic):
        self._event_handler: EventHandler = event_handler
        event_handler.add_reciever(self)
        self._model: GameLogic = game_model
        self._is_initialized: bool = False
        self._screen: pygame.Surface = None
        self._clock: pygame.time.Clock = None
        self._main_menu: view.menus.MainMenu = view.menus.MainMenu()
    
    def update(self, event: Event):
        """
        Графическая обработка ивентов
        """

        if isinstance(event, InitializeEvent):
            self._initialize()
        if isinstance(event, QuitEvent):
            self._is_initialized = False
            pygame.quit()
            exit() # без этого программа продолжает работать в файле controller/main.py (не выявил причину)
        if isinstance(event, TickEvent):
            if not self._is_initialized:
                return
            current_state = self._model.state.peek()
            if current_state == STATE_MAIN_MENU:
                self._main_menu.draw(self._screen)
                self._event_handler.post(self._main_menu.do())
            self._clock.tick(FPS)
        if isinstance(event, InputEvent):
            if not self._is_initialized:
                return
            current_state = self._model.state.peek()
            if current_state == STATE_MAIN_MENU:
                self._main_menu.button_click(event.click_pos)
    
    def _initialize(self):
        """
        Первоначальная графическая настройка игры
        """

        pygame.init()
        pygame.display.set_caption(GAME_NAME)
        if FULLSCREEN:
            self._screen = pygame.display.set_mode(RESOLUTION, pygame.FULLSCREEN)
        else:
            self._screen = pygame.display.set_mode(RESOLUTION)
        self._clock = pygame.time.Clock()
        self._is_initialized = True
