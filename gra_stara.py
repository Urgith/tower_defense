import os
import time
import random
import datetime
import pygame.math as math
import pygame


pygame.display.set_mode()

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
PINK = (255, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

colours = {
  0:pygame.image.load('dane/poziomo.jpg').convert(),
  10:pygame.image.load('dane/pionowo.jpg').convert(),

  3:pygame.image.load('dane/las.jpg').convert(),

  5:pygame.image.load('dane/lg.jpg').convert(),
  50:pygame.image.load('dane/ld.jpg').convert(),

  6:pygame.image.load('dane/pg.jpg').convert(),
  60:pygame.image.load('dane/pd.jpg').convert(),

  7:pygame.image.load('dane/pd.jpg').convert(),
  70:pygame.image.load('dane/ld.jpg').convert(),

  8:pygame.image.load('dane/pg.jpg').convert(),
  80:pygame.image.load('dane/lg.jpg').convert()
}

trawa = pygame.image.load('dane/trawa.jpg').convert()
zacznij = pygame.image.load('dane/zacznij.jpg').convert()
domek = pygame.image.load('dane/domek.jpg').convert()
glosnik = pygame.image.load('dane/glosnik.jpg').convert()
glosnik_wylaczony = pygame.image.load('dane/glosnik_wylaczony.jpg').convert()

mysz = pygame.image.load('dane/mysz.jpg').convert()
szczur = pygame.image.load('dane/szczur.jpg').convert()

celownik_zielony = pygame.image.load('dane/celownik_zielony.jpg').convert()
celownik_zolty = pygame.image.load('dane/celownik_zolty.jpg').convert()
celownik_niebieski = pygame.image.load('dane/celownik_niebieski.jpg').convert()
celownik_rozowy = pygame.image.load('dane/celownik_rozowy.jpg').convert()
zasieg_zielony = pygame.image.load('dane/zasieg_zielony.jpg').convert()
zasieg_zolty = pygame.image.load('dane/zasieg_zolty.jpg').convert()
zasieg_niebieski = pygame.image.load('dane/zasieg_niebieski.jpg').convert()
zasieg_rozowy = pygame.image.load('dane/zasieg_rozowy.jpg').convert()
dolar_zielony = pygame.image.load('dane/dolar_zielony.jpg').convert()
dolar_zolty = pygame.image.load('dane/dolar_zolty.jpg').convert()
dolar_niebieski = pygame.image.load('dane/dolar_niebieski.jpg').convert()
dolar_rozowy = pygame.image.load('dane/dolar_rozowy.jpg').convert()
atak_zielony = pygame.image.load('dane/atak_zielony.jpg').convert()
atak_zolty = pygame.image.load('dane/atak_zolty.jpg').convert()
atak_niebieski = pygame.image.load('dane/atak_niebieski.jpg').convert()
atak_rozowy = pygame.image.load('dane/atak_rozowy.jpg').convert()

map = (
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
  GRAY:(1, 5, 1, 1, 15),
  BLACK:(0.8, 8, 2, 3, 17),
  WHITE:(1.2, 12, 2, 2, 20)
}

waves = (
  ((100,GRAY), (100,GRAY), (100,GRAY), (100,GRAY), (100,GRAY), (100,GRAY), (100,GRAY), (100,GRAY), (100,GRAY), (100,GRAY)),
  ((110,GRAY), (110,GRAY), (110,GRAY), (110,GRAY), (110,GRAY), (110,GRAY), (110,GRAY), (110,GRAY), (110,GRAY), (110,GRAY), (110,GRAY), (110,GRAY), (110,GRAY), (110,GRAY), (110,GRAY)),
  ((121,GRAY), (121,GRAY), (121,GRAY), (121,GRAY), (121,GRAY), (200,BLACK), (200,BLACK), (200,BLACK), (200,BLACK), (200,BLACK)),
  ((133.1,GRAY), (133.1,GRAY), (133.1,GRAY), (133.1,GRAY), (133.1,GRAY), (220,BLACK), (220,BLACK), (220,BLACK), (220,BLACK), (220,BLACK), (220,BLACK), (220,BLACK), (220,BLACK), (220,BLACK), (220,BLACK)),
  ((146.41,GRAY), (146.41,GRAY), (146.41,GRAY), (146.41,GRAY), (146.41,GRAY), (146.41,GRAY), (146.41,GRAY), (146.41,GRAY), (146.41,GRAY), (146.41,GRAY), (242,BLACK), (242,BLACK), (242,BLACK), (242,BLACK), (242,BLACK), (242,BLACK), (242,BLACK), (242,BLACK), (242,BLACK), (242,BLACK)),
  ((161.051,GRAY), (161.051,GRAY), (161.051,GRAY), (161.051,GRAY), (161.051,GRAY), (266.2,BLACK), (266.2,BLACK), (266.2,BLACK), (266.2,BLACK), (266.2,BLACK), (266.2,BLACK), (266.2,BLACK), (266.2,BLACK), (266.2,BLACK), (266.2,BLACK), (266.2,BLACK), (266.2,BLACK), (266.2,BLACK), (266.2,BLACK), (266.2,BLACK), (250,WHITE), (250,WHITE), (250,WHITE), (250,WHITE), (250,WHITE))
)

TILESIZE = 25
MAPWIDTH = len(map[0])
MAPHEIGHT = len(map)

GAME_WIDTH = TILESIZE*MAPWIDTH + 100
GAME_HEIGHT = TILESIZE*MAPHEIGHT + 100

LISTA_WIEZ = (
  ((GAME_WIDTH - 90, 20, 40, 40), GREEN, pygame.Rect(GAME_WIDTH - 90, 20, 40, 40)),
  ((GAME_WIDTH - 90, 80, 40, 40), YELLOW, pygame.Rect(GAME_WIDTH - 90, 80, 40, 40)),
  ((GAME_WIDTH - 90, 140, 40, 40), BLUE, pygame.Rect(GAME_WIDTH - 90, 140, 40, 40)),
  ((GAME_WIDTH - 90, 200, 40, 40), PINK, pygame.Rect(GAME_WIDTH - 90, 200, 40, 40))
)

def quit():
  import sys;pygame.quit();sys.exit(0)

def wlaczenie_muzyki():
  global muzyka_gra
  pygame.mixer.music.play(-1)
  muzyka_gra=True

def wylaczenie_muzyki():
  global muzyka_gra
  pygame.mixer.music.stop()
  muzyka_gra=False

def click(click, obiekt):
  ''' Funkcja działająca na przyciskach wieżyczek '''
  for i,wieza in enumerate(obiekt):
    if wieza[2].colliderect(pygame.Rect(click[0],click[1],1,1)):
      return wieza,i

def wczytywanie_ustawien():
  plik_ustawien=open('dane/ustawienia.txt','r')
  lista_ustawien=[]
  for ustawienie in plik_ustawien:
    lista_ustawien.append(ustawienie.rstrip())
  plik_ustawien.close()
  return tuple(lista_ustawien)

def zapisywanie_ustawien():
  global muzyka
  global trudnosc
  global sterowanie
  plik_ustawien=open('dane/ustawienia.txt','w')
  plik_ustawien.write(muzyka+'\n')
  plik_ustawien.write(trudnosc+'\n')
  plik_ustawien.write(sterowanie)
  plik_ustawien.close()

def wczytywanie_rekordow():
  plik_rekordow=open('dane/rekordy.txt','r')
  lista_rekordow=[]
  for i,rekord in enumerate(plik_rekordow):
    lista_rekordow.append(rekord.split())
    if len(lista_rekordow[i])==3:
      lista_rekordow[i]=[lista_rekordow[i][0],lista_rekordow[i][1]+' '+lista_rekordow[i][2]]
  plik_rekordow.close()
  return lista_rekordow

def zapisywanie_rekordow(lista_wynikow):
  global wynik

  lista_wynikow.append([wynik,str(datetime.datetime.now())[:16]])
  posortowana_lista_wynikow=[]
  lista_rekordow=[]
  for zawartosc in lista_wynikow:
    zawartosc[0]=int(zawartosc[0])
    lista_rekordow.append(zawartosc[0])
  lista_rekordow.sort(reverse=True)
  lista_rekordow.pop(-1)

  for rekord in lista_rekordow:
    for wynik in lista_wynikow:
      if rekord==wynik[0]:
        posortowana_lista_wynikow.append(str(rekord)+' '+str(wynik[1]))
        break

  plik_rekordow=open('dane/rekordy.txt','r+')
  for rekord in posortowana_lista_wynikow:
    plik_rekordow.write(str(rekord)+'\n')
  plik_rekordow.close()

#--------------------------------------------------

class Pocisk:

  def __init__(self,wieza,gra,przeciwnik=0):
    self.position=math.Vector2(wieza.x+10,wieza.y+10)
    self.obiekt=pygame.Rect(self.position[0],self.position[1],5,5)
    self.rodzaj=wieza.rodzaj
    self.id=wieza.id
    self.ruch=True

    if self.rodzaj==0:
      self.moving=math.Vector2((przeciwnik.x-wieza.x)/100,(przeciwnik.y-wieza.y)/100)
      self.obrazenia=50
    elif self.rodzaj==2:
      x=przeciwnik.x-wieza.x
      y=przeciwnik.y-wieza.y
      self.moving=math.Vector2(x/((x**2+y**2)**(1/2)),y/((x**2+y**2)**(1/2)))*2
      self.obrazenia=100
      self.id=random.random()
    elif self.rodzaj==3:
      x=przeciwnik.x-self.position[0]
      y=przeciwnik.y-self.position[1]
      self.moving=math.Vector2(x/((x**2+y**2)**(1/2)),(y/(x**2+y**2)**(1/2)))*1.1
      self.obrazenia=100
    elif self.rodzaj==4:
      x=gra.pos[0]-self.position[0]
      y=gra.pos[1]-self.position[1]
      self.moving=math.Vector2(x/((x**2+y**2)**(1/2)),(y/(x**2+y**2)**(1/2)))*1.5
      self.obrazenia=30

  def move(self,przeciwnik=0,gra=0,wieza=0):
    if self.rodzaj==3:
      for przeciwnik in gra.lista_przeciwnikow:
        x=przeciwnik.x-self.position[0]
        y=przeciwnik.y-self.position[1]
        if (x**2+y**2)**(1/2)<wieza.range:
          self.ruch=False
          self.moving=math.Vector2(x/((x**2+y**2)**(1/2)),(y/(x**2+y**2)**(1/2)))*1.1
          break
    self.obiekt=pygame.Rect(self.position[0],self.position[1],5,5)
    self.position+=self.moving


class Wieza:

  def __init__(self,gra,rodzaj):
    self.wieza=pygame.Rect(gra.nowa_wieza[0],gra.nowa_wieza[1],20,20)
    self.rodzaj=rodzaj
    self.okno_gry=gra.okno_gry
    self.x=gra.nowa_wieza[0]
    self.y=gra.nowa_wieza[1]
    self.id=random.random()
    self.czas_pocisk=time.time()

    if self.rodzaj==0:
      self.koszt=20
      self.range=75
    elif self.rodzaj==1:
      self.przeladowanie=0
      self.koszt=50
      self.range=50
      self.energia=2
    elif self.rodzaj==2:
      self.koszt=100
      self.range=150
    else:
      self.koszt=40
      self.range=100

    gra.money-=self.koszt

  def strzal(self,przeciwnik,gra):
    if ((self.x-przeciwnik.x)**2+(self.y-przeciwnik.y)**2)**(1/2)<self.range:
      if self.rodzaj==0:
        if time.time()-self.czas_pocisk>0.5:
          gra.lista_pociskow.append(Pocisk(self,gra,przeciwnik))
          self.czas_pocisk=time.time()
      elif self.rodzaj==1:
        if self.przeladowanie==self.energia:
         self.przeladowanie=0
        else:
          self.przeladowanie+=1
          przeciwnik.zdrowie-=1
          przeciwnik.stan=True
          return True
      elif self.rodzaj==2:
        if time.time()-self.czas_pocisk>1:
          gra.lista_pociskow.append(Pocisk(self,gra,przeciwnik))
          self.czas_pocisk=time.time()
      elif self.rodzaj==3:
        if time.time()-self.czas_pocisk>1.5:
          gra.lista_pociskow.append(Pocisk(self,gra,przeciwnik))
          self.czas_pocisk=time.time()
        
    else:
      przeciwnik.stan=False

class Przeciwnik:

  def __init__(self,gra,ustawienia):
    self.przeciwnik=pygame.Rect((5,5,enemies[ustawienia[1]][4],enemies[ustawienia[1]][4]))
    self.startowe_zdrowie=ustawienia[0]
    self.zdrowie=ustawienia[0]
    self.kolor=ustawienia[1]
    self.predkosc=enemies[ustawienia[1]][0]
    self.punkty=enemies[ustawienia[1]][1]
    self.money=enemies[ustawienia[1]][2]
    self.atak=enemies[ustawienia[1]][3]
    self.pole=map[0][0]
    self.stan=False
    self.ids=[]
    self.x=5
    self.y=5

  def ruch(self,ustawienia):
    pole=map[int((self.y-5)/TILESIZE)][int((self.x-5)/TILESIZE)]

    if (self.pole==6 or self.pole==60) and (self.pole!=pole):
      pole=map[int((self.y-5)/TILESIZE)][int((self.x+19)/TILESIZE)]
    elif (self.pole==7 or self.pole==70) and (self.pole!=pole):
      pole=map[int((self.y+19)/TILESIZE)][int((self.x+19)/TILESIZE)]

    if pole==0 or pole==10:
      pole=self.pole

    if pole==5:
      self.pole=5
      self.x+=self.predkosc
    elif pole==50:
      self.pole=50
      self.x+=self.predkosc
    elif pole==6:
      self.pole=6
      self.x-=self.predkosc
    elif pole==60:
      self.pole=60
      self.x-=self.predkosc
    elif pole==7:
      self.pole=7
      self.y-=self.predkosc
    elif pole==70:
      self.pole=70
      self.y-=self.predkosc
    elif pole==8:
      self.pole=8
      self.y+=self.predkosc
    elif pole==80:
      self.pole=80
      self.y+=self.predkosc

    self.przeciwnik=pygame.Rect((self.x,self.y,enemies[ustawienia[1]][4],enemies[ustawienia[1]][4]))

  def klikniecie(self,click):
    if self.przeciwnik.colliderect(pygame.Rect(click[0],click[1],1,1)):
      self.zdrowie-=0.5

class Gracz:

  def __init__(self,gra):
    self.x=100
    self.y=100
    self.rodzaj=4
    self.id=-1
    self.obiekt=pygame.Rect(self.x,self.y,30,30)
    self.atak=5
    self.predkosc=1.2
    self.pos=gra.pos

  def move(self,przycisk):
    if przycisk=='w':
      self.y-=self.predkosc
    if przycisk=='a':
      self.x-=self.predkosc
    if przycisk=='s':
      self.y+=self.predkosc
    if przycisk=='d':
      self.x+=self.predkosc
    self.obiekt=pygame.Rect(self.x,self.y,30,30)

  def strzal(self,gra):
    gra.lista_pociskow.append(Pocisk(self,gra))

class Gra:

  def __init__(self):
    global wybrana
    global muzyka_gra
    wybrana=6

    self.pos=(0,0)
    self.gracz=Gracz(self)
    pygame.display.set_caption('Inwazja')
    self.font=pygame.font.SysFont(None,40)
    self.skroty=((self.font.render('1',True,(255,255,255)),(GAME_WIDTH-40,30)),(self.font.render('2',True,(255,255,255)),(GAME_WIDTH-40,90)),(self.font.render('3',True,(255,255,255)),(GAME_WIDTH-40,150)),(self.font.render('4',True,(255,255,255)),(GAME_WIDTH-40,210)))
    self.zaznaczono=False					# kliknięcie w ustawioną wieżę
    self.nic=True

    self.zdrowie=100
    self.money=80
    self.wynik=0

    self.turka=0
    self.tura=0

    self.tekstury=((zacznij,pygame.Rect(GAME_WIDTH-190,GAME_HEIGHT-60,50,50)),(domek,pygame.Rect(GAME_WIDTH-85,GAME_HEIGHT-85,70,70)))
    self.glosniki=((glosnik,pygame.Rect(GAME_WIDTH-85,GAME_HEIGHT-165,70,70)),(glosnik_wylaczony,pygame.Rect(GAME_WIDTH-85,GAME_HEIGHT-165,70,70)))
    self.tekstury_wiez=((atak_zielony,pygame.Rect(300,640,70,70)),(zasieg_zielony,pygame.Rect(380,640,70,70)),(dolar_zielony,pygame.Rect(460,640,70,70)),(celownik_zielony,pygame.Rect(620,640,70,70)),(atak_zolty,pygame.Rect(300,640,70,70)),(zasieg_zolty,pygame.Rect(380,640,70,70)),(dolar_zolty,pygame.Rect(460,640,70,70)),(celownik_zolty,pygame.Rect(620,640,70,70)),(atak_niebieski,pygame.Rect(300,640,70,70)),(zasieg_niebieski,pygame.Rect(380,640,70,70)),(dolar_niebieski,pygame.Rect(460,640,70,70)),(celownik_niebieski,pygame.Rect(620,640,70,70)),(atak_rozowy,pygame.Rect(300,640,70,70)),(zasieg_rozowy,pygame.Rect(380,640,70,70)),(dolar_rozowy,pygame.Rect(460,640,70,70)),(celownik_rozowy,pygame.Rect(620,640,70,70)))
    self.lista_przeciwnikow=[Przeciwnik(self,waves[0][0])]
    self.lista_pociskow=[]
    self.polepszanie=[]
    self.obszar=[]
    self.wieze=[]

    for row in range(MAPHEIGHT):
      self.obszar.append([])
      for column in range(MAPWIDTH):
        self.obszar[row].append((pygame.Rect(TILESIZE*column,TILESIZE*row,TILESIZE,TILESIZE),row,column))
      self.obszar[row]=tuple(self.obszar[row])
    self.obszar=tuple(self.obszar)

    self.okno_gry=pygame.display.set_mode((GAME_WIDTH,GAME_HEIGHT))
    self.licznik=0

    while self.nic:
      self.napisy=((self.font.render(f'Money: {self.money}',True,(255,255,255)),(20,GAME_HEIGHT-90)),(self.font.render(f'Wynik: {self.wynik}',True,(255,255,255)),(20,GAME_HEIGHT-50)),(self.font.render(f'Runda: {self.tura+1}',True,(255,255,255)),(GAME_WIDTH-230,GAME_HEIGHT-90)),(self.font.render(f'{self.zdrowie}',True,(255,255,255)),(463,550)))
      self.licznik+=1
      self.wybrana=False
      self.petla=True
      self.klikniete=pygame.key.get_pressed()

      if self.licznik==100:
        self.licznik=0
        self.turka+=1
        try:
          self.lista_przeciwnikow.append(Przeciwnik(self,waves[self.tura][self.turka]))
        except: pass
        try:
          if self.turka>=len(waves[self.tura]):
            self.turka=-1
            self.tura+=1
        except:
          self.nic=False
          Koniec(self,'Wygrana')

      if self.klikniete[pygame.K_w]:
        Gracz.move(self.gracz,'w')
      if self.klikniete[pygame.K_a]:
        Gracz.move(self.gracz,'a')
      if self.klikniete[pygame.K_s]:
        Gracz.move(self.gracz,'s')
      if self.klikniete[pygame.K_d]:
        Gracz.move(self.gracz,'d')
	  
      for event in pygame.event.get():
        if event.type==pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE): quit()
        elif event.type==pygame.KEYDOWN:
          if event.key==pygame.K_m:
            wylaczenie_muzyki()
          if event.key==pygame.K_u: 
            wlaczenie_muzyki()
          if event.key==pygame.K_p:
            nie_wlaczono=True
            while nie_wlaczono:
              for event in pygame.event.get():
                if event.type==pygame.QUIT: quit()
                elif (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE) or (event.type==pygame.KEYDOWN and event.key==pygame.K_p): nie_wlaczono=False
          if event.key==pygame.K_1: self.wybrana=(LISTA_WIEZ[0],0)
          if event.key==pygame.K_2: self.wybrana=(LISTA_WIEZ[1],1)
          if event.key==pygame.K_3: self.wybrana=(LISTA_WIEZ[2],2)
          if event.key==pygame.K_4: self.wybrana=(LISTA_WIEZ[3],3)

        elif event.type==pygame.MOUSEBUTTONUP:
          self.pos=pygame.mouse.get_pos()
          self.wybrana=click(self.pos,LISTA_WIEZ)
          self.zaznaczono=self.click2()

        if self.wybrana:				# jeżeli kliknęliśmy w wieżę do postawienia
          self.wybranie_wiezy=True
          self.petla=False

          while self.wybranie_wiezy:
            self.pos=pygame.mouse.get_pos()

            self.nowa_wieza=self.click1()
            self.wybranie_wiezy=True

            for event in pygame.event.get():
              if event.type==pygame.QUIT: quit()
              elif event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE: self.wybranie_wiezy=False
              elif event.type==pygame.KEYDOWN and event.key==pygame.K_m:
                wylaczenie_muzyki()
              elif event.type==pygame.KEYDOWN and event.key==pygame.K_u:
                wlaczenie_muzyki()

              elif event.type == pygame.MOUSEBUTTONUP:
                self.nowa_wieza1=self.click1()
                if self.nowa_wieza1:
                  self.wieze.append(Wieza(self,self.wybrana[1]))
                  if self.money<0:
                    self.money+=self.wieze[-1].koszt
                    self.wieze.pop(-1)
                  else:
                    for i in range(len(self.wieze)-1):
                      if self.wieze[-1].wieza.colliderect(self.wieze[i].wieza):	# nie możemy postawić wieży w miejscu już zajmowanym przez inną wieżę
                        self.wieze.pop(-1)
                        break

            self.drawing()

            try:		# jeżeli możemy postawić wieżę
              pygame.draw.rect(self.okno_gry,self.wybrana[0][1],(self.nowa_wieza[0],self.nowa_wieza[1],self.wybrana[0][0][2]-20,self.wybrana[0][0][3]-20))
              if self.wybrana[0][1]==GREEN:
                pygame.draw.circle(self.okno_gry,GREEN,(self.nowa_wieza[0]+10,self.nowa_wieza[1]+10),75,1)
              elif self.wybrana[0][1]==YELLOW:
                pygame.draw.circle(self.okno_gry,YELLOW,(self.nowa_wieza[0]+10,self.nowa_wieza[1]+10),50,1)
              elif self.wybrana[0][1]==BLUE:
                pygame.draw.circle(self.okno_gry,BLUE,(self.nowa_wieza[0]+10,self.nowa_wieza[1]+10),150,1)
              else:
                pygame.draw.circle(self.okno_gry,PINK,(self.nowa_wieza[0]+10,self.nowa_wieza[1]+10),100,1)

            except:	# jeżeli nie możemy postawić wieży
              pygame.draw.rect(self.okno_gry,self.wybrana[0][1],(pygame.mouse.get_pos()[0]-10,pygame.mouse.get_pos()[1]-10,self.wybrana[0][0][2]-20,self.wybrana[0][0][3]-20))
              if self.wybrana[0][1]==GREEN:
                pygame.draw.circle(self.okno_gry,GREEN,(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]),75,1)
              elif self.wybrana[0][1]==YELLOW:
                pygame.draw.circle(self.okno_gry,YELLOW,(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]),50,1)
              elif self.wybrana[0][1]==BLUE:
                pygame.draw.circle(self.okno_gry,BLUE,(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]),150,1)
              else:
                pygame.draw.circle(self.okno_gry,PINK,(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]),100,1)

            pygame.display.update()

        elif self.pos[0]<GAME_WIDTH-100 and self.pos[1]<GAME_HEIGHT-100 and self.pos!=(0,0):
          Gracz.strzal(self.gracz,self)
          self.pos=(0,0)

      self.przebieg()
      self.drawing()
      pygame.display.update()
      if self.zdrowie<=0:
        wynik=self.wynik
        Koniec(self,'Porażka')

  def przebieg(self):
    ''' Funkcja sprwadzająca czy nie pokonaliśmy jakiegoś przeciwnika, usówa przeciwników i pociski oraz porusza graczem '''
    for i,przeciwnik in enumerate(self.lista_przeciwnikow):
        if przeciwnik.zdrowie>0:
          Przeciwnik.klikniecie(przeciwnik,self.pos)
          Przeciwnik.ruch(przeciwnik,waves[self.tura][self.turka])
          if 520<=przeciwnik.x<=525 and przeciwnik.y==555:
            self.zdrowie-=przeciwnik.atak
            self.lista_przeciwnikow.pop(i)
        else:
          self.wynik+=przeciwnik.punkty
          self.money+=przeciwnik.money
          self.lista_przeciwnikow.pop(i)

    for i,pocisk in enumerate(self.lista_pociskow):
      if pocisk.rodzaj!=3:
        Pocisk.move(pocisk)
      for przeciwnik in self.lista_przeciwnikow:
        if pocisk.rodzaj==3:
          for wieza in self.wieze:
            if wieza.id==pocisk.id and pocisk.ruch:
              Pocisk.move(pocisk,przeciwnik,self,wieza)
        if przeciwnik.przeciwnik.colliderect(pocisk.obiekt):
          if pocisk.rodzaj!=2:
            przeciwnik.zdrowie-=pocisk.obrazenia
            self.lista_pociskow.pop(i)
            break
          else:
            if not pocisk.id in przeciwnik.ids:
              przeciwnik.zdrowie-=pocisk.obrazenia
              przeciwnik.ids.append(pocisk.id)

        elif pocisk.position[0]<0 or pocisk.position[0]>=GAME_WIDTH-125 or pocisk.position[1]<0 or pocisk.position[1]>=GAME_HEIGHT-125:
          self.lista_pociskow.pop(i)
          break
      pocisk.ruch=True

  def drawing(self):
    global muzyka_gra
    self.okno_gry.blit(trawa,(0,0))
    pygame.draw.rect(self.okno_gry, BLACK, (GAME_WIDTH-100,0,100,GAME_HEIGHT))
    pygame.draw.rect(self.okno_gry, BLACK, (0,GAME_HEIGHT-100,GAME_WIDTH,100))

    for row in range(MAPHEIGHT):
      for column in range(MAPWIDTH):
        if map[row][column]!=1:
          self.okno_gry.blit(colours[map[row][column]],(column*TILESIZE,row*TILESIZE))

    for tekstura in self.tekstury:
      self.okno_gry.blit(tekstura[0], (tekstura[1].x,tekstura[1].y))
    try:
      if muzyka_gra:
        self.okno_gry.blit(self.glosniki[0][0], (self.glosniki[0][1].x,self.glosniki[0][1].y))
      else:
        self.okno_gry.blit(self.glosniki[1][0], (self.glosniki[1][1].x,self.glosniki[1][1].y))
    except:
      muzyka_gra=True

    for wieza in LISTA_WIEZ:
      pygame.draw.rect(self.okno_gry,wieza[1],wieza[0])

    for napis in self.napisy:
      self.okno_gry.blit(napis[0],napis[1])

    for skrot in self.skroty:
      self.okno_gry.blit(skrot[0],skrot[1])

    for przeciwnik in self.lista_przeciwnikow:		# rysujemy przeciwników i ich paski zdrowia
      if przeciwnik.kolor==GRAY:
        self.okno_gry.blit(mysz,(przeciwnik.x,przeciwnik.y))
      elif przeciwnik.kolor==BLACK:
        self.okno_gry.blit(szczur,(przeciwnik.x,przeciwnik.y))
      else:
        pygame.draw.rect(self.okno_gry, przeciwnik.kolor, przeciwnik.przeciwnik)
      if przeciwnik.zdrowie>0:
        pygame.draw.rect(self.okno_gry, (0,255,0), pygame.Rect(przeciwnik.przeciwnik[0]-5,przeciwnik.przeciwnik[1]-10,(25*przeciwnik.zdrowie)//przeciwnik.startowe_zdrowie,3))
        if przeciwnik.startowe_zdrowie-przeciwnik.zdrowie>0:
          pygame.draw.rect(self.okno_gry, RED, pygame.Rect(przeciwnik.przeciwnik[0]-5+(25*przeciwnik.zdrowie)//przeciwnik.startowe_zdrowie,przeciwnik.przeciwnik[1]-10,(25*(przeciwnik.startowe_zdrowie-przeciwnik.zdrowie))//przeciwnik.startowe_zdrowie,3))

    for wieza in self.wieze:						# rysujemy wieże oraz porażenia przeciwników
      wieza.przeladowanie=0
      for przeciwnik in self.lista_przeciwnikow:
        if self.petla:
          if Wieza.strzal(wieza,przeciwnik,self):
            pygame.draw.rect(self.okno_gry,YELLOW,(przeciwnik.x+3,przeciwnik.y+3,przeciwnik.przeciwnik[2]-6,przeciwnik.przeciwnik[3]-6))
        else:
          if przeciwnik.stan:
            pygame.draw.rect(self.okno_gry,YELLOW,(przeciwnik.x+3,przeciwnik.y+3,przeciwnik.przeciwnik[2]-6,przeciwnik.przeciwnik[3]-6))
        if wieza.rodzaj==1 and wieza.przeladowanie==wieza.energia:
          break
      pygame.draw.rect(self.okno_gry,LISTA_WIEZ[wieza.rodzaj][1],wieza.wieza)

    for pocisk in self.lista_pociskow:
      if pocisk.rodzaj==0:
        pygame.draw.rect(self.okno_gry,GREEN,pocisk.obiekt)
      elif pocisk.rodzaj==2:
        pygame.draw.rect(self.okno_gry,BLUE,pocisk.obiekt)
      elif pocisk.rodzaj==3:
        pygame.draw.rect(self.okno_gry,PINK,pocisk.obiekt)
      elif pocisk.rodzaj==4:
        pygame.draw.rect(self.okno_gry,RED,pocisk.obiekt)

    if self.zaznaczono:
      pygame.draw.circle(self.okno_gry,LISTA_WIEZ[self.wieze[self.zaznaczono[1]].rodzaj][1],(self.wieze[self.zaznaczono[1]].x+10,self.wieze[self.zaznaczono[1]].y+10),self.wieze[self.zaznaczono[1]].range,1)
      if LISTA_WIEZ[self.wieze[self.zaznaczono[1]].rodzaj][1]==GREEN:
        for tekstura in self.tekstury_wiez[:4]:
          self.okno_gry.blit(tekstura[0], (tekstura[1].x,tekstura[1].y))
      elif LISTA_WIEZ[self.wieze[self.zaznaczono[1]].rodzaj][1]==YELLOW:
        for tekstura in self.tekstury_wiez[4:8]:
          self.okno_gry.blit(tekstura[0], (tekstura[1].x,tekstura[1].y))
      elif LISTA_WIEZ[self.wieze[self.zaznaczono[1]].rodzaj][1]==BLUE:
        for tekstura in self.tekstury_wiez[8:12]:
          self.okno_gry.blit(tekstura[0], (tekstura[1].x,tekstura[1].y))
      else:
        for tekstura in self.tekstury_wiez[12:16]:
          self.okno_gry.blit(tekstura[0], (tekstura[1].x,tekstura[1].y))

    pygame.draw.rect(self.okno_gry,BLUE,self.gracz.obiekt)

  def click1(self):
    for row in self.obszar:
      for column in row:
        if column[0].colliderect(pygame.Rect(self.pos[0],self.pos[1],1,1)) and map[column[1]][column[2]]==1:
          self.wybranie_wiezy=False
          return column[0].x,column[0].y

  def click2(self):
    global zaznaczona
    for i,wieza in enumerate(self.wieze):
      if wieza.wieza.colliderect(pygame.Rect(self.pos[0],self.pos[1],1,1)):
        zaznaczona=i
        return (),i
      else:
        for i,tekstura in enumerate(self.tekstury_wiez):
          if tekstura[1].colliderect(self.pos[0],self.pos[1],1,1):
            return (),zaznaczona,i

#--------------------------------------------------

class Menu:

  def __init__(self, napisy, tla, rozmiar,nazwa):
    global muzyka_gra

    pygame.display.set_caption(nazwa)
    self.font=pygame.font.SysFont(None,30)

    self.okno_menu=pygame.display.set_mode((rozmiar[0],rozmiar[1]))
    self.okno_menu.blit(trawa,(0,0))
    self.okno_wyjscia=pygame.Rect(rozmiar[0]-60,rozmiar[1]-60,50,50)
    self.lista_napisow=napisy
    self.lista_tel=tla
    self.nic=True

    while self.nic:
      for event in pygame.event.get():
        if event.type==pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE): quit()
        elif event.type==pygame.KEYDOWN and event.key==pygame.K_m:
          wylaczenie_muzyki()
        elif event.type==pygame.KEYDOWN and event.key==pygame.K_u:
          wlaczenie_muzyki()
        elif event.type==pygame.MOUSEBUTTONUP:
          self.pos=pygame.mouse.get_pos()
          self.klikniecie()

      self.panele(rozmiar)
      pygame.display.update()

  def panele(self,rozmiar):
    for i,napis in enumerate(self.lista_napisow):
      self.text=self.font.render(napis,True,(255,255,255))
      self.obiekt=self.lista_tel[i]
      pygame.draw.rect(self.okno_menu,(0,128,0),self.obiekt)
      self.okno_menu.blit(self.text,(self.lista_tel[i].x+10,self.lista_tel[i].y+10))
    self.okno_menu.blit(zacznij,(rozmiar[0]-60,rozmiar[1]-60))

  def klikniecie(self):
    global wybrana
    for i,tlo in enumerate(self.lista_tel):
      if tlo.colliderect(pygame.Rect(self.pos[0],self.pos[1],1,1)):
        self.nic=False
        wybrana=i
        return
    if self.okno_wyjscia.colliderect(pygame.Rect(self.pos[0],self.pos[1],1,1)):
      self.nic=False
      wybrana=6

class Ustawienia(Menu):

  def __init__(self, napisy, tla, rozmiar,nazwa):
    global muzyka_gra
    global wybrana
    global muzyka
    global trudnosc
    global sterowanie

    super().__init__(napisy, tla, rozmiar,nazwa)

    muzyka=wczytywanie_ustawien()[0]
    trudnosc=wczytywanie_ustawien()[1]
    sterowanie=wczytywanie_ustawien()[2]

    if wybrana==0:
      if muzyka=='ON':
        muzyka='OFF'
      else:
        muzyka='ON'
    elif wybrana==1:
      if trudnosc=='HARD':
        trudnosc='EASY'
      else:
        trudnosc='HARD'
    elif wybrana==2:
      if sterowanie=='WASD':
        sterowanie='><^V'
      else:
        sterowanie='WASD'
    os.remove('dane/ustawienia.txt')
    zapisywanie_ustawien()
    if wybrana!=6:
      wybrana=1

class Rekordy(Menu):

  def __init__(self, napisy, tla, rozmiar,nazwa):
    global wybrana

    super().__init__(napisy, tla, rozmiar,nazwa)
    if wybrana!=6:
      wybrana=2

class O_Grze(Menu):

  def __init__(self, napisy, tla, rozmiar,nazwa):
    global wybrana

    super().__init__(napisy, tla, rozmiar,nazwa)
    if wybrana!=6:
      wybrana=3

class O_Autorze(Menu):

  def __init__(self, napisy, tla, rozmiar,nazwa):
    global wybrana

    super().__init__(napisy, tla, rozmiar,nazwa)
    if wybrana!=6:
      wybrana=4

class Koniec:

  def __init__(self,gra,stan):
    global muzyka_gra
    global wybrana
    global wynik

    wynik=gra.wynik

    pygame.draw.rect(gra.okno_gry,(100,100,100),pygame.Rect(250,200,375,225))
    gra.okno_gry.blit(gra.font.render(f'{stan}',True,(255,255,255)),(390,240))
    gra.okno_gry.blit(gra.font.render(f'Wynik: {wynik}',True,(255,255,255)),(390,300))
    gra.okno_gry.blit(gra.font.render(f'Rekord: {wczytywanie_rekordow()[0][0]}',True,(255,255,255)),(390,360))
    zapisywanie_rekordow(wczytywanie_rekordow())
    pygame.display.update()

    self.nic=True
    while self.nic:
      for event in pygame.event.get():
        if event.type==pygame.QUIT: quit()
        elif event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE:
          self.nic=False
          gra.nic=False
          wybrana=6
        elif event.type==pygame.KEYDOWN and event.key==pygame.K_c:
          self.nic=False
          gra.nic=False
          wybrana=0
        elif event.type==pygame.KEYDOWN and event.key==pygame.K_m:
          wylaczenie_muzyki()
        elif event.type==pygame.KEYDOWN and event.key==pygame.K_u:
          wlaczenie_muzyki()

#--------------------------------------------------

wybrana=6

pygame.font.init()
pygame.mixer.init()
pygame.mixer.music.load('dane/muzyka.ogg')
pygame.mixer.music.play(-1)

while True:
  if wybrana==6:
    Menu(('Nowa Gra','Ustawienia','Rekordy','O Grze','O Autorze','Wyjdź'),(pygame.Rect(50,20,150,40),pygame.Rect(50,90,150,40),pygame.Rect(50,160,150,40),pygame.Rect(50,230,150,40),pygame.Rect(50,300,150,40),pygame.Rect(50,370,150,40)),(300,440),'Menu główne')

  elif wybrana==0:
    Gra()

  elif wybrana==1:
    Ustawienia((f'Muzyka: {wczytywanie_ustawien()[0]}',f'Trudność: {wczytywanie_ustawien()[1]}',f'Sterowanie: {wczytywanie_ustawien()[2]}'),(pygame.Rect(10,20,200,40),pygame.Rect(10,90,200,40),pygame.Rect(10,160,200,40)),(300,230),'Ustawienia')

  elif wybrana==2:
    Rekordy((f'1:  {wczytywanie_rekordow()[0][0]}  {wczytywanie_rekordow()[0][1]}',f'2:  {wczytywanie_rekordow()[1][0]}  {wczytywanie_rekordow()[1][1]}',f'3:  {wczytywanie_rekordow()[2][0]}  {wczytywanie_rekordow()[2][1]}',f'4:  {wczytywanie_rekordow()[3][0]}  {wczytywanie_rekordow()[3][1]}',f'5:  {wczytywanie_rekordow()[4][0]}  {wczytywanie_rekordow()[4][1]}'),(pygame.Rect(10,20,300,40),pygame.Rect(10,90,300,40),pygame.Rect(10,160,300,40),pygame.Rect(10,230,300,40),pygame.Rect(10,300,300,40)),(400,360),'Rekordy')

  elif wybrana==3:
    O_Grze(('Typ gry: Tower Defense','Język: Python'),(pygame.Rect(10,20,400,40),pygame.Rect(10,90,400,40)),(500,160),'O Grze')

  elif wybrana==4:
    O_Autorze(('Autor: Patryk Olejniczak','Data realizacji: 01.06.2019-07.06.2019','Email: 249798@student.pwr.edu.pl'),(pygame.Rect(10,20,400,40),pygame.Rect(10,90,400,40),pygame.Rect(10,160,400,40)),(500,230),'O Autorze')

  elif wybrana==5:
    quit()
