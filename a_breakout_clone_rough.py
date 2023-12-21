'''
a_breakout_clone_rough.py
eyecode4you - 21/12/2023

A rough initial draft of the breakout clone to be refined
'''

import time
import pygame
from pygame.locals import *

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Breakout Clone")

# paddle
paddle = pygame.image.load("./resources/paddle1.png")
paddle = paddle.convert_alpha()
paddle_rect = paddle.get_rect()
paddle_rect[1] = screen.get_height() - 100

# ball
ball = pygame.image.load("./resources/football1.png")
ball = ball.convert_alpha()
ball_rect = ball.get_rect()
ball_start = (screen.get_width()/2 - ball_rect[2]/2, screen.get_height()/2)
ball_speed = (5.0, 5.0)
ball_served = False
sx, sy = ball_speed
ball_rect.topleft = ball_start

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

paddleX, paddleY = screen.get_width()/2 - paddle.get_width()/2, screen.get_height() - paddle.get_height()

title_start = pygame.image.load("./resources/title_image.png")
title_start = pygame.transform.scale(title_start, (480, 261))
title_start = title_start.convert_alpha()
title_rect = title_start.get_rect()
title_rect = screen.get_width() * 0.20, screen.get_height() * 0.25
screen.blit(title_start, title_rect)
pygame.display.update()
time.sleep(3)

while not game_over:
    dt = clock.tick(60)
    screen.fill((0, 0, 0))

    for b in bricks:
        screen.blit(brick, b)

    screen.blit(paddle, paddle_rect)
    screen.blit(ball, ball_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    # controls
    pressed = pygame.key.get_pressed()
    if pressed[K_LEFT]:
        paddleX -= 0.75 * dt
    if pressed[K_RIGHT]:
        paddleX += 0.75 * dt
    paddle_rect[0], paddle_rect[1] = paddleX, paddleY

    if pressed[K_SPACE]:
        ball_served = True
    if ball_served:
        ball_rect[0] += sx
        ball_rect[1] += sy

    if pressed[K_ESCAPE]:
        game_over = True

    # ball collision with paddle
    if paddle_rect[0] + paddle_rect.width >= ball_rect[0] >= paddle_rect[0] and \
            ball_rect[1] + ball_rect.height >= paddle_rect[1] and \
            sy > 0:
        sy *= -1
        sx *=1.5 # increase difficulty and speed
        sy *=1.1
        continue

    delete_brick = None
    for b in bricks:
        bx, by = b
        if bx <= ball_rect[0] <= bx + brick_rect.width and \
            by <= ball_rect[1] <= by + brick_rect.height:
            delete_brick = b

            if ball_rect[0] <= bx +2: # 2 is for colliding with brick a little bit
                sx *= -1
            elif ball_rect[0] >= bx + brick_rect.width - 2:
                sx *= -1
            if ball_rect[1] <= by + 2:
                sy *= -1
            elif ball_rect[1] >= by + brick_rect.height - 2:
                sy *= -1

    if delete_brick is not None:
        bricks.remove(delete_brick)


    # keep ball within boundary
    if ball_rect[1] <= 0: # top
        ball_rect[1] = 0
        sy *= -1

    if ball_rect[1] >= screen.get_height() - ball_rect.height: # bottom
        # reset ball & paddle back to start pos'
        ball_served = False
        sx, sy = ball_speed
        ball_rect.topleft = ball_start

        paddleX, paddleY = screen.get_width()/2 - paddle.get_width()/2, screen.get_height() - paddle.get_height()

    if ball_rect[0] <= 0: # left
        ball_rect[0] = 0
        sx *= -1

    if ball_rect[0] >= screen.get_width() - ball_rect.width: # right
        ball_rect[0] = screen.get_width() - ball_rect.width
        sx *= -1

    # keep paddle within boundary
    if paddleX > (screen.get_width() - paddle.get_width()):
        paddleX = screen.get_width() - paddle.get_width()
    if paddleX < 0:
        paddleX = 0

    pygame.display.update()
pygame.quit()
