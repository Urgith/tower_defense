from funkcje import *

import os


# CHANGEABLE
TILESIZE = 30  # 30
MENUSIZE = 5 * TILESIZE  # 5 *

BASE_X = 18 * TILESIZE  # 18 *
BASE_Y = 21 * TILESIZE  # 21 *

DRUID_SIZE = 2 * TILESIZE  # 2 *
DRUID_X = 150  # 150
DRUID_Y = 150  # 150

FRAMERATE = 30  # 30
GAME_SPEED = 0.001  # 0.001
OPPONENTS_GAP = 250  # 250

MAPA = (
    ( 8, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
    (10, 1, 1, 1, 1, 1, 1, 5, 0, 0, 8, 1, 1, 1, 5, 0, 8, 1, 1, 1, 1, 1, 1, 1, 1, 5, 0, 0, 8, 1, 1, 1, 1, 1, 1),
    (50, 0, 0, 8, 1, 1, 1,10, 1, 1,10, 1, 1, 5, 7, 1,10, 1, 1, 5, 0, 0, 0, 0, 0, 7, 1, 1,10, 1,80, 0, 0, 6, 1),
    ( 1, 1, 1,10, 1, 1, 1,10, 1, 1,10, 1, 1,10, 1, 1,10, 1, 1,10, 1, 1, 1, 1, 1, 1, 1, 1,10, 1,10, 1, 1,10, 1),
    ( 1, 5, 0,10, 0, 0, 0,10, 0, 0,10, 0, 0,10, 0, 0,10, 0, 0,10, 0, 0, 0, 0, 0, 8, 1, 1,10, 1,10, 1, 1,10, 1),
    ( 1,10, 1,10, 1, 1, 1,10, 1, 1,10, 1, 1,10, 1, 1,10, 1, 1,10, 1, 1, 1, 1, 1,10, 1, 1,50, 0, 0, 0, 0, 7, 1),
    ( 1,70, 0,10, 0, 0, 0,10, 0, 0,10, 0, 0,10, 0, 0,10, 0, 0,10, 0, 6, 1, 1, 1,10, 1, 1, 1, 1,10, 1, 1, 1, 1),
    ( 1, 1, 1,10, 1, 1, 1,10, 1, 1,10, 1, 1,10, 1, 1,10, 1, 1,10, 1,10, 1, 5, 0,10, 0, 8, 1, 1,10, 1, 1, 1, 1),
    ( 1, 1, 1,10, 1, 1, 5, 7, 1, 1,10, 1, 1,10, 1, 1,10, 1, 1,10, 1,10, 1,10, 1,10, 1,10, 1, 1,10, 1, 1, 1, 1),
    ( 1, 1, 1,10, 1, 1,10, 1, 1, 1,10, 1, 1,10, 1, 1,50, 0, 0, 7, 1,10, 1,10, 1,10, 1,10, 1, 1,50, 8, 1, 1, 1),
    ( 1, 1, 1,10, 1, 1,70, 6, 1, 1,50, 0, 0, 7, 1, 1, 1, 1, 1, 1, 1,10, 1,70, 0,60, 1,10, 1, 1, 1,10, 1, 1, 1),
    ( 1, 1, 1,10, 1, 1, 1,10, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,10, 1, 1, 1, 1, 1,10, 1, 1, 1,10, 1, 1, 1),
    ( 1, 1, 1,10, 1,80, 0,10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,10, 0, 6, 1),
    ( 1, 1, 1,10, 1,10, 1,10, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,10, 1, 1, 1, 1, 1,10, 1, 1, 1,10, 1,10, 1),
    ( 1, 1, 1,10, 1,50, 0,10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 1, 1, 1, 1, 1,10, 1, 5, 0,10, 0, 7, 1),
    ( 1, 1, 1,10, 1, 1, 1,10, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,10, 1,10, 1,10, 1, 1, 1),
    ( 1,80, 0,60, 1, 1, 1,70, 0, 0, 0, 0, 0, 0, 0, 0, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,10, 1,10, 1,10, 1, 1, 1),
    ( 1,10, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,10, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,10, 1,10, 1,10, 1, 1, 1),
    ( 1,10, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5, 0, 8, 1,10, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,10, 1,10, 1,50, 0, 8, 1),
    ( 1,50, 8, 1, 1, 5, 0, 0, 0, 8, 1, 1,10, 1,10, 1,10, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,10, 1,10, 1, 1, 1,10, 1),
    ( 1, 1,10, 1, 1,10, 1, 1, 1,10, 1, 1,10, 1,10, 1,10, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,10, 1,70, 6, 1, 1,10, 1),
    ( 1, 1,50, 8, 1,10, 1, 1, 1,10, 1, 1,10, 1,10, 1,10, 1, 3, 3, 3, 1, 1, 1, 1, 1, 1,10, 1, 1,10, 1, 1,10, 1),
    ( 1, 1, 1,10, 1,10, 1, 1, 1,50, 0, 0, 7, 1,10, 1,10, 1, 3, 3, 3, 0, 0, 0, 0, 0, 0,60, 1, 1,70, 0, 0,60, 1),
    ( 1, 1, 1,50, 0, 7, 1, 1, 1, 1, 1, 1, 1, 1,50, 0, 7, 1, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ( 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
)
#-------------------------------------------------
PURPLE = (255, 0, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

BASE_RECT = pygame.Rect(BASE_X, BASE_Y, (3 * TILESIZE), (3 * TILESIZE))
BASE_HP_STRING = pygame.Rect(BASE_X + (TILESIZE / 2) + 5, BASE_Y + TILESIZE + 3, 44, 20)

MAP_TILES_W = len(MAPA[0])
MAP_TILES_H = len(MAPA)

MAP_WIDTH = (TILESIZE * MAP_TILES_W)
MAP_HEIGHT = (TILESIZE * MAP_TILES_H)

INTERFACE_LOW_HEIGHT = pygame.Rect(MAP_WIDTH, MAP_HEIGHT - 123, MENUSIZE, 123)

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.display.set_mode((MAP_WIDTH + MENUSIZE, MAP_HEIGHT))
pygame.display.set_caption('Inwazja')

TRAWA = image_load('dane/_trawa.jpg')
LAS = image_load('dane/las.jpg', scale=(3 * TILESIZE, 3 * TILESIZE))

KULA_MOCY = image_load('dane/kula_mocy.png')
DRUID = image_load('dane/druid.png', (0, 0), scale=(DRUID_SIZE, DRUID_SIZE))
PRAD = image_load('dane/prad.png', (0, 0))

zielony = image_load('dane/zielony.jpg')
niebieski = image_load('dane/niebieski.jpg')
zolty = image_load('dane/zolty.jpg')
                        # cost, damage, range, reload, life span, size
                        #   c,  d,  ra,  re,    l, s
WIEZE = (
    (zielony, (0,255,0),   10, 10, 100, 100, 1000, 4),
    (niebieski, (0,0,255), 30, 40, 150, 150, 1500, 5),
    (zolty, (255,255,0),   50,  2,  75,  10,  750, 2),
    (image_load('dane/zielony2.jpg'), 0),
    (image_load('dane/niebieski2.jpg'), 0),
    (image_load('dane/zolty2.jpg'), 0),
    (image_load('dane/zielony3.jpg'), 0),
    (image_load('dane/niebieski3.jpg'), 0),
    (image_load('dane/zolty3.jpg'), 0),
    (image_load('dane/zielony4.jpg'), 0),
    (image_load('dane/niebieski4.jpg'), 0),
    (image_load('dane/zolty4.jpg'), 0),
    (image_load('dane/zielony5.jpg'), 0),
    (image_load('dane/niebieski5.jpg'), 0),
    (image_load('dane/zolty5.jpg'), 0),
    (image_load('dane/zielony6.jpg'), 0),
    (image_load('dane/niebieski6.jpg'), 0),
    (image_load('dane/zolty6.jpg'), 0)
)

lg = image_load('dane/lg.jpg', scale=(TILESIZE, TILESIZE))
ld = image_load('dane/ld.jpg', scale=(TILESIZE, TILESIZE))
pg = image_load('dane/pg.jpg', scale=(TILESIZE, TILESIZE))
pd = image_load('dane/pd.jpg', scale=(TILESIZE, TILESIZE))

TEREN = {
    0:  image_load('dane/poziomo.jpg', scale=(TILESIZE, TILESIZE)),
    10: image_load('dane/pionowo.jpg', scale=(TILESIZE, TILESIZE)),
    5:  lg,
    50: ld,
    6:  pg,
    60: pd,
    7:  pd,
    70: ld,
    8:  pg,
    80: lg
}

'''
TRASA = (
    (0, 0), (1, 2), (3, 2), (2, 16), (1, 16), (2, 19), (3, 21), (4, 23), (5, 19), (6, 19),
    (9, 19), (10, 22), (12, 18), (13, 18), (14, 18), (15, 23), (16, 16), (8, 16), (7, 10), (6, 8),
    (7, 1), (8, 1), (10, 1), (11, 10), (13, 2), (14, 1), (15, 1), (16, 1), (17, 9), (19, 2),
    (20, 2), (25, 1), (26, 1), (28, 1), (29, 5), (33, 2), (31, 2), (30, 2), (31, 9), (32, 18),
    (33, 18), (31, 22), (30, 20), (29, 14), (30, 14), (33, 12), (6, 12), (5, 12), (6, 14), (21, 6),
    (2, 6), (1, 4), (2, 4), (25, 4), (24, 10), (23, 7), (24, 7), (27, 7), (21, 22)
)
MAPA_DRAW = list((image_load('dane/trasa/{}.jpg'.format(i + 1)), (TRASA[i][0] * TILESIZE, TRASA[i][1] * TILESIZE)) for i in range(len(TRASA)))
MAPA_DRAW.reverse()
'''

MAPA_DRAW = []
for row in range(MAP_TILES_H):
    for column in range(MAP_TILES_W):
        if MAPA[row][column] not in  {1, 3}:
            MAPA_DRAW.append((TEREN[MAPA[row][column]], (column * TILESIZE, row * TILESIZE)))

MYSZ = image_load('dane/mysz.png', (0, 0))
SZCZUR = image_load('dane/szczur.png', (0, 0))
PAJAK = image_load('dane/pajak.png', (0, 0))
WAZ = image_load('dane/waz.png', (0, 0))
        # health, speed, damage, points, money, size
ENEMIES = { # hp,  sp, d,  p, m, si
    MYSZ:   ( 80, 100, 1,  2, 1, 15),
    SZCZUR: (150,  90, 2,  4, 2, 17),
    PAJAK:  (300, 110, 3,  8, 3, 19),
    WAZ:    (500, 120, 5, 12, 4, 21)
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

W_3 = MAP_WIDTH + 3
W_23 = MAP_WIDTH + 23
W_75 = MAP_WIDTH + 75
W_93 = MAP_WIDTH + 93
W_115 = MAP_WIDTH + 115

TEKSTURY = (
    (image_load('dane/zacznij.jpg'), (W_3, MAP_HEIGHT - 123)),
    (image_load('dane/domek.jpg'), (W_3, MAP_HEIGHT - 70)),
    (zielony, (W_93, MAP_HEIGHT - 74)),
    (niebieski, (W_93, MAP_HEIGHT - 49)),
    (zolty, (W_93, MAP_HEIGHT - 24)),
    (image_load('dane/_arrow.png', (0, 0)), (MAP_WIDTH + 5, 2)),
    (image_load('dane/_kula_mocy.png', (0, 0)), (MAP_WIDTH + 6, 25)),
    (image_load('dane/_boots.png', (0, 0)), (MAP_WIDTH + 4, 43)),
    (image_load('dane/_heart.png', (0, 0)), (MAP_WIDTH + 2, 60)),   
    (image_load('dane/_coin.png', (0, 0)), (MAP_WIDTH + 5, 82))
)

RECT3 = pygame.Rect(W_3, 119, 70, 70)
RECT78 = pygame.Rect(MAP_WIDTH + 78, 119, 70, 70)
RECT_3 = pygame.Rect(W_3, 194, 70, 70)
RECT_78 = pygame.Rect(MAP_WIDTH + 78, 194, 70, 70)

TEKSTURY_INTERFEJSU_WIEZY = (
    (image_load('dane/atak_zielony.jpg'), RECT3),
    (image_load('dane/zasieg_zielony.jpg'), RECT78),
    (image_load('dane/predkosc_zielony.jpg'), RECT_3),
    (image_load('dane/dolar_zielony.jpg'), RECT_78),
    (image_load('dane/atak_niebieski.jpg'), RECT3),
    (image_load('dane/zasieg_niebieski.jpg'), RECT78),
    (image_load('dane/przebicie_niebieski.jpg'), RECT_3),
    (image_load('dane/dolar_niebieski.jpg'), RECT_78),
    (image_load('dane/atak_zolty.jpg'), RECT3),
    (image_load('dane/zasieg_zolty.jpg'), RECT78),
    (image_load('dane/elektryzacja_zolty.jpg'), RECT_3),
    (image_load('dane/dolar_zolty.jpg'), RECT_78)
)

pygame.font.init()
FONT30 = pygame.font.SysFont(None, 30)
FONT40 = pygame.font.SysFont(None, 40)
