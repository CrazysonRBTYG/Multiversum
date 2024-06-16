import pygame
from model.main import GameLogic
from eventmanager.main import *
from global_consts import *


class InputHandler:
    """
    Осуществляет работу с кликами по кнопочкам
    """

    def __init__(self, event_handler: EventHandler, game_model: GameLogic):
        self._event_handler: EventHandler = event_handler
        event_handler.add_reciever(self)
        self._model: GameLogic = game_model

    def update(self, event: Event):
        """
        Обработка нажатий кнопок на каждый ивент игрового тика 
        """
        
        if isinstance(event, TickEvent):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._event_handler.post(QuitEvent())
                if event.type == pygame.KEYUP:
                    current_state = self._model.state.peek()
                    if current_state == STATE_MAIN_MENU:
                        self.main_menu_keydown(event)
                if event.type == pygame.MOUSEBUTTONUP:
                    current_state = self._model.state.peek()
                    if current_state == STATE_MAIN_MENU:
                        self.main_menu_keydown(event)
    
    def main_menu_keydown(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            self._event_handler.post(InputEvent(None, pygame.mouse.get_pos()))