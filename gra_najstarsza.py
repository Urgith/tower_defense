import pygame.math as math
import pygame
import time

pygame.display.set_mode()

BLACK=(0,0,0)
BLUE=(0,0,255)
GREEN=(0,255,0)
GRAY=(128,128,128)
RED=(255,0,0)
YELLOW=(255,255,0)
WHITE=(255,255,255)

colours={
        0:pygame.image.load('dane/poziomo.jpg').convert(),
        10:pygame.image.load('dane/pionowo.jpg').convert(),

#        1:pygame.image.load('dane/zielony.jpg').convert(),
        2:pygame.image.load('dane/niebieski.jpg').convert(),
        3:pygame.image.load('dane/las.jpg').convert(),

        5:pygame.image.load('dane/lg.jpg').convert(),
        50:pygame.image.load('dane/ld.jpg').convert(),

        6:pygame.image.load('dane/pg.jpg').convert(),
        60:pygame.image.load('dane/pd.jpg').convert(),

        7:pygame.image.load('dane/pd.jpg').convert(),
        70:pygame.image.load('dane/ld.jpg').convert(),

        8:pygame.image.load('dane/pg.jpg').convert(),
        80:pygame.image.load('dane/lg.jpg').convert(),
        }

zacznij=pygame.image.load('dane/zacznij.jpg').convert()
trawa=pygame.image.load('dane/trawa.jpg').convert()
domek=pygame.image.load('dane/domek.jpg').convert()

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

enemies={
        GRAY:(1,5,1,1),
        BLACK:(0.8,8,2,3),
        WHITE:(1.2,12,2,2)
        }

waves=(
      ((100,GRAY),(100,GRAY),(100,GRAY),(100,GRAY),(100,GRAY),(100,GRAY),(100,GRAY),(100,GRAY),(100,GRAY),(100,GRAY)),
      ((110,GRAY),(110,GRAY),(110,GRAY),(110,GRAY),(110,GRAY),(110,GRAY),(110,GRAY),(110,GRAY),(110,GRAY),(110,GRAY),(110,GRAY),(110,GRAY),(110,GRAY),(110,GRAY),(110,GRAY)),
      ((121,GRAY),(121,GRAY),(121,GRAY),(121,GRAY),(121,GRAY),(200,BLACK),(200,BLACK),(200,BLACK),(200,BLACK),(200,BLACK)),
      ((133.1,GRAY),(133.1,GRAY),(133.1,GRAY),(133.1,GRAY),(133.1,GRAY),(220,BLACK),(220,BLACK),(220,BLACK),(220,BLACK),(220,BLACK),(220,BLACK),(220,BLACK),(220,BLACK),(220,BLACK),(220,BLACK)),
      ((146.41,GRAY),(146.41,GRAY),(146.41,GRAY),(146.41,GRAY),(146.41,GRAY),(146.41,GRAY),(146.41,GRAY),(146.41,GRAY),(146.41,GRAY),(146.41,GRAY),(242,BLACK),(242,BLACK),(242,BLACK),(242,BLACK),(242,BLACK),(242,BLACK),(242,BLACK),(242,BLACK),(242,BLACK),(242,BLACK)),
      ((161.051,GRAY),(161.051,GRAY),(161.051,GRAY),(161.051,GRAY),(161.051,GRAY),(266.2,BLACK),(266.2,BLACK),(266.2,BLACK),(266.2,BLACK),(266.2,BLACK),(266.2,BLACK),(266.2,BLACK),(266.2,BLACK),(266.2,BLACK),(266.2,BLACK),(266.2,BLACK),(266.2,BLACK),(266.2,BLACK),(266.2,BLACK),(266.2,BLACK),(250,WHITE),(250,WHITE),(250,WHITE),(250,WHITE),(250,WHITE))
      )

TILESIZE=25
MAPWIDTH=len(map[0])
MAPHEIGHT=len(map)

GAME_WIDTH=TILESIZE*MAPWIDTH+100
GAME_HEIGHT=TILESIZE*MAPHEIGHT+100

