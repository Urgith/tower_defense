from _IMAGES import *


PURPLE = (255, 0, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

TILESIZE_BY_2 = (TILESIZE / 2)

BASE_RECT = pygame.Rect(BASE_X, BASE_Y, (3 * TILESIZE), (3 * TILESIZE))
BASE_HP_STRING = pygame.Rect(BASE_X + TILESIZE_BY_2 + 5, BASE_Y + TILESIZE + 3, 44, 20)

#      DMG     RANGE
TOWER_UPGRADES = (
    ((5, 10), (1, 25), 4),
    ((5, 20), (2, 15), 15),
    ((25, 4), (5, 10), 50)
)

'''
INTERFACE_LOW_HEIGHT = pygame.Rect(MAP_WIDTH, MAP_HEIGHT - 123, MENUSIZE, 123)

TRASA = (
    (0, 0), (1, 2), (3, 2), (2, 16), (1, 16), (2, 19), (3, 21), (4, 23), (5, 19), (6, 19),
    (9, 19), (10, 22), (12, 18), (13, 18), (14, 18), (15, 23), (16, 16), (8, 16), (7, 10), (6, 8),
    (7, 1), (8, 1), (10, 1), (11, 10), (13, 2), (14, 1), (15, 1), (16, 1), (17, 9), (19, 2),
    (20, 2), (25, 1), (26, 1), (28, 1), (29, 5), (33, 2), (31, 2), (30, 2), (31, 9), (32, 18),
    (33, 18), (31, 22), (30, 20), (29, 14), (30, 14), (33, 12), (6, 12), (5, 12), (6, 14), (21, 6),
    (2, 6), (1, 4), (2, 4), (25, 4), (24, 10), (23, 7), (24, 7), (27, 7), (21, 22)
)
MAP_DRAW = list((image_load('dane/unused/trasa/{}.jpg'.format(i + 1)), (TRASA[i][0] * TILESIZE, TRASA[i][1] * TILESIZE)) for i in range(len(TRASA)))
MAP_DRAW.reverse()
'''

MAP_DRAW = []
for row in range(MAP_TILES_H):
    for column in range(MAP_TILES_W):
        if AREA[row][column] not in  {1, 3}:
            MAP_DRAW.append((TERRAIN[AREA[row][column]], (column * TILESIZE, row * TILESIZE)))

        # health, speed, damage, points, money, size
ENEMIES = { # hp,  sp, d,  p, m, si
    MOUSE:  ( 80, 100, 1,  2, 1, 20),
    RAT:    (150,  90, 2,  4, 2, 22),
    SPIDER: (300, 110, 3,  8, 3, 24),
    SNAKE:  (500, 120, 5, 12, 4, 26)
}

WAVES = (
    (MOUSE,) * 6,
    (MOUSE,) * 15,
    (MOUSE,) * 25 + (RAT,) * 5,
    (MOUSE,) * 20 + (RAT,) * 10,
    (MOUSE,) * 18 + (RAT,) * 15,
    (MOUSE,) * 15 + (RAT,) * 20 + (SPIDER,) * 3,
    (MOUSE,) * 12 + (RAT,) * 20 + (SPIDER,) * 8,
    (MOUSE,) * 10 + (RAT,) * 18 + (SPIDER,) * 15,
    (MOUSE,) * 8  + (RAT,) * 15 + (SPIDER,) * 15 + (SNAKE,) * 3,
    (MOUSE,) * 5  + (RAT,) * 12 + (SPIDER,) * 20 + (SNAKE,) * 8,
    (MOUSE,) * 3  + (RAT,) * 10 + (SPIDER,) * 20 + (SNAKE,) * 15
)

LEN_WAVES = len(WAVES)

pygame.font.init()
FONT30 = pygame.font.SysFont(None, 30)
FONT40 = pygame.font.SysFont(None, 40)

PYGAME_K1_K2_K3 = {pygame.K_1, pygame.K_2, pygame.K_3}
