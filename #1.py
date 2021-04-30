import pygame
import random

pygame.font.init()
pygame.mixer.init()

# GLOBALS VARS
s_width = 1100
s_height = 800
play_width = 300  # meaning 300 // 10 = 30 width per block ||
play_height = 600  # meaning 600 // 20 = 20 height per block
block_size = 30
row = 10

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

# SHAPE FORMATS

S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(76, 80, 237), (76, 80, 237), (35, 185, 114), (237, 99, 76), (236, 145, 48), (236, 145, 48),
                (51, 106, 147)]


class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.shape_color = shape_colors[shapes.index(shape)]
        self.rotation = 0

# class map(object):
#     def __init__(self, x, y, shape):
#         self.x = x
#         self.y = y
#         self.shape = shape
#         self.shape_color = shape_colors[]
def create_grid(locked_positions={}):
    grid = [[(63, 63, 63) for x in range(10)] for x in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                c = locked_positions[(j, i)]
                grid[i][j] = c
    return grid


def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)
    return positions


def valid_space(shape, grid):
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (63, 63, 63)] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True
    return formatted


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True

    return False


def get_shape():
    return Piece(5, 0, random.choice(shapes))

def draw_map(surface, x, y):
    map = pygame.image.load('assets/map.png')
    surface.blit(map, (random.randrange(x, x + 245), random.randrange(y, y + 560)))

# (random.randrange(x, x + 300)
def draw_text_middle(text, size, color, surface):
    pass


def draw_grid(surface, grid):
    sx = top_left_x
    sy = top_left_y

    for i in range(len(grid)):
        pygame.draw.line(surface, (94, 94, 94), (sx, sy + i * block_size), (sx + play_width, sy + i * block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (94, 94, 94), (sx + j * block_size, sy),
                             (sx + j * block_size, sy + play_height))
    # formatted = convert_shape_format(shape)

    draw_map(surface, sx, sy)

def clear_rows(grid, locked):
    inc = 0
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        if (63, 63, 63) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                new_key = (x, y + inc)
                locked[new_key] = locked.pop(key)
    return inc


def draw_next_shape(shape, surface):
    pass


# def randomSnack(item):
#     positions = item.shape
#
#     while True:
#         x = random.randrange(1, 9)
#         y = random.randrange(1, 19)
#         if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
#                continue
#         else:
#                break
#
#     return (x,y)


# class maps():
#     rows = 20
#     width = 300
#
#     def __init__(self, start, color=(255, 0, 0)):
#         self.position = start
#         self.color = color
#
#     def draw(self, grid):
#         dis = 30
#         i = 0
#         j = 0
#
#         pygame.draw.rect(grid, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))


# def random_map():
    # positions = shape.shape[shape.rotation % len(shape.shape)]

    # while True:
    #     x = 2
    #     y = 5
    #     # if locked_positions == positions:
    #     #     break
    #     # elif locked_positions ==
    #     # else:
    #     #     continue
    #     return (x, y)

#
# class keys(maps):
#     image = pygame.image.load('assets/key.png')
#
#     def draw(self, grid):
#         self.hitbox = (self.x, self.y)
#
#         pygame.draw.rect(grid, (63, 63, 63), self.hitbox, 2)
#         grid.blit(self.image, (self.x, self.y))
#         pygame.draw.rect(grid, (255, 0, 0), self.hitbox, 2)

def background(surface):
    surface.fill((168, 232, 236))

    pygame.mixer.init()
    pygame.font.init()
    title_font = pygame.font.SysFont('Roboto', 60)
    point_font = pygame.font.SysFont('Roboto', 35)

    wave = pygame.image.load('assets/waves.png')
    left_island = pygame.image.load('assets/left_island.png')
    right_island = pygame.image.load('assets/right_island.png')
    single_wave = pygame.image.load('assets/single_wave.png')
    yellow = pygame.image.load('assets/yellow.png')
    sun = pygame.image.load('assets/sun.png')
    ship = pygame.image.load('assets/ship.png')

    surface.blit(sun, (950, 50))
    surface.blit(left_island, (0, 450))
    surface.blit(right_island, (710, 400))
    surface.blit(wave, (-30, 600))
    surface.blit(ship, (50, 600))
    surface.blit(single_wave, (0, 700))
    surface.blit(single_wave, (250, 700))
    surface.blit(yellow, ((top_left_x + play_width / 2) - (yellow.get_width() / 2), 0))


def draw_window(surface, grid, score):
    surface.fill((168, 232, 236))

    pygame.mixer.init()
    pygame.font.init()
    title_font = pygame.font.SysFont('Roboto', 60)
    point_font = pygame.font.SysFont('Roboto', 35)

    label = title_font.render('Ilha do Tesouro', 1, (255, 255, 255))
    point = point_font.render(str(score), 1, (255, 255, 255))

    blue_title = pygame.image.load('assets/blue_title.png')
    key_count = pygame.image.load('assets/key_count.png')
    map_count = pygame.image.load('assets/map_count.png')

    background(surface)
    surface.blit(key_count, (420, 140))
    surface.blit(map_count, (580, 140))
    surface.blit(blue_title, (300, 30))
    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 55))
    surface.blit(point, (473, 150))
    surface.blit(point, (645, 150))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j],
                             (top_left_x + j * block_size, top_left_y + i * block_size, block_size, block_size), 0)

    pygame.draw.rect(surface, (63, 63, 63), (top_left_x, top_left_y, play_width, play_height), 4)
    draw_grid(surface, grid)
    pygame.display.update()


