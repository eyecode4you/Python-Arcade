import pygame
import random
from pygame import Vector2
from pygame.transform import rotozoom


class Ship:
    def __init__(self, position):
        self.position = Vector2(position)
        self.image = pygame.image.load("./resources/ship1.png")
        self.forward = Vector2(0, -1)
        self.bullets = []
        self.can_shoot = 0
        self.drift = (0, 0)

    def update(self):
        is_key_pressed = pygame.key.get_pressed()
        if is_key_pressed[pygame.K_UP]:
            self.position += self.forward
            self.drift = (self.drift + self.forward) / 1.5
        if is_key_pressed[pygame.K_DOWN]:
            self.position -= self.forward
            self.drift = (self.drift + self.forward) / 1.5
        if is_key_pressed[pygame.K_LEFT]:
            self.forward = self.forward.rotate(-1)
        if is_key_pressed[pygame.K_RIGHT]:
            self.forward = self.forward.rotate(1)
        if is_key_pressed[pygame.K_SPACE] and self.can_shoot == 0:
            self.bullets.append(Bullet(Vector2(self.position), self.forward * 10))
            self.can_shoot = 500  # 500ms
        if is_key_pressed[pygame.K_ESCAPE]:
            pygame.quit()

        self.position += self.drift

        #  cooldown shoot
        if self.can_shoot > 0:
            self.can_shoot -= clock.get_time()
        else:
            self.can_shoot = 0

    def draw(self, screen):
        angle = self.forward.angle_to(Vector2(0, -1))
        rotated_surface = rotozoom(self.image, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size // 2
        screen.blit(rotated_surface, blit_position)


class Bullet:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity

    def update(self):
        self.position += self.velocity

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), [self.position.x, self.position.y, 5, 5])


class Asteroid:
    def __init__(self, position):
        self.position = Vector2(position)
        self.velocity = Vector2(random.randint(-3, 3), random.randint(-3, 3))
        self.image = pygame.image.load("./resources/asteroid.png")

    def update(self):
        self.position += self.velocity

        if self.position.x < out_of_bounds[0] or \
                self.position.x > out_of_bounds[2]:
            self.velocity.x *= -1
        if self.position.y < out_of_bounds[1] or \
                self.position.y > out_of_bounds[3]:
            self.velocity.y *= -1

    def draw(self, screen):
        screen.blit(self.image, self.position)


pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("pyAsteroids")

bg = pygame.image.load("./resources/space.png")

game_over = False
ship = Ship((100, 700))

asteroids = []
out_of_bounds = [-150, -150, 950, 950]
for i in range(10):
    asteroids.append(Asteroid((random.randint(0, screen.get_width()),
                               random.randint(0, screen.get_height()))))

clock = pygame.time.Clock()
while not game_over:
    clock.tick(55)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
    screen.blit(bg, (0, 0))

    ship.update()
    ship.draw(screen)

    for a in asteroids:
        a.update()
        a.draw(screen)

    for b in ship.bullets:
        b.update()
        b.draw(screen)

    pygame.display.update()
pygame.quit()
