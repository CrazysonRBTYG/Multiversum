from controller.imports import *


class InputHandler:
    """
    Осуществляет работу с кликами по кнопочкам
    """

    def __init__(self, event_handler: EventHandler, game_model: GameLogic):
        self.event_handler: EventHandler = event_handler
        event_handler.add_reciever(self)
        self.model: GameLogic = game_model

    def update(self, event: Event):
        """
        Обработка нажатий кнопок на каждый ивент игрового тика 
        """

        if isinstance(event, TickEvent):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.event_handler.post(QuitEvent())
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.event_handler.post(StateChangeEvent(None))