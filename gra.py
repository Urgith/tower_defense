import pygame
import random


def image_load(name, transparency=False):
    image = pygame.image.load(name).convert()

    if transparency: 
        image.set_colorkey(image.get_at((0, 0)))

    return image


def quit():
    import sys

    pygame.quit()
    sys.exit(0)


pygame.font.init()
pygame.display.set_mode()
pygame.display.set_caption('Inwazja')

poziomo = image_load('dane/poziomo.jpg')
pionowo = image_load('dane/pionowo.jpg')
lg = image_load('dane/lg.jpg')
ld = image_load('dane/ld.jpg')
pg = image_load('dane/pg.jpg')
pd = image_load('dane/pd.jpg')

las = image_load('dane/las.jpg')
trawa = image_load('dane/trawa.jpg')
domek = image_load('dane/domek.jpg')
zacznij = image_load('dane/zacznij.jpg')
zielony = image_load('dane/zielony.jpg')
niebieski = image_load('dane/niebieski.jpg')
zolty = image_load('dane/zolty.jpg')

atak_zielony = image_load('dane/atak_zielony.jpg')
atak_niebieski = image_load('dane/atak_niebieski.jpg')
atak_zolty = image_load('dane/atak_zolty.jpg')

zasieg_zielony = image_load('dane/zasieg_zielony.jpg')
zasieg_niebieski = image_load('dane/zasieg_niebieski.jpg')
zasieg_zolty = image_load('dane/zasieg_zolty.jpg')

predkosc_zielony = image_load('dane/predkosc_zielony.jpg')
przebicie_niebieski = image_load('dane/przebicie_niebieski.jpg')
elektryzacja_zolty = image_load('dane/elektryzacja_zolty.jpg')

dolar_zielony = image_load('dane/dolar_zielony.jpg')
dolar_niebieski = image_load('dane/dolar_niebieski.jpg')
dolar_zolty = image_load('dane/dolar_zolty.jpg')

kula_mocy = image_load('dane/kula_mocy.png', True)
druid = image_load(    'dane/druid.png', True)

MYSZ = image_load('dane/mysz.png', True)
SZCZUR = image_load('dane/szczur.png', True)
PAJAK = image_load('dane/pajak.png', True)
WAZ = image_load('dane/waz.png', True)

