import pygame
import settings
from random import randint

class AlienBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, yspeed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/bullet.png")
        self.x = x - self.image.get_width() // 2
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.dy = yspeed
    
    def draw(self, screen):
        self.y += self.dy
        self.rect.topleft = (self.x, self.y)
        screen.blit(self.image, [self.x, self.y, self.image.get_width(), self.image.get_height()])
        if self.y > screen.get_height():
            del self

class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y, atype):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.atype = atype
        self.frame = 0
        self.image = pygame.image.load('images/aliens_sm.png')
        self.sprite_size = 32 # aliens on sprite sheet are sep. by 32x32 intervals
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x * self.sprite_size + settings.x_offset, 
                            self.y * self.sprite_size + settings.y_offset)
    
    def flip_frame(self):
        if self.frame == 0:
            self.frame = 1
        else:
            self.frame = 0

    def draw(self, screen):
        if randint(0, 3000) < 1:
            settings.abullets.append(AlienBullet(self.x * self.sprite_size + settings.x_offset, 
                            self.y * self.sprite_size + settings.y_offset, 5))
        if settings.x_offset % 10 == 0:
            self.flip_frame()
        self.rect.topleft = (self.x * self.sprite_size + settings.x_offset, 
                            self.y * self.sprite_size + settings.y_offset)
        # multiply sprite pos by size & change alien graphic based on frame value
        screen.blit(self.image, [self.x * self.sprite_size + settings.x_offset, 
                                 self.y * self.sprite_size + settings.y_offset, 
                                 self.sprite_size, self.sprite_size],
                                [self.frame * self.sprite_size, 
                                self.sprite_size * self.atype, 
                                self.sprite_size, self.sprite_size])