from _CHANGEABLE import *
from imports_and_functions import *


MENUSIZE = 150
BASE_X = 18 * TILESIZE
BASE_Y = 21 * TILESIZE
DRUID_SIZE = 2 * TILESIZE

MAP_TILES_W = len(AREA[0])
MAP_TILES_H = len(AREA)

MAP_WIDTH = (TILESIZE * MAP_TILES_W)
MAP_HEIGHT = (TILESIZE * MAP_TILES_H)

GAME_RECT = pygame_Rect(0, 0, MAP_WIDTH + MENUSIZE, MAP_HEIGHT)

W_10_ = MAP_WIDTH - 10
W_8_ = MAP_WIDTH - 8
W_3 = MAP_WIDTH + 3
W_10 = MAP_WIDTH + 10
W_23 = MAP_WIDTH + 23
W_57 = MAP_WIDTH + 57
W_75 = MAP_WIDTH + 75
W_93 = MAP_WIDTH + 93
W_115 = MAP_WIDTH + 115

H_105_ = MAP_HEIGHT - 105
H_73_ = MAP_HEIGHT - 73
H_48_ = MAP_HEIGHT - 48
H_23_ = MAP_HEIGHT - 23
H_10_ = MAP_HEIGHT - 10
H_8_ = MAP_HEIGHT - 8

W_MINUS_DRUID = (MAP_WIDTH - DRUID_SIZE)
H_MINUS_DRUID = (MAP_HEIGHT - DRUID_SIZE)

import os
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame_display_set_mode((MAP_WIDTH + MENUSIZE, MAP_HEIGHT), FULLSCREEN)

GRASS = image_load('data/trawa.jpg', scale=(MAP_WIDTH, MAP_HEIGHT))
FOREST = image_load('data/trace/las.jpg', scale=(3 * TILESIZE, 3 * TILESIZE))

MAGIC_BALL = image_load('data/kula_mocy.png', (0, 0))
DRUID = image_load('data/druid.png', (0, 0), scale=(DRUID_SIZE, DRUID_SIZE))
ELECTRO = image_load('data/prad.png', (0, 0))

green = image_load('data/towers/zielony.jpg')
blue = image_load('data/towers/niebieski.jpg')
yellow = image_load('data/towers/zolty.jpg')
                        # cost, damage, speed, range, reload, size
                        #   c,  d,  sp,  ra,  re, s
TOWERS = (
    (green, (0,255,0),     10, 10, 250, 130, 200, 4),
    (blue, (0,0,255),      30, 15, 150, 100, 300, 6),
    (yellow, (255,255,0),  50,  5, 350,  80, 100, 3),
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

MOUSE = image_load('data/enemies/mouse_r.png', (0, 0), scale=(20, 20))
RAT = image_load('data/enemies/rat_r.png', (0, 0), scale=(22, 22))
SPIDER = image_load('data/enemies/spider_r.png', (0, 0), scale=(24, 24))
SNAKE = image_load('data/enemies/snake_r.png', (0, 0), scale=(26, 26))

TEXTURES = (
    (image_load('data/zacznij.jpg'), pygame_Rect(W_3, MAP_HEIGHT - 125, 50, 50)),
    (image_load('data/domek.jpg'), pygame_Rect(W_3, MAP_HEIGHT - 72, 70, 70)),
    (green, pygame_Rect(W_93, MAP_HEIGHT - 74, 20, 20)),
    (blue, pygame_Rect(W_93, MAP_HEIGHT - 49, 20, 20)),
    (yellow, pygame_Rect(W_93, MAP_HEIGHT - 24, 20, 20)),
    (image_load('data/interface_icons/arrow.png', (0, 0)), (MAP_WIDTH + 5, 2)),
    (image_load('data/interface_icons/kula_mocy.png', (0, 0)), (MAP_WIDTH + 6, 25)),
    (image_load('data/interface_icons/boots.png', (0, 0)), (MAP_WIDTH + 4, 43)),
    (image_load('data/interface_icons/heart.png', (0, 0)), (MAP_WIDTH + 2, 60)),   
    (image_load('data/interface_icons/coin.png', (0, 0)), (MAP_WIDTH + 5, 82))
)

RECT3 = pygame_Rect(W_3, 119, 70, 70)
RECT78 = pygame_Rect(MAP_WIDTH + 78, 119, 70, 70)
RECT_3 = pygame_Rect(W_3, 194, 70, 70)
RECT_78 = pygame_Rect(MAP_WIDTH + 78, 194, 70, 70)

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