wieze = (
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

teren = {
    0:  poziomo,
    10: pionowo,
    3:  las,
    5:  lg,
    50: ld,
    6:  pg,
    60: pd,
    7:  pd,
    70: ld,
    8:  pg,
    80: lg
}

mapa = (
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

enemies = {
    MYSZ:   (100, 1  , 1, 5 , 1, 15),
    SZCZUR: (200, 0.8, 3, 8 , 2, 17),
    PAJAK:  (250, 1.2, 2, 12, 2, 19),
    WAZ:    (350, 1.3, 3, 15, 3, 21)
}

waves = (
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
MAPWIDTH = len(mapa[0])
MAPHEIGHT = len(mapa)
GAME_WIDTH = (TILESIZE * MAPWIDTH) + MENUSIZE
GAME_HEIGHT = (TILESIZE * MAPHEIGHT) + MENUSIZE

tekstury = (
    (zacznij, pygame.Rect(GAME_WIDTH - 180, GAME_HEIGHT - 65, 50, 50)),
    (domek, pygame.Rect(GAME_WIDTH - 85, GAME_HEIGHT - 85, 70, 70)),
    (zielony, pygame.Rect(GAME_WIDTH - 80, 10, 40, 40)),
    (niebieski, pygame.Rect(GAME_WIDTH - 80, 60, 40, 40)),
    (zolty, pygame.Rect(GAME_WIDTH - 80, 110, 40, 40))
)

tekstury_interfejsu_wiezy = (
    (atak_zielony, pygame.Rect(400, GAME_HEIGHT - 140, 70, 70)),
    (zasieg_zielony, pygame.Rect(480, GAME_HEIGHT - 140, 70, 70)),
    (predkosc_zielony, pygame.Rect(560, GAME_HEIGHT - 140, 70, 70)),
    (dolar_zielony, pygame.Rect(640, GAME_HEIGHT - 140, 70,70)),
    (atak_niebieski, pygame.Rect(400, GAME_HEIGHT - 140, 70, 70)),
    (zasieg_niebieski, pygame.Rect(480, GAME_HEIGHT - 140, 70, 70)),
    (przebicie_niebieski, pygame.Rect(560, GAME_HEIGHT - 140, 70, 70)),
    (dolar_niebieski, pygame.Rect(640, GAME_HEIGHT - 140, 70, 70)),
    (atak_zolty, pygame.Rect(400, GAME_HEIGHT - 140, 70, 70)),
    (zasieg_zolty, pygame.Rect(480, GAME_HEIGHT - 140, 70, 70)),
    (elektryzacja_zolty, pygame.Rect(560, GAME_HEIGHT - 140, 70, 70)),
    (dolar_zolty, pygame.Rect(640, GAME_HEIGHT - 140, 70, 70))
)

obszar = []
for row in range(MAPHEIGHT):
    obszar.append([])

    for column in range(MAPWIDTH):
        obszar[row].append((pygame.Rect(TILESIZE * column, TILESIZE * row, TILESIZE, TILESIZE), row, column))

    obszar[row] = tuple(obszar[row])
obszar = tuple(obszar)

class Gracz:
  def __init__(self):
    self.obiekt=        pygame.Rect(100, 100, 30, 30)
    self.doswiadczenie= 0
    self.poziom=        0
    self.max_zdrowie= 1000
    self.zdrowie=     1000
    self.predkosc=  1
    self.rodzaj=    'gracz'
    self.x, self.y= 100, 100

  def ruch(self):
    self.klikniete= pygame.key.get_pressed()
    x, y= 0, 0

    if self.klikniete[pygame.K_w]: self.y-= self.predkosc; y= -1
    if self.klikniete[pygame.K_a]: self.x-= self.predkosc; x= -1
    if self.klikniete[pygame.K_s]: self.y+= self.predkosc; y= 1
    if self.klikniete[pygame.K_d]: self.x+= self.predkosc; x= 1

    if self.x<0                      : self.x= 0
    if self.y<0                      : self.y= 0
    if self.x>GAME_WIDTH-MENUSIZE-30 : self.x= GAME_WIDTH-MENUSIZE-30
    if self.y>GAME_HEIGHT-MENUSIZE-30: self.y= GAME_HEIGHT-MENUSIZE-30

    if x and y:
      if x==1: self.x= self.x-self.predkosc+self.predkosc/(2**(1/2))
      else   : self.x= self.x+self.predkosc-self.predkosc/(2**(1/2))

      if y==1: self.y= self.y-self.predkosc+self.predkosc/(2**(1/2))
      else   : self.y= self.y+self.predkosc-self.predkosc/(2**(1/2))

    self.obiekt.x= self.x
    self.obiekt.y= self.y

  def strzal(self, gra):
    gra.lista_pociskow.append(Pocisk(self,gra))

  def awansowanie(self):
    poziom= int((self.doswiadczenie//100)**(1/2))
    if poziom!=self.poziom:
      self.poziom=      poziom
      self.predkosc=    1+poziom/10
      self.max_zdrowie= int(1000*(1+poziom/10))
      self.zdrowie=     self.max_zdrowie

class Pocisk:
  def __init__(self, rodzaj, gra):
    self.rodzaj=         rodzaj.rodzaj
    self.czas_powstania= gra.licznik
    if self.rodzaj=='gracz':
      self.x, self.y= gra.gracz.obiekt.x, gra.gracz.obiekt.y
      self.obiekt=    pygame.Rect(self.x, self.y, 8, 8)
      self.obrazenia= 5+rodzaj.poziom
      x, y= gra.pozycja_myszy[0]-self.x, gra.pozycja_myszy[1]-self.y
      self.kierunek_x= x/((x**2+y**2)**(1/2))*(2+rodzaj.poziom/5)
      self.kierunek_y= y/((x**2+y**2)**(1/2))*(2+rodzaj.poziom/5)
    else:
      if   self.rodzaj==2: self.id= random.random(); self.przebicie= rodzaj.przebicie
      elif self.rodzaj==3: self.elektryzacja= rodzaj.elektryzacja
      self.dlugosc_zycia= rodzaj.dlugosc_zycia
      self.x, self.y= rodzaj.pole
      self.obiekt=    pygame.Rect(self.x, self.y, rodzaj.rozmiar_pocisku, rodzaj.rozmiar_pocisku)
      self.kolor=     wieze[self.rodzaj-1][1]
      self.obrazenia= rodzaj.obrazenia
      x, y= gra.celowany_przeciwnik.x+gra.celowany_przeciwnik.rozmiar/2-self.x, gra.celowany_przeciwnik.y+gra.celowany_przeciwnik.rozmiar/2-self.y
      self.kierunek_x= x/((x**2+y**2)**(1/2))*self.rodzaj*rodzaj.predkosc
      self.kierunek_y= y/((x**2+y**2)**(1/2))*self.rodzaj*rodzaj.predkosc

  def ruch(self):
      self.x+= self.kierunek_x
      self.y+= self.kierunek_y
      self.obiekt.x, self.obiekt.y= self.x, self.y

class Przeciwnik:
  def __init__(self, gra):
    self.rodzaj=    waves[gra.runda][gra.numer_przeciwnika]
    self.rozmiar=   enemies[self.rodzaj][5]
    self.x, self.y= 5, 5
    self.ids=       []
    self.obiekt=    pygame.Rect((self.x, self.y, self.rozmiar, self.rozmiar))
    self.pole=      mapa[0][0]
    self.startowe_zdrowie= int(enemies[self.rodzaj][0]*(1.1**gra.runda))
    self.zdrowie=          int(enemies[self.rodzaj][0]*(1.1**gra.runda))
    self.predkosc=         enemies[self.rodzaj][1]
    self.atak=             enemies[self.rodzaj][2]
    self.punkty=           enemies[self.rodzaj][3]
    self.monety=           enemies[self.rodzaj][4]

  def ruch(self):
    pole= mapa[int((self.y-5)/TILESIZE)][int((self.x-5)/TILESIZE)]
    if   (self.pole==6 or self.pole==60) and (self.pole!=pole): pole= mapa[int((self.y-5)/TILESIZE)][int((self.x+20-self.predkosc)/TILESIZE)]
    elif (self.pole==7 or self.pole==70) and (self.pole!=pole): pole= mapa[int((self.y+20-self.predkosc)/TILESIZE)][int((self.x+20-self.predkosc)/TILESIZE)]

    if   pole==0 or pole==10: pole= self.pole
    if   pole==5 or pole==50: self.x+= self.predkosc
    elif pole==6 or pole==60: self.x-= self.predkosc
    elif pole==7 or pole==70: self.y-= self.predkosc
    elif pole==8 or pole==80: self.y+= self.predkosc
    self.pole= pole

    self.obiekt.x, self.obiekt.y= self.x, self.y

class Wieza:
  def __init__(self, gra):
    self.obiekt=   pygame.Rect(gra.pozycja_myszy[0]-10, gra.pozycja_myszy[1]-10, 20, 20)
    self.pole=     gra.pozycja_myszy
    self.rodzaj=   gra.rodzaj_wybranej_wiezy
    self.licznik=  0
    self.predkosc= 1
    self.poziom_atak, self.poziom_zasieg, self.poziom_reszta, self.poziom=  0, 0, 0, 0

    self.typ, self.kolor, self.koszt, self.obrazenia, self.zasieg, self.przeladowanie, self.dlugosc_zycia, self.rozmiar_pocisku= wieze[self.rodzaj-1]
    self.cena_calkowita= self.koszt
    if self.rodzaj==1:    self.koszt_atak=4; self.koszt_zasieg=1; self.koszt_reszta=2
    elif self.rodzaj==2: self.koszt_atak=10; self.koszt_zasieg=2; self.koszt_reszta=20; self.przebicie=  1
    elif self.rodzaj==3: self.koszt_atak=40; self.koszt_zasieg=4; self.koszt_reszta=30; self.ilu_na_raz= 3; self.elektryzacja= 0

  def strzal(self, gra):
    if self.licznik+self.przeladowanie<=gra.licznik:
      self.licznik= gra.licznik
      gra.lista_pociskow.append(Pocisk(self, gra))

  def polepszenie(self, gra):
    gra.wybrano_wieze= True
    if self.rodzaj==1:
      if gra.polepszenie%4==0:
        if gra.pieniadze>=4 and self.poziom_atak<=4:
          self.cena_calkowita+= 4
          gra.pieniadze-=       4
          self.obrazenia+=      5
          self.poziom_atak+=    1
      elif gra.polepszenie%4==1:
        if gra.pieniadze>=1 and self.poziom_zasieg<=4:
          self.cena_calkowita+= 1
          gra.pieniadze-=       1
          self.dlugosc_zycia+=  30
          self.zasieg+=         15
          self.poziom_zasieg+=  1
      elif gra.polepszenie%4==2:
        if gra.pieniadze>=2 and self.poziom_reszta<=4:
          self.cena_calkowita+= 2
          gra.pieniadze-=       2
          self.przeladowanie-=  1
          self.predkosc+=       0.4
          self.poziom_reszta+=  1
      elif gra.polepszenie%4==3:
        gra.wybrano_wieze= False
        gra.pieniadze+=    self.cena_calkowita
        gra.lista_wiez.pop(gra.wybrana_wieza)
    elif self.rodzaj==2:
      if gra.polepszenie%4==0:
        if gra.pieniadze>=10 and self.poziom_atak<=4:
          self.cena_calkowita+= 10
          gra.pieniadze-=       10
          self.obrazenia+=      20
          self.poziom_atak+=    1
      elif gra.polepszenie%4==1:
        if gra.pieniadze>=2 and self.poziom_zasieg<=4:
          self.cena_calkowita+= 2
          gra.pieniadze-=       2
          self.dlugosc_zycia+=  15
          self.zasieg+=         30
          self.poziom_zasieg+=  1
      elif gra.polepszenie%4==2:
        if gra.pieniadze>=20 and self.poziom_reszta<=4:
          self.cena_calkowita+= 20
          gra.pieniadze-=       20
          self.przeladowanie-=  1
          self.przebicie+=      1
          self.poziom_reszta+=  1
      elif gra.polepszenie%4==3:
        gra.wybrano_wieze= False
        gra.pieniadze+=    self.cena_calkowita
        gra.lista_wiez.pop(gra.wybrana_wieza)
    elif self.rodzaj==3:
      if gra.polepszenie%4==0:
        if gra.pieniadze>=40 and self.poziom_atak<=4:
          self.cena_calkowita+= 40
          gra.pieniadze-=       40
          self.obrazenia+=      1
          self.ilu_na_raz+=     1
          self.poziom_atak+=    1
      elif gra.polepszenie%4==1:
        if gra.pieniadze>=4 and self.poziom_zasieg<=4:
          self.cena_calkowita+= 4
          gra.pieniadze-=       4
          self.dlugosc_zycia+=  5
          self.zasieg+=         15
          self.poziom_zasieg+=  1
      elif gra.polepszenie%4==2:
        if gra.pieniadze>=30 and self.poziom_reszta<=4:
          self.cena_calkowita+= 30
          gra.pieniadze-=       30
          self.predkosc+=       0.2
          self.elektryzacja+=   1
          self.poziom_reszta+=  1
      elif gra.polepszenie%4==3:
        gra.wybrano_wieze= False
        gra.pieniadze+=    self.cena_calkowita
        gra.lista_wiez.pop(gra.wybrana_wieza)
    self.poziom= (self.poziom_atak+self.poziom_zasieg+self.poziom_reszta)//3
    self.typ=    wieze[self.rodzaj-1+self.poziom*3][0]

class Gra:
  def __init__(self):
    self.okno_gry= pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
    self.gracz=    Gracz()

    self.lista_przeciwnikow= []
    self.lista_pociskow=     []
    self.lista_wiez=         []

    self.numer_przeciwnika= 0
    self.licznik=           0
    self.runda=             0
    self.pozycja_myszy=    (0,0)

    self.kliknieto_w_kolejna_runde= False
    self.wybrano_wieze_do_kupienia= False
    self.mozliwosc_polepszenia=     False
    self.wybrano_wieze=             False
    self.start=                     False

    self.predkosc_wychodzenia= 10
    self.zdrowie_lasu=         100
    self.pieniadze=            50
    self.punkty=               0

    while True:
      if self.start:
        self.licznik+= 1
        if self.licznik%self.predkosc_wychodzenia==0 and (self.runda!=len(waves)-1 or self.numer_przeciwnika!=len(waves[-1])-1):
          try:
            self.lista_przeciwnikow.append(Przeciwnik(self))
            self.numer_przeciwnika+= 1
          except: pass

          if self.numer_przeciwnika==len(waves[self.runda]) and self.kliknieto_w_kolejna_runde:
            self.kliknieto_w_kolejna_runde= False
            self.numer_przeciwnika= 0
            self.runda+=            1
            Gracz.awansowanie(self.gracz)

      for event in pygame.event.get():
        if event.type==pygame.QUIT: quit()
        elif event.type==pygame.KEYDOWN:
          if event.key==pygame.K_ESCAPE:
            if self.wybrano_wieze_do_kupienia or self.wybrano_wieze: self.wybrano_wieze_do_kupienia= False; self.wybrano_wieze= False
            else: quit()

          elif event.key==pygame.K_p:
            pauza= True
            while pauza:
              for event in pygame.event.get():
                if event.type==pygame.QUIT: quit()
                elif event.type==pygame.KEYDOWN and (event.key==pygame.K_ESCAPE or event.key==pygame.K_p): pauza= False

          elif event.key==pygame.K_1: self.wybrano_wieze_do_kupienia= True; self.zasieg_wybranej_wiezy= wieze[0][4]; self.kolor_wybranej_wiezy= wieze[0][1]; self.rodzaj_wybranej_wiezy= 1; self.wybrano_wieze= False
          elif event.key==pygame.K_2: self.wybrano_wieze_do_kupienia= True; self.zasieg_wybranej_wiezy= wieze[1][4]; self.kolor_wybranej_wiezy= wieze[1][1]; self.rodzaj_wybranej_wiezy= 2; self.wybrano_wieze= False
          elif event.key==pygame.K_3: self.wybrano_wieze_do_kupienia= True; self.zasieg_wybranej_wiezy= wieze[2][4]; self.kolor_wybranej_wiezy= wieze[2][1]; self.rodzaj_wybranej_wiezy= 3; self.wybrano_wieze= False

        elif event.type==pygame.MOUSEBUTTONUP and event.button==1:
          self.pozycja_myszy= pygame.mouse.get_pos()
          self.mozliwosc_polepszenia= False
          if self.wybrano_wieze: self.mozliwosc_polepszenia= True
          self.wybrano_wieze= False

          if self.pozycja_myszy[0]<GAME_WIDTH-MENUSIZE and self.pozycja_myszy[1]<GAME_HEIGHT-MENUSIZE:
            if self.wybrano_wieze_do_kupienia:
              if self.postawienie_wiezy():
                self.lista_wiez.append(Wieza(self))
                self.pieniadze-= self.lista_wiez[-1].koszt
                if self.pieniadze<0:
                  self.pieniadze+= self.lista_wiez[-1].koszt
                  self.lista_wiez.pop(-1)
              self.wybrano_wieze_do_kupienia= False
            else:
              for i, wieza in enumerate(self.lista_wiez):
                if wieza.obiekt.collidepoint(self.pozycja_myszy):
                  self.wybrano_wieze= True
                  self.wybrana_wieza= i
                  break
              Gracz.strzal(self.gracz, self)

          elif tekstury[0][1].collidepoint(self.pozycja_myszy):
            if self.licznik: self.kliknieto_w_kolejna_runde= True
            self.start= True
          elif tekstury[1][1].collidepoint(self.pozycja_myszy): quit()

          else:
            for i, tekstura in enumerate(tekstury):
              if i>=2 and tekstura[1].collidepoint(self.pozycja_myszy):
                self.wybrano_wieze_do_kupienia= True
                self.zasieg_wybranej_wiezy=     wieze[i-2][4]
                self.kolor_wybranej_wiezy=      wieze[i-2][1]
                self.rodzaj_wybranej_wiezy=     i-1
                break

            if self.mozliwosc_polepszenia:
              for i in range((self.lista_wiez[self.wybrana_wieza].rodzaj-1)*4, self.lista_wiez[self.wybrana_wieza].rodzaj*4):
                if tekstury_interfejsu_wiezy[i][1].collidepoint(self.pozycja_myszy):
                  self.polepszenie= i
                  Wieza.polepszenie(self.lista_wiez[self.wybrana_wieza], self)

      self.przebieg()
      self.rysowanie()
      pygame.display.flip()

  def przebieg(self):
    Gracz.ruch(self.gracz)

    for wieza in self.lista_wiez:
      ilu_juz_zaatakowano= 0
      for przeciwnik in self.lista_przeciwnikow:
        if ((przeciwnik.obiekt.x-wieza.pole[0])**2+(przeciwnik.obiekt.y-wieza.pole[1])**2)**(1/2)<=wieza.zasieg or ((przeciwnik.obiekt.x+przeciwnik.rozmiar-wieza.pole[0])**2+(przeciwnik.obiekt.y-wieza.pole[1])**2)**(1/2)<=wieza.zasieg or ((przeciwnik.obiekt.x-wieza.pole[0])**2+(przeciwnik.obiekt.y+przeciwnik.rozmiar-wieza.pole[1])**2)**(1/2)<=wieza.zasieg or ((przeciwnik.obiekt.x+przeciwnik.rozmiar-wieza.pole[0])**2+(przeciwnik.obiekt.y+przeciwnik.rozmiar-wieza.pole[1])**2)**(1/2)<=wieza.zasieg:
          self.celowany_przeciwnik= przeciwnik
          Wieza.strzal(wieza, self)
          ilu_juz_zaatakowano+= 1
          if wieza.rodzaj!=3 or ilu_juz_zaatakowano==wieza.ilu_na_raz: break

    for i, pocisk in enumerate(self.lista_pociskow):
      pocisk.ruch()
      if pocisk.rodzaj!='gracz':
        if pocisk.czas_powstania+pocisk.dlugosc_zycia<=self.licznik:
          self.lista_pociskow.pop(i)
          continue
      if pocisk.obiekt.x<0 or pocisk.obiekt.y<0 or pocisk.obiekt.x>GAME_WIDTH-MENUSIZE-8 or pocisk.obiekt.y>GAME_HEIGHT-MENUSIZE-8:
        self.lista_pociskow.pop(i)
        continue
      for j, przeciwnik in enumerate(self.lista_przeciwnikow):
        if pocisk.obiekt.colliderect(przeciwnik.obiekt):
          if pocisk.rodzaj==2 and (pocisk.id not in przeciwnik.ids):
            przeciwnik.ids.append(pocisk.id)
            przeciwnik.zdrowie-= pocisk.obrazenia
            pocisk.przebicie-=   1
            if not pocisk.przebicie: self.lista_pociskow.pop(i)
          elif pocisk.rodzaj!=2:
            przeciwnik.zdrowie-= pocisk.obrazenia
            ostatni_pocisk= self.lista_pociskow.pop(i)

          if przeciwnik.zdrowie<=0:
            self.punkty+=    przeciwnik.punkty
            self.pieniadze+= przeciwnik.monety
            self.lista_przeciwnikow.pop(j)
            try:
              if ostatni_pocisk.rodzaj=='gracz': self.gracz.doswiadczenie+= przeciwnik.punkty
            except: pass
          break

    for i,przeciwnik in enumerate(self.lista_przeciwnikow):
      if przeciwnik.obiekt.colliderect(self.gracz.obiekt):
        self.gracz.zdrowie-= przeciwnik.atak
      przeciwnik.ruch()
      if przeciwnik.obiekt.colliderect(obszar[22][20][0]):
        self.zdrowie_lasu-= przeciwnik.atak
        self.lista_przeciwnikow.pop(i)

    if self.wybrano_wieze_do_kupienia:                self.pozycja_myszy= pygame.mouse.get_pos()
    if self.gracz.zdrowie<=0 or self.zdrowie_lasu<=0: quit()

  def rysowanie(self):
    self.okno_gry.blit(trawa,(0,0))

    for row in range(MAPHEIGHT):
      for column in range(MAPWIDTH):
        if mapa[row][column]!=1: self.okno_gry.blit(teren[mapa[row][column]], (column*TILESIZE,row*TILESIZE))

    for wieza in self.lista_wiez: self.okno_gry.blit(wieza.typ, (wieza.obiekt[0],wieza.obiekt[1]))

    for przeciwnik in self.lista_przeciwnikow:
      self.okno_gry.blit(przeciwnik.rodzaj, (przeciwnik.obiekt.x-(przeciwnik.rozmiar-15)/2, przeciwnik.obiekt.y-(przeciwnik.rozmiar-15)/2))
      if przeciwnik.zdrowie>0:
        pygame.draw.rect(self.okno_gry, (0,255,0), pygame.Rect(przeciwnik.obiekt.x-5, przeciwnik.obiekt.y-10, (25*przeciwnik.zdrowie)//przeciwnik.startowe_zdrowie, 3))
        if przeciwnik.startowe_zdrowie-przeciwnik.zdrowie>0:
          pygame.draw.rect(self.okno_gry, (255,0,0), pygame.Rect(przeciwnik.obiekt.x-5+(25*przeciwnik.zdrowie)//przeciwnik.startowe_zdrowie, przeciwnik.obiekt.y-10, (25*(przeciwnik.startowe_zdrowie-przeciwnik.zdrowie))//przeciwnik.startowe_zdrowie, 3))

    self.okno_gry.blit(druid, (self.gracz.obiekt.x,self.gracz.obiekt.y))

    stan= int((self.gracz.zdrowie/(self.gracz.max_zdrowie+1))*3)
    if stan==2:
      color= int((self.gracz.max_zdrowie-self.gracz.zdrowie)/self.gracz.max_zdrowie*3*255)
      pygame.draw.rect(self.okno_gry, (color,255,0), (self.gracz.x-5, self.gracz.y-5, self.gracz.zdrowie/self.gracz.max_zdrowie*40, 5))
    elif stan==1:
      color= int((self.gracz.zdrowie-self.gracz.max_zdrowie/3)/self.gracz.max_zdrowie*3*255)
      pygame.draw.rect(self.okno_gry, (255,color,0), (self.gracz.x-5, self.gracz.y-5, self.gracz.zdrowie/self.gracz.max_zdrowie*40, 5))
    elif stan==0:
      color= int(self.gracz.zdrowie/self.gracz.max_zdrowie*3*255)
      pygame.draw.rect(self.okno_gry, (color,0,0),   (self.gracz.x-5, self.gracz.y-5, self.gracz.zdrowie/self.gracz.max_zdrowie*40, 5))

    for pocisk in self.lista_pociskow:
      if pocisk.rodzaj=='gracz': self.okno_gry.blit(kula_mocy, (pocisk.obiekt.x, pocisk.obiekt.y))
      else: pygame.draw.rect(self.okno_gry, pocisk.kolor, pocisk.obiekt)

    if self.wybrano_wieze: pygame.draw.circle(self.okno_gry, self.lista_wiez[self.wybrana_wieza].kolor, self.lista_wiez[self.wybrana_wieza].pole, self.lista_wiez[self.wybrana_wieza].zasieg, 1)

    pygame.draw.rect(self.okno_gry, (0,0,0), (GAME_WIDTH-MENUSIZE,                    0,   MENUSIZE, GAME_HEIGHT))
    pygame.draw.rect(self.okno_gry, (0,0,0), (                  0, GAME_HEIGHT-MENUSIZE, GAME_WIDTH,    MENUSIZE))

    if self.wybrano_wieze:
      for i in range((self.lista_wiez[self.wybrana_wieza].rodzaj-1)*4, self.lista_wiez[self.wybrana_wieza].rodzaj*4):
        self.okno_gry.blit(tekstury_interfejsu_wiezy[i][0], tekstury_interfejsu_wiezy[i][1])
      self.okno_gry.blit(pygame.font.SysFont(None, 30).render(f'{self.lista_wiez[self.wybrana_wieza].koszt_atak}$'    , True,     (255,0,0)), (tekstury_interfejsu_wiezy[0][1][0]+5, tekstury_interfejsu_wiezy[0][1][1]+50))
      self.okno_gry.blit(pygame.font.SysFont(None, 30).render(f'{self.lista_wiez[self.wybrana_wieza].koszt_zasieg}$'  , True,     (255,0,0)), (tekstury_interfejsu_wiezy[1][1][0]+5, tekstury_interfejsu_wiezy[1][1][1]+50))
      self.okno_gry.blit(pygame.font.SysFont(None, 30).render(f'{self.lista_wiez[self.wybrana_wieza].koszt_reszta}$'  , True,     (255,0,0)), (tekstury_interfejsu_wiezy[2][1][0]+5, tekstury_interfejsu_wiezy[2][1][1]+50))
      self.okno_gry.blit(pygame.font.SysFont(None, 30).render(f'{self.lista_wiez[self.wybrana_wieza].cena_calkowita}$', True,     (255,0,0)), (tekstury_interfejsu_wiezy[3][1][0]+5, tekstury_interfejsu_wiezy[3][1][1]+50))
      self.okno_gry.blit(pygame.font.SysFont(None, 30).render(f'{self.lista_wiez[self.wybrana_wieza].poziom_atak}'    , True,   (255,0,255)), (tekstury_interfejsu_wiezy[0][1][0]+5,  tekstury_interfejsu_wiezy[0][1][1]+5))
      self.okno_gry.blit(pygame.font.SysFont(None, 30).render(f'{self.lista_wiez[self.wybrana_wieza].poziom_zasieg}'  , True,   (255,0,255)), (tekstury_interfejsu_wiezy[1][1][0]+5,  tekstury_interfejsu_wiezy[1][1][1]+5))
      self.okno_gry.blit(pygame.font.SysFont(None, 30).render(f'{self.lista_wiez[self.wybrana_wieza].poziom_reszta}'  , True,   (255,0,255)), (tekstury_interfejsu_wiezy[2][1][0]+5,  tekstury_interfejsu_wiezy[2][1][1]+5))

    for tekstura in tekstury: self.okno_gry.blit(tekstura[0], (tekstura[1].x,tekstura[1].y))

    self.okno_gry.blit(pygame.font.SysFont(None, 30).render(f'Doświadczenie:{self.gracz.doswiadczenie}/{((self.gracz.poziom+1)*10)**2}', True, (255,255,255)), (             5, GAME_HEIGHT-145))
    self.okno_gry.blit(pygame.font.SysFont(None, 30).render(                                         f'Poziom:{self.gracz.poziom}'     , True, (255,255,255)), (             5, GAME_HEIGHT-115))
    self.okno_gry.blit(pygame.font.SysFont(None, 30).render(                                         f'Obrażenia:{5+self.gracz.poziom}', True, (255,255,255)), (             5,  GAME_HEIGHT-85))
    self.okno_gry.blit(pygame.font.SysFont(None, 30).render(                                         f'Szybkość:{self.gracz.predkosc}' , True, (255,255,255)), (             5,  GAME_HEIGHT-55))
    self.okno_gry.blit(pygame.font.SysFont(None, 30).render(                                         f'Zdrowie:{self.gracz.zdrowie}'   , True, (255,255,255)), (             5,  GAME_HEIGHT-25))
    self.okno_gry.blit(pygame.font.SysFont(None, 30).render(                                         f'Pieniądze:{self.pieniadze}'     , True, (255,255,255)), (           200,  GAME_HEIGHT-25))
    self.okno_gry.blit(pygame.font.SysFont(None, 30).render(                                         f'Punkty:{self.punkty}'           , True, (255,255,255)), (           200,  GAME_HEIGHT-55))
    if self.start: self.okno_gry.blit(pygame.font.SysFont(None, 30).render(                          f'Runda:{self.runda+1}'           , True, (255,255,255)), (GAME_WIDTH-195,  GAME_HEIGHT-85))
    else:          self.okno_gry.blit(pygame.font.SysFont(None, 30).render(                          f'Runda:{self.runda}'             , True, (255,255,255)), (GAME_WIDTH-195,  GAME_HEIGHT-85))
    self.okno_gry.blit(pygame.font.SysFont(None, 30).render(                                                                      '10$', True, (255,255,255)), (GAME_WIDTH-130,              20))
    self.okno_gry.blit(pygame.font.SysFont(None, 30).render(                                                                      '30$', True, (255,255,255)), (GAME_WIDTH-130,              70))
    self.okno_gry.blit(pygame.font.SysFont(None, 30).render(                                                                      '50$', True, (255,255,255)), (GAME_WIDTH-130,             120))
    self.okno_gry.blit(pygame.font.SysFont(None, 30).render(                                                                       '1.', True, (255,255,255)), ( GAME_WIDTH-30,              20))
    self.okno_gry.blit(pygame.font.SysFont(None, 30).render(                                                                       '2.', True, (255,255,255)), ( GAME_WIDTH-30,              70))
    self.okno_gry.blit(pygame.font.SysFont(None, 30).render(                                                                       '3.', True, (255,255,255)), ( GAME_WIDTH-30,             120))

    self.okno_gry.blit(pygame.font.SysFont(None, 40).render(f'{self.zdrowie_lasu}', True, (255,255,255)), ( 465, 550))

    if self.wybrano_wieze_do_kupienia:
      pygame.draw.rect  (self.okno_gry, self.kolor_wybranej_wiezy, (self.pozycja_myszy[0]-10, self.pozycja_myszy[1]-10, 20, 20))
      pygame.draw.circle(self.okno_gry, self.kolor_wybranej_wiezy, self.pozycja_myszy,            self.zasieg_wybranej_wiezy, 1)

  def postawienie_wiezy(self):
    for row in obszar:
      for column in row:
        if column[0].colliderect(pygame.Rect(self.pozycja_myszy[0]-10, self.pozycja_myszy[1]-10, 20, 20)) and (mapa[column[1]][column[2]]==0 or mapa[column[1]][column[2]]==10 or mapa[column[1]][column[2]]==3 or mapa[column[1]][column[2]]==5 or mapa[column[1]][column[2]]==50 or mapa[column[1]][column[2]]==6 or mapa[column[1]][column[2]]==60 or mapa[column[1]][column[2]]==7 or mapa[column[1]][column[2]]==70 or mapa[column[1]][column[2]]==8 or mapa[column[1]][column[2]]==80) or self.pozycja_myszy[0]-10<0 or self.pozycja_myszy[1]-10<0 or self.pozycja_myszy[0]+10>GAME_WIDTH-MENUSIZE or self.pozycja_myszy[1]+10>GAME_HEIGHT-MENUSIZE: return False
    for wieza in self.lista_wiez:
      if wieza.obiekt.colliderect(pygame.Rect(self.pozycja_myszy[0]-10, self.pozycja_myszy[1]-10, 20, 20)): return False
    return True

Gra()