LISTA_WIEZ=(
           ((GAME_WIDTH-70,20,40,40),GREEN,pygame.Rect(GAME_WIDTH-70,20,40,40)),
           ((GAME_WIDTH-70,80,40,40),YELLOW,pygame.Rect(GAME_WIDTH-70,80,40,40)),
           ((GAME_WIDTH-70,140,40,40),BLUE,pygame.Rect(GAME_WIDTH-70,140,40,40))
           )

global wybrana

def quit():
  import sys;pygame.quit();sys.exit(0)

def click(click, obiekt):
  ''' Funkcja działająca na przyciskach wieżyczek '''
  pozycja=pygame.Rect(click[0],click[1],1,1)
  for i,wieza in enumerate(obiekt):
    if wieza[2].colliderect(pozycja):
      return wieza,i

class Gra:

  def __init__(self):
    self.font=pygame.font.SysFont(None,40)
    self.zaznaczono=False					# kliknięcie w ustawioną wieżę
    self.nic=True

    self.pos=(0,0)
    self.minelo=0

    self.zdrowie=100
    self.money=80
    self.wynik=0

    self.turka=0
    self.tura=0

    self.tekstury=((zacznij,pygame.Rect(GAME_WIDTH-190,GAME_HEIGHT-60,50,50)),(domek,pygame.Rect(GAME_WIDTH-85,GAME_HEIGHT-80,70,70)))
    self.lista_przeciwnikow=[Przeciwnik(self,waves[0][0])]
    self.lista_pociskow=[]
    self.obszar=[]
    self.wieze=[]

    for row in range(MAPHEIGHT):
      self.obszar.append([])
      for column in range(MAPWIDTH):
        self.obszar[row].append((pygame.Rect(TILESIZE*column,TILESIZE*row,TILESIZE,TILESIZE),row,column))
      self.obszar[row]=tuple(self.obszar[row])
    self.obszar=tuple(self.obszar)

    self.okno_gry=pygame.display.set_mode((GAME_WIDTH,GAME_HEIGHT))
    self.time=time.time()

    while self.nic:
      self.napisy=((self.font.render(f'Money: {self.money}',True,(255,255,255)),(20,GAME_HEIGHT-90)),(self.font.render(f'Wynik: {self.wynik}',True,(255,255,255)),(20,GAME_HEIGHT-50)),(self.font.render(f'Runda: {self.tura+1}',True,(255,255,255)),(GAME_WIDTH-230,GAME_HEIGHT-90)),(self.font.render(f'{self.zdrowie}',True,(255,255,255)),(463,550)))
      self.petla=True

      self.czas=time.time()

      if time.time()-self.time-self.minelo>1:
        self.turka+=1
        try:
          self.lista_przeciwnikow.append(Przeciwnik(self,waves[self.tura][self.turka]))
        except: pass

        if self.turka>=len(waves[self.tura]):
          self.turka=-1
          self.tura+=1

        self.time=time.time()
        self.minelo=0

      for event in pygame.event.get():
        if event.type==pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE): quit()
        elif event.type==pygame.KEYDOWN and event.key==pygame.K_m: pygame.mixer.music.stop()
        elif event.type==pygame.KEYDOWN and event.key==pygame.K_u: pygame.mixer.music.play(-1)
        elif event.type==pygame.KEYDOWN and event.key==pygame.K_p:
          nie_wlaczono=True
          while nie_wlaczono:
            for event in pygame.event.get():
              if event.type==pygame.QUIT: quit()
              elif (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE) or (event.type==pygame.KEYDOWN and event.key==pygame.K_p): nie_wlaczono=False

        elif event.type==pygame.MOUSEBUTTONUP:
          self.pos=pygame.mouse.get_pos()
          self.wybrana=click(self.pos,LISTA_WIEZ)
          self.zaznaczono=self.click2()

          if self.wybrana:				# jeżeli kliknęliśmy w wieżę do postawienia
            self.wybranie_wiezy=True
            self.petla=False
            czas=time.time()

            while self.wybranie_wiezy:
              self.pos=pygame.mouse.get_pos()
              self.czas=time.time()

              self.nowa_wieza=self.click1()
              self.wybranie_wiezy=True

              for event in pygame.event.get():
                if event.type==pygame.QUIT: quit()
                elif event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE: self.wybranie_wiezy=False
                elif event.type==pygame.KEYDOWN and event.key==pygame.K_m: pygame.mixer.music.stop()
                elif event.type==pygame.KEYDOWN and event.key==pygame.K_u: pygame.mixer.music.play(-1)

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
                pygame.draw.rect(self.okno_gry,self.wybrana[0][1],(self.nowa_wieza[0]+2,self.nowa_wieza[1]+2,self.wybrana[0][0][2]-20,self.wybrana[0][0][3]-20))
                if self.wybrana[0][1]==GREEN:
                  pygame.draw.circle(self.okno_gry,GREEN,(self.nowa_wieza[0]+10,self.nowa_wieza[1]+10),75,1)
                elif self.wybrana[0][1]==YELLOW:
                  pygame.draw.circle(self.okno_gry,YELLOW,(self.nowa_wieza[0]+10,self.nowa_wieza[1]+10),50,1)
                elif self.wybrana[0][1]==BLUE:
                  pygame.draw.circle(self.okno_gry,BLUE,(self.nowa_wieza[0]+10,self.nowa_wieza[1]+10),100,1)

              except:	# jeżeli nie możemy postawić wieży
                pygame.draw.rect(self.okno_gry,self.wybrana[0][1],(pygame.mouse.get_pos()[0]-10,pygame.mouse.get_pos()[1]-10,self.wybrana[0][0][2]-20,self.wybrana[0][0][3]-20))
                if self.wybrana[0][1]==GREEN:
                  pygame.draw.circle(self.okno_gry,GREEN,(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]),75,1)
                elif self.wybrana[0][1]==YELLOW:
                  pygame.draw.circle(self.okno_gry,YELLOW,(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]),50,1)
                elif self.wybrana[0][1]==BLUE:
                  pygame.draw.circle(self.okno_gry,BLUE,(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]),100,1)

              pygame.display.set_caption(f'Inwazja {1//(time.time()-self.czas)} FPS')
              pygame.display.update()
            self.minelo=time.time()-czas

      self.przebieg()
      self.drawing()
      pygame.display.set_caption(f'Inwazja {1//(time.time()-self.czas)} FPS')
      pygame.display.update()

  def przebieg(self):
    ''' Funkcja sprwadzająca czy nie pokonaliśmy jakiegoś przeciwnika usówa przeciwników i pociski '''
    for i,przeciwnik in enumerate(self.lista_przeciwnikow):
        if przeciwnik.zdrowie>0:
          Przeciwnik.klikniecie(przeciwnik,self.pos)
          Przeciwnik.ruch(przeciwnik)
          if 520<=przeciwnik.x<=525 and przeciwnik.y==555:
            self.zdrowie-=przeciwnik.atak
            self.lista_przeciwnikow.pop(i)
        else:
          self.wynik+=przeciwnik.punkty
          self.money+=przeciwnik.money
          self.lista_przeciwnikow.pop(i)

    for i,pocisk in enumerate(self.lista_pociskow):
      Pocisk.move(pocisk)
      for przeciwnik in self.lista_przeciwnikow:
        if przeciwnik.przeciwnik.colliderect(pocisk.obiekt):
          przeciwnik.zdrowie-=pocisk.obrazenia
          self.lista_pociskow.pop(i)
          break
        elif pocisk.pos[0]<0 or pocisk.pos[0]>=GAME_WIDTH-125 or pocisk.pos[1]<0 or pocisk.pos[1]>=GAME_HEIGHT-125:
          self.lista_pociskow.pop(i)
          break

  def drawing(self):
    self.okno_gry.blit(trawa,(0,0))
    pygame.draw.rect(self.okno_gry, BLACK, (GAME_WIDTH-100,0,100,GAME_HEIGHT))
    pygame.draw.rect(self.okno_gry, BLACK, (0,GAME_HEIGHT-100,GAME_WIDTH,100))

    for row in range(MAPHEIGHT):
      for column in range(MAPWIDTH):
        if map[row][column]!=1:
          self.okno_gry.blit(colours[map[row][column]],(column*TILESIZE,row*TILESIZE))

    for tekstura in self.tekstury:
      self.okno_gry.blit(tekstura[0], (tekstura[1].x,tekstura[1].y))

    for wieza in LISTA_WIEZ:
      pygame.draw.rect(self.okno_gry,wieza[1],wieza[0])

    for napis in self.napisy:
      self.okno_gry.blit(napis[0],napis[1])

    for przeciwnik in self.lista_przeciwnikow:		# rysujemy przeciwników i ich paski zdrowia
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

    if self.zaznaczono:
      pygame.draw.circle(self.okno_gry,LISTA_WIEZ[self.wieze[self.zaznaczono[1]].rodzaj][1],(self.wieze[self.zaznaczono[1]].x+10,self.wieze[self.zaznaczono[1]].y+10),self.wieze[self.zaznaczono[1]].range,1)

  def click1(self):
    for row in self.obszar:
      for column in row:
        if column[0].colliderect(pygame.Rect(self.pos[0],self.pos[1],1,1)) and map[column[1]][column[2]]==1:
          self.wybranie_wiezy=False
          return column[0].x,column[0].y

  def click2(self):
    for i,wieza in enumerate(self.wieze):
      if wieza.wieza.colliderect(pygame.Rect(self.pos[0],self.pos[1],1,1)):
        return (wieza,i)

