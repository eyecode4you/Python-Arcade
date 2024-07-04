import pygame

class MainMenu:
    def __init__(self):
        self.font = pygame.font.Font('fonts/Cyber-BoldRustique.ttf', 80)
        self.title = self.font.render("Py Invaders", True, (255, 255, 255))
        self.title_position = (10, 10)
    
    def update(self, events):
        return self

    def draw(self, screen):
        screen.blit(self.title, self.title_position)
