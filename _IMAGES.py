from imports_and_functions import *
from _CHANGEABLE import *


MENUSIZE = 150
BASE_X = 18 * TILESIZE
BASE_Y = 21 * TILESIZE
DRUID_SIZE = 2 * TILESIZE

MAP_TILES_W = len(AREA[0])
MAP_TILES_H = len(AREA)

MAP_WIDTH = (TILESIZE * MAP_TILES_W)
MAP_HEIGHT = (TILESIZE * MAP_TILES_H)

W_8_ = (MAP_WIDTH - 8)
W_3 = (MAP_WIDTH + 3)
W_5 = (MAP_WIDTH + 5)
W_10 = (MAP_WIDTH + 10)
W_23 = (MAP_WIDTH + 23)
W_57 = (MAP_WIDTH + 57)
W_75 = (MAP_WIDTH + 75)
W_78 = (MAP_WIDTH + 78)
W_93 = (MAP_WIDTH + 93)
W_115 = (MAP_WIDTH + 115)

H_105_ = (MAP_HEIGHT - 105)
H_73_ = (MAP_HEIGHT - 73)
H_48_ = (MAP_HEIGHT - 48)
H_23_ = (MAP_HEIGHT - 23)
H_8_ = (MAP_HEIGHT - 8)

RECT3 = pygame_Rect(W_3, 119, 70, 70)
RECT78 = pygame_Rect(W_78, 119, 70, 70)
RECT_3 = pygame_Rect(W_3, 194, 70, 70)
RECT_78 = pygame_Rect(W_78, 194, 70, 70)

BASE_RECT = pygame_Rect(BASE_X, BASE_Y, (3 * TILESIZE), (3 * TILESIZE))

GAME_RECT = pygame_Rect(0, 0, MAP_WIDTH, MAP_HEIGHT)
INTERFACE_RECT = pygame_Rect(W_23, 0, MAP_WIDTH + MENUSIZE - W_23, 119)
TOWER_INTERFACE_RECT = pygame_Rect(MAP_WIDTH, 0, MENUSIZE, 306)
ROUND_RECT = pygame_Rect(W_115 + 10, H_105_, MAP_WIDTH + MENUSIZE - W_115 - 10, 17)

update_rects = [GAME_RECT, INTERFACE_RECT, ROUND_RECT]

W_MINUS_DRUID = (MAP_WIDTH - DRUID_SIZE)
H_MINUS_DRUID = (MAP_HEIGHT - DRUID_SIZE)

import os
os.environ['SDL_VIDEO_CENTERED'] = '1'
WINDOW = pygame_display_set_mode((MAP_WIDTH + MENUSIZE, MAP_HEIGHT), FULLSCREEN)

GRASS = (image_load('data/trawa.jpg', scale=(MAP_WIDTH, MAP_HEIGHT)), (0, 0, MAP_WIDTH, MAP_HEIGHT))
FOREST = (image_load('data/trace/las.jpg', scale=(3 * TILESIZE, 3 * TILESIZE)), BASE_RECT)

MAGIC_BALL = image_load('data/kula_mocy.png', (0, 0))
DRUID = image_load('data/druid.png', (0, 0), scale=(DRUID_SIZE, DRUID_SIZE))
ELECTRO = image_load('data/prad.png', (0, 0))

TRACE = (
    (0, 0), (1, 2), (3, 2), (2, 16), (1, 16), (2, 19), (3, 21), (4, 23), (5, 19), (6, 19),
    (9, 19), (10, 22), (12, 18), (13, 18), (14, 18), (15, 23), (16, 16), (8, 16), (7, 10), (6, 8),
    (7, 1), (8, 1), (10, 1), (11, 10), (13, 2), (14, 1), (15, 1), (16, 1), (17, 9), (19, 2),
    (20, 2), (25, 1), (26, 1), (28, 1), (29, 5), (33, 2), (31, 2), (30, 2), (31, 9), (32, 18),
    (33, 18), (31, 22), (30, 20), (29, 14), (30, 14), (33, 12), (6, 12), (5, 12), (6, 14), (21, 6),
    (2, 6), (1, 4), (2, 4), (25, 4), (24, 10), (23, 7), (24, 7), (27, 7), (21, 22)
)
TRACE_IMAGES = [(image_load(f'data/trace/trace/{i}.jpg')) for i in range(len(TRACE))]

green = image_load('data/towers/zielony.jpg')
blue = image_load('data/towers/niebieski.jpg')
yellow = image_load('data/towers/zolty.jpg')
                        # cost, damage, speed, range, reload, size
                        #   c,  d,  sp,  ra,  re, s
