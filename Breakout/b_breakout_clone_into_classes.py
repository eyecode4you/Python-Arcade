import time
import pygame
from pygame.locals import *


def title_screen():
    title_start = pygame.image.load("./resources/title_image.png")
    title_start = pygame.transform.scale(title_start, (480, 261))
    title_start = title_start.convert_alpha()
    title_rect = screen.get_width() * 0.20, screen.get_height() * 0.25
    screen.blit(title_start, title_rect)
    pygame.display.update()
    time.sleep(2)


class Paddle:
    def __init__(self):
        """ Load in paddle image, get paddle rectangle, set position """
        self.paddle = pygame.image.load("./resources/paddle1.png")
        self.paddle = self.paddle.convert_alpha()
        self.paddle_rect = self.paddle.get_rect()
        self.paddle_rect[1] = screen.get_height() - 100
        self.x, self.y = 0, 0
        self.reset()

    def reset(self):
        """ reset paddle position """
        self.x, self.y = \
            screen.get_width() / 2 - self.paddle.get_width() / 2, screen.get_height() - self.paddle.get_height()

    def boundary(self):
        """ keep paddle within screen boundaries """
        if self.x > (screen.get_width() - p.paddle.get_width()):
            self.x = screen.get_width() - p.paddle.get_width()
        if self.x < 0:
            self.x = 0


class Ball:
    def __init__(self):
        self.ball = pygame.image.load("./resources/football1.png")
        self.ball = self.ball.convert_alpha()
        self.rect = self.ball.get_rect()
        self.start = 0
        self.reset()
        self.speed = (5.0, 5.0)
        self.served = False
        self.x, self.y = self.speed
        self.rect.topleft = self.start

    def reset(self):
        """ reset ball position """
        self.start = (screen.get_width() / 2 - self.rect[2] / 2, screen.get_height() / 2)

    def boundary(self):
        if self.rect[1] <= 0:  # top
            self.rect[1] = 0
            self.y *= -1
        if self.rect[1] >= screen.get_height() - self.rect.height:  # right
            self.served = False
            self.x, self.y = self.speed
            self.rect.topleft = self.start
            p.reset()
        if self.rect[0] <= 0:  # left
            self.rect[0] = 0
            self.x *= -1
        if self.rect[0] >= screen.get_width() - self.rect.width:  # right
            self.rect[0] = screen.get_width() - self.rect.width
            self.x *= -1


screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Breakout Clone")
title_screen()
p = Paddle()
ball = Ball()

# brick
brick = pygame.image.load("./resources/brick1.png")
brick = brick.convert_alpha()
brick_rect = brick.get_rect()
bricks = []
brick_rows = 5
brick_gap = 2
brick_cols = screen.get_width() // (brick_rect[2] + brick_gap)
side_gap = (screen.get_width() - (brick_rect[2] + brick_gap) * brick_cols + brick_gap) // 2

for y in range(brick_rows):
    brickY = y * (brick_rect[3] + brick_gap)
    for x in range(brick_cols):
        brickX = x * (brick_rect[2] + brick_gap) + side_gap
        bricks.append((brickX, brickY))

clock = pygame.time.Clock()
game_over = False

while not game_over:
    dt = clock.tick(60)
    screen.fill((0, 0, 0))

    for b in bricks:
        screen.blit(brick, b)

    screen.blit(p.paddle, p.paddle_rect)
    screen.blit(ball.ball, ball.rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    # controls
    pressed = pygame.key.get_pressed()
    if pressed[K_a]:
        p.x -= 0.75 * dt
    if pressed[K_d]:
        p.x += 0.75 * dt
    p.paddle_rect[0], p.paddle_rect[1] = p.x, p.y

    if pressed[K_SPACE]:
        ball.served = True
    if ball.served:
        ball.rect[0] += ball.x
        ball.rect[1] += ball.y

    if pressed[K_ESCAPE]:
        game_over = True

    # ball collision with paddle
    if p.paddle_rect[0] + p.paddle_rect.width >= ball.rect[0] >= p.paddle_rect[0] and \
            ball.rect[1] + ball.rect.height >= p.paddle_rect[1] and \
            ball.y > 0:
        ball.y *= -1
        ball.x *= 1.1  # increase difficulty and speed
        ball.y *= 1.1
        continue

    delete_brick = None
    for b in bricks:
        bx, by = b
        if bx <= ball.rect[0] <= bx + brick_rect.width and \
                by <= ball.rect[1] <= by + brick_rect.height:
            delete_brick = b

            if ball.rect[0] <= bx + 2:  # 2 is for colliding with brick a little bit
                ball.x *= -1
            elif ball.rect[0] >= bx + brick_rect.width - 2:
                ball.x *= -1
            if ball.rect[1] <= by + 2:
                ball.y *= -1
            elif ball.rect[1] >= by + brick_rect.height - 2:
                ball.y *= -1

    if delete_brick is not None:
        bricks.remove(delete_brick)

    ball.boundary()  # keep ball within boundary
    p.boundary()  # keep paddle within boundary

    pygame.display.update()
pygame.quit()
