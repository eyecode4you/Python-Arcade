import pygame
from pygame.locals import *
from pygame.mixer import Sound

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, yspeed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/bullet.png")
        self.x = x - self.image.get_width() // 2
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.dy = yspeed
    
    def draw(self, screen):
        self.y -= self.dy
        self.rect.topleft = (self.x, self.y)
        screen.blit(self.image, [self.x, self.y, self.image.get_width(), self.image.get_height()])

class Player:
    def __init__(self, ypos):
        self.image = pygame.image.load('images/ship.png')
        self.x = 10
        self.y = ypos

        # shooting
        self.bullets = []
        self.can_shoot = 0
        self.shoot_fx = Sound("sounds/shoot.wav")

    def update(self):
        keys = pygame.key.get_pressed() 
        
        # moving the ship
        if keys[K_RIGHT]:
            self.x += 5
        elif keys[K_LEFT]:
            self.x -= 5
        
        # shooting
        if keys[K_SPACE] and self.can_shoot == 0:
            self.shoot_fx.play()
            self.bullets.append(Bullet(self.x + self.image.get_width() // 2, self.y, 20))
            self.can_shoot = 500
        
        # shoot cooldown
        if self.can_shoot > 0:
            self.can_shoot -= 15
        else:
            self.can_shoot = 0

    def draw(self, screen):
        screen.blit(self.image, [self.x, self.y, self.image.get_width(), self.image.get_height()])
        for b in self.bullets:
            b.draw(screen)