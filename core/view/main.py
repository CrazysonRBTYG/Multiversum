import pygame
import view.menus
import time
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
        self._delay = None
    
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
        if isinstance(event, StateChangeEvent):
            if not self._is_initialized:
                return
            current_state = self._model.state.peek()
            if current_state == STATE_GAME:
                self._game_menu = view.menus.GameMenu(self._model.chosen_char)
            if current_state == STATE_COLLECTION:
                self._collection_menu = view.menus.CollectionMenu(self._model.available_chars, self._model.chosen_char)
        if isinstance(event, TickEvent):
            if not self._is_initialized:
                return
            current_state = self._model.state.peek()
            if current_state == STATE_MAIN_MENU:
                self._main_menu.draw(self._screen)
                self._event_handler.post(self._main_menu.do())
            if current_state == STATE_GAME:
                if self._model.game.find_matches():
                    if self._delay == None:
                        self._delay = pygame.time.get_ticks()
                    else:
                        if self._model.game.remove_matches() != 0:
                            if self._delay != None:
                                if pygame.time.get_ticks() - self._delay >= 800:
                                    self._model.game.drop_tiles()
                                    self._delay = None
                self._game_menu.draw(self._screen, self._model.game.board, self._model.game.score, str(self._model.game.timer),
                                     self._model.game_over, self._model.record, self._model.ability_status, self._model.ability_cd_timer)
            if current_state == STATE_COLLECTION:
                self._collection_menu.draw(self._screen, self._model.chosen_char)
                try:
                    self._event_handler.post(self._collection_menu.do())
                except:
                    pass
            self._clock.tick(FPS)
        if isinstance(event, InputEvent):
            if not self._is_initialized:
                return
            current_state = self._model.state.peek()
            if current_state == STATE_MAIN_MENU:
                self._main_menu.button_click(event.click_pos)
            if current_state == STATE_GAME:
                if self._model.game_over == False:
                    self._game_menu.match_click(event.click_pos)
                    if self._game_menu.do() is not None:
                        if self._model.game.make_move(*self._game_menu.do()) == False:
                            self._model.game.moves += 1
                        self._game_menu.move = None
            if current_state == STATE_COLLECTION:
                self._collection_menu.button_click(event.click_pos)
    
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
