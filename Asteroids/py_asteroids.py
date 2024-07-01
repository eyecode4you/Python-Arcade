import pygame
import random, time
from pygame import Vector2
from pygame.transform import rotozoom
from pygame.mixer import Sound

asteroid_images = ['./resources/asteroid1.png', './resources/asteroid2.png', './resources/asteroid3.png']
clock = pygame.time.Clock()

def wrap_position(position, screen):
    x, y = position
    w, h = screen.get_size()
    return Vector2(x % w, y % h)


def blit_rotated(position, image, forward, screen):
    angle = forward.angle_to(Vector2(0, -1))
    rotated_surface = rotozoom(image, angle, 1.0)
    rotated_surface_size = Vector2(rotated_surface.get_size())
    blit_position = position - rotated_surface_size // 2
    screen.blit(rotated_surface, blit_position)


class Ship:
    def __init__(self, position):
        self.position = Vector2(position)
        self.image = pygame.image.load("./resources/ship1.png")
        self.forward = Vector2(0, -1)
        self.bullets = []
        self.can_shoot = 0
        self.drift = (0, 0)
        self.shoot_fx = Sound("./resources/shoot.wav")

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
            self.shoot_fx.play()
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
        self.position = wrap_position(self.position, screen)
        blit_rotated(self.position, self.image, self.forward, screen)


class Bullet:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity

    def update(self):
        self.position += self.velocity

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), [self.position.x, self.position.y, 5, 5])


class Asteroid:
    def __init__(self, position, size):
        self.position = Vector2(position)
        self.velocity = Vector2(random.randint(-3, 3), random.randint(-3, 3))
        self.image = pygame.image.load(asteroid_images[size])
        self.radius = self.image.get_width() // 2
        self.explode = Sound("./resources/explode.mp3")
        self.size = size

    def update(self):
        self.position += self.velocity

    def draw(self, screen):
        self.position = wrap_position(self.position, screen)
        blit_rotated(self.position, self.image, self.velocity, screen)

    def hit(self, position):
        if self.position.distance_to(position) <= self.radius:
            self.explode.play()
            return True
        return False


def main():
    pygame.init()
    pygame.mixer.music.load("./resources/bgmusic.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.25)

    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("pyAsteroids")

    # TITLE SCREEN
    title = pygame.image.load("./resources/asteroid_splash_screen.jpg")
    screen.blit(title, (0,0))
    pygame.display.update()
    time.sleep(2)

    bg = pygame.image.load("./resources/bg.gif")

    game_over = False
    ship = Ship((screen.get_width() // 2, screen.get_height() // 2))

    asteroids = []
    out_of_bounds = [-150, -150, 950, 950]
    for i in range(3):
        """ Create a few asteroids on game start """
        posx, posy = (random.randint(0, screen.get_width()),
                    random.randint(0, screen.get_height()))
        asteroid_position = (posx, posy)
        asteroid_direction_away_from_screen_center = ((screen.get_width()/2 - posx) * 0.8,
                                                    (screen.get_height()/2 - posy) * 0.8)
        asteroid_position += asteroid_direction_away_from_screen_center
        asteroids.append(Asteroid((asteroid_position[0], asteroid_position[1]), 0))

    font = pygame.font.Font("./resources/Cyber-BoldRustique.ttf", 80)
    txt_win = font.render("You Win", True, (255, 255, 255))
    txt_lose = font.render("Game Over", True, (255, 255, 255))
    txt_pos = ((screen.get_width() - txt_lose.get_width()) // 2,
            (screen.get_height() - txt_lose.get_height()) // 2)

    while not game_over:
        clock.tick(55)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
        screen.blit(bg, (0, 0))

        if ship is None:
            screen.blit(txt_lose, txt_pos)
            pygame.display.update()
            time.sleep(3)
            main()
            continue

        if len(asteroids) == 0:
            screen.blit(txt_win, txt_pos)
            pygame.display.update()
            continue

        ship.update()
        ship.draw(screen)

        for a in asteroids:
            a.update()
            a.draw(screen)
            if a.hit(ship.position):
                ship = None
                break

        if ship is None:
            continue

        deadbullets = []
        deadasteroids = []

        for b in ship.bullets:
            b.update()
            b.draw(screen)

            if b.position.x < out_of_bounds[0] or \
                    b.position.x > out_of_bounds[2] or \
                    b.position.y < out_of_bounds[1] or \
                    b.position.y > out_of_bounds[3]:
                if not deadbullets.__contains__(b):
                    deadbullets.append(b)

            for a in asteroids:
                if a.hit(b.position):
                    if not deadbullets.__contains__(b):
                        deadbullets.append(b)
                    if not deadasteroids.__contains__(a):
                        deadasteroids.append(a)

        for b in deadbullets:
            ship.bullets.remove(b)

        for a in deadasteroids:
            if a.size < 2:
                asteroids.append(Asteroid(a.position, a.size + 1))
                asteroids.append(Asteroid(a.position, a.size + 1))
            asteroids.remove(a)

        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()