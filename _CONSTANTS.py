from _IMAGES import *


PURPLE = (255, 0, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

TILESIZE_BY_2 = (TILESIZE // 2)
DRUID_BY_20 = (DRUID_SIZE // 20)
DRUID_BY_10_PLUS_1 = 1 + (DRUID_SIZE // 10)

BASE_HP_STRING = pygame_Rect(BASE_X + TILESIZE_BY_2 + 5, BASE_Y + TILESIZE + 3, 44, 20)

BULLET_COLORS = (
    (0, 255, 255),
    (0, 0, 64),
    (255, 192, 0)
)

#      DMG     RANGE
TOWER_UPGRADES = (
    ((3, 8),  (1, 20),  5),
    ((10, 5), (3, 25),  10),
    ((15, 3), (10, 10), 50)
)

TRACE_TILES = [(image, pygame_Rect(TRACE[i][0] * TILESIZE, TRACE[i][1] * TILESIZE, *(image.get_size()))) for i, image in enumerate(TRACE_IMAGES)]

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

LEN_WAVES_1 = len(WAVES) - 1

pygame_font_init()
FONT30 = pygame_font_SysFont(None, 30)
FONT40 = pygame_font_SysFont(None, 40)
FONT30_render = FONT30.render
FONT40_render = FONT40.render

WINDOW_blits = WINDOW.blits
WINDOW_blit = WINDOW.blit

PYGAME_K1_K2_K3 = {K_1, K_2, K_3}

PLAYER_LEVEL_RECT = pygame_Rect(W_23, 2, 1, 1)
PLAYER_DAMAGE_RECT = pygame_Rect(W_23, 23, 1, 1)
PLAYER_SPEED_RECT = pygame_Rect(W_23, 41, 1, 1)
PLAYER_HEALTH_RECT = pygame_Rect(W_23, 59, 1, 1)
PLAYER_MONEY_RECT = pygame_Rect(W_23, 81, 1, 1)
POINTS_RECT = pygame_Rect(W_10, 100, 1, 1)

RECT_10_DOL = pygame_Rect(W_115, H_73_, 1, 1)
RECT_30_DOL = pygame_Rect(W_115, H_48_, 1, 1)
RECT_50_DOL = pygame_Rect(W_115, H_23_, 1, 1)
DOT_1 = pygame_Rect(W_75, H_73_, 1, 1)
DOT_2 = pygame_Rect(W_75, H_48_, 1, 1)
DOT_3 = pygame_Rect(W_75, H_23_, 1, 1)