TOWERS = (
    (green, (0,255,0),     10, 10, 250, 130, 200, 5),
    (blue, (0,0,255),      30, 15, 150, 100, 300, 8),
    (yellow, (255,255,0),  50,  5, 350,  80, 100, 4),
    (image_load('data/towers/zielony2.jpg'), 0),
    (image_load('data/towers/niebieski2.jpg'), 0),
    (image_load('data/towers/zolty2.jpg'), 0),
    (image_load('data/towers/zielony3.jpg'), 0),
    (image_load('data/towers/niebieski3.jpg'), 0),
    (image_load('data/towers/zolty3.jpg'), 0),
    (image_load('data/towers/zielony4.jpg'), 0),
    (image_load('data/towers/niebieski4.jpg'), 0),
    (image_load('data/towers/zolty4.jpg'), 0),
    (image_load('data/towers/zielony5.jpg'), 0),
    (image_load('data/towers/niebieski5.jpg'), 0),
    (image_load('data/towers/zolty5.jpg'), 0),
    (image_load('data/towers/zielony6.jpg'), 0),
    (image_load('data/towers/niebieski6.jpg'), 0),
    (image_load('data/towers/zolty6.jpg'), 0)
)

l_up = image_load('data/trace/lg.jpg', scale=(TILESIZE, TILESIZE))
l_down = image_load('data/trace/ld.jpg', scale=(TILESIZE, TILESIZE))
r_up = image_load('data/trace/pg.jpg', scale=(TILESIZE, TILESIZE))
r_down = image_load('data/trace/pd.jpg', scale=(TILESIZE, TILESIZE))
TERRAIN = {
    0:  image_load('data/trace/poziomo.jpg', scale=(TILESIZE, TILESIZE)),
    10: image_load('data/trace/pionowo.jpg', scale=(TILESIZE, TILESIZE)),
    5:  l_up,
    50: l_down,
    6:  r_up,
    60: r_down,
    7:  r_down,
    70: l_down,
    8:  r_up,
    80: l_up
}

TEXTURES = (
    (image_load('data/zacznij.jpg'), pygame_Rect(W_3, MAP_HEIGHT - 125, 50, 50)),
    (image_load('data/domek.jpg'), pygame_Rect(W_3, MAP_HEIGHT - 72, 70, 70)),
    (green, pygame_Rect(W_93, MAP_HEIGHT - 74, 20, 20)),
    (blue, pygame_Rect(W_93, MAP_HEIGHT - 49, 20, 20)),
    (yellow, pygame_Rect(W_93, MAP_HEIGHT - 24, 20, 20)),
    (image_load('data/interface_icons/arrow.png', (0, 0)), pygame_Rect(W_5, 2, 13, 15)),
    (image_load('data/interface_icons/kula_mocy.png', (0, 0)), pygame_Rect(MAP_WIDTH + 6, 25, 12, 12)),
    (image_load('data/interface_icons/boots.png', (0, 0)), pygame_Rect(MAP_WIDTH + 4, 43, 15, 14)),
    (image_load('data/interface_icons/heart.png', (0, 0)), pygame_Rect(MAP_WIDTH + 2, 60, 21, 20)),   
    (image_load('data/interface_icons/coin.png', (0, 0)), pygame_Rect(W_5, 82, 15, 15))
)

TOWER_TEXTURES = (
    (image_load('data/upgrades/atak_zielony.jpg'), RECT3),
    (image_load('data/upgrades/zasieg_zielony.jpg'), RECT78),
    (image_load('data/upgrades/predkosc_zielony.jpg'), RECT_3),
    (image_load('data/upgrades/dolar_zielony.jpg'), RECT_78),
    (image_load('data/upgrades/atak_niebieski.jpg'), RECT3),
    (image_load('data/upgrades/zasieg_niebieski.jpg'), RECT78),
    (image_load('data/upgrades/przebicie_niebieski.jpg'), RECT_3),
    (image_load('data/upgrades/dolar_niebieski.jpg'), RECT_78),
    (image_load('data/upgrades/atak_zolty.jpg'), RECT3),
    (image_load('data/upgrades/zasieg_zolty.jpg'), RECT78),
    (image_load('data/upgrades/elektryzacja_zolty.jpg'), RECT_3),
    (image_load('data/upgrades/dolar_zolty.jpg'), RECT_78)
)

MOUSE = image_load('data/enemies/mouse_r.png', (0, 0), scale=(20, 20))
RAT = image_load('data/enemies/rat_r.png', (0, 0), scale=(22, 22))
SPIDER = image_load('data/enemies/spider_r.png', (0, 0), scale=(24, 24))
SNAKE = image_load('data/enemies/snake_r.png', (0, 0), scale=(26, 26))
