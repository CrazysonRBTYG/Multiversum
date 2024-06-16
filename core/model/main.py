from global_consts import *
from eventmanager.main import *


class GameLogic:
    """
    Основной игровой костяк
    """

    def __init__(self, event_handler: EventHandler):
        self._event_handler: EventHandler = event_handler
        event_handler.add_reciever(self)
        self._is_running: bool = False
        self.state: StateChanger = StateChanger()
    
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
