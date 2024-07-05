import pygame
from pygame.locals import *

class Player:
    def __init__(self, ypos):
        self.image = pygame.image.load('images/ship.png')
        self.x = 10
        self.y = ypos

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[K_RIGHT]:
            self.x += 5
        elif keys[K_LEFT]:
            self.x -= 5

    def draw(self, screen):
        screen.blit(self.image, [self.x, self.y, self.image.get_width(), self.image.get_height()])