from view.imports import *


class Drawer:
    """
    Отображает текущее игровое состояние на экране
    """

    def __init__(self, event_handler: EventHandler, game_model: GameLogic):
        self.event_handler: EventHandler = event_handler
        event_handler.add_reciever(self)
        self.model: GameLogic = game_model
        self.is_initialized: bool = False
        self.screen: pygame.Surface = None
        self.clock: pygame.time.Clock = None
    
    def update(self, event: Event):
        """
        Графическая обработка ивентов
        """

        if isinstance(event, InitializeEvent):
            self._initialize()
        if isinstance(event, QuitEvent):
            self.is_initialized = False
            pygame.quit()
        if isinstance(event, TickEvent):
            if self.is_initialized == False:
                return
            self.clock.tick(FPS)
    
    def _initialize(self):
        """
        Первоначальная графическая настройка игры
        """

        pygame.init()
        pygame.display.set_caption(GAME_NAME)
        self.screen = pygame.display.set_mode(RESOLUTION)
        self.clock = pygame.time.Clock()
        self.is_initialized = True
