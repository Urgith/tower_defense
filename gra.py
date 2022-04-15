'''
Moduł ten jest prostą grą typu 'OBRONA WIEŻY'

Importowane moduły to:

	os
	time
	pygame
	random
	datetime
	sys

Klasy zdefiniowane w module:

	Gracz
	Pocisk
	Przeciwnik
	Wieza
	Gra
	Menu
		Ustawienia
		Rekordy
		Zasady_Gry
		O_Autorze
	Koniec
'''
import os
import time
import pygame
import random
import datetime
import pygame.math as math

os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/dane') # zmieniamy aktualny katalog na katalog,w którym jest gra
pygame.display.set_mode()

def image_load(name,transparency=False):
  '''
  funkcja konwertująca obrazek, która może również ustawić przezroczystość obrazka (True/False)
  argumenty: obrazek, przezroczystość
  zwraca: obrazek
  '''
  image=pygame.image.load(name)
  image=image.convert()
  if transparency is True:
    color_transparency=image.get_at((0,0))
    image.set_colorkey(color_transparency)
  return image

BLACK=(0,0,0)
BLUE=(0,0,255)
GREEN=(0,255,0)
GRAY=(128,128,128)
RED=(255,0,0)
PINK=(255,0,255)
YELLOW=(255,255,0)
WHITE=(255,255,255)

poziomo=image_load('poziomo.jpg')	# ładujemy obrazki terenu
pionowo=image_load('pionowo.jpg')
czarny=image_load('las.jpg')
lg=image_load('lg.jpg')
ld=image_load('ld.jpg')
pg=image_load('pg.jpg')
pd=image_load('pd.jpg')

# zmienne terenu sterujące m. in. ruchem przeciwników
colours={
        0:poziomo,
        10:pionowo,

        3:czarny,

        5:lg,
        50:ld,

        6:pg,
        60:pd,

        7:pd,
        70:ld,

        8:pg,
        80:lg,
        }

# ładujemy grafiki tekstur i tła w grze
trawa=image_load('trawa.jpg')
zacznij=image_load('zacznij.jpg')
cofnij=image_load('cofnij.jpg')
domek=image_load('domek.jpg')
glosnik=image_load('glosnik.jpg')
glosnik_wylaczony=image_load('glosnik_wylaczony.jpg')

# ładujemy grafiki okna wygranej/porażki
zwyciestwo=image_load('zwyciestwo.jpg')
porazka=image_load('porazka.jpg')

# ładujemy grafiki przeciwników,gracza i prądu
prad=image_load('prad.png',True)
druid=image_load('druid.png',True)
mysz=image_load('mysz.png',True)
szczur=image_load('szczur.png',True)
pajak=image_load('pajak.png',True)
waz=image_load('waz.png',True)

# ładujemy grafiki pocisków
mina=image_load('mina.png',True)
lisc=image_load('lisc.png',True)
kula=image_load('kula.png',True)
kula_mocy=image_load('kula_mocy.png',True)

# ładujemy grafiki polepszeń wież
zasieg_zielony=image_load('zasieg_zielony.jpg')
zasieg_zolty=image_load('zasieg_zolty.jpg')
zasieg_niebieski=image_load('zasieg_niebieski.jpg')
zasieg_rozowy=image_load('zasieg_rozowy.jpg')
dolar_zielony=image_load('dolar_zielony.jpg')
dolar_zolty=image_load('dolar_zolty.jpg')
dolar_niebieski=image_load('dolar_niebieski.jpg')
dolar_rozowy=image_load('dolar_rozowy.jpg')
atak_zielony=image_load('atak_zielony.jpg')
atak_zolty=image_load('atak_zolty.jpg')
atak_niebieski=image_load('atak_niebieski.jpg')
atak_rozowy=image_load('atak_rozowy.jpg')

# grafiki wież
wieze=(
      (image_load('zielony.jpg')),
      (image_load('zielony2.jpg')),
      (image_load('zielony3.jpg')),
      (image_load('zielony4.jpg')),
      (image_load('zielony5.jpg')),
      (image_load('zielony6.jpg')),
      (image_load('zolty.jpg')),
      (image_load('zolty2.jpg')),
      (image_load('zolty3.jpg')),
      (image_load('zolty4.jpg')),
      (image_load('zolty5.jpg')),
      (image_load('zolty6.jpg')),
      (image_load('niebieski.jpg')),
      (image_load('niebieski2.jpg')),
      (image_load('niebieski3.jpg')),
      (image_load('niebieski4.jpg')),
      (image_load('niebieski5.jpg')),
      (image_load('niebieski6.jpg')),
      (image_load('rozowy.jpg')),
      (image_load('rozowy2.jpg')),
      (image_load('rozowy3.jpg')),
      (image_load('rozowy4.jpg')),
      (image_load('rozowy5.jpg')),
      (image_load('rozowy6.jpg'))
      )

