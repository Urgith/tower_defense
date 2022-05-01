import pygame

from STALE import *


class Przeciwnik:

    def __init__(self, runda, numer_przeciwnika):
        self.rodzaj = WAVES[runda][numer_przeciwnika]
        (self.predkosc, self.atak, self.punkty,
            self.monety, self.rozmiar) = ENEMIES[self.rodzaj][1:]

        self.x, self.y = (5, 5)
        self.obiekt = pygame.Rect((self.x, self.y, self.rozmiar, self.rozmiar))
        self.obiekt_z_paskiem = pygame.Rect((self.x - 5, self.y - 10, self.rozmiar + 5, self.rozmiar + 10))

        self.startowe_zdrowie = int(ENEMIES[self.rodzaj][0] * (1.1**runda))
        self.zdrowie = int(ENEMIES[self.rodzaj][0] * (1.1**runda))

        self.pole = MAPA[0][0]
        self.ids = []

    def ruch(self):
        self_x = self.x - 5
        pole = MAPA[int((self.y - 5) / TILESIZE)][int(self_x / TILESIZE)]

        if pole != self.pole and self.pole in {6, 60, 7, 70}:
            pole = MAPA[int((self.y - 5 + ((25 - self.predkosc) * (self.pole % 7 == 0))) / TILESIZE)][int((self.x + 20 - self.predkosc) / TILESIZE)]

        if pole in {0, 10}:
            pole = self.pole

        if pole in {5, 50}:
            self.x += self.predkosc
        elif pole in {6, 60}:
            self.x -= self.predkosc
        elif pole in {7, 70}:
            self.y -= self.predkosc
        elif pole in {8, 80}:
            self.y += self.predkosc

        self.obiekt.x, self.obiekt.y = (self.x, self.y)
        self.obiekt_z_paskiem.x, self.obiekt_z_paskiem.y = (self_x, self.y - 10)

        self.pole = pole
