import pygame

from _STALE import *


class Przeciwnik:

    def __init__(self, runda, numer_przeciwnika):
        self.rodzaj = WAVES[min(runda, LEN_WAVES - 1)][numer_przeciwnika]
        (self.zdrowie, self.predkosc, self.atak, self.punkty,
            self.monety, self.rozmiar) = ENEMIES[self.rodzaj]

        self.TILESIZE_ROZMIAR_BY_2 = (TILESIZE - self.rozmiar) // 2
        self.x, self.y = (self.TILESIZE_ROZMIAR_BY_2 // 2, 0)
        self.hp_bar_x, self.hp_bar_y = (0, -5)
        self.mov_x, self.mov_y = (0, 0)

        self.obiekt = pygame.Rect(self.x, self.y, self.rozmiar, self.rozmiar)
        self.hp_bar = pygame.Rect(self.hp_bar_x, self.y - 5, TILESIZE, 2)
        self.hp_bar_lost = pygame.Rect(TILESIZE, self.hp_bar_y, TILESIZE, 2)

        self.zdrowie = int(self.zdrowie * (1.1**runda))
        self.startowe_zdrowie = self.zdrowie

        self.predkosc_test = (self.predkosc / 100)
        self.pole = MAPA[0][0]
        self.ids = []

        self.is_electrified = False

    def move(self, dt):
        pole = MAPA[int((self.obiekt.centery + self.mov_y) / TILESIZE)][int((self.obiekt.centerx + self.mov_x) / TILESIZE)]

        if pole != self.pole and pole not in {0, 1, 10}:
            self.pole = pole

            if self.pole in {5, 50}:
                self.mov_x = -TILESIZE_BY_2
                self.mov_y = 0
            elif self.pole in {6, 60}:
                self.mov_x = TILESIZE_BY_2
                self.mov_y = 0
            elif self.pole in {7, 70}:
                self.mov_y = TILESIZE_BY_2
                self.mov_x = 0
            else:
                self.mov_y = -TILESIZE_BY_2
                self.mov_x = 0

        if self.pole in {5, 50}:
            self.x += self.predkosc * dt

            self.obiekt.x = self.x
            self.hp_bar.x = self.x - self.TILESIZE_ROZMIAR_BY_2
            self.hp_bar_lost.x = self.hp_bar.x + self.hp_bar.w

        elif self.pole in {6, 60}:
            self.x -= self.predkosc * dt
            
            self.obiekt.x = self.x
            self.hp_bar.x = self.x - self.TILESIZE_ROZMIAR_BY_2
            self.hp_bar_lost.x = self.hp_bar.x + self.hp_bar.w

        elif self.pole in {7, 70}:
            self.y -= self.predkosc * dt
            self.obiekt.y = self.hp_bar.y = self.hp_bar_lost.y = self.y

        else:
            self.y += self.predkosc * dt
            self.obiekt.y = self.hp_bar.y = self.hp_bar_lost.y = self.y

    def lose_hp(self, damage):
        self.zdrowie -= damage
        self.update_hp_bar()

    def update_hp_bar(self):
        self.hp_bar.w = TILESIZE * (self.zdrowie / self.startowe_zdrowie)
        self.hp_bar_lost.w = TILESIZE - self.hp_bar.w

        self.hp_bar.x = self.x - self.TILESIZE_ROZMIAR_BY_2
        self.hp_bar_lost.x = self.hp_bar.x + self.hp_bar.w