class Pocisk:

  def __init__(self,wieza,przeciwnik):
    self.pos=math.Vector2(wieza.x+10,wieza.y+10)
    self.obiekt=pygame.Rect(self.pos[0],self.pos[1],4,4)
    self.rodzaj=wieza.rodzaj

    if self.rodzaj==0:
      self.move=math.Vector2((przeciwnik.x-wieza.x)/100,(przeciwnik.y-wieza.y)/100)
      self.obrazenia=50
    elif self.rodzaj==2:
      x=przeciwnik.x-wieza.x
      y=przeciwnik.y-wieza.y
      self.move=math.Vector2(x/((x**2+y**2)**(1/2)),y/((x**2+y**2)**(1/2)))*2
      self.obrazenia=100

  def move(self):
    self.obiekt=pygame.Rect(self.pos[0],self.pos[1],4,4)
    self.pos+=self.move

class Wieza:

  def __init__(self,gra,rodzaj):
    self.wieza=pygame.Rect(gra.nowa_wieza[0]+2,gra.nowa_wieza[1]+2,20,20)
    self.rodzaj=rodzaj
    self.okno_gry=gra.okno_gry
    self.x=gra.nowa_wieza[0]
    self.y=gra.nowa_wieza[1]
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
      self.koszt=30
      self.range=100

    gra.money-=self.koszt

  def strzal(self,przeciwnik,gra):
    if ((self.x-przeciwnik.x)**2+(self.y-przeciwnik.y)**2)**(1/2)<self.range:
      if self.rodzaj==0:
        if time.time()-self.czas_pocisk>0.5:
          gra.lista_pociskow.append(Pocisk(self,przeciwnik))
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
          gra.lista_pociskow.append(Pocisk(self,przeciwnik))
          self.czas_pocisk=time.time()
    else:
      przeciwnik.stan=False

