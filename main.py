import pygame
import random

pygame.font.init()

# GLOBALS VARS
s_width = 1100
s_height = 800
play_width = 300  # meaning 300 // 10 = 30 width per block ||
play_height = 600  # meaning 600 // 20 = 20 height per block
block_size = 30
row = 10
count = 0


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


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True

    return False


def get_shape():
    return Piece(5, 0, random.choice(shapes))

def draw_map(surface, x, y, count):
    count += 1
    if count == 2:
        map = pygame.image.load('assets/map.png')
        surface.blit(map, (random.randrange(x, x + 245), random.randrange(y, y + 560)))


def draw_objects(count, coordinate_x, coordinate_y, grid, map_score, key_score):
    validation = 0
    print(map_score, key_score)
    if ((count == 320) or (count == 100)) and (validation == 0):
        coordinate_x = (random.randrange(1, 9) * 30) + 400
        coordinate_y = (random.randrange(1, 19) * 30) + 200
        validation += 1
    if (count > 100) and (count <= 140) and (map_score[0] == 0):
        if grid[(coordinate_y - 200)//30][(coordinate_x-400)//30] != (63, 63, 63):
            map_score[0] += 1
            map_score[1] += 1

        map = pygame.image.load('assets/map.png')
        win.blit(map, (coordinate_x, coordinate_y))
        print(map_score)

    if count == 400:
        count = 0
        validation = 0
        print(count)
        map_score[0] = 0
        key_score[0] = 0
    if (count > 320) and (count <= 370) and (key_score[0] == 0):
            if grid[(coordinate_y - 200)//30][(coordinate_x-400)//30] != (63, 63, 63):
                key_score[0] += 1
                key_score[1] += 1
                print(count)
            else:
                key = pygame.image.load('assets/key.png')
                win.blit(key, (coordinate_x, coordinate_y))
    pygame.display.update()
    return count, coordinate_x, coordinate_y, map_score, key_score



def draw_grid(surface, grid, count):
    sx = top_left_x
    sy = top_left_y

    for i in range(len(grid)):
        pygame.draw.line(surface, (94, 94, 94), (sx, sy + i * block_size), (sx + play_width, sy + i * block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (94, 94, 94), (sx + j * block_size, sy),
                             (sx + j * block_size, sy + play_height))


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


def background(surface):
    surface.fill((168, 232, 236))

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



def draw_window(surface, grid, map_score, key_score, count):
    surface.fill((168, 232, 236))

    pygame.font.init()
    title_font = pygame.font.SysFont('Roboto', 60)
    point_font = pygame.font.SysFont('Roboto', 35)

    label = title_font.render('Ilha do Tesouro', 1, (255, 255, 255))
    map_point = point_font.render(str(map_score), 1, (255, 255, 255))
    key_point = point_font.render(str(key_score), 1, (255, 255, 255))

    blue_title = pygame.image.load('assets/blue_title.png')
    key_count = pygame.image.load('assets/key_count.png')
    map_count = pygame.image.load('assets/map_count.png')

    background(surface)
    surface.blit(key_count, (420, 140))
    surface.blit(map_count, (580, 140))
    surface.blit(blue_title, (300, 30))
    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 55))
    surface.blit(map_point, (473, 150))
    surface.blit(key_point, (645, 150))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j],
                             (top_left_x + j * block_size, top_left_y + i * block_size, block_size, block_size), 0)

    pygame.draw.rect(surface, (63, 63, 63), (top_left_x, top_left_y, play_width, play_height), 4)
    draw_grid(surface, grid, count)
    pygame.display.update()


def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont("comicsans", size)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + play_width /2 - (label.get_width()/2), 320))


def main(win):
    locked_positions = {}
    grid = create_grid(locked_positions)
    level_time = 0
    map_count = 0
    coordinate_x = 0
    coordinate_y = 0
    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    count = 0
    fall_speed = 0.27
    score = 0
    map_score = [0, 0]
    key_score = [0, 0]

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()
        level_time += clock.get_rawtime()
        count += 1

        if level_time/1000 > 40:
            level_time = 0
            if fall_speed > 0.12:
                level_time -= 0.005

        # PIECE FALLING
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

        draw_window(win, grid, key_score[1], map_score[1], count)
        count, coordinate_x, coordinate_y, map_score, key_score = draw_objects(count, coordinate_x, coordinate_y, grid, map_score, key_score)


        #Check if user lost
        if check_lost(locked_positions):
            background(win)
            modal = pygame.image.load('assets/game_over.png')
            win.blit(modal, (280, 250))
            draw_text_middle(win, "Argh! Não foi dessa vez", 60, (255, 255, 255))
            text_font = pygame.font.SysFont('Roboto', 30)
            text = text_font.render('Aguarde para jogar', 1, (255, 255, 255))
            win.blit(text, (468, 445))
            pygame.display.update()
            pygame.time.delay(6000)
            run = False

        if ((key_score[1] == 5) and (map_score[1] == 5)):
            draw_text_middle(win, "Boa, pirata!", 60, (255, 255, 255))
            modal = pygame.image.load('assets/game_over.png')
            win.blit(modal, (280, 250))
            draw_text_middle(win, "Ouro!", 60, (255, 255, 255))
            small_text_font = pygame.font.SysFont('Roboto', 36)
            small_text = small_text_font.render('Você econtrou o tesouro!', 1, (255, 255, 255))
            win.blit(small_text, (420, 380))
            text_font = pygame.font.SysFont('Roboto', 30)
            text = text_font.render('Aguarde para jogar', 1, (255, 255, 255))
            win.blit(text, (468, 445))
            pygame.display.update()
            pygame.time.delay(6000)
            run = False



def main_menu(win):
    run = True
    while run:
        win.fill((0,0,0))
        background(win)
        blue_background = pygame.image.load('assets/blue_background.png')
        win.blit(blue_background, (290, 120))
        ship = pygame.image.load('assets/treasure.png')
        win.blit(ship, (460, 400))
        text_font = pygame.font.SysFont('Roboto', 60)
        text = text_font.render('Encontre o tesouro!', 1, (255, 255, 255))
        small_text_font = pygame.font.SysFont('Roboto', 36)
        small_text = small_text_font.render('Pressione qualquer tecla para jogar', 1, (255, 255, 255))
        win.blit(text, (350, 250))
        win.blit(small_text,(340, 320))
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
