import pygame
import os
from eventmanager.events import Event


class Button(pygame.sprite.Sprite):
    def __init__(self, event: Event, x: int, y: int, animation,
                 sprite_transform_x, sprite_transform_y):
        super().__init__()
        _sprites_amount = len([entry for entry in os.listdir(animation) 
                               if os.path.isfile(os.path.join(animation, entry))])
        self.sprites = [pygame.transform.scale(pygame.image.load(f"{animation}/{i}.png"), 
                                               (sprite_transform_x, sprite_transform_y)) 
                        for i in range(1, _sprites_amount+1)]
        self.func = event
        self.is_animating = False
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    
    def update(self, speed=0.5):
        if self.is_animating == True:
            self.current_sprite += speed

            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
                self.is_animating = False

            self.image = self.sprites[int(self.current_sprite)]
    
    def click(self):
        self.is_animating = True