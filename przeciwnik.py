import pygame

from STALE import *


class Przeciwnik:

    def __init__(self, runda, numer_przeciwnika):
        self.rodzaj = WAVES[runda][numer_przeciwnika]

        self.rozmiar = ENEMIES[self.rodzaj][5]
        self.x, self.y = 5, 5
        self.obiekt = pygame.Rect((self.x, self.y, self.rozmiar, self.rozmiar))

        self.pole = MAPA[0][0]
        self.startowe_zdrowie = int(ENEMIES[self.rodzaj][0] * (1.1**runda))
        self.zdrowie = int(ENEMIES[self.rodzaj][0] * (1.1**runda))
        self.predkosc = ENEMIES[self.rodzaj][1]
        self.atak = ENEMIES[self.rodzaj][2]
        self.punkty = ENEMIES[self.rodzaj][3]
        self.monety = ENEMIES[self.rodzaj][4]

        self.ids = []

    def ruch(self):
        pole = MAPA[int((self.y - 5) / TILESIZE)][int((self.x - 5) / TILESIZE)]

        if (self.pole == 6 or self.pole == 60) and self.pole != pole:
            pole = MAPA[int((self.y - 5) / TILESIZE)][int((self.x + 20 - self.predkosc) / TILESIZE)]
        elif (self.pole == 7 or self.pole == 70) and self.pole != pole:
            pole = MAPA[int((self.y + 20 - self.predkosc) / TILESIZE)][int((self.x + 20 - self.predkosc) / TILESIZE)]

        if pole == 0 or pole == 10:
            pole = self.pole

        if pole == 5 or pole == 50:
            self.x += self.predkosc
        elif pole == 6 or pole == 60:
            self.x -= self.predkosc
        elif pole == 7 or pole == 70:
            self.y -= self.predkosc
        elif pole == 8 or pole == 80:
            self.y += self.predkosc

        self.obiekt.x, self.obiekt.y = self.x, self.y
        self.pole = pole
