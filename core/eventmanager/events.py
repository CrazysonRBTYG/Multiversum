class Event:
    """
    Суперкласс для всех возможных ивентов
    """

    def __init__(self):
        self._name = "Common (Generic) Event"


class TickEvent(Event):
    """
    Ивент игрового тика
    """

    def __init__(self):
        self._name = "Tick Event"


class QuitEvent(Event):
    """
    Ивент выхода из игры
    """

    def __init__ (self):
        self._name = "Quit Event"


class InputEvent(Event):
    """
    Ивент клика по мышке/клавиатуре
    """

    def __init__(self, input_key, click_position):
        self._name = "Input Event"
        self._input_key = input_key
        self.click_pos = click_position


class InitializeEvent(Event):
    """
    Ивент инициализации игрово
    """
    
    def __init__ (self):
        self._name = "Initialize Event"


class StateChangeEvent(Event):
    """
    Ивент изменения состояния игры
    """

    def __init__(self, state):
        self._name = "State Change Event"
        self.state = state
