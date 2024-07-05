import pygame
import settings

class Alien:
    def __init__(self, x, y, atype):
        self.x = x
        self.y = y
        self.atype = atype

        # alien graphics
        self.frame = 0
        self.image = pygame.image.load('images/aliens_sm.png')
        self.sprite_size = 32 # aliens on sprite sheet are sep. by 32x32 intervals
        
    def draw(self, screen):
        # multiply sprite pos by size & change alien graphic based on frame value
        screen.blit(self.image, [self.x * self.sprite_size + settings.x_offset, 
                                 self.y * self.sprite_size + settings.y_offset, 
                                 self.sprite_size, self.sprite_size],
                    (self.frame * self.sprite_size, 
                     self.sprite_size * self.atype, 
                     self.sprite_size, self.sprite_size))