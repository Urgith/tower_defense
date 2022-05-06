from _IMAGES import *


PURPLE = (255, 0, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

TILESIZE_BY_2 = (TILESIZE // 2)

BASE_RECT = pygame_Rect(BASE_X, BASE_Y, (3 * TILESIZE), (3 * TILESIZE))
BASE_HP_STRING = pygame_Rect(BASE_X + TILESIZE_BY_2 + 5, BASE_Y + TILESIZE + 3, 44, 20)

#      DMG     RANGE
TOWER_UPGRADES = (
    ((3, 8),  (1, 20),  5),
    ((10, 5), (3, 25),  10),
    ((15, 3), (10, 10), 50)
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
    [(MOUSE, GAP) for _ in range(5)],
    [(MOUSE, GAP)  for _ in range(10)],
    [(MOUSE, GAP) for _ in range(13)] + [(RAT, GAP) for _ in range(2)],
    [(MOUSE, GAP) for _ in range(16)] + [(RAT, GAP) for _ in range(5)],
    [(MOUSE, GAP) for _ in range(18)] + [(RAT, GAP) for _ in range(10)],
    [(MOUSE, GAP) for _ in range(15)] + [(RAT, GAP) for _ in range(15)] + [(SPIDER, GAP) for _ in range(3)],
    [(MOUSE, GAP) for _ in range(12)] + [(RAT, GAP) for _ in range(18)] + [(SPIDER, GAP) for _ in range(6)],
    [(MOUSE, GAP) for _ in range(10)] + [(RAT, GAP) for _ in range(18)] + [(SPIDER, GAP) for _ in range(12)],
    [(MOUSE, GAP) for _ in range(8)]  + [(RAT, GAP) for _ in range(15)] + [(SPIDER, GAP) for _ in range(15)] + [(SNAKE, GAP) for _ in range(2)],
    [(MOUSE, GAP) for _ in range(5)]  + [(RAT, GAP) for _ in range(12)] + [(SPIDER, GAP) for _ in range(18)] + [(SNAKE, GAP) for _ in range(6)],
    [(MOUSE, GAP) for _ in range(3)]  + [(RAT, GAP) for _ in range(10)] + [(SPIDER, GAP) for _ in range(20)] + [(SNAKE, GAP) for _ in range(12)]
)

OPPONENTS_GAPS = (
    [[opponent[1] for opponent in wave] for wave in WAVES]
)

LEN_WAVES = len(WAVES)

pygame_font_init()
FONT30 = pygame_font_SysFont(None, 30)
FONT40 = pygame_font_SysFont(None, 40)

PYGAME_K1_K2_K3 = {K_1, K_2, K_3}
