import pygame
import random

"""
[0][1][2]
[3][4][5]
[6][7][8]
"""
blocks = [
    [[1, 4, 7], [3, 4, 5]],  # straight
    [[1, 3, 4, 5, 7]],  # cross
    [[0, 1, 4, 5], [1, 3, 4, 6]],  # two on two 1
    [[1, 2, 3, 4], [0, 3, 4, 7]],  # two on two 2
    [[0, 1, 3, 6], [0, 1, 2, 5], [2, 5, 7, 8], [3, 6, 7, 8]],  # L-shape 1
    [[1, 2, 5, 8], [5, 6, 7, 8], [0, 3, 6, 7], [0, 1, 2, 3]],  # L-shape 2
    [[4, 6, 7, 8], [0, 3, 4, 6], [0, 1, 2, 4], [2, 4, 5, 8]],  # T-shape
    [[0, 1, 3, 4]]  # Square
]

colors = [
    (255, 255, 5),
    (255, 123, 255),
    (0, 255, 200),
    (255, 255, 255),
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
]


class Block:
    def __init__(self):
        self.x = starting_pos[0]
        self.y = starting_pos[1]
        self.type = random.randint(0, len(blocks) - 1)  # what shape it is
        self.rotation = 0  # what rotation of the shape it is
        self.color = colors[random.randint(0, len(colors) - 1)]

    def shape(self):
        return blocks[self.type][self.rotation]


def rotate():
    last_rotation = block.rotation
    block.rotation = (block.rotation + 1) % len(blocks[block.type])
    can_rotate = True
    for y in range(3):
        for x in range(3):
            if y * 3 + x in block.shape():
                #  check if rotation will put piece off grid
                if collides(0, 0):
                    can_rotate = False
    if not can_rotate:
        block.rotation = last_rotation


def draw_block():
    """ Draw Tetris shapes """
    for y in range(3):  # 3 x 3 matrix
        for x in range(3):
            if y * 3 + x in block.shape():  # flatten matrix
                pygame.draw.rect(screen, block.color,
                                 [(x + block.x) * grid_size + x_gap + 1,
                                  (y + block.y) * grid_size + y_gap + 1,
                                  grid_size - 2, grid_size - 2]
                                 )


def draw_grid(cols, rows, grid_size, x_gap, y_gap):
    """ draw game grid based on screen size """
    for y in range(rows):  # rows
        for x in range(cols):  # cols
            pygame.draw.rect(screen, (100, 100, 100),
                             [x * grid_size + x_gap, y * grid_size + y_gap, grid_size, grid_size], 1)
            if game_board[x][y] != (0, 0, 0):
                pygame.draw.rect(screen, game_board[x][y],
                                 [x * grid_size + x_gap + 1, y * grid_size + y_gap + 1, grid_size - 1, grid_size - 1])


def collides(nx, ny):
    collision = False
    for y in range(3):
        for x in range(3):
            if y * 3 + x in block.shape():
                if block.x + x + nx < 0 or block.x + x + nx > cols - 1:
                    collision = True
                    break
                if block.y + y + ny < 0 or block.y + y + ny > rows - 1:
                    collision = True
                    break
                if game_board[block.x + x + nx][block.y + y + ny] != (0, 0, 0):
                    collision = True
                    break
    return collision


def drop_block():
    """ move blocks down screen, limit to bottom boundary """
    can_drop = True
    for y in range(3):
        for x in range(3):
            if y * 3 + x in block.shape():
                if collides(0, 1):
                    can_drop = False
    if can_drop:
        block.y += 1
    else:
        for y in range(3):
            for x in range(3):
                if y * 3 + x in block.shape():
                    game_board[block.x + x][block.y + y] = block.color
    return can_drop


def side_move(dx):
    can_move = True
    for y in range(3):
        for x in range(3):
            if y * 3 + x in block.shape():
                if collides(dx, 0):
                    can_move = False
    if can_move:
        block.x += dx
    else:
        drop_block()


def find_lines():
    lines = 0
    for y in range(rows):
        empty = 0
        for x in range(cols):
            if game_board[x][y] == (0, 0, 0):
                empty += 1
        if empty == 0:
            lines += 1
            for y2 in range(y, 1, -1):
                for x2 in range(cols):
                    game_board[x2][y2] = game_board[x2][y2 - 1]
    return lines


pygame.init()
screen = pygame.display.set_mode((400, 600))
pygame.display.set_caption("Py Tetris")

grid_size = 30
cols = screen.get_width() // grid_size
rows = screen.get_height() // grid_size
x_gap = (screen.get_width() - cols * grid_size) // 2  # 20 / 2 = 10
y_gap = (screen.get_height() - rows * grid_size) // 2

starting_pos = ((cols - 1) // 2, 0)

game_over = False
block = Block()

clock = pygame.time.Clock()
fps = 8

game_board = []
#  initialize game board
for i in range(cols):
    new_col = []
    for j in range(rows):
        new_col.append((0, 0, 0))
    game_board.append(new_col)

score = 0
font = pygame.font.SysFont("Arial", 24, True, False)
font2 = pygame.font.SysFont("Arial", 50, True, False)
finished_text = font2.render("Game Over :(", True, (255, 255, 255))
ftpos = ((screen.get_width() - finished_text.get_width()) // 2,
         (screen.get_height() - finished_text.get_height()) // 2)

game_finished = False
while not game_over:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
            continue
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                rotate()
            if event.key == pygame.K_ESCAPE:
                game_over = True
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            side_move(-1)
        if event.key == pygame.K_RIGHT:
            side_move(1)

    screen.fill((0, 0, 0))
    draw_grid(cols, rows, grid_size, x_gap, y_gap)
    if block is not None:
        draw_block()
        if event.type != pygame.KEYDOWN:
            if not drop_block():
                score += find_lines()
                block = Block()
                if collides(0, 0):
                    game_finished = True
    text = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(text, [0, 0])
    if game_finished:
        screen.blit(finished_text, ftpos)

    pygame.display.update()
pygame.quit()
