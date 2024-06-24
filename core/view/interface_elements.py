import pygame
import os
from eventmanager.events import Event


class Button(pygame.sprite.Sprite):
    """
    Шаблон кнопки по спрайту/анимации
    """

    def __init__(self, event: Event, x: int, y: int, path: str, sprite_transform_resolution: tuple[int, int]):
        super().__init__()
        sprites_amount: int = len([entry for entry in os.listdir(path) 
                                    if os.path.isfile(os.path.join(path, entry))])
        self._sprites: list[pygame.Surface] = [pygame.transform.scale(pygame.image.load(f"{path}/{i}.png"), 
                                               sprite_transform_resolution) for i in range(1, sprites_amount+1)]
        self.func: Event = event
        self.is_animating: bool = False
        self._current_sprite: int = 0
        self.image: pygame.Surface = self._sprites[self._current_sprite]
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.center = (x, y)
    
    def update(self, speed: float = 0.5):
        """
        Цикл анимации
        """

        if self.is_animating == True:
            self._current_sprite += speed

            if self._current_sprite >= len(self._sprites):
                self._current_sprite = 0
                self.is_animating = False

            self.image = self._sprites[int(self._current_sprite)]
    
    def click(self):
        """
        Запуск анимации
        """

        self.is_animating = True


class Image():
    """
    Шаблон изображения
    """

    def __init__(self, x: int, y: int, path: str, sprite_transform_resolution: tuple[int, int]):
        super().__init__()
        self.path = path
        self._transform_res = sprite_transform_resolution
        self._xy_rect = (x, y)
        self._sprite: pygame.Surface = pygame.transform.scale(pygame.image.load(path), sprite_transform_resolution)
        self.rect = self._sprite.get_rect()
        self.rect.topleft = (x, y)
    
    def draw(self, where: pygame.Surface):
        """
        
        """

        where.blit(self._sprite, self.rect)
    
    def update(self, path: str):
        self._sprite: pygame.Surface = pygame.transform.scale(pygame.image.load(path), self._transform_res)
        self.rect = self._sprite.get_rect()
        self.rect.topleft = self._xy_rect
    
    def get_rect(self):
        return self.rect