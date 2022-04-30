import pygame

from STALE import *
from pocisk import Pocisk


class Gracz:

    def __init__(self):
        self.x, self.y = (DRUID_X, DRUID_Y)
        self.obiekt = pygame.Rect(self.x, self.y, DRUID_SIZE, DRUID_SIZE)

        self.doswiadczenie = 0
        self.poziom = 0

        self.max_zdrowie = 1000
        self.zdrowie = 1000

        self.predkosc = 1
        self.rodzaj = 'gracz'

    def ruch(self):
        self.klikniete = pygame.key.get_pressed()
        x, y = (0, 0)

        if self.klikniete[pygame.K_w]:
            self.y -= self.predkosc
            y = -1

        if self.klikniete[pygame.K_a]:
            self.x -= self.predkosc
            x = -1

        if self.klikniete[pygame.K_s]:
            self.y += self.predkosc
            y = 1

        if self.klikniete[pygame.K_d]:
            self.x += self.predkosc
            x = 1
        # 0.4 ~= 2**0.5 - 1
        if x and y:
            self.x -= x * self.predkosc * 0.4
            self.y -= y * self.predkosc * 0.4

        if not 0 < self.x < MAP_WIDTH - DRUID_SIZE:
            self.x = self.obiekt.x

        if not 0 < self.y < MAP_HEIGHT - DRUID_SIZE:
            self.y = self.obiekt.y

        self.obiekt.x = self.x
        self.obiekt.y = self.y

    def strzal(self, gra):
        gra.lista_pociskow.append(Pocisk(self, gra))

    def awansowanie(self):
        poziom = int((self.doswiadczenie // 100) ** 0.5)

        if poziom != self.poziom:
            self.poziom = poziom

            self.predkosc = 1 + (poziom / 10)
            self.max_zdrowie = int(1000 * (1 + (poziom / 10)))

            self.zdrowie = self.max_zdrowie
