import pygame


def image_load(name, location=None):
    image = pygame.image.load(name).convert()

    if location is not None: 
        image.set_colorkey(image.get_at(location))

    return image


def quit():
    import sys

    pygame.quit()
    sys.exit(0)


pygame.font.init()
pygame.display.set_mode()
pygame.display.set_caption('Inwazja')

lg = image_load('dane/lg.jpg')
ld = image_load('dane/ld.jpg')
pg = image_load('dane/pg.jpg')
pd = image_load('dane/pd.jpg')

TRAWA = image_load('dane/trawa.jpg')

KULA_MOCY = image_load('dane/kula_mocy.png', (0, 0))
DRUID = image_load('dane/druid.png', (0, 0))

MYSZ = image_load('dane/mysz.png', (0, 0))
SZCZUR = image_load('dane/szczur.png', (0, 0))
PAJAK = image_load('dane/pajak.png', (0, 0))
WAZ = image_load('dane/waz.png', (0, 0))

WIEZE = (
    (image_load('dane/zielony.jpg'), (0,255,0), 10, 10, 100, 10, 200, 4),
    (image_load('dane/niebieski.jpg'), (0,0,255), 30, 40, 150, 15,  75, 5),
    (image_load('dane/zolty.jpg'), (255,255,0), 50,  2,  75,  0,  25, 2),
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

TEREN = {
    0:  image_load('dane/poziomo.jpg'),
    10: image_load('dane/pionowo.jpg'),
    3:  image_load('dane/las.jpg'),
    5:  lg,
    50: ld,
    6:  pg,
    60: pd,
    7:  pd,
    70: ld,
    8:  pg,
    80: lg
}

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

ENEMIES = {
    MYSZ:   (100, 1  , 1, 5 , 1, 15),
    SZCZUR: (200, 0.8, 3, 8 , 2, 17),
    PAJAK:  (250, 1.2, 2, 12, 2, 19),
    WAZ:    (350, 1.3, 3, 15, 3, 21)
}

WAVES = (
    (MYSZ,MYSZ,MYSZ,MYSZ,MYSZ,MYSZ,MYSZ,MYSZ,MYSZ,MYSZ),
    (MYSZ,MYSZ,MYSZ,MYSZ,MYSZ,MYSZ,MYSZ,MYSZ,MYSZ,MYSZ,MYSZ,MYSZ,MYSZ,MYSZ,MYSZ),
    (MYSZ,MYSZ,MYSZ,MYSZ,MYSZ,MYSZ,MYSZ,MYSZ,MYSZ,MYSZ,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR),
    (MYSZ,MYSZ,MYSZ,MYSZ,MYSZ,MYSZ,MYSZ,MYSZ,MYSZ,MYSZ,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR),
    (MYSZ,MYSZ,MYSZ,MYSZ,MYSZ,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR),
    (MYSZ,MYSZ,MYSZ,MYSZ,MYSZ,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,PAJAK,PAJAK,PAJAK,PAJAK,PAJAK),
    (MYSZ,MYSZ,MYSZ,MYSZ,MYSZ,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,PAJAK,PAJAK,PAJAK,PAJAK,PAJAK,PAJAK,PAJAK,PAJAK,PAJAK,PAJAK),
    (SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,PAJAK,PAJAK,PAJAK,PAJAK,PAJAK,PAJAK,PAJAK,PAJAK,PAJAK,PAJAK,PAJAK,PAJAK,PAJAK,PAJAK,PAJAK),
    (SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,PAJAK,PAJAK,PAJAK,PAJAK,PAJAK,PAJAK,PAJAK,PAJAK,PAJAK,PAJAK,PAJAK,PAJAK,PAJAK,PAJAK,PAJAK,PAJAK,PAJAK,PAJAK,PAJAK,PAJAK,WAZ,WAZ,WAZ,WAZ,WAZ),
    (SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,SZCZUR,PAJAK,PAJAK,PAJAK,PAJAK,PAJAK,PAJAK,PAJAK,PAJAK,PAJAK,PAJAK,PAJAK,PAJAK,PAJAK,PAJAK,PAJAK,PAJAK,PAJAK,PAJAK,PAJAK,PAJAK,PAJAK,PAJAK,PAJAK,PAJAK,PAJAK,WAZ,WAZ,WAZ,WAZ,WAZ,WAZ,WAZ,WAZ,WAZ,WAZ,WAZ,WAZ,WAZ,WAZ,WAZ)
)

TILESIZE = 25
MENUSIZE = 150
MAPWIDTH = len(MAPA[0])
MAPHEIGHT = len(MAPA)
GAME_WIDTH = (TILESIZE * MAPWIDTH) + MENUSIZE
GAME_HEIGHT = (TILESIZE * MAPHEIGHT) + MENUSIZE

TEKSTURY = (
    (image_load('dane/zacznij.jpg'), pygame.Rect(GAME_WIDTH - 180, GAME_HEIGHT - 65, 50, 50)),
    (image_load('dane/domek.jpg'), pygame.Rect(GAME_WIDTH - 85, GAME_HEIGHT - 85, 70, 70)),
    (image_load('dane/zielony.jpg'), pygame.Rect(GAME_WIDTH - 80, 10, 40, 40)),
    (image_load('dane/niebieski.jpg'), pygame.Rect(GAME_WIDTH - 80, 60, 40, 40)),
    (image_load('dane/zolty.jpg'), pygame.Rect(GAME_WIDTH - 80, 110, 40, 40))
)

TEKSTURY_INTERFEJSU_WIEZY = (
    (image_load('dane/atak_zielony.jpg'), pygame.Rect(400, GAME_HEIGHT - 140, 70, 70)),
    (image_load('dane/zasieg_zielony.jpg'), pygame.Rect(480, GAME_HEIGHT - 140, 70, 70)),
    (image_load('dane/predkosc_zielony.jpg'), pygame.Rect(560, GAME_HEIGHT - 140, 70, 70)),
    (image_load('dane/dolar_zielony.jpg'), pygame.Rect(640, GAME_HEIGHT - 140, 70,70)),
    (image_load('dane/atak_niebieski.jpg'), pygame.Rect(400, GAME_HEIGHT - 140, 70, 70)),
    (image_load('dane/zasieg_niebieski.jpg'), pygame.Rect(480, GAME_HEIGHT - 140, 70, 70)),
    (image_load('dane/przebicie_niebieski.jpg'), pygame.Rect(560, GAME_HEIGHT - 140, 70, 70)),
    (image_load('dane/dolar_niebieski.jpg'), pygame.Rect(640, GAME_HEIGHT - 140, 70, 70)),
    (image_load('dane/atak_zolty.jpg'), pygame.Rect(400, GAME_HEIGHT - 140, 70, 70)),
    (image_load('dane/zasieg_zolty.jpg'), pygame.Rect(480, GAME_HEIGHT - 140, 70, 70)),
    (image_load('dane/elektryzacja_zolty.jpg'), pygame.Rect(560, GAME_HEIGHT - 140, 70, 70)),
    (image_load('dane/dolar_zolty.jpg'), pygame.Rect(640, GAME_HEIGHT - 140, 70, 70))
)

OBSZAR = []
for row in range(MAPHEIGHT):
    OBSZAR.append([])

    for column in range(MAPWIDTH):
        OBSZAR[row].append((pygame.Rect(TILESIZE * column, TILESIZE * row, TILESIZE, TILESIZE), row, column))

    OBSZAR[row] = tuple(OBSZAR[row])

OBSZAR = tuple(OBSZAR)
