import pygame
import random

from STALE import *


class Pocisk:

    def __init__(self, rodzaj, gra):
        self.rodzaj = rodzaj.rodzaj
        self.czas_powstania = gra.licznik

        if self.rodzaj == 'gracz':
            self.x, self.y = (gra.gracz.obiekt.x, gra.gracz.obiekt.y)
            self.obiekt = pygame.Rect(self.x, self.y, 8, 8)
            self.obrazenia = gra.gracz.obrazenia

            x, y = (gra.pozycja_myszy[0] - self.x, gra.pozycja_myszy[1] - self.y)
            self.kierunek_x = x / ((x**2 + y**2)**0.5) * (2 + (rodzaj.poziom / 5))
            self.kierunek_y = y / ((x**2 + y**2)**0.5) * (2 + (rodzaj.poziom / 5))

        else:
            if self.rodzaj == 2:
                self.id = random.random()
                self.przebicie = rodzaj.przebicie

            elif self.rodzaj == 3:
                self.elektryzacja = rodzaj.elektryzacja

            self.dlugosc_zycia = rodzaj.dlugosc_zycia
            self.x, self.y = rodzaj.pole
            self.obiekt = pygame.Rect(self.x, self.y, rodzaj.rozmiar_pocisku, rodzaj.rozmiar_pocisku)
            self.kolor = WIEZE[self.rodzaj - 1][1]
            self.obrazenia = rodzaj.obrazenia

            x, y = (gra.celowany_przeciwnik.x + (gra.celowany_przeciwnik.rozmiar / 2) - self.x,
                   gra.celowany_przeciwnik.y + (gra.celowany_przeciwnik.rozmiar / 2) - self.y)

            self.kierunek_x = x / ((x**2 + y**2)**0.5) * self.rodzaj * rodzaj.predkosc
            self.kierunek_y = y / ((x**2 + y**2)**0.5) * self.rodzaj * rodzaj.predkosc

    def ruch(self):
        self.x += self.kierunek_x
        self.y += self.kierunek_y
        self.obiekt.x, self.obiekt.y = (self.x, self.y)