class Przeciwnik:

  def __init__(self,gra,ustawienia):
    self.przeciwnik=pygame.Rect((5,5,15,15))
    self.startowe_zdrowie=ustawienia[0]
    self.zdrowie=ustawienia[0]
    self.kolor=ustawienia[1]
    self.predkosc=enemies[ustawienia[1]][0]
    self.punkty=enemies[ustawienia[1]][1]
    self.money=enemies[ustawienia[1]][2]
    self.atak=enemies[ustawienia[1]][3]
    self.pole=map[0][0]
    self.stan=False
    self.x=5
    self.y=5

  def ruch(self):
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

    self.przeciwnik=pygame.Rect((self.x,self.y,15,15))

  def klikniecie(self,click):
    if self.przeciwnik.colliderect(pygame.Rect(click[0],click[1],1,1)):
      self.zdrowie-=0.5



class Menu:

  def __init__(self, napisy, tla, rozmiar):
    self.font=pygame.font.SysFont(None,30)

    self.okno_menu=pygame.display.set_mode((rozmiar[0],rozmiar[1]))
    self.lista_napisow=napisy
    self.lista_tel=tla
    self.nic=True

    while self.nic:
      for event in pygame.event.get():
        if event.type==pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE): quit()
        elif event.type==pygame.KEYDOWN and event.key==pygame.K_m: pygame.mixer.music.stop()
        elif event.type==pygame.KEYDOWN and event.key==pygame.K_u: pygame.mixer.music.play(-1)

        elif event.type==pygame.MOUSEBUTTONUP:
          self.pos=pygame.mouse.get_pos()
          self.klikniecie()

      self.panele()
      pygame.display.update()

  def panele(self):
    for i,napis in enumerate(self.lista_napisow):
      self.text=self.font.render(napis,True,(255,255,255))
      self.obiekt=self.lista_tel[i]
      pygame.draw.rect(self.okno_menu,(100,100,100),self.obiekt)
      self.okno_menu.blit(self.text,(self.lista_tel[i].x+10,self.lista_tel[i].y+10))

  def klikniecie(self):
    global wybrana
    pozycja=pygame.Rect(self.pos[0],self.pos[1],1,1)
    for i,tlo in enumerate(self.lista_tel):
      if tlo.colliderect(pozycja):
        self.nic=False
        wybrana=i

