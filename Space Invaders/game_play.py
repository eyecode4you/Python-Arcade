import pygame
from player import Player
from alien import Alien
from explosion import Explosion
import random
import settings

class GamePlay:
    def __init__(self, screen):
        self.text_colour = (255, 255, 255)
        self.main_menu = None

        # back to menu btn
        self.btn_colour = (0, 0, 170)
        self.btn_over_colour = (255, 50, 50)
        self.btn_width = 90
        self.btn_height = 60
        self.btn_rect = [screen.get_width() - self.btn_width,
                         0,
                         self.btn_width, self.btn_height]
        self.btn_font = pygame.font.Font('fonts/Cyber-BoldRustique.ttf', 20)
        self.btn_text = self.btn_font.render("Back", True, self.text_colour)
        self.mousex, self.mousey = (0, 0)

        # Player Character
        self.player = Player(screen.get_height() - 100)

        # Aliens
        self.aliens = []
        self.alienrows = 5
        self.aliencols = 15

        for r in range(self.alienrows):
            for c in range(self.aliencols):
                self.aliens.append(Alien(c, r, random.randint(0, 1)))
        
        # border control
        self.left_border = 50
        self.right_border = screen.get_width() - self.left_border
        self.dx = 1
        self.dy = 10
        self.direction = self.dx

        # explosions
        self.explosions = []

        # game over text
        self.font = pygame.font.Font('fonts/Cyber-BoldRustique.ttf', 80)
        self.game_over_title = self.font.render("Game Over!", True, self.text_colour)
        self.game_over_title_position = ((screen.get_width() - self.game_over_title.get_width()) // 2, 
                               (screen.get_height() - self.game_over_title.get_height()) // 2)
        
        self.game_win_title = self.font.render("You Win!", True, self.text_colour)
        self.game_win_title_position = ((screen.get_width() - self.game_win_title.get_width()) // 2, 
                               (screen.get_height() - self.game_win_title.get_height()) // 2)

        self.screen = screen
    
    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mousex, self.mousey = event.pos
                if self.btn_rect[0] <= self.mousex <= self.btn_rect[0] + self.btn_rect[2] and \
                    self.btn_rect[1] <= self.mousey <= self.btn_rect[1] + self.btn_rect[3]:

                    # reset game
                    self.player = Player(self.screen.get_height() - 100)
                    self.aliens = []
                    self.alienrows = 5
                    self.aliencols = 15
                    self.lives = 3
                    settings.x_offset = 10
                    settings.y_offset = 50
                    settings.abullets = []
                    for r in range(self.alienrows):
                        for c in range(self.aliencols):
                            self.aliens.append(Alien(c, r, random.randint(0, 1)))

                    return self.main_menu
            if event.type == pygame.MOUSEMOTION:
                self.mousex, self.mousey = event.pos
        self.player.update()

        # collision test
        deadbullets = []
        if self.player.bullets != [] and self.aliens != []:
            for b in self.player.bullets:
                found = False
                for a in pygame.sprite.spritecollide(b, self.aliens, 0):
                    self.aliens.remove(a)
                    self.explosions.append(Explosion(a.x, a.y))
                    a.kill()
                    found = True
                if found:
                    deadbullets.append(b)
        for b in deadbullets:
            self.player.bullets.remove(b)
            b.kill()

        return self

    def draw(self, screen):
        if self.btn_rect[0] <= self.mousex <= self.btn_rect[0] + self.btn_rect[2] and \
            self.btn_rect[1] <= self.mousey <= self.btn_rect[1] + self.btn_rect[3]:
            pygame.draw.rect(screen, self.btn_over_colour, self.btn_rect)
        else:
            pygame.draw.rect(screen, self.btn_colour, self.btn_rect)
        
        screen.blit(self.btn_text, (self.btn_rect[0] + (self.btn_width - self.btn_text.get_width()) /2,
                                    self.btn_rect[1] + (self.btn_height - self.btn_text.get_height()) /2))
        
        # draw game over screen
        if self.player.lives <= 0:
            screen.blit(self.game_over_title, self.game_over_title_position)
            return self
        elif len(self.aliens) <= 0:
            screen.blit(self.game_win_title, self.game_win_title_position)
            return self

        # draw player, aliens, alien bullets
        for a in self.aliens:
            a.draw(screen)
        
        self.player.draw(screen)
        
        deadabullets = []
        for b in settings.abullets:
            if b.y > screen.get_height():
                deadabullets.append(b)
            b.draw(screen)
        for b in deadabullets:
            settings.abullets.remove(b)

        # moving alien grid across screen & bouncing off borders
        update_y = False
        if (settings.x_offset + self.aliencols * 32) > self.right_border:
            self.direction *= -1
            update_y = True
            settings.x_offset = self.right_border - self.aliencols * 32
        
        if settings.x_offset < self.left_border:
            self.direction *= -1
            update_y = True
            settings.x_offset = self.left_border
        
        settings.x_offset += self.direction
        
        if update_y:
            settings.y_offset += self.dy
        
        # explosion
        deadexplosions = []
        for e in self.explosions:
            e.draw(screen)
            if e.framey < 0:
                deadexplosions.append(e)
        for e in deadexplosions:
            self.explosions.remove(e)