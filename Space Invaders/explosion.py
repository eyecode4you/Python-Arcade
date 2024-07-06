import pygame, settings

class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load('images/explode.png')

        # See explosion.png, we'll treat it as a grid to use single sprites
        self.framex = 3
        self.framey = 3
        self.sprite_size = 32

    def draw(self, screen):
        screen.blit(self.image, [self.x * self.sprite_size + settings.x_offset, 
                                 self.y * self.sprite_size + settings.y_offset, 
                                 self.sprite_size, self.sprite_size],
                                [self.framex * self.sprite_size, 
                                 self.framey * self.sprite_size, 
                                 self.sprite_size, self.sprite_size])
        # go through sprite sheet for explosion fx
        self.framex -= 1
        if self.framex < 0:
            self.framex = 3
            self.framey -= 1