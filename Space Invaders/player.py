import pygame
import settings
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

class Player(pygame.sprite.Sprite):
    def __init__(self, ypos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/ship.png')
        self.x = 10
        self.y = ypos
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

        # player lives
        self.font = pygame.font.SysFont('Arial', 20)
        self.lives = 3

        # shooting
        self.bullets = []
        self.can_shoot = 0
        self.shoot_fx = Sound("sounds/shoot.wav")

    def update(self):
        keys = pygame.key.get_pressed()
        self.rect.topleft = (self.x, self.y)
        
        # moving the ship
        if keys[K_RIGHT]:
            self.x += 5
        elif keys[K_LEFT]:
            self.x -= 5
        
        # shooting & cooldown
        if keys[K_SPACE] and self.can_shoot == 0:
            self.shoot_fx.play()
            self.bullets.append(Bullet(self.x + self.image.get_width() // 2, self.y, 20))
            self.can_shoot = 500
        if self.can_shoot > 0:
            self.can_shoot -= 15
        else:
            self.can_shoot = 0
        
        # collision and lives --
        for x in pygame.sprite.spritecollide(self, settings.abullets, 0):
            settings.abullets.remove(x)
            x.kill()
            self.lives -= 1

    def draw(self, screen):
        screen.blit(self.image, [self.x, self.y, self.image.get_width(), self.image.get_height()])
        self.lives_text = self.font.render("Lives: " + str(self.lives), True, (255, 255, 255))
        screen.blit(self.lives_text, (0, 0))
        
        deadbullets = []
        for b in self.bullets:
            if b.y < 0:
                deadbullets.append(b)
            b.draw(screen)
        for b in deadbullets:
            self.bullets.remove(b)