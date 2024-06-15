import pygame


class Button:
    def __init__(self, x: int, y: int, image: pygame.Surface):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    
    def draw(self, where):
        where.blit(self.image, (self.rect.x, self.rect.y))