# mapa planszy
map=(
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

# rodzaje przeciwników
enemies={
        GRAY:(1,5,1,1,15),
        BLACK:(0.8,8,2,3,17),
        WHITE:(1.2,12,2,2,19),
        RED:(1.3,15,3,3,21,)
        }

# poziomy na hard
waveshard=(
          ((100,GRAY),     (100,GRAY),     (100,GRAY),     (100,GRAY),     (100,GRAY),     (100,GRAY),    (100,GRAY),    (100,GRAY),   (100,GRAY),   (100,GRAY)),
          ((110,GRAY),     (110,GRAY),     (110,GRAY),     (110,GRAY),     (110,GRAY),     (110,GRAY),    (110,GRAY),    (110,GRAY),   (110,GRAY),   (110,GRAY),   (110,GRAY),   (110,GRAY),   (110,GRAY),   (110,GRAY),   (110,GRAY)),
          ((121,GRAY),     (121,GRAY),     (121,GRAY),     (121,GRAY),     (121,GRAY),     (121,GRAY),    (121,GRAY),    (121,GRAY),   (121,GRAY),   (121,GRAY),   (200,BLACK),   (200,BLACK),   (200,BLACK),  (200,BLACK),  (200,BLACK)),
          ((133.1,GRAY),   (133.1,GRAY),   (133.1,GRAY),   (133.1,GRAY),   (133.1,GRAY),   (220,BLACK),   (220,BLACK),   (220,BLACK),  (220,BLACK),  (220,BLACK),  (220,BLACK),  (220,BLACK),  (220,BLACK),  (220,BLACK),  (220,BLACK)),
          ((146.41,GRAY),  (146.41,GRAY),  (146.41,GRAY),  (146.41,GRAY),  (146.41,GRAY),  (146.41,GRAY), (146.41,GRAY), (146.41,GRAY),(146.41,GRAY),(146.41,GRAY),(242,BLACK),  (242,BLACK),  (242,BLACK),  (242,BLACK),  (242,BLACK),  (242,BLACK),  (242,BLACK),  (242,BLACK),  (242,BLACK),  (242,BLACK)),
          ((161.051,GRAY), (161.051,GRAY), (161.051,GRAY), (161.051,GRAY), (161.051,GRAY), (266.2,BLACK), (266.2,BLACK), (266.2,BLACK),(266.2,BLACK),(266.2,BLACK),(266.2,BLACK),(266.2,BLACK),(266.2,BLACK),(266.2,BLACK),(266.2,BLACK),(266.2,BLACK),(266.2,BLACK),(266.2,BLACK),(266.2,BLACK),(266.2,BLACK),(250,WHITE),(250,WHITE),(250,WHITE),(250,WHITE),(250,WHITE)),
		  ((177.1561,GRAY),(177.1561,GRAY),(177.1561,GRAY),(177.1561,GRAY),(177.1561,GRAY),(292.82,BLACK),(292.82,BLACK),(292.82,BLACK),(292.82,BLACK),(292.82,BLACK),(292.82,BLACK),(292.82,BLACK),(292.82,BLACK),(292.82,BLACK),(292.82,BLACK),(275,WHITE),(275,WHITE),(275,WHITE),(275,WHITE),(275,WHITE),(275,WHITE),(275,WHITE),(275,WHITE),(275,WHITE),(275,WHITE)),
		  ((194.87171,GRAY),(194.87171,GRAY),(194.87171,GRAY),(194.87171,GRAY),(194.87171,GRAY),(194.87171,GRAY),(194.87171,GRAY),(194.87171,GRAY),(194.87171,GRAY),(194.87171,GRAY),(322.102,BLACK),(322.102,BLACK),(322.102,BLACK),(322.102,BLACK),(322.102,BLACK),(322.102,BLACK),(322.102,BLACK),(322.102,BLACK),(322.102,BLACK),(322.102,BLACK),(302.5,WHITE),(302.5,WHITE),(302.5,WHITE),(302.5,WHITE),(302.5,WHITE),(302.5,WHITE),(302.5,WHITE),(302.5,WHITE),(302.5,WHITE),(302.5,WHITE),(302.5,WHITE),(302.5,WHITE),(302.5,WHITE),(302.5,WHITE),(302.5,WHITE)),
          ((214.358881,GRAY),(214.358881,GRAY),(214.358881,GRAY),(214.358881,GRAY),(214.358881,GRAY),(354.3122,BLACK),(354.3122,BLACK),(354.3122,BLACK),(354.3122,BLACK),(354.3122,BLACK),(354.3122,BLACK),(322.102,BLACK),(322.102,BLACK),(322.102,BLACK),(322.102,BLACK),(332.75,WHITE),(332.75,WHITE),(332.75,WHITE),(332.75,WHITE),(332.75,WHITE),(332.75,WHITE),(332.75,WHITE),(332.75,WHITE),(332.75,WHITE),(332.75,WHITE),(302.5,WHITE),(332.75,WHITE),(332.75,WHITE),(332.75,WHITE),(332.75,WHITE),(400,RED),(400,RED),(400,RED),(400,RED),(400,RED)),
          ((440,RED),(440,RED),(440,RED),(440,RED),(440,RED),(440,RED),(440,RED),(440,RED),(440,RED),(440,RED),(440,RED),(440,RED),(440,RED),(440,RED),(440,RED),(440,RED),(440,RED),(440,RED),(440,RED),(440,RED),(440,RED),(440,RED),(440,RED),(440,RED),(440,RED),(440,RED),(440,RED),(440,RED),(440,RED),(440,RED)),
          ((100,GRAY))
          )

# poziomy na easy
waveseasy=[
          ((100,GRAY),(100,GRAY),(100,GRAY),(100,GRAY),(100,GRAY),(100,GRAY), (100,GRAY), (100,GRAY), (100,GRAY), (100,GRAY)),
          ((100,GRAY),(100,GRAY),(100,GRAY),(100,GRAY),(100,GRAY),(100,GRAY), (100,GRAY), (100,GRAY), (100,GRAY), (100,GRAY), (100,GRAY), (100,GRAY), (100,GRAY), (100,GRAY), (100,GRAY)),
          ((100,GRAY),(100,GRAY),(100,GRAY),(100,GRAY),(100,GRAY),(100,GRAY), (100,GRAY), (100,GRAY), (100,GRAY), (100,GRAY), (200,BLACK),(200,BLACK),(200,BLACK),(200,BLACK),(200,BLACK)),
          ((100,GRAY),(100,GRAY),(100,GRAY),(100,GRAY),(100,GRAY),(200,BLACK),(200,BLACK),(200,BLACK),(200,BLACK),(200,BLACK),(200,BLACK),(200,BLACK),(200,BLACK),(200,BLACK),(200,BLACK)),
          ((100,GRAY),(100,GRAY),(100,GRAY),(100,GRAY),(100,GRAY),(100,GRAY), (100,GRAY), (100,GRAY), (100,GRAY), (100,GRAY), (200,BLACK),(200,BLACK),(200,BLACK),(200,BLACK),(200,BLACK),(200,BLACK),(200,BLACK),(200,BLACK),(200,BLACK),(200,BLACK)),
          ((100,GRAY),(100,GRAY),(100,GRAY),(100,GRAY),(100,GRAY),(200,BLACK),(200,BLACK),(200,BLACK),(200,BLACK),(200,BLACK),(200,BLACK),(200,BLACK),(200,BLACK),(200,BLACK),(200,BLACK),(200,BLACK),(200,BLACK),(200,BLACK),(200,BLACK),(200,BLACK),(250,WHITE),(250,WHITE),(250,WHITE),(250,WHITE),(250,WHITE)),
		  ((100,GRAY),(100,GRAY),(100,GRAY),(100,GRAY),(100,GRAY),(200,BLACK),(200,BLACK),(200,BLACK),(200,BLACK),(200,BLACK),(200,BLACK),(200,BLACK),(200,BLACK),(200,BLACK),(200,BLACK),(250,WHITE),(250,WHITE),(250,WHITE),(250,WHITE),(250,WHITE),(250,WHITE),(250,WHITE),(250,WHITE),(250,WHITE),(250,WHITE)),
		  ((100,GRAY),(100,GRAY),(100,GRAY),(100,GRAY),(100,GRAY),(100,GRAY), (100,GRAY), (100,GRAY), (100,GRAY), (100,GRAY), (200,BLACK),(200,BLACK),(200,BLACK),(200,BLACK),(200,BLACK),(200,BLACK),(200,BLACK),(200,BLACK),(200,BLACK),(200,BLACK),(250,WHITE),(250,WHITE),(250,WHITE),(250,WHITE),(250,WHITE),(250,WHITE),(250,WHITE),(250,WHITE),(250,WHITE),(250,WHITE),(250,WHITE),(250,WHITE),(250,WHITE),(250,WHITE),(250,WHITE)),
          ((100,GRAY),(100,GRAY),(100,GRAY),(100,GRAY),(100,GRAY),(200,BLACK),(200,BLACK),(200,BLACK),(200,BLACK),(200,BLACK),(200,BLACK),(200,BLACK),(200,BLACK),(200,BLACK),(200,BLACK),(250,WHITE),(250,WHITE),(250,WHITE),(250,WHITE),(250,WHITE),(250,WHITE),(250,WHITE),(250,WHITE),(250,WHITE),(250,WHITE),(250,WHITE),(250,WHITE),(250,WHITE),(250,WHITE),(250,WHITE),(400,RED),  (400,RED),  (400,RED),  (400,RED),  (400,RED)),
		  ((400,RED), (400,RED), (400,RED), (400,RED), (400,RED), (400,RED),  (400,RED),  (400,RED),  (400,RED),  (400,RED),  (400,RED),  (400,RED),  (400,RED),  (400,RED),  (400,RED),  (400,RED),  (400,RED),  (400,RED),  (400,RED),  (400,RED),  (400,RED),  (400,RED),  (400,RED),  (400,RED),  (400,RED),  (400,RED),  (400,RED),  (400,RED),  (400,RED),  (400,RED)),
          ]

# rozmiar gry
TILESIZE=25
MAPWIDTH=len(map[0])
MAPHEIGHT=len(map)
GAME_WIDTH=TILESIZE*MAPWIDTH+100
GAME_HEIGHT=TILESIZE*MAPHEIGHT+100

# wieże do postawienia
LISTA_WIEZ=(
           ((GAME_WIDTH-95,20,35,35),GREEN,pygame.Rect(GAME_WIDTH-95,20,35,35)),
           ((GAME_WIDTH-95,80,35,35),YELLOW,pygame.Rect(GAME_WIDTH-95,80,35,35)),
           ((GAME_WIDTH-95,140,35,35),BLUE,pygame.Rect(GAME_WIDTH-95,140,35,35)),
           ((GAME_WIDTH-95,200,35,35),PINK,pygame.Rect(GAME_WIDTH-95,200,35,35))
           )

def quit():
  ''' funkcja wyłączająca program, nie pobiera żadnych argumentów '''
  import sys;pygame.quit();sys.exit(0)

def wlaczenie_muzyki():
  ''' funkcja włączająca muzykę, nie pobiera żadnych argumentów '''
  global muzyka_gra
  global muzyka

  pygame.mixer.music.play(-1)
  muzyka_gra=True

  muzyka='ON'
  ustawienia=wczytywanie_ustawien()

  zapisywanie_ustawien()

def wylaczenie_muzyki():
  ''' funkcja wyłączająca muzykę, nie pobiera żadnych argumentów '''
  global muzyka_gra
  global muzyka

  pygame.mixer.music.stop()
  muzyka_gra=False

  muzyka='OFF'
  ustawienia=wczytywanie_ustawien()

  zapisywanie_ustawien()

def click(click, obiekt):
  '''
  funkcja sprawdzająca, czy kliknęliśmy w którąś z wież do wyboru
  argumenty: obiekt myszy,obiekt wieży
  zwraca: wieża, indeks wieży
  '''
  for i,wieza in enumerate(obiekt):
    if wieza[2].colliderect(pygame.Rect(click[0],click[1],1,1)):
      return wieza,i

def wczytywanie_ustawien():
  '''
  funkcja sczytująca ustawienia z pliku ustawień, nie pobiera żadnych argumentów
  zwraca: krotka ustawień
  '''
  plik_ustawien=open('ustawienia.txt','r')
  lista_ustawien=[]
  for ustawienie in plik_ustawien:
    lista_ustawien.append(ustawienie.rstrip())
  plik_ustawien.close()
  return tuple(lista_ustawien)

def zapisywanie_ustawien():
  ''' funkcja zapisująca ustawienia do pliku ustawień, nie pobiera żadnych argumentów '''
  global muzyka
  global trudnosc
  global sterowanie
  plik_ustawien=open('ustawienia.txt','w')
  plik_ustawien.write(muzyka+'\n')
  plik_ustawien.write(trudnosc+'\n')
  plik_ustawien.write(sterowanie)
  plik_ustawien.close()

def wczytywanie_rekordow():
  '''
  funkcja sczytująca rekordy z pliku rekordów, nie pobiera żadnych argumentów
  zwraca: lista rekordów
  '''
  plik_rekordow=open('rekordy.txt','r')
  lista_rekordow=[]
  for i,rekord in enumerate(plik_rekordow):
    lista_rekordow.append(rekord.split())
    if len(lista_rekordow[i])==3:
      lista_rekordow[i]=[lista_rekordow[i][0],lista_rekordow[i][1]+' '+lista_rekordow[i][2]]
  plik_rekordow.close()
  return lista_rekordow

def zapisywanie_rekordow(lista_wynikow,wynik):
  '''
  funkcja zapisująca ostatni wynik do pliku o ile jest wystarczająco dobry
  argumenty: lista rekordów, ostatni wynik
  '''
  lista_wynikow.append([wynik,str(datetime.datetime.now())[:16]])
  posortowana_lista_wynikow=[]
  lista_rekordow=[]
  for zawartosc in lista_wynikow:
    zawartosc[0]=int(zawartosc[0])
    lista_rekordow.append(zawartosc[0])
  lista_rekordow.sort(reverse=True)
  lista_rekordow.pop(-1)

  for rekord in lista_rekordow:
    for wyniczek in lista_wynikow:
      if rekord==wyniczek[0]:
        posortowana_lista_wynikow.append(str(rekord)+' '+str(wyniczek[1]))
        break

  plik_rekordow=open('rekordy.txt','r+')
  for rekord in posortowana_lista_wynikow:
    plik_rekordow.write(str(rekord)+'\n')
  plik_rekordow.close()

#--------------------------------------------------

class Gracz:
  '''
  Klasa bohatera modułu gry, odpowiada ona za zachowanie sterowanego bohatera, klasa ta nie dziedziczy po żadnej klasie
  
  Metody zdefiniowane w klasie to:
  
	__init__
	move
    strzal
  '''
  def __init__(self,gra):
    ''' Konstruktor klasy Gracz, inicjalizujemy w nim zmienne bohatera '''
    self.x=100
    self.y=100
    self.rodzaj=4
    self.id=-1
    self.obiekt=pygame.Rect(self.x,self.y,30,30)
    self.atak=5
    self.predkosc=1.5
    self.pos=gra.pos
    self.poziom=0
    self.doswiadczenie=0
    self.zdrowie=1000
    self.acc_x=0
    self.acc_y=0
    self.predkosc_x=0
    self.predkosc_y=0
    if trudnosc=='HARD':	# na poziomie trudności HARD przeciwnik rusza się ZNACZNIE wolniej
      self.wsp=0.001
    else: self.wsp=0.01

  def move(self):
    ''' funkcja ruchu bohatera, aplikująca również działanie przyspieszenia oraz chodzenie na ukos nie jest bardziej wydajne '''
    self.wspolczynnik=self.wsp*(self.poziom+1)
    self.acc_x*=self.wspolczynnik
    self.acc_y*=self.wspolczynnik
    self.predkosc_x*=1-self.wspolczynnik
    self.predkosc_y*=1-self.wspolczynnik
    self.predkosc_x+=self.acc_x
    self.predkosc_y+=self.acc_y
    if self.predkosc_x**2+self.predkosc_y**2>1:
      self.predkosc_x=self.predkosc_x/((self.predkosc_x**2+self.predkosc_y**2)**(1/2))
      self.predkosc_y=self.predkosc_y/((self.predkosc_x**2+self.predkosc_y**2)**(1/2))
    self.x+=self.predkosc_x*self.predkosc
    self.y+=self.predkosc_y*self.predkosc

    if self.x<0: self.x=0
    if self.x>GAME_WIDTH-100-30: self.x=GAME_WIDTH-100-30
    if self.y<0: self.y=0
    if self.y>GAME_HEIGHT-100-30: self.y=GAME_HEIGHT-100-30
    if trudnosc=='HARD':
      self.poziom=self.doswiadczenie//50
    else:
      self.poziom=self.doswiadczenie//200
    self.obiekt=pygame.Rect(self.x,self.y,30,30)

  def strzal(self,gra):
    ''' funkcja strzelania bohatera '''
    if trudnosc=='HARD':
      self.poziom=self.doswiadczenie//50
    else:
      self.poziom=self.doswiadczenie//200
    self.atak=5+self.poziom
    gra.lista_pociskow.append(Pocisk(self,gra))


class Pocisk:
  '''
  Klasa pocisku modułu gry, odpowiada ona za zachowanie pocisków, którymi strzelają wieżyczki oraz bohater, klasa ta nie dziedziczy po żadnej klasie
  
  Metody zdefiniowane w klasie to:
  
	__init__
	move
  '''
  def __init__(self,wieza,gra,przeciwnik=0):
    ''' Konstruktor klasy Pocisk, inicjalizujemy w nim zmienne pocisku '''
    self.rodzaj=wieza.rodzaj
    if self.rodzaj!=4:	# jeżeli nie jest to pocisk gracza
      self.position=math.Vector2(wieza.x+10,wieza.y+10)
    else:
      self.position=math.Vector2(wieza.x+1,wieza.y+1)
    self.obiekt=pygame.Rect(self.position[0],self.position[1],7,7)
    self.id=wieza.id
    self.ruch=True

    if self.rodzaj==0:	# wieża podstawowa
      self.moving=math.Vector2((przeciwnik.x-wieza.x)/100,(przeciwnik.y-wieza.y)/100)
      self.obrazenia=wieza.obrazenia
    elif self.rodzaj==2:	# wieża przebijająca
      x=przeciwnik.x-wieza.x
      y=przeciwnik.y-wieza.y
      self.moving=math.Vector2(x/((x**2+y**2)**(1/2)),y/((x**2+y**2)**(1/2)))*2
      self.obrazenia=wieza.obrazenia
      self.id=random.random()
    elif self.rodzaj==3:	# wieża samonaprowadzająca
      x=przeciwnik.x-self.position[0]
      y=przeciwnik.y-self.position[1]
      self.moving=math.Vector2(x/((x**2+y**2)**(1/2)),(y/(x**2+y**2)**(1/2)))*1.1
      self.obrazenia=wieza.obrazenia
    elif self.rodzaj==4:	# gracz
      x=gra.pos[0]-self.position[0]
      y=gra.pos[1]-self.position[1]
      self.moving=math.Vector2(x/((x**2+y**2)**(1/2)),(y/(x**2+y**2)**(1/2)))*1.5
      self.obrazenia=gra.gracz.atak*6

  def move(self,przeciwnik=0,gra=0,wieza=0):
    ''' funkcja poruszająca pociskiem '''
    if self.rodzaj==3:	# tylko pocisk samonaprowadzający porusza się nietypowo
      for przeciwnik in gra.lista_przeciwnikow:
        x=przeciwnik.x-self.position[0]
        y=przeciwnik.y-self.position[1]
        if (x**2+y**2)**(1/2)<wieza.range:
          self.ruch=False
          self.moving=math.Vector2(x/((x**2+y**2)**(1/2)),(y/(x**2+y**2)**(1/2)))*1.1
          break
    if self.rodzaj!=4:
      self.obiekt=pygame.Rect(self.position[0],self.position[1],7,7)
    else:
      self.obiekt=pygame.Rect(self.position[0],self.position[1],8,8)
    self.position+=self.moving


class Przeciwnik:
  '''
  Klasa przeciwnika modułu gry, odpowiada ona za zachowanie przeciwników, klasa ta nie dziedziczy po żadnej klasie
  
  Metody zdefiniowane w klasie to:
  
	__init__
	ruch
  '''
  def __init__(self,gra,ustawienia):
    ''' Konstruktor klasy Przeciwnik, inicjalizujemy w nim zmienne przeciwnika '''
    self.przeciwnik=pygame.Rect((5,5,enemies[ustawienia[1]][4],enemies[ustawienia[1]][4]))
    self.startowe_zdrowie=ustawienia[0]
    if trudnosc=='HARD':	# na poziomie hard przeciwnicy mają więcej zdrowia
      self.startowe_zdrowie=int(ustawienia[0]*2)
      self.zdrowie=int(ustawienia[0]*2)
    else: self.zdrowie=ustawienia[0]	# na easy standardowo
    self.kolor=ustawienia[1]
    self.predkosc=enemies[ustawienia[1]][0]
    self.punkty=random.random()*enemies[ustawienia[1]][1]
    self.money=enemies[ustawienia[1]][2]
    self.atak=enemies[ustawienia[1]][3]
    self.rozmiar=enemies[ustawienia[1]][4]
    self.pole=map[0][0]
    self.stan=False
    self.ids=[]
    self.x=5
    self.y=5

  def ruch(self,ustawienia):
    ''' funkcja ruchu przeciwnika '''
    pole=map[int((self.y-5)/TILESIZE)][int((self.x-5)/TILESIZE)]

    if (self.pole==6 or self.pole==60) and (self.pole!=pole):
      pole=map[int((self.y-5)/TILESIZE)][int((self.x+20-self.predkosc)/TILESIZE)]
    elif (self.pole==7 or self.pole==70) and (self.pole!=pole):
      pole=map[int((self.y+20-self.predkosc)/TILESIZE)][int((self.x+20-self.predkosc)/TILESIZE)]

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


class Wieza:
  '''
  Klasa wieży modułu gry, odpowiada ona za zachowanie postawionych wież, klasa ta nie dziedziczy po żadnej klasie

  Metody zdefiniowane w klasie to:

	__init__
	strzal
    polepsz
  '''
  def __init__(self,gra,rodzaj):
    ''' Konstruktor klasy Wieza, inicjalizujemy w nim zmienne wieży '''
    self.wieza=pygame.Rect(gra.nowa_wieza[0],gra.nowa_wieza[1],20,20)
    self.rodzaj=rodzaj
    self.okno_gry=gra.okno_gry
    self.x=gra.nowa_wieza[0]
    self.y=gra.nowa_wieza[1]
    self.id=random.random()
    self.czas_pocisk=gra.licznik2
    self.poziom=1

    if self.rodzaj==0:		# wieża podstawowa
      self.koszt=20
      self.range=75
      self.obrazenia=50
      self.koszt1=10
      self.koszt2=5
    elif self.rodzaj==1:	# wieża elektryczna
      self.przeladowanie=0
      self.koszt=80
      self.range=50
      self.energia=2
      self.obrazenia='NaN'
      self.koszt1=100
      self.koszt2=10
    elif self.rodzaj==2:	# wieża przebijająca
      self.koszt=60
      self.range=100
      self.obrazenia=50
      self.koszt1=20
      self.koszt2=10
    else:					# wieża samonaprowadzająca
      self.koszt=40
      self.range=150
      self.obrazenia=150
      self.koszt1=10
      self.koszt2=10

    gra.money-=self.koszt

  def strzal(self,przeciwnik,gra):
    ''' funkcja strzału wieży '''
    if ((self.x-przeciwnik.x)**2+(self.y-przeciwnik.y)**2)**(1/2)<self.range:
      if self.rodzaj==0:
        if gra.licznik2-self.czas_pocisk>50:
          gra.lista_pociskow.append(Pocisk(self,gra,przeciwnik))
          self.czas_pocisk=gra.licznik2
      elif self.rodzaj==1:
        if self.przeladowanie==self.energia:
         self.przeladowanie=0
        else:
          self.przeladowanie+=1
          przeciwnik.zdrowie-=1
          przeciwnik.stan=True
          return True
      elif self.rodzaj==2:
        if gra.licznik2-self.czas_pocisk>100:
          gra.lista_pociskow.append(Pocisk(self,gra,przeciwnik))
          self.czas_pocisk=gra.licznik2
      elif self.rodzaj==3:
        if gra.licznik2-self.czas_pocisk>150:
          gra.lista_pociskow.append(Pocisk(self,gra,przeciwnik))
          self.czas_pocisk=gra.licznik2
        
    else:
      przeciwnik.stan=False

  def polepsz(self,opcja,gra):
    ''' funkcja ulepszenia wieży '''
    if opcja!=2:	# jeżeli nie sprzedaliśmy wieży
      self.poziom+=1
    if self.poziom>11:	# jeżeli wieża miałaby za wysoki poziom
      self.poziom=11
    if self.rodzaj==0:
      if opcja==0:		# polepszanie obrażeń
        if gra.money>=10:
          gra.money-=10
          self.koszt+=10
          self.obrazenia+=30
        else: self.poziom-=1
      elif opcja==1:	# polepszenie zasięgu
        if gra.money>=5:
          gra.money-=5
          self.koszt+=5
          self.range+=20
        else: self.poziom-=1
      elif opcja==2:	# sprzedaż
        gra.money+=self.koszt
        gra.wieze.pop(gra.zaznaczono[3])
    if self.rodzaj==1:
      if opcja==0:		# polepszanie ilości atakowanych przeciwników
        if gra.money>=30:
          gra.money-=30
          self.koszt+=30
          self.energia+=1
        else: self.poziom-=1
      elif opcja==1:	# polepszenie zasięgu
        if gra.money>=10:
          gra.money-=10
          self.koszt+=10
          self.range+=10
        else: self.poziom-=1
      elif opcja==2:	# sprzedaż
        gra.money+=self.koszt
        gra.wieze.pop(gra.zaznaczono[3])
    if self.rodzaj==2:
      if opcja==0:		# polepszanie obrażeń
        if gra.money>=20:
          gra.money-=20
          self.koszt+=20
          self.obrazenia+=20
        else: self.poziom-=1
      elif opcja==1:	# polepszenie zasięgu
        if gra.money>=10:
          gra.money-=10
          self.koszt+=10
          self.range+=15
        else: self.poziom-=1
      elif opcja==2:	# sprzedaż
        gra.money+=self.koszt
        gra.wieze.pop(gra.zaznaczono[3])
    if self.rodzaj==3:
      if opcja==0:		# polepszanie obrażeń
        if gra.money>=10:
          gra.money-=10
          self.koszt+=10
          self.obrazenia+=50
        else: self.poziom-=1
      elif opcja==1:	# polepszenie zasięgu
        if gra.money>=10:
          gra.money-=10
          self.koszt+=10
          self.range+=20
        else: self.poziom-=1
      elif opcja==2:	# sprzedaż
        gra.money+=self.koszt
        gra.wieze.pop(gra.zaznaczono[3])


class Gra:
  '''
  Główna klasa modułu gry, to w niej dzieje się cała 'akcja', klasa ta nie dziedziczy po żadnej klasie
  
  Metody zdefiniowane w module to:
  
	__init__
	przebieg
	drawing
	click1
	click2
	sprawdzanie_muzyki
	klikanie_tekstury
  '''
  def __init__(self):
    ''' Konstruktor klasy Gra '''
    global wybrana
    global muzyka_gra
    global zaznaczona

    if wczytywanie_ustawien()[0]=='ON':
      muzyka_gra=True
    else:
      muzyka_gra=False
    if wczytywanie_ustawien()[2]=='WASD':
      self.sterowanie=[pygame.K_w,pygame.K_a,pygame.K_s,pygame.K_d]
    else:
      self.sterowanie=[pygame.K_UP,pygame.K_LEFT,pygame.K_DOWN,pygame.K_RIGHT]
    wybrana=6

    self.pos=(0,0)
    self.gracz=Gracz(self)
    pygame.display.set_caption('Inwazja')
    self.font=pygame.font.SysFont(None,40)
    self.skroty=((self.font.render('1',True,(255,255,255)),(GAME_WIDTH-55,5)),(self.font.render('2',True,(255,255,255)),(GAME_WIDTH-55,65)),(self.font.render('3',True,(255,255,255)),(GAME_WIDTH-55,125)),(self.font.render('4',True,(255,255,255)),(GAME_WIDTH-55,185)))
    self.zaznaczono=False	# zmienna odpowiedzialna za kontrolę kliknięcia w wieżę
    self.polepszono=False	# zmienna sprawdzająca czy polepszyliśmy wieżę
    zaznaczona=False		# zaznaczona wieża
    self.next=False			# zmienna sprawdzająca przechodzenie do następnej rundy
    self.nic=True			# zmienna kontrolująca pętlę

    self.sprawdzenie=20		# szybkość wychodzenia przeciwnikóœ (im większa tym później wychodzą)
    self.zdrowie=100
    self.money=80
    self.wynik=0

    self.turka=0			# indeks przeciwnika w turze
    self.tura=0				# tura

    self.tekstury=((zacznij,pygame.Rect(GAME_WIDTH-190,GAME_HEIGHT-60,50,50)),(domek,pygame.Rect(GAME_WIDTH-85,GAME_HEIGHT-85,70,70)))
    self.glosniki=((glosnik,pygame.Rect(GAME_WIDTH-85,GAME_HEIGHT-165,70,70)),(glosnik_wylaczony,pygame.Rect(GAME_WIDTH-85,GAME_HEIGHT-165,70,70)))
    self.tekstury_wiez=((atak_zielony,pygame.Rect(190,640,70,70)),(zasieg_zielony,pygame.Rect(270,640,70,70)),(dolar_zielony,pygame.Rect(350,640,70,70)),(atak_zolty,pygame.Rect(190,640,70,70)),(zasieg_zolty,pygame.Rect(270,640,70,70)),(dolar_zolty,pygame.Rect(350,640,70,70)),(atak_niebieski,pygame.Rect(190,640,70,70)),(zasieg_niebieski,pygame.Rect(270,640,70,70)),(dolar_niebieski,pygame.Rect(350,640,70,70)),(atak_rozowy,pygame.Rect(190,640,70,70)),(zasieg_rozowy,pygame.Rect(270,640,70,70)),(dolar_rozowy,pygame.Rect(350,640,70,70)))
    self.lista_przeciwnikow=[Przeciwnik(self,waves[0][0])]
    self.lista_pociskow=[]
    self.polepszanie=[]
    self.obszar=[]
    self.wieze=[]

    # obszar to cała mapa gry
    for row in range(MAPHEIGHT):
      self.obszar.append([])
      for column in range(MAPWIDTH):
        self.obszar[row].append((pygame.Rect(TILESIZE*column,TILESIZE*row,TILESIZE,TILESIZE),row,column))
      self.obszar[row]=tuple(self.obszar[row])
    self.obszar=tuple(self.obszar)

    self.okno_gry=pygame.display.set_mode((GAME_WIDTH,GAME_HEIGHT))
    # zmienne kontrolujące czas w pętli
    self.licznik=0
    self.licznik2=0
    self.ticking=0
    self.zegar=pygame.time.Clock()

    while self.nic:
      self.zegar.tick(100)
      self.napisy=((self.font.render(f'Money: {self.money}$',True,(255,255,255)),(20,GAME_HEIGHT-90)),(self.font.render(f'Wynik: {int(self.wynik)}',True,(255,255,255)),(20,GAME_HEIGHT-50)),(self.font.render(f'Runda: {self.tura+1}',True,(255,255,255)),(GAME_WIDTH-230,GAME_HEIGHT-90)),(self.font.render(f'{self.zdrowie}',True,(255,255,255)),(463,550)))
      self.licznik+=1
      self.licznik2+=1
      self.ticking+=1
      self.polepszono=False
      self.wybrana=False
      self.petla=True	# zmienna sprawdzająca, w której pętli jesteśmy
      self.klikniete=pygame.key.get_pressed()

      if self.licznik==self.sprawdzenie:	# jeżeli wyszli już wszyscy przeciwnicy
        self.licznik=0
        try:
          if self.turka<len(waves[self.tura])-1:
            self.turka+=1
            self.lista_przeciwnikow.append(Przeciwnik(self,waves[self.tura][self.turka]))
          if (self.turka>=len(waves[self.tura])-1) and self.next:
            self.next=False
            self.turka=-1
            self.tura+=1
            if trudnosc=='HARD' and self.tura==len(wieze)-1:
              Koniec(self,'Wygrana')
              break
            elif trudnosc=='EASY' and self.tura>=len(waveseasy):	# na poziomie easy nie ma ostatniej fali przeciwników
              waves.append(waveseasy[-1])
        except:
          self.nic=False
          Koniec(self,'Wygrana')

      # ruchy gracza
      if self.klikniete[self.sterowanie[0]]:
        self.gracz.acc_y-=self.gracz.predkosc
      if self.klikniete[self.sterowanie[1]]:
        self.gracz.acc_x-=self.gracz.predkosc
      if self.klikniete[self.sterowanie[2]]:
        self.gracz.acc_y+=self.gracz.predkosc
      if self.klikniete[self.sterowanie[3]]:
        self.gracz.acc_x+=self.gracz.predkosc
      Gracz.move(self.gracz)
	  
      for event in pygame.event.get():
        if event.type==pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE): quit()
        elif event.type==pygame.KEYDOWN:
          if event.key==pygame.K_m:
            wylaczenie_muzyki()
          if event.key==pygame.K_u: 
            wlaczenie_muzyki()
          if event.key==pygame.K_p:	# pauza
            nie_wlaczono=True
            while nie_wlaczono:
              for event in pygame.event.get():
                if event.type==pygame.QUIT: quit()
                elif (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE) or (event.type==pygame.KEYDOWN and event.key==pygame.K_p): nie_wlaczono=False
          # skróty klawiszowe do stawiania wież
          if event.key==pygame.K_1: self.wybrana=(LISTA_WIEZ[0],0)
          if event.key==pygame.K_2: self.wybrana=(LISTA_WIEZ[1],1)
          if event.key==pygame.K_3: self.wybrana=(LISTA_WIEZ[2],2)
          if event.key==pygame.K_4: self.wybrana=(LISTA_WIEZ[3],3)

        elif event.type==pygame.MOUSEBUTTONUP:
          self.pos=pygame.mouse.get_pos()
          self.sprawdzanie_muzyki()
          if self.tura==7 and not self.lista_przeciwnikow:
            self.next=True
          else:
            self.klikanie_tekstury()

          self.wybrana=click(self.pos,LISTA_WIEZ)
          self.zaznaczono=self.click2()
          if self.polepszono:
            Wieza.polepsz(self.zaznaczono[0],self.zaznaczono[2],self)

        if self.wybrana:	# jeżeli wybraliśmy jakąś wieżę do postawienia
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
                      if self.wieze[-1].wieza.colliderect(self.wieze[i].wieza):
                        self.wieze.pop(-1)
                        break

            self.drawing()

            # ciągle rysujemy wybraną wieżę
            try:
              pygame.draw.rect(self.okno_gry,self.wybrana[0][1],(self.nowa_wieza[0],self.nowa_wieza[1],self.wybrana[0][0][2]-20,self.wybrana[0][0][3]-20))
              if self.wybrana[0][1]==GREEN:
                pygame.draw.circle(self.okno_gry,GREEN,(self.nowa_wieza[0]+10,self.nowa_wieza[1]+10),75,1)
              elif self.wybrana[0][1]==YELLOW:
                pygame.draw.circle(self.okno_gry,YELLOW,(self.nowa_wieza[0]+10,self.nowa_wieza[1]+10),50,1)
              elif self.wybrana[0][1]==BLUE:
                pygame.draw.circle(self.okno_gry,BLUE,(self.nowa_wieza[0]+10,self.nowa_wieza[1]+10),100,1)
              else:
                pygame.draw.circle(self.okno_gry,PINK,(self.nowa_wieza[0]+10,self.nowa_wieza[1]+10),150,1)
            except:
              pygame.draw.rect(self.okno_gry,self.wybrana[0][1],(pygame.mouse.get_pos()[0]-10,pygame.mouse.get_pos()[1]-10,self.wybrana[0][0][2]-20,self.wybrana[0][0][3]-20))
              if self.wybrana[0][1]==GREEN:
                pygame.draw.circle(self.okno_gry,GREEN,(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]),75,1)
              elif self.wybrana[0][1]==YELLOW:
                pygame.draw.circle(self.okno_gry,YELLOW,(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]),50,1)
              elif self.wybrana[0][1]==BLUE:
                pygame.draw.circle(self.okno_gry,BLUE,(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]),100,1)
              else:
                pygame.draw.circle(self.okno_gry,PINK,(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]),150,1)

            pygame.display.update()

        # strzelanie gracza
        elif self.pos[0]<GAME_WIDTH-100 and self.pos[1]<GAME_HEIGHT-100 and self.pos!=(0,0) and self.ticking >=20:
          self.ticking=0
          Gracz.strzal(self.gracz,self)
          self.pos=(0,0)

      self.przebieg()
      self.drawing()
      pygame.display.update()
      if self.zdrowie<=0 or self.gracz.zdrowie<=0:	# jeżeli zdrowie gracza lub lasu jast odpowiednio niskie-przegrywamy
        Koniec(self,'Porażka')

  def przebieg(self):
    ''' funkcja sprawdzająca m.in. czy jakiś pocisk trafił przeciwnika, czy nie pokonaliśmy jakiegoś przeciwnika oraz czy przeciwnik nas nie zabił '''
	# ruch pocisków i sprawdzanie kolizji z przeciwnikiem
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
            if pocisk.rodzaj==4:
              self.gracz.doswiadczenie+=1
            przeciwnik.zdrowie-=pocisk.obrazenia
            self.lista_pociskow.pop(i)
            break
          else:
            if not pocisk.id in przeciwnik.ids:
              przeciwnik.zdrowie-=pocisk.obrazenia
              przeciwnik.ids.append(pocisk.id)

        # znikanie pocisków blisko końca ekranu
        elif pocisk.position[0]<0 or pocisk.position[0]>=GAME_WIDTH-125 or pocisk.position[1]<0 or pocisk.position[1]>=GAME_HEIGHT-125:
          self.lista_pociskow.pop(i)
          break
      pocisk.ruch=True

    # ruch przeciwników
    for i,przeciwnik in enumerate(self.lista_przeciwnikow):
        if przeciwnik.zdrowie>0:
          try:
            Przeciwnik.ruch(przeciwnik,waves[self.tura][self.turka])
          except: pass
          if 520<=przeciwnik.x<=526 and 550<=przeciwnik.y<=560:
            self.zdrowie-=przeciwnik.atak
            self.lista_przeciwnikow.pop(i)
          if przeciwnik.przeciwnik.colliderect(self.gracz.obiekt):
            self.gracz.zdrowie-=przeciwnik.atak
        else:
          self.wynik+=przeciwnik.punkty
          self.money+=przeciwnik.money
          self.lista_przeciwnikow.pop(i)

  def drawing(self):
    '''
    funkcja rysująca wiele rzeczy na ekranie, są to:
		tło
		boczna i dolna ramka ekranu(to czarne)
		teren
		przycisk następnej tury i przejścia do menu
		przycisk włączenia/wyłączenia muzyki
		wieże na bocznym panelu
		wszystkie napisy
		przeciwników
		postawione wieże
		pociski
		menu wieży o ile w jakąś kliknęliśmy
    '''
    global muzyka_gra
	# rysujemy tło ,panel prawy, dolny 
    self.okno_gry.blit(trawa,(0,0))
    pygame.draw.rect(self.okno_gry, BLACK, (GAME_WIDTH-100,0,100,GAME_HEIGHT))
    pygame.draw.rect(self.okno_gry, BLACK, (0,GAME_HEIGHT-100,GAME_WIDTH,100))

    # rysujemy mapę gry
    for row in range(MAPHEIGHT):
      for column in range(MAPWIDTH):
        if map[row][column]!=1:
          self.okno_gry.blit(colours[map[row][column]],(column*TILESIZE,row*TILESIZE))

    # rysujemy przycisk następnej rundy i powrotu do menu
    for tekstura in self.tekstury:
      self.okno_gry.blit(tekstura[0], (tekstura[1].x,tekstura[1].y))

    # rysujemy przyciski muzyki
    if muzyka_gra:
      self.okno_gry.blit(self.glosniki[0][0], (self.glosniki[0][1].x,self.glosniki[0][1].y))
    else:
      self.okno_gry.blit(self.glosniki[1][0], (self.glosniki[1][1].x,self.glosniki[1][1].y))

    # rysujemy możliwe wieże do postawienia
    for wieza in LISTA_WIEZ:
      pygame.draw.rect(self.okno_gry,wieza[1],wieza[0])
    # wypisujemy ilość pieniędzy, wynik, zdrowie
    for napis in self.napisy:
      self.okno_gry.blit(napis[0],napis[1])

    # rysujemy ceny postawienia wież
    self.okno_gry.blit(self.font.render('20$',True,(255,255,255)),(GAME_WIDTH-55,35))
    self.okno_gry.blit(self.font.render('80$',True,(255,255,255)),(GAME_WIDTH-55,95))
    self.okno_gry.blit(self.font.render('60$',True,(255,255,255)),(GAME_WIDTH-55,155))
    self.okno_gry.blit(self.font.render('40$',True,(255,255,255)),(GAME_WIDTH-55,215))

    if trudnosc=='HARD':	# napis HARD
      self.okno_gry.blit(pygame.font.SysFont(None,49).render(f'{trudnosc}',True,(153,0,0)),(GAME_WIDTH-99,520))
    else:	# napis EASY
      self.okno_gry.blit(pygame.font.SysFont(None,49).render(f'{trudnosc}',True,(0,255,255)),(GAME_WIDTH-99,520))

    # rysujemy skróty klawiszowe przy wieżyczkach do postawienia
    for skrot in self.skroty:
      self.okno_gry.blit(skrot[0],skrot[1])

    # rysujemy przeciwnika i jego pasek zdrowia
    for przeciwnik in self.lista_przeciwnikow:
      if przeciwnik.kolor==GRAY:
        self.okno_gry.blit(mysz,(przeciwnik.x-(przeciwnik.rozmiar-15)/2,przeciwnik.y-(przeciwnik.rozmiar-15)/2))
      elif przeciwnik.kolor==BLACK:
        self.okno_gry.blit(szczur,(przeciwnik.x-(przeciwnik.rozmiar-15)/2,przeciwnik.y-(przeciwnik.rozmiar-15)/2))
      elif przeciwnik.kolor==WHITE:
        self.okno_gry.blit(pajak,(przeciwnik.x-(przeciwnik.rozmiar-15)/2,przeciwnik.y-(przeciwnik.rozmiar-15)/2))
      elif przeciwnik.kolor==RED:
        self.okno_gry.blit(waz,(przeciwnik.x-(przeciwnik.rozmiar-15)/2,przeciwnik.y-(przeciwnik.rozmiar-15)/2))
      if przeciwnik.zdrowie>0:
        pygame.draw.rect(self.okno_gry, (0,255,0), pygame.Rect(przeciwnik.przeciwnik[0]-5,przeciwnik.przeciwnik[1]-10,(25*przeciwnik.zdrowie)//przeciwnik.startowe_zdrowie,3))
        if przeciwnik.startowe_zdrowie-przeciwnik.zdrowie>0:
          pygame.draw.rect(self.okno_gry, RED, pygame.Rect(przeciwnik.przeciwnik[0]-5+(25*przeciwnik.zdrowie)//przeciwnik.startowe_zdrowie,przeciwnik.przeciwnik[1]-10,(25*(przeciwnik.startowe_zdrowie-przeciwnik.zdrowie))//przeciwnik.startowe_zdrowie,3))

    # rysujemy wszystkie wieże oraz prądy na odpowiednich przeciwnikach
    for wieza in self.wieze:
      wieza.przeladowanie=0
      for przeciwnik in self.lista_przeciwnikow:
        if self.petla:
          if Wieza.strzal(wieza,przeciwnik,self):
            self.okno_gry.blit(prad, (przeciwnik.x+(przeciwnik.rozmiar-15)/2,przeciwnik.y+(przeciwnik.rozmiar-15)/2))
        else:
          if przeciwnik.stan:
            self.okno_gry.blit(prad, (przeciwnik.x+(przeciwnik.rozmiar-15)/2,przeciwnik.y+(przeciwnik.rozmiar-15)/2))
        if wieza.rodzaj==1 and wieza.przeladowanie==wieza.energia:
          break
      self.okno_gry.blit(wieze[wieza.rodzaj*6+wieza.poziom//2],wieza.wieza)

    # rysujemy wszystkie pociski
    for pocisk in self.lista_pociskow:
      if pocisk.rodzaj==0:
        self.okno_gry.blit(lisc,(pocisk.obiekt.x,pocisk.obiekt.y))
      elif pocisk.rodzaj==2:
        self.okno_gry.blit(kula,(pocisk.obiekt.x,pocisk.obiekt.y))
      elif pocisk.rodzaj==3:
        self.okno_gry.blit(mina,(pocisk.obiekt.x,pocisk.obiekt.y))
      elif pocisk.rodzaj==4:
        self.okno_gry.blit(kula_mocy,(pocisk.obiekt.x,pocisk.obiekt.y))

    # rysujemy tekstury polepszeń wież oraz ceny tych polepszeń
    if self.zaznaczono:
      try:
        pygame.draw.circle(self.okno_gry,LISTA_WIEZ[self.wieze[self.zaznaczono[1]].rodzaj][1],(self.wieze[self.zaznaczono[1]].x+10,self.wieze[self.zaznaczono[1]].y+10),self.wieze[self.zaznaczono[1]].range,1)
        if LISTA_WIEZ[self.wieze[self.zaznaczono[1]].rodzaj][1]==GREEN:
          for tekstura in self.tekstury_wiez[:3]:
            self.okno_gry.blit(tekstura[0], (tekstura[1].x,tekstura[1].y))
          self.okno_gry.blit(self.font.render('10',True,(255,255,255)),(tekstura[1].x-160,tekstura[1].y+45))
          self.okno_gry.blit(self.font.render('5',True,(255,255,255)),(tekstura[1].x-80,tekstura[1].y+45))
        elif LISTA_WIEZ[self.wieze[self.zaznaczono[1]].rodzaj][1]==YELLOW:
          for tekstura in self.tekstury_wiez[3:6]:
            self.okno_gry.blit(tekstura[0], (tekstura[1].x,tekstura[1].y))
          self.okno_gry.blit(self.font.render('30',True,(0,0,0)),(tekstura[1].x-160,tekstura[1].y+45))
          self.okno_gry.blit(self.font.render('10',True,(0,0,0)),(tekstura[1].x-80,tekstura[1].y+45))
        elif LISTA_WIEZ[self.wieze[self.zaznaczono[1]].rodzaj][1]==BLUE:
          for tekstura in self.tekstury_wiez[6:9]:
            self.okno_gry.blit(tekstura[0], (tekstura[1].x,tekstura[1].y))
          self.okno_gry.blit(self.font.render('20',True,(255,255,255)),(tekstura[1].x-160,tekstura[1].y+45))
          self.okno_gry.blit(self.font.render('10',True,(255,255,255)),(tekstura[1].x-80,tekstura[1].y+45))
        else:
          for tekstura in self.tekstury_wiez[9:12]:
            self.okno_gry.blit(tekstura[0], (tekstura[1].x,tekstura[1].y))
          self.okno_gry.blit(self.font.render('10',True,(255,255,255)),(tekstura[1].x-160,tekstura[1].y+45))
          self.okno_gry.blit(self.font.render('10',True,(255,255,255)),(tekstura[1].x-80,tekstura[1].y+45))
      except: pass

    # rysujemy pasek zdrowia gracza
    self.gracz.stan=(self.gracz.zdrowie-2)//333
    try:
      if self.gracz.stan==2:
        color=int(((1000-self.gracz.zdrowie)/333)*255)
        pygame.draw.rect(self.okno_gry,(color,255,0),(self.gracz.x-5,self.gracz.y-5,self.gracz.zdrowie//25,5))
        self.okno_gry.blit(pygame.font.SysFont(None,50).render(f'Poziom bohatera: {self.gracz.poziom}',True,(color,255,0)),(430,675))
      elif self.gracz.stan==1:
        color=int(((self.gracz.zdrowie-333)/333)*255)
        pygame.draw.rect(self.okno_gry,(255,color,0),(self.gracz.x-5,self.gracz.y-5,self.gracz.zdrowie//25,5))
        self.okno_gry.blit(pygame.font.SysFont(None,50).render(f'Poziom bohatera: {self.gracz.poziom}',True,(255,color,0)),(460,675))
      else:
        color=int(((self.gracz.zdrowie)/333)*255)
        pygame.draw.rect(self.okno_gry,(color,0,0),(self.gracz.x-5,self.gracz.y-5,self.gracz.zdrowie//25,5))
        self.okno_gry.blit(pygame.font.SysFont(None,50).render(f'Poziom bohatera: {self.gracz.poziom}',True,(255,0,0)),(460,675))
    except: pass

    # rysujemy gracza
    self.okno_gry.blit(druid,(self.gracz.obiekt.x,self.gracz.obiekt.y))

  def click1(self):
    '''
    funkcja sprawdzająca, czy chcemy postawić wieżę w dobrym miejscu
    zwraca: współrzędna x obszaru, współrzędna y obszaru
    '''
    for row in self.obszar:
      for column in row:
        if column[0].colliderect(pygame.Rect(self.pos[0],self.pos[1],1,1)) and map[column[1]][column[2]]==1:
          self.wybranie_wiezy=False
          return column[0].x,column[0].y

  def click2(self):
    '''
    funkcja sprawdzająca, czy kliknęliśmy w wieżę już postawioną lub też,
    czy nie polepszyliśmy zaznaczonej wieży
    '''
    global zaznaczona
    for i,wieza in enumerate(self.wieze):
      if wieza.wieza.colliderect(pygame.Rect(self.pos[0],self.pos[1],1,1)):
        zaznaczona=i
        return (),i
    if zaznaczona+1:
      for j,tekstura in enumerate(self.tekstury_wiez):
        if tekstura[1].colliderect(self.pos[0],self.pos[1],1,1):
          self.polepszono=True
          return self.wieze[zaznaczona],zaznaczona,j,zaznaczona

  def sprawdzanie_muzyki(self):
    ''' funkcja włączająca/wyłączająca muzykę, po kliknięciu w ikonkę muzyki '''
    for glosnik in self.glosniki:
      if glosnik[1].colliderect(pygame.Rect(self.pos[0],self.pos[1],1,1)):
        if muzyka_gra:
          wylaczenie_muzyki()
          break
        else:
          wlaczenie_muzyki()
          break

  def klikanie_tekstury(self):
    ''' funkcja sprawdzająca, czy kliknęliśmy w przycisk następnej rundy/powrotu do menu '''
    for i,tekstura in enumerate(self.tekstury):
      if tekstura[1].colliderect(pygame.Rect(self.pos[0],self.pos[1],1,1)):
        if i==0:
          if not len(self.lista_przeciwnikow):
            self.next=True
        else:
          self.nic=False

#--------------------------------------------------

class Menu:
  '''
  Klasa menu modułu gry, w niej otwarte jest menu, klasa ta nie dziedziczy po żadnej klasie
  
  Metody zdefiniowane w module to:
  
	__init__
	panele
	klikniecie
  '''
  def __init__(self, napisy, tla, rozmiar, nazwa, dodatek=True):
    '''
	Konstruktor klasy Menu
    Parametry:
		1) krotka napisów do wyświetlenia
		2) kotka prostokątów do wyświetlenia
		3) rozmiar okna (x,y)
		4) nazwa okna
		5) jeżeli dodatek==True to rysowany jest przycisk powrotu do menu głównego
	'''
    global muzyka
    global trudnosc
    global sterowanie
    global waves

    pygame.display.set_caption(nazwa)
    self.font=pygame.font.SysFont(None,30)

    self.okno_menu=pygame.display.set_mode((rozmiar[0],rozmiar[1]))
    self.okno_menu.blit(trawa,(0,0))
    self.okno_wyjscia=pygame.Rect(rozmiar[0]-60,rozmiar[1]-60,50,50)
    self.lista_napisow=napisy
    self.lista_tel=tla
    self.dodatek=dodatek
    self.nic=True

    while self.nic:
      for event in pygame.event.get():
        if event.type==pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE): quit()
        elif event.type==pygame.MOUSEBUTTONUP:
          self.pos=pygame.mouse.get_pos()
          self.klikniecie()

      self.panele(rozmiar)
      pygame.display.update()

    muzyka=wczytywanie_ustawien()[0]
    trudnosc=wczytywanie_ustawien()[1]
    sterowanie=wczytywanie_ustawien()[2]

    if trudnosc=='HARD':
      waves=waveshard
    else:
      waves=waveseasy

  def panele(self,rozmiar):
    ''' funkcja rysująca napisyw menu oraz jeżeli nie jest to menu główne rysuje również przycisk przejścia do menu głównego '''
    for i,napis in enumerate(self.lista_napisow):
      self.text=self.font.render(napis,True,(255,255,255))
      self.obiekt=self.lista_tel[i]
      pygame.draw.rect(self.okno_menu,(0,128,0),self.obiekt)
      self.okno_menu.blit(self.text,(self.lista_tel[i].x+10,self.lista_tel[i].y+10))
    if self.dodatek:
      self.okno_menu.blit(cofnij,(rozmiar[0]-60,rozmiar[1]-60))

  def klikniecie(self):
    ''' funkcja sprawdzająca, czy nie przeszliśmy do innego menu, poprzez kliknięcie odpowiedniego przycisku '''
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
  '''
  Klasa ustawień modułu gry, w niej mamy dostęp do ustawień, klasa ta dziedziczy po klasie Menu
  
  Metody zdefiniowane w module to:
  
	__init__
  '''
  def __init__(self, napisy, tla, rozmiar, nazwa, dodatek=True):
    ''' Konstruktor klasy Ustawienia, w którym wywoływana jest metoda init z klasy dziedziczonej '''
    global wybrana
    global muzyka
    global trudnosc
    global sterowanie
    global waves

    super().__init__(napisy, tla, rozmiar, nazwa, dodatek=True)

    if wybrana==0:
      if muzyka=='ON':
        muzyka='OFF'
        wylaczenie_muzyki()
      else:
        muzyka='ON'
        wlaczenie_muzyki()
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
    os.remove('ustawienia.txt')
    zapisywanie_ustawien()
    if wybrana!=6:
      wybrana=1

class Rekordy(Menu):
  '''
  Klasa rekordów modułu gry, w niej mamy wgląd w rekordy, klasa ta dziedziczy po klasie Menu
  
  Metody zdefiniowane w module to:
  
	__init__
  '''
  def __init__(self, napisy, tla, rozmiar, nazwa, dodatek=True):
    ''' Konstruktor klasy Rekordy, w którym wywoływana jest metoda init z klasy dziedziczonej '''
    global wybrana

    super().__init__(napisy, tla, rozmiar, nazwa, dodatek=True)
    if wybrana!=6:
      wybrana=2

class Zasady_Gry(Menu):
  '''
  Klasa zasad gry modułu gry, w niej mamy wgląd w porady nt gry, klasa ta dziedziczy po klasie Menu
  
  Metody zdefiniowane w module to:
  
	__init__
  '''
  def __init__(self, napisy, tla, rozmiar, nazwa, dodatek=True):
    ''' Konstruktor klasy Zasady_Gry, w którym wywoływana jest metoda init z klasy dziedziczonej '''
    global wybrana

    super().__init__(napisy, tla, rozmiar, nazwa, dodatek=True)
    if wybrana!=6:
      wybrana=3

class O_Autorze(Menu):
  '''
  Klasa informacji o autorze modułu gry, w niej mamy wgląd niektóre dane autora, klasa ta dziedziczy po klasie Menu
  
  Metody zdefiniowane w module to:
  
	__init__
  '''
  def __init__(self, napisy, tla, rozmiar, nazwa, dodatek=True):
    ''' Konstruktor klasy O_Autorze, w którym wywoływana jest metoda init z klasy dziedziczonej '''
    global wybrana

    super().__init__(napisy, tla, rozmiar, nazwa, dodatek=True)
    if wybrana!=6:
      wybrana=4


class Koniec:
  '''
  Klasa okna porażki/zwycięstwa modułu gry, w niej zdefiniowene jest okienko porażki/zwycięstwa oraz to, co po tym następuje, klasa ta nie dziedziczy po żadnej klasie
  
  Metody zdefiniowane w module to:
  
	__init__
	panele
	klikniecie
  '''
  def __init__(self,gra,stan):
    '''
	Konstruktor klasy Koniec
	Argumenty: obiekt gry, stan(Zwycięstwo lub Porażka)
	'''
    global wybrana
    global trudnosc

    if stan=='Wygrana':
      gra.okno_gry.blit(zwyciestwo,(250,225))
    else:
      gra.okno_gry.blit(porazka,(250,225))

    gra.okno_gry.blit(gra.font.render(f'{stan}',True,(255,255,255)),(380,250))
    gra.okno_gry.blit(gra.font.render(f'Wynik: {int(gra.wynik)}',True,(255,255,255)),(430,300))
    gra.okno_gry.blit(gra.font.render(f'Rekord: {wczytywanie_rekordow()[0][0]}',True,(255,255,255)),(430,340))
    gra.okno_gry.blit(gra.font.render('Press C',True,(255,255,255)),(290,360))
    gra.okno_gry.blit(gra.font.render('to new game',True,(255,255,255)),(290,400))
    if trudnosc=='HARD':
      zapisywanie_rekordow(wczytywanie_rekordow(),int(gra.wynik))
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

wybrana=6	# zaczynamy od menu

pygame.font.init()
pygame.mixer.init()

pygame.mixer.music.load('muzyka.ogg')
if wczytywanie_ustawien()[0]=='ON':
  pygame.mixer.music.play(-1)

while True:	# pętla sprawdzająca co aktualnie jest włączone
  if wybrana==6:
    Menu(('Nowa Gra','Ustawienia','Rekordy','Zasady Gry','O Autorze','Wyjdź'),(pygame.Rect(50,20,150,40),pygame.Rect(50,90,150,40),pygame.Rect(50,160,150,40),pygame.Rect(50,230,150,40),pygame.Rect(50,300,150,40),pygame.Rect(50,370,150,40)),(250,440),'Menu główne',False)

  elif wybrana==0:
    Gra()

  elif wybrana==1:
    Ustawienia((f'Muzyka: {wczytywanie_ustawien()[0]}',f'Trudność: {wczytywanie_ustawien()[1]}',f'Sterowanie: {wczytywanie_ustawien()[2]}'),(pygame.Rect(10,20,200,40),pygame.Rect(10,90,200,40),pygame.Rect(10,160,200,40)),(300,230),'Ustawienia')

  elif wybrana==2:
    Rekordy((f'1:  {wczytywanie_rekordow()[0][0]}  {wczytywanie_rekordow()[0][1]}',f'2:  {wczytywanie_rekordow()[1][0]}  {wczytywanie_rekordow()[1][1]}',f'3:  {wczytywanie_rekordow()[2][0]}  {wczytywanie_rekordow()[2][1]}',f'4:  {wczytywanie_rekordow()[3][0]}  {wczytywanie_rekordow()[3][1]}',f'5:  {wczytywanie_rekordow()[4][0]}  {wczytywanie_rekordow()[4][1]}'),(pygame.Rect(10,20,300,40),pygame.Rect(10,90,300,40),pygame.Rect(10,160,300,40),pygame.Rect(10,230,300,40),pygame.Rect(10,300,300,40)),(400,360),'Rekordy')

  elif wybrana==3:
    Zasady_Gry(('Pradawny las','Jest to klasyczna gra typu "Tower Defense"','Jesteś druidem, który strzeże pradawnego lasu.','Zagrażają mu hordy zbuntowanych zwierząt,','nie pozwól im przedostać się do niego.','Ogólne zasady gry:','Do lasu nie może wejść więcej niż setka zwierząt,','niektóre są jeszcze groźniejsze. Aby się ich pozbyć','strzelaj do nich PPM/LPM oraz stawiaj wieże.','Niestety wieże nie są darmowe, musisz je kupić.','W prawym panelu kupujesz odpowiednią wieżę,','możesz to zrobić również klawiszami 1,2,3,4.','Po kliknięciu na wieżę możesz ją również ulepszyć.','Czeka na Ciebię 10 trudnych poziomów','Niech natura będzie z Tobą!'),(pygame.Rect(190,10,150,40),pygame.Rect(10,50,520,40),pygame.Rect(10,90,520,40),pygame.Rect(10,130,520,40),pygame.Rect(10,170,520,40),pygame.Rect(155,220,210,40),pygame.Rect(10,260,520,40),pygame.Rect(10,300,520,40),pygame.Rect(10,340,520,40),pygame.Rect(10,380,520,40),pygame.Rect(10,420,520,40),pygame.Rect(10,460,520,40),pygame.Rect(10,500,520,40),pygame.Rect(10,540,520,40),pygame.Rect(130,580,290,40)),(600,625),'Zasady Gry')

  elif wybrana==4:
    O_Autorze(('Autor: Patryk Olejniczak','Data realizacji: 01.06.2019-07.06.2019','Email: 249798@student.pwr.edu.pl'),(pygame.Rect(10,20,400,40),pygame.Rect(10,90,400,40),pygame.Rect(10,160,400,40)),(500,230),'O Autorze')

  elif wybrana==5:
    quit()