class Ustawienia(Menu):

  def __init__(self, napisy, tla, rozmiar):
    super().__init__(napisy, tla, rozmiar)

class Rekordy(Menu):

  def __init__(self, napisy, tla, rozmiar):
    super().__init__(napisy, tla, rozmiar)

class Informacje(Menu):

  def __init__(self, napisy, tla, rozmiar):
    super().__init__(napisy, tla, rozmiar)

pygame.font.init()
pygame.mixer.init()
pygame.mixer.music.load('dane/muzyka.ogg')
pygame.mixer.music.play(-1)

while True:
  Menu(('Nowa Gra','Ustawienia','Rekordy','O Grze','Wyjdź'),(pygame.Rect(50,20,150,40),pygame.Rect(50,90,150,40),pygame.Rect(50,160,150,40),pygame.Rect(50,230,150,40),pygame.Rect(50,300,150,40)),(250,400))

  if wybrana==0:
    Gra()

  elif wybrana==1:
    Ustawienia(('Muzyka','Dźwięki','Trudność','Sterowanie'),(pygame.Rect(50,20,150,40),pygame.Rect(50,90,150,40),pygame.Rect(50,160,150,40),pygame.Rect(50,230,150,40)),(250,300))
    wybrana=0

  elif wybrana==2:
    Rekordy(('1.','2.','3.','4.','5.'),(pygame.Rect(50,20,150,40),pygame.Rect(50,90,150,40),pygame.Rect(50,160,150,40),pygame.Rect(50,230,150,40),pygame.Rect(50,300,150,40)),(250,400))
    wybrana=0

  elif wybrana==3:
    Informacje(('Autor:Patryk Olejniczak','Data realizacji:01.06.2019-07.06.2019','Email:249798@student.pwr.edu.pl','Typ gry: Tower Defense','Język:Python'),(pygame.Rect(50,20,150,40),pygame.Rect(50,90,150,40),pygame.Rect(50,160,150,40),pygame.Rect(50,230,150,40),pygame.Rect(50,300,150,40)),(500,400))
    wybrana=0

  elif wybrana==4:
    quit()
