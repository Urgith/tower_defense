from CHANGABLE import *
from funkcje import *

import os


MENUSIZE = 5 * TILESIZE  # 5 *
BASE_X = 18 * TILESIZE  # 18 *
BASE_Y = 21 * TILESIZE  # 21 *
DRUID_SIZE = 2 * TILESIZE  # 2 *

MAP_TILES_W = len(MAPA[0])
MAP_TILES_H = len(MAPA)

MAP_WIDTH = (TILESIZE * MAP_TILES_W)
MAP_HEIGHT = (TILESIZE * MAP_TILES_H)

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.display.set_mode((MAP_WIDTH + MENUSIZE, MAP_HEIGHT))

TRAWA = image_load('data/_trawa.jpg')
LAS = image_load('data/trace/las.jpg', scale=(3 * TILESIZE, 3 * TILESIZE))

KULA_MOCY = image_load('data/kula_mocy.png')
DRUID = image_load('data/druid.png', (0, 0), scale=(DRUID_SIZE, DRUID_SIZE))
PRAD = image_load('data/prad.png', (0, 0))

zielony = image_load('data/towers/zielony.jpg')
niebieski = image_load('data/towers/niebieski.jpg')
zolty = image_load('data/towers/zolty.jpg')
                        # cost, damage, speed, range, reload, size
                        #   c,  d,  sp,  ra,  re, s
WIEZE = (
    (zielony, (0,255,0),   10, 10, 200, 150, 200, 4),
    (niebieski, (0,0,255), 30, 20, 100, 100, 400, 6),
    (zolty, (255,255,0),   50,  5, 300,  80, 100, 3),
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

lg = image_load('data/trace/lg.jpg', scale=(TILESIZE, TILESIZE))
ld = image_load('data/trace/ld.jpg', scale=(TILESIZE, TILESIZE))
pg = image_load('data/trace/pg.jpg', scale=(TILESIZE, TILESIZE))
pd = image_load('data/trace/pd.jpg', scale=(TILESIZE, TILESIZE))

TEREN = {
    0:  image_load('data/trace/poziomo.jpg', scale=(TILESIZE, TILESIZE)),
    10: image_load('data/trace/pionowo.jpg', scale=(TILESIZE, TILESIZE)),
    5:  lg,
    50: ld,
    6:  pg,
    60: pd,
    7:  pd,
    70: ld,
    8:  pg,
    80: lg
}

MYSZ = image_load('data/enemies/mysz.png', (0, 0), scale=(20, 20))
SZCZUR = image_load('data/enemies/szczur.png', (0, 0), scale=(22, 22))
PAJAK = image_load('data/enemies/pajak.png', (0, 0), scale=(24, 24))
WAZ = image_load('data/enemies/waz.png', (0, 0), scale=(26, 26))

W_3 = MAP_WIDTH + 3
W_23 = MAP_WIDTH + 23
W_75 = MAP_WIDTH + 75
W_93 = MAP_WIDTH + 93
W_115 = MAP_WIDTH + 115

TEKSTURY = (
    (image_load('data/zacznij.jpg'), pygame.Rect(W_3, MAP_HEIGHT - 125, 50, 50)),
    (image_load('data/domek.jpg'), pygame.Rect(W_3, MAP_HEIGHT - 72, 70, 70)),
    (zielony, pygame.Rect(W_93, MAP_HEIGHT - 74, 20, 20)),
    (niebieski, pygame.Rect(W_93, MAP_HEIGHT - 49, 20, 20)),
    (zolty, pygame.Rect(W_93, MAP_HEIGHT - 24, 20, 20)),
    (image_load('data/stats_icons/_arrow.png', (0, 0)), (MAP_WIDTH + 5, 2)),
    (image_load('data/stats_icons/_kula_mocy.png', (0, 0)), (MAP_WIDTH + 6, 25)),
    (image_load('data/stats_icons/_boots.png', (0, 0)), (MAP_WIDTH + 4, 43)),
    (image_load('data/stats_icons/_heart.png', (0, 0)), (MAP_WIDTH + 2, 60)),   
    (image_load('data/stats_icons/_coin.png', (0, 0)), (MAP_WIDTH + 5, 82))
)

RECT3 = pygame.Rect(W_3, 119, 70, 70)
RECT78 = pygame.Rect(MAP_WIDTH + 78, 119, 70, 70)
RECT_3 = pygame.Rect(W_3, 194, 70, 70)
RECT_78 = pygame.Rect(MAP_WIDTH + 78, 194, 70, 70)

TEKSTURY_INTERFEJSU_WIEZY = (
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
