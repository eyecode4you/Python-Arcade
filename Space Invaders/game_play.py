import pygame

class GamePlay:
    def __init__(self, screen):
        self.text_colour = (255, 255, 255)
        self.font = pygame.font.Font('fonts/Cyber-BoldRustique.ttf', 80)
        self.title = self.font.render("Gameplay", True, self.text_colour)
        self.title_position = (10, 10)
        self.main_menu = None

        # back to menu btn
        self.btn_colour = (0, 0, 170)
        self.btn_over_colour = (255, 50, 50)
        self.btn_width = 100
        self.btn_height = 70
        self.btn_rect = [screen.get_width() - self.btn_width,
                         0,
                         self.btn_width, self.btn_height]
        self.btn_font = pygame.font.Font('fonts/Cyber-BoldRustique.ttf', 30)
        self.btn_text = self.btn_font.render("Back", True, self.text_colour)
        self.mousex, self.mousey = (0, 0)
    
    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mousex, self.mousey = event.pos
                if self.btn_rect[0] <= self.mousex <= self.btn_rect[0] + self.btn_rect[2] and \
                    self.btn_rect[1] <= self.mousey <= self.btn_rect[1] + self.btn_rect[3]:
                    return self.main_menu
            if event.type == pygame.MOUSEMOTION:
                self.mousex, self.mousey = event.pos
        return self

    def draw(self, screen):
        if self.btn_rect[0] <= self.mousex <= self.btn_rect[0] + self.btn_rect[2] and \
            self.btn_rect[1] <= self.mousey <= self.btn_rect[1] + self.btn_rect[3]:
            pygame.draw.rect(screen, self.btn_over_colour, self.btn_rect)
        else:
            pygame.draw.rect(screen, self.btn_colour, self.btn_rect)
        
        screen.blit(self.btn_text, (self.btn_rect[0] + (self.btn_width - self.btn_text.get_width()) /2,
                                    self.btn_rect[1] + (self.btn_height - self.btn_text.get_height()) /2))