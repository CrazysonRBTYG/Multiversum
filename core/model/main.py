import pygame
import json
from global_consts import *
from model.local_consts import *
from eventmanager.main import *
from model.match3 import Match3Game


class GameLogic:
    """
    Основной игровой костяк
    """

    def __init__(self, event_handler: EventHandler):
        self._event_handler: EventHandler = event_handler
        event_handler.add_reciever(self)
        self._is_running: bool = False
        self.state: StateChanger = StateChanger()
        self._timer_counter = None
        self._timer_in_ms = DEFAULT_TIMER
        self.record = self._json_read(STATS_FILE)["record"]
        self.available_chars = self._json_read(STATS_FILE)["owned-characters"]

    def run(self):
        """
        Запуск игрового цикла
        """

        self._is_running = True
        self._event_handler.post(InitializeEvent())
        self.state.push(STATE_MAIN_MENU)
        while self._is_running:
            self._event_handler.post(TickEvent())
    
    def update(self, event: Event):
        """
        Логическая обработка ивентов
        """

        if isinstance(event, QuitEvent):
            self._is_running = False
        if isinstance(event, StateChangeEvent):
            if not event.state:
                if not self.state.pop():
                    self._event_handler.post(QuitEvent())
            else:
                self.state.push(event.state)
            if self.state.peek() == STATE_GAME:
                self.game = Match3Game()
                self.game_over = False
                self._started = False
                self._ability_cd = CHARACTERS_ABILITIES[self.chosen_char][2]
                self._is_ability_on_cd: bool = False
                self._ability_cooldown_start = None
                self.ability_cd_timer = self._ability_cd
                self.ability_status: int = ABILITY_READY
        if isinstance(event, TickEvent):
            self.chosen_char = self._json_read(STATS_FILE)["chosen-character"]
            if self.state.peek() == STATE_GAME:
                if self.game.score > self.record:
                    self.record = self.game.score
                    self._json_write(STATS_FILE, "record", self.record)
                if self._started:
                    if self.game.timer == 0:
                        self.game_over = True
                        self._started = False
                    if self._timer_counter == None:
                        self._timer_counter = pygame.time.get_ticks()
                    else:
                        if pygame.time.get_ticks() - self._timer_counter >= self._timer_in_ms:
                            self.game.timer -= 1
                            self._timer_counter = None
                if self._is_ability_on_cd and not self.game_over:
                    if self._ability_cooldown_start == None:
                        if CHARACTERS_ABILITIES[self.chosen_char][1] != None: # проверка является ли способность удерживающей
                            if pygame.time.get_ticks() - self._ability_start >= CHARACTERS_ABILITIES[self.chosen_char][1] * 1000:
                                self._ability_cooldown_start = pygame.time.get_ticks()
                                self._deuse_ability(self.chosen_char)
                                self._ability_start = None
                        else:
                            self._ability_cooldown_start = pygame.time.get_ticks()
                    else:
                        if pygame.time.get_ticks() - self._ability_cooldown_start >= self._ability_cd * 1000:
                            self._is_ability_on_cd = False
                            self._ability_cooldown_start = None
                            self.ability_status = ABILITY_READY
                        else:
                            self.ability_status = ABILITY_ON_CD
                            self.ability_cd_timer = round(self._ability_cd - (pygame.time.get_ticks() - self._ability_cooldown_start) / 1000,
                                                           2)
        if isinstance(event, InputEvent):
            if self.state.peek() == STATE_GAME:
                try:
                    if event.input_key == 'f' or event.input_key == 'F' or event.input_key == 'а' or event.input_key == 'А':
                        if not self._is_ability_on_cd and self.game_over == False and CHARACTERS_ABILITIES[self.chosen_char][0] != None:
                            self._is_ability_on_cd = True
                            if CHARACTERS_ABILITIES[self.chosen_char][1] != None: # проверка является ли способность удерживающей
                                self._ability_start = pygame.time.get_ticks()
                                self.ability_status = ABILITY_ACTIVE
                            self._use_ability(self.chosen_char)
                except:
                    pass
                if self.game_over == False:
                    self._started = True
        if isinstance(event, CharacterChangeEvent):
            self._json_write(STATS_FILE, "chosen-character", event.character)
    
    def _json_read(self, file_path: str):
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data

    def _json_write(self, file_path: str, key, value):
        data = self._json_read(file_path)
        data[key] = value
        with open(file_path, 'w') as file:
            json.dump(data, file)
    
    def _use_ability(self, character: int):
        if character == CHAR_NORMIS:
            pass
        if character == CHAR_DIO_BRANDO:
            self._timer_in_ms = CHARACTERS_ABILITIES[self.chosen_char][0]
    
    def _deuse_ability(self, character: int):
        if character == CHAR_NORMIS:
            pass
        if character == CHAR_DIO_BRANDO:
            self._timer_in_ms = DEFAULT_TIMER
        
class StateChanger:
    """
    Реализация состояния игры (пауза, игра, меню и т.д.) через стек
    """

    def __init__ (self):
        self._stack = []
    
    def push(self, state: int) -> int:
        """
        Добавляет новое игровое состояние в стек и возвращает его
        """

        self._stack.append(state)
        return state

    def pop(self) -> int | None:
        """
        Удаляет последнее игровое состояние из стека и возвращает его
        """

        try:
            self._stack.pop()
            return len(self._stack) > 0
        except IndexError:
            return None
    
    def peek(self) -> int | None:
        """
        Возвращает текущее игровое состояние в стеке
        """

        try:
            return self._stack[-1]
        except IndexError:
            return None
