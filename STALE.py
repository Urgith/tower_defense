from funkcje import *

import os


# CHANGEABLE
TILESIZE = 25
MENUSIZE = 150

BASE_LOC_X = 20
BASE_LOC_Y = 22

DRUID_SIZE = 50
DRUID_X = 100
DRUID_Y = 100

FPS_MAX = 2000
PREDKOSC_WYCHODZENIA = 10

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
##################################################
BASE_RECT = pygame.Rect(TILESIZE * BASE_LOC_X, TILESIZE * BASE_LOC_Y, TILESIZE, TILESIZE)

MAP_TILES_W = len(MAPA[0])
MAP_TILES_H = len(MAPA)

MAP_WIDTH = (TILESIZE * MAP_TILES_W)
MAP_HEIGHT = (TILESIZE * MAP_TILES_H)

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.display.set_mode((MAP_WIDTH + MENUSIZE, MAP_HEIGHT))
pygame.display.set_caption('Inwazja')

TRAWA = image_load('dane/trawa.jpg', scale=(MAP_WIDTH, MAP_HEIGHT))

KULA_MOCY = image_load('dane/kula_mocy.png')
DRUID = image_load('dane/druid.png', (0, 0), scale=(DRUID_SIZE, DRUID_SIZE))

zielony = image_load('dane/zielony.jpg')
niebieski = image_load('dane/niebieski.jpg')
zolty = image_load('dane/zolty.jpg')

WIEZE = (
    (zielony, (0,255,0), 10, 10, 100, 10, 200, 4),
    (niebieski, (0,0,255), 30, 40, 150, 15, 75, 5),
    (zolty, (255,255,0), 50, 2, 75, 0, 25, 2),
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
    3:  image_load('dane/las.jpg', scale=(TILESIZE, TILESIZE)),
    5:  lg,
    50: ld,
    6:  pg,
    60: pd,
    7:  pd,
    70: ld,
    8:  pg,
    80: lg
}

MAPA_DRAW = []
for row in range(MAP_TILES_H):
    for column in range(MAP_TILES_W):
        if MAPA[row][column] != 1:
            MAPA_DRAW.append((TEREN[MAPA[row][column]], (column * TILESIZE, row * TILESIZE)))

MYSZ = image_load('dane/mysz.png', (0, 0))
SZCZUR = image_load('dane/szczur.png', (0, 0))
PAJAK = image_load('dane/pajak.png', (0, 0))
WAZ = image_load('dane/waz.png', (0, 0))

ENEMIES = {
    MYSZ:   (100, 1  , 1, 5 , 1, 15),
    SZCZUR: (200, 0.8, 3, 8 , 2, 17),
    PAJAK:  (250, 1.2, 2, 12, 2, 19),
    WAZ:    (350, 1.3, 3, 15, 3, 21)
}

WAVES = (
    (MYSZ,) * 10,
    (MYSZ,) * 15,
    (MYSZ,) * 10 + (SZCZUR,) * 5,
    (MYSZ,) * 10 + (SZCZUR,) * 10,
    (MYSZ,) * 5 + (SZCZUR,) * 20,
    (MYSZ,) * 5 + (SZCZUR,) * 15 + (PAJAK,) * 5,
    (MYSZ,) * 5 + (SZCZUR,) * 15 + (PAJAK,) * 10,
    (SZCZUR,) * 20 + (PAJAK,) * 15,
    (SZCZUR,) * 15 + (PAJAK,) * 20 + (WAZ,) * 5,
    (SZCZUR,) * 10 + (PAJAK,) * 25 + (WAZ,) * 15
)

TEKSTURY = (
    (image_load('dane/zacznij.jpg'), (MAP_WIDTH + 3, MAP_HEIGHT - 123)),
    (image_load('dane/domek.jpg'), (MAP_WIDTH + 3, MAP_HEIGHT - 70)),
    (zielony, (MAP_WIDTH + 93, MAP_HEIGHT - 74)),
    (niebieski, (MAP_WIDTH + 93, MAP_HEIGHT - 49)),
    (zolty, (MAP_WIDTH + 93, MAP_HEIGHT - 24)),
    (image_load('dane/_arrow.png', (0, 0)), (MAP_WIDTH + 5, 2)),
    (image_load('dane/_kula_mocy.png', (0, 0)), (MAP_WIDTH + 6, 25)),
    (image_load('dane/_boots.png', (0, 0)), (MAP_WIDTH + 4, 43)),
    (image_load('dane/_heart.png', (0, 0)), (MAP_WIDTH + 2, 60)),   
    (image_load('dane/_coin.png', (0, 0)), (MAP_WIDTH + 5, 82))
)

TEKSTURY_INTERFEJSU_WIEZY = (
    (image_load('dane/atak_zielony.jpg'), pygame.Rect(MAP_WIDTH + 3, 119, 70, 70)),
    (image_load('dane/zasieg_zielony.jpg'), pygame.Rect(MAP_WIDTH + 78, 119, 70, 70)),
    (image_load('dane/predkosc_zielony.jpg'), pygame.Rect(MAP_WIDTH + 3, 194, 70, 70)),
    (image_load('dane/dolar_zielony.jpg'), pygame.Rect(MAP_WIDTH + 78, 194, 70,70)),
    (image_load('dane/atak_niebieski.jpg'), pygame.Rect(MAP_WIDTH + 3, 119, 70, 70)),
    (image_load('dane/zasieg_niebieski.jpg'), pygame.Rect(MAP_WIDTH + 78, 119, 70, 70)),
    (image_load('dane/przebicie_niebieski.jpg'), pygame.Rect(MAP_WIDTH + 3, 194, 70, 70)),
    (image_load('dane/dolar_niebieski.jpg'), pygame.Rect(MAP_WIDTH + 78, 194, 70, 70)),
    (image_load('dane/atak_zolty.jpg'), pygame.Rect(MAP_WIDTH + 3, 119, 70, 70)),
    (image_load('dane/zasieg_zolty.jpg'), pygame.Rect(MAP_WIDTH + 78, 119, 70, 70)),
    (image_load('dane/elektryzacja_zolty.jpg'), pygame.Rect(MAP_WIDTH + 3, 194, 70, 70)),
    (image_load('dane/dolar_zolty.jpg'), pygame.Rect(MAP_WIDTH + 78, 194, 70, 70))
)

pygame.font.init()
FONT30 = pygame.font.SysFont(None, 30)
FONT40 = pygame.font.SysFont(None, 40)
