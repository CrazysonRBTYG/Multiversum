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

        self.main_menu = view.menus.MainMenu()
    
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
            if not self.is_initialized:
                return
            current_state = self.model.state.peek()
            if current_state == STATE_MAIN_MENU:
                self.main_menu.draw(self.screen)
                self.event_handler.post(self.main_menu.do())
            self.clock.tick(FPS)
        if isinstance(event, InputEvent):
            current_state = self.model.state.peek()
            if current_state == STATE_MAIN_MENU:
                self.main_menu.button_click(self.screen, event.click_pos)
    
    def _initialize(self):
        """
        Первоначальная графическая настройка игры
        """

        pygame.init()
        pygame.display.set_caption(GAME_NAME)
        self.screen = pygame.display.set_mode(RESOLUTION, pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.is_initialized = True
