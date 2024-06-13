from eventmanager.main import EventHandler
from model.main import GameLogic
from view.main import Drawer
from controller.main import InputHandler


def run():
    """
    Запуск игры
    """

    event_handler = EventHandler()
    game_model = GameLogic(event_handler)
    inputs = Drawer(event_handler, game_model)
    graphics = InputHandler(event_handler, game_model)
    game_model.run()


if __name__ == "__main__":
    run()
