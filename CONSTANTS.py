from IMAGES import *
from funkcje import *


PURPLE = (255, 0, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

BASE_RECT = pygame.Rect(BASE_X, BASE_Y, (3 * TILESIZE), (3 * TILESIZE))
BASE_HP_STRING = pygame.Rect(BASE_X + (TILESIZE / 2) + 5, BASE_Y + TILESIZE + 3, 44, 20)

INTERFACE_LOW_HEIGHT = pygame.Rect(MAP_WIDTH, MAP_HEIGHT - 123, MENUSIZE, 123)

#      DMG     RANGE
WIEZE_POLEPSZENIA = (
    ((5, 10), (1, 25), 4),
    ((5, 20), (2, 15), 15),
    ((25, 4), (5, 10), 50)
)

'''
TRASA = (
    (0, 0), (1, 2), (3, 2), (2, 16), (1, 16), (2, 19), (3, 21), (4, 23), (5, 19), (6, 19),
    (9, 19), (10, 22), (12, 18), (13, 18), (14, 18), (15, 23), (16, 16), (8, 16), (7, 10), (6, 8),
    (7, 1), (8, 1), (10, 1), (11, 10), (13, 2), (14, 1), (15, 1), (16, 1), (17, 9), (19, 2),
    (20, 2), (25, 1), (26, 1), (28, 1), (29, 5), (33, 2), (31, 2), (30, 2), (31, 9), (32, 18),
    (33, 18), (31, 22), (30, 20), (29, 14), (30, 14), (33, 12), (6, 12), (5, 12), (6, 14), (21, 6),
    (2, 6), (1, 4), (2, 4), (25, 4), (24, 10), (23, 7), (24, 7), (27, 7), (21, 22)
)
MAPA_DRAW = list((image_load('dane/unused/trasa/{}.jpg'.format(i + 1)), (TRASA[i][0] * TILESIZE, TRASA[i][1] * TILESIZE)) for i in range(len(TRASA)))
MAPA_DRAW.reverse()
'''

MAPA_DRAW = []
for row in range(MAP_TILES_H):
    for column in range(MAP_TILES_W):
        if MAPA[row][column] not in  {1, 3}:
            MAPA_DRAW.append((TEREN[MAPA[row][column]], (column * TILESIZE, row * TILESIZE)))

        # health, speed, damage, points, money, size
ENEMIES = { # hp,  sp, d,  p, m, si
    MYSZ:   ( 80, 100, 1,  2, 1, 20),
    SZCZUR: (150,  90, 2,  4, 2, 22),
    PAJAK:  (300, 110, 3,  8, 3, 24),
    WAZ:    (500, 120, 5, 12, 4, 26)
}

WAVES = (
    (MYSZ,) * 6,
    (MYSZ,) * 15,
    (MYSZ,) * 25 + (SZCZUR,) * 5,
    (MYSZ,) * 20 + (SZCZUR,) * 10,
    (MYSZ,) * 18 + (SZCZUR,) * 15,
    (MYSZ,) * 15 + (SZCZUR,) * 20 + (PAJAK,) * 3,
    (MYSZ,) * 12 + (SZCZUR,) * 20 + (PAJAK,) * 8,
    (MYSZ,) * 10 + (SZCZUR,) * 18 + (PAJAK,) * 15,
    (MYSZ,) * 8  + (SZCZUR,) * 15 + (PAJAK,) * 15 + (WAZ,) * 3,
    (MYSZ,) * 5  + (SZCZUR,) * 12 + (PAJAK,) * 20 + (WAZ,) * 8,
    (MYSZ,) * 3  + (SZCZUR,) * 10 + (PAJAK,) * 20 + (WAZ,) * 15
)

LEN_WAVES = len(WAVES)

pygame.font.init()
FONT30 = pygame.font.SysFont(None, 30)
FONT40 = pygame.font.SysFont(None, 40)
