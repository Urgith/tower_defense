import pygame

from CONSTANTS import *


class Przeciwnik:

    def __init__(self, runda, numer_przeciwnika):
        self.rodzaj = WAVES[min(runda, LEN_WAVES - 1)][numer_przeciwnika]
        (self.zdrowie, self.predkosc, self.atak, self.punkty,
            self.monety, self.rozmiar) = ENEMIES[self.rodzaj]

        self.x, self.y = (5, 5)
        self.obiekt = pygame.Rect((self.x, self.y, self.rozmiar, self.rozmiar))
        self.obiekt_z_paskiem = pygame.Rect((self.x - 5, self.y - 10, self.rozmiar + 5, self.rozmiar + 10))

        self.zdrowie = int(self.zdrowie * (1.1**runda))
        self.startowe_zdrowie = self.zdrowie

        self.predkosc_test = (self.predkosc / 100)
        self.pole = MAPA[0][0]
        self.ids = []

        self.is_electrified = False

    def move(self, dt):
        pole = MAPA[int((self.y - 5) / TILESIZE)][int((self.x - 5) / TILESIZE)]

        if pole != self.pole and self.pole in {6, 60, 7, 70}:
            pole = MAPA[int((self.y - 5 + ((25 - self.predkosc_test) * (self.pole % 7 == 0))) / TILESIZE)][int((self.x + 20 - self.predkosc_test) / TILESIZE)]

        if pole in {0, 10}:
            pole = self.pole

        if pole in {5, 50}:
            self.x += self.predkosc * dt
        elif pole in {6, 60}:
            self.x -= self.predkosc * dt
        elif pole in {7, 70}:
            self.y -= self.predkosc * dt
        elif pole in {8, 80}:
            self.y += self.predkosc * dt

        self.obiekt.x, self.obiekt.y = (self.x, self.y)
        self.obiekt_z_paskiem.x, self.obiekt_z_paskiem.y = (self.x - 5, self.y - 10)

        self.pole = pole
