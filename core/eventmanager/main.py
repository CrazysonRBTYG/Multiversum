from eventmanager.events import *

class EventHandler:
    """
    Осуществление коммуникации между компонентами MVC архитектуры
    """

    def __init__(self):
        from weakref import WeakKeyDictionary
        self._who_is_recieving: WeakKeyDictionary = WeakKeyDictionary() # список получателей
    
    def add_reciever(self, reciever):
        """
        Добавляет компонент в список тех, кто получает ивенты
        """

        self._who_is_recieving[reciever] = 1
    
    def delete_reciever(self, reciever):
        """
        Удаляет компонент из списка тех, кто получает ивенты
        """
        
        if reciever in self._who_is_recieving.keys():
            del self._who_is_recieving[reciever]
    
    def post(self, event: Event):
        """
        Передача информации о текущем ивенте для всех компонентов в списке получателей
        """

        for reciever in self._who_is_recieving.keys():
            reciever.update(event)