def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont("comicsans", size)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + play_width /2 - (label.get_width()/2), 320))


def main(win):
    locked_positions = {}
    grid = create_grid(locked_positions)
    level_time = 0
    map_count = 1
    key_count = 1

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    # obstacle = draw_map()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    score = 0
    # key = keys(random_key(, current_piece))
    # map = maps((random_map()))
    # map.draw(win)

    # try:
    #     snack = maps(random_map(current_piece, locked_positions), color=(0, 255, 0))
    # except:
    #     print('nao')

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()
        level_time += clock.get_rawtime()

        if level_time/1000 > 40:
            level_time = 0
            if fall_speed > 0.12:
                level_time -= 0.005

        # PIECE FALLING CODE
        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True
        # PIECE FALLING CODE END

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.rotation -= 1

        shape_pos = convert_shape_format(current_piece)

        # add color of piece to the grid for drawing
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:  # If we are not above the screen
                grid[y][x] = current_piece.shape_color
        # IF PIECE HIT GROUND
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.shape_color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            clear_rows(grid, locked_positions)

        draw_window(win, grid, score)

        # Check if user lost
        if check_lost(locked_positions):
            background(win)
            modal = pygame.image.load('assets/game_over.png')
            win.blit(modal, (280, 250))
            draw_text_middle(win, "Não foi dessa vez", 60, (255, 255, 255))
            pygame.display.update()
            pygame.time.delay(8000)
            run = False

        if key_count == 0 and map_count == 0:
            background(win)
            modal = pygame.image.load('assets/game_over.png')
            win.blit(modal, (280, 250))
            draw_text_middle(win, "Vitória!", 60, (255, 255, 255))
            pygame.display.update()
            pygame.time.delay(8000)
            run = False
            title_font = pygame.font.SysFont('Roboto', 60)
            w_button = title_font.render('Pressione', 1, (255, 255, 255))
            win.blit(w_button, (top_left_x + play_width / 2 - (w_button.get_width() / 2), 55))
            pygame.display.update()




def main_menu(win):
    run = True

    while run:
        draw_text_middle(win, "Piratas de BV", 60, (255, 255, 255))
        pygame.display.update()
        win.fill((0,0,0))
        background(win)
        blue_background = pygame.image.load('assets/blue_background.png')
        win.blit(blue_background, (280, 100))
        red_button = pygame.image.load('assets/red_button.png')
        win.blit(red_button, (365, 650))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(win)

    pygame.display.quit()



win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')

main_menu(win)# start game